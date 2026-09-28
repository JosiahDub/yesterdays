"""Maintain the ``WikidataAlias`` mirror.

Aliases (``skos:altLabel``) ride along in every closure load and land on the
Memgraph ``:Entity`` nodes as ``aliases_{lang}`` list properties. This module
projects them into Postgres, where the autocompletes can trigram-match them.
"""

from django.db import transaction

from .models import WikidataAlias, WikidataItem

ALIAS_KEY_PREFIX = "aliases_"


def aliases_from_props(props):
    """Return the ``{(language, alias), ...}`` set in a node property map."""
    return {
        (key.removeprefix(ALIAS_KEY_PREFIX), alias)
        for key, values in props.items()
        if key.startswith(ALIAS_KEY_PREFIX)
        for alias in values
    }


def aliases_from_payload(entities):
    """Map each entity in ``build_graph_payload``'s ``entities`` to its aliases.

    Every entity gets a key, including those with no aliases: their empty set
    tells ``sync_wikidata_aliases`` to clear anything removed upstream.
    """
    return {entity["id"]: aliases_from_props(entity["props"]) for entity in entities}


def sync_wikidata_aliases(aliases_by_qid):
    """Make each item's ``WikidataAlias`` rows match ``aliases_by_qid``.

    Each Q-ID's set is treated as complete. Diffs against the existing rows
    rather than replacing them, since aliases rarely change and a rewrite
    would churn the trigram index on every refresh. Q-IDs without a
    ``WikidataItem`` row are skipped.

    Returns ``(created, deleted)``.
    """
    item_pks = dict(
        WikidataItem.objects.filter(wikidata_id__in=aliases_by_qid).values_list(
            "wikidata_id", "pk"
        )
    )
    if not item_pks:
        return 0, 0

    wanted = {
        (item_pks[qid], language, alias)
        for qid, aliases in aliases_by_qid.items()
        if qid in item_pks
        for language, alias in aliases
    }

    with transaction.atomic():
        existing = {
            (item_id, language, alias): pk
            for pk, item_id, language, alias in WikidataAlias.objects.filter(
                item_id__in=item_pks.values()
            ).values_list("pk", "item_id", "language", "alias")
        }
        stale = [pk for key, pk in existing.items() if key not in wanted]
        if stale:
            WikidataAlias.objects.filter(pk__in=stale).delete()
        new = [
            WikidataAlias(item_id=item_id, language=language, alias=alias)
            for item_id, language, alias in wanted
            if (item_id, language, alias) not in existing
        ]
        if new:
            WikidataAlias.objects.bulk_create(new, ignore_conflicts=True)

    return len(new), len(stale)
