"""
Style-neutral query embedding for a subject's "find similar images" search.

Builds the query vector from a subject's tagged images by centering each
embedding on its own collection's mean before averaging ("technique G" from
the July 2026 similarity experiments). Collection-level style — medium, film
stock, era, color vs. black-and-white — is shared within a collection, so
subtracting the collection mean cancels it, while the subject content shared
across the set survives and reinforces. Candidates are then scored raw with
the ordinary pgvector cosine query: no index changes, and HNSW ordering is
exact for this query vector.

Compared to the alternatives tested, this construction is also stable under
bulk imports: a new collection gets its own mean and shifts nothing else,
whereas corpus-mean subtraction re-biases every subject's query whenever the
corpus composition changes.

Small collections get noisy means, so means are shrunk toward the corpus mean
(itself derived as the weighted average of the collection means):

    mu_c = (n * mean_c + n0 * mu_corpus) / (n + n0)

The residuals are then averaged with collection balancing: each is weighted
by n_c ** (gamma - 1), where n_c is how many of the kept residuals come from
its collection, so a collection's total weight grows as n_c ** gamma
(gamma = settings.SUBJECT_SIMILARITY_COLLECTION_EXPONENT). With gamma = 0.5 a
subject photographed 100 times in one collection and twice in another no
longer queries for essentially that one collection's take on it; the October
2026 evaluation measured about +1 point Recall@24 on held-out subjects.
gamma = 1 is the plain average.

If CollectionEmbeddingStats has not been populated yet, this degrades
gracefully to the plain normalized centroid.
"""

import numpy as np
from django.conf import settings

from images.models import CollectionEmbeddingStats


def _normalize(v):
    return v / max(np.linalg.norm(v), 1e-12)


def _dedupe(X):
    """
    Indices of rows to keep, greedily dropping near-duplicates.

    Multiple scans or prints of the same photograph would otherwise weight
    that one view of the subject several times in the centroid.
    """
    threshold = settings.SUBJECT_SIMILARITY_DEDUPE_COSINE
    sims = X @ X.T
    keep = []
    for i in range(len(X)):
        if all(sims[i, j] < threshold for j in keep):
            keep.append(i)
    return keep


def _collection_weights(collection_ids):
    """Per-row weights n_c ** (gamma - 1) for collection balancing."""
    gamma = settings.SUBJECT_SIMILARITY_COLLECTION_EXPONENT
    _, inverse, counts = np.unique(
        np.array(collection_ids), return_inverse=True, return_counts=True
    )
    return counts[inverse].astype(np.float64) ** (gamma - 1.0)


def build_subject_query_embedding(set_rows):
    """
    Build a unit-length query embedding from a subject's tagged images.

    Args:
        set_rows: iterable of (collection_id, embedding) tuples for the
            subject's images (embeddings as float lists).

    Returns:
        list[float] unit-length query vector, or None if no usable embeddings.
    """
    set_rows = [(cid, emb) for cid, emb in set_rows if emb]
    if not set_rows:
        return None

    X = np.array([emb for _, emb in set_rows], dtype=np.float64)
    X /= np.linalg.norm(X, axis=1, keepdims=True).clip(1e-12)
    keep = _dedupe(X)
    X = X[keep]
    collection_ids = [set_rows[i][0] for i in keep]

    stats = list(
        CollectionEmbeddingStats.objects.values_list(
            "collection_id", "embedding_count", "mean_embedding"
        )
    )
    plain_centroid = _normalize(X.mean(axis=0))
    if not stats:
        # Stats not populated yet (refresh_collection_embedding_stats has
        # never run): fall back to the plain centroid.
        return plain_centroid.tolist()

    counts = np.array([n for _, n, _ in stats], dtype=np.float64)
    means = np.array([m for _, _, m in stats], dtype=np.float64)
    mu_corpus = (counts[:, None] * means).sum(axis=0) / counts.sum()
    mean_by_collection = {cid: (n, mean) for (cid, n, _), mean in zip(stats, means)}

    n0 = settings.SUBJECT_SIMILARITY_SHRINKAGE_N0
    residuals = []
    residual_collections = []
    for x, cid in zip(X, collection_ids):
        n, mean_c = mean_by_collection.get(cid, (0, mu_corpus))
        mu_c = (n * mean_c + n0 * mu_corpus) / (n + n0)
        residual = x - mu_c
        norm = np.linalg.norm(residual)
        if norm > 1e-6:
            residuals.append(residual / norm)
            residual_collections.append(cid)

    if not residuals:
        # Every set image sits essentially on its collection mean; there is
        # no subject-specific signal left to query with.
        return plain_centroid.tolist()

    query = np.average(
        residuals, axis=0, weights=_collection_weights(residual_collections)
    )
    if np.linalg.norm(query) < 1e-6:
        # Residuals cancelled each other out (pathological); fall back.
        return plain_centroid.tolist()
    return _normalize(query).tolist()
