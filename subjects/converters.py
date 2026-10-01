from .models import Subject


class SubjectKeyConverter:
    """Match a subject URL key: a Q-ID, optionally followed by ``-<slug>``.

    Only the Q-ID identifies the subject; whatever follows the hyphen is
    decoration for humans and is discarded. The hyphen is mandatory when
    anything follows the digits, so ``Q12345old-house`` does not match.
    """

    regex = r"Q[0-9]+(?:-[^/]*)?"

    def to_python(self, value):
        return value.split("-", 1)[0]

    def to_url(self, value):
        """Accept a Subject, or an already-built key (e.g. a bare Q-ID)."""
        if isinstance(value, Subject):
            return value.url_key
        return value
