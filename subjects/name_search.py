"""Title-and-alias name matching shared by the subject autocompletes.

Both ``subject_autocomplete`` (tagging) and ``browse_autocomplete`` rank
candidates the same way: literal matches (exact, then prefix, then substring)
always rank above fuzzy-only trigram hits, and word similarity orders within a
tier. A candidate's rank is the best of its title and its Wikidata aliases.
"""

from django.contrib.postgres.search import TrigramWordSimilarity
from django.db.models import (
    Case,
    CharField,
    Exists,
    F,
    FloatField,
    IntegerField,
    OuterRef,
    Q,
    Subquery,
    Value,
    When,
)
from django.db.models.functions import Coalesce, Greatest, Least

from .models import WikidataAlias

# Minimum ``word_similarity(query, title)`` for a fuzzy-only hit. Deliberately
# below Postgres's 0.3 default so a transposition in a ~6-letter word still
# matches (``word_similarity('chruch', 'Church Hill')`` is about 0.29).
WORD_SIMILARITY_THRESHOLD = 0.25

# The same for aliases, set much higher. Aliases are numerous and often short
# or abbreviated, so at the title threshold unrelated ones slip through on a
# shared fragment (``word_similarity('capitol', 'El Cerrito, CA')`` is 0.33,
# ``('tredegar', 'group of trees')`` also 0.33), while real alias typos score
# well above it (``('the jeferson', 'The Jefferson')`` is 0.80).
ALIAS_WORD_SIMILARITY_THRESHOLD = 0.5

# ``match_rank`` tiers.
EXACT, PREFIX, SUBSTRING, FUZZY = 0, 1, 2, 3


def _literal_rank(field, query):
    return Case(
        When(**{f"{field}__iexact": query}, then=Value(EXACT)),
        When(**{f"{field}__istartswith": query}, then=Value(PREFIX)),
        When(**{f"{field}__icontains": query}, then=Value(SUBSTRING)),
        default=Value(FUZZY),
        output_field=IntegerField(),
    )


def annotate_name_match(queryset, query, *, title_field, item_field):
    """Filter ``queryset`` to name matches for ``query`` and annotate ranking.

    ``title_field`` is the displayed name; ``item_field`` is the path to the
    row's ``WikidataItem`` pk, whose aliases also count (``"wikidata_item"``
    for Subjects, ``"pk"`` for WikidataItems).

    Adds ``match_rank`` (0 exact, 1 prefix, 2 substring, 3 fuzzy),
    ``similarity``, and ``matched_alias``: the best-matching alias when it
    beats the title, else NULL. Aliases match fuzzily only above the
    stricter ``ALIAS_WORD_SIMILARITY_THRESHOLD``. Callers order by
    ``match_rank`` and then their own tiebreakers.
    """
    # Only aliases that match count, for filtering and for ranking alike.
    aliases = (
        WikidataAlias.objects.filter(item=OuterRef(item_field))
        .annotate(
            rank=_literal_rank("alias", query),
            similarity=TrigramWordSimilarity(query, "alias"),
        )
        .filter(
            Q(alias__icontains=query)
            | Q(similarity__gte=ALIAS_WORD_SIMILARITY_THRESHOLD)
        )
    )
    best_alias = aliases.order_by("rank", "-similarity", "alias")
    return (
        queryset.annotate(
            title_rank=_literal_rank(title_field, query),
            title_similarity=TrigramWordSimilarity(query, title_field),
        )
        .filter(
            Q(**{f"{title_field}__icontains": query})
            | Q(title_similarity__gte=WORD_SIMILARITY_THRESHOLD)
            | Exists(aliases)
        )
        .annotate(
            alias_rank=Subquery(
                best_alias.values("rank")[:1], output_field=IntegerField()
            ),
            alias_similarity=Subquery(
                best_alias.values("similarity")[:1], output_field=FloatField()
            ),
            best_alias=Subquery(best_alias.values("alias")[:1]),
        )
        .annotate(
            match_rank=Least("title_rank", Coalesce("alias_rank", Value(FUZZY))),
            similarity=Greatest(
                "title_similarity", Coalesce("alias_similarity", Value(0.0))
            ),
            matched_alias=Case(
                When(
                    Q(alias_rank__lt=F("title_rank"))
                    | Q(
                        alias_rank=F("title_rank"),
                        alias_similarity__gt=F("title_similarity"),
                    ),
                    then=F("best_alias"),
                ),
                default=Value(None),
                output_field=CharField(),
            ),
        )
    )
