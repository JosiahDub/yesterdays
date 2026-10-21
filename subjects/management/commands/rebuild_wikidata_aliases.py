"""Rebuild the ``WikidataAlias`` mirror from the aliases already in Memgraph."""

from django.core.management.base import BaseCommand, CommandError

from subjects.memgraph import GRAPH_ERRORS, MemgraphClient
from subjects.wikidata_aliases import aliases_from_props, sync_wikidata_aliases

# Only the alias keys come back, not each entity's whole property map.
_ALIASES_QUERY = """\
MATCH (e:Entity)
WITH e, properties(e) AS p
RETURN e.id AS qid,
       [k IN keys(p) WHERE k STARTS WITH 'aliases_' | [k, p[k]]] AS aliases
"""


class Command(BaseCommand):
    help = (
        "Sync every WikidataItem's aliases from the Memgraph mirror, without "
        "waiting for each item's next closure refresh. Safe to re-run."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=1000,
            help="Q-IDs synced per Postgres transaction (default: 1000)",
        )

    def handle(self, *args, **options):
        try:
            with MemgraphClient() as client:
                rows = client.read(_ALIASES_QUERY)
        except GRAPH_ERRORS as e:
            raise CommandError(f"Memgraph query failed: {e}") from e

        aliases_by_qid = {
            row["qid"]: aliases_from_props(dict(row["aliases"])) for row in rows
        }
        qids = list(aliases_by_qid)
        batch_size = options["batch_size"]
        created = deleted = 0
        for start in range(0, len(qids), batch_size):
            batch = {q: aliases_by_qid[q] for q in qids[start : start + batch_size]}
            batch_created, batch_deleted = sync_wikidata_aliases(batch)
            created += batch_created
            deleted += batch_deleted

        self.stdout.write(
            self.style.SUCCESS(
                f"Synced aliases for {len(qids)} entities "
                f"({created} created, {deleted} deleted)"
            )
        )
