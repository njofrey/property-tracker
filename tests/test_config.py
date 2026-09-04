import os
import unittest
from unittest.mock import patch

from config import Settings, _search_urls


class SearchUrlsTests(unittest.TestCase):
    def test_reads_multiple_urls_one_per_line(self):
        value = (
            "https://www.portalinmobiliario.com/providencia\n"
            "https://www.portalinmobiliario.com/vitacura\n"
        )
        with patch.dict(os.environ, {"PORTAL_SEARCH_URLS": value}, clear=True):
            self.assertEqual(
                _search_urls(),
                (
                    "https://www.portalinmobiliario.com/providencia",
                    "https://www.portalinmobiliario.com/vitacura",
                ),
            )

    def test_accepts_legacy_single_url(self):
        value = "https://www.portalinmobiliario.com/providencia"
        with patch.dict(os.environ, {"PORTAL_SEARCH_URL": value}, clear=True):
            self.assertEqual(_search_urls(), (value,))

    def test_rejects_urls_from_other_domains(self):
        with patch.dict(
            os.environ,
            {"PORTAL_SEARCH_URLS": "https://example.com/propiedades"},
            clear=True,
        ):
            with self.assertRaisesRegex(RuntimeError, "www.portalinmobiliario.com"):
                _search_urls()

    def test_allows_baseline_without_telegram_credentials(self):
        value = "https://www.portalinmobiliario.com/providencia"
        with patch.dict(os.environ, {"PORTAL_SEARCH_URL": value}, clear=True):
            settings = Settings.from_env()
            self.assertIsNone(settings.telegram_token)
            self.assertIsNone(settings.telegram_chat_id)
            with self.assertRaisesRegex(RuntimeError, "TELEGRAM_TOKEN"):
                settings.telegram_credentials()


if __name__ == "__main__":
    unittest.main()
