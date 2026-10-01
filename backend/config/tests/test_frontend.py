from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import TestCase, override_settings


class FrontendTests(TestCase):
    def test_a_page_route_serves_the_react_app(self):
        with TemporaryDirectory() as build_dir:
            (Path(build_dir) / 'index.html').write_text('<div id="root"></div>')
            with override_settings(FRONTEND_BUILD_DIR=Path(build_dir)):
                response = self.client.get('/settings/profile')
                body = b''.join(response.streaming_content)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<div id="root">', body)

    def test_an_unknown_api_route_is_not_served_the_react_app(self):
        response = self.client.get('/api/auth/nope/')
        self.assertEqual(response.status_code, 404)
        self.assertNotIn(b'<div id="root">', response.content)
