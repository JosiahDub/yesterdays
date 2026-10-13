"""
SQL fragments for pgvector queries over Image.embedding.

Image.embedding is a plain float array; queries cast it to a fixed-size
vector. The HNSW indexes (images/migrations/0069_pe_core_embeddings.py) are
expression indexes on exactly VECTOR_SQL, so every ORDER BY must use this text
verbatim, and bind its query vector through QUERY_VECTOR_SQL, or the planner
falls back to a sequential scan.
"""

from django.conf import settings

VECTOR_SQL = f"embedding::vector({settings.EMBEDDING_DIMENSION})"
QUERY_VECTOR_SQL = f"%s::vector({settings.EMBEDDING_DIMENSION})"
