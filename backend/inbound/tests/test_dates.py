from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from django.test import SimpleTestCase

from ..dates import parse_received

LONDON = ZoneInfo('Europe/London')


class ParseReceivedTests(SimpleTestCase):
    def test_every_sample_format_is_read(self):
        cases = {
            '03/09/2026 09:14': datetime(2026, 9, 3, 9, 14, tzinfo=LONDON),
            '2026-09-08T07:52:00Z': datetime(2026, 9, 8, 7, 52, tzinfo=UTC),
            'Mon 15 Sep 2026 16:02': datetime(2026, 9, 15, 16, 2, tzinfo=LONDON),
            '2026-09-29 10:40': datetime(2026, 9, 29, 10, 40, tzinfo=LONDON),
            '01-10-2026': datetime(2026, 10, 1, tzinfo=LONDON),
            '6 Oct 2026 14:21': datetime(2026, 10, 6, 14, 21, tzinfo=LONDON),
            '09/10/2026 08:03': datetime(2026, 10, 9, 8, 3, tzinfo=LONDON),
        }

        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(parse_received(text), expected)

    def test_day_comes_before_month(self):
        self.assertEqual(parse_received('03/09/2026').month, 9)

    def test_a_date_without_a_year_is_not_guessed(self):
        self.assertIsNone(parse_received('22/9'))

    def test_blank_or_nonsense_gives_none(self):
        for text in ['', '   ', 'not a date', '31/02/2026']:
            with self.subTest(text=text):
                self.assertIsNone(parse_received(text))
