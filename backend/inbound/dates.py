from datetime import datetime

from django.utils import timezone

# Day comes before month, as in the UK. A date without a year is never guessed.
FORMATS = [
    '%d/%m/%Y %H:%M',
    '%d/%m/%Y',
    '%d-%m-%Y %H:%M',
    '%d-%m-%Y',
    '%a %d %b %Y %H:%M',
    '%a %d %b %Y',
    '%d %b %Y %H:%M',
    '%d %b %Y',
]


def read_date(text: str) -> datetime | None:
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        pass

    for date_format in FORMATS:
        try:
            return datetime.strptime(text, date_format)
        except ValueError:
            continue

    return None


def parse_received(text: str) -> datetime | None:
    """Turn a received date in any known format into a datetime, or None if it can't be read."""
    parsed = read_date(text.strip())

    if parsed and timezone.is_naive(parsed):
        # Times without a zone are local council time (settings.TIME_ZONE).
        return timezone.make_aware(parsed)

    return parsed
