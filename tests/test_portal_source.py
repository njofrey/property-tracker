import unittest
from unittest.mock import patch

from portal_source import Property, extract_property_id, fetch_all_properties, parse_price


class PortalSourceTests(unittest.TestCase):
    def test_extract_property_id_with_hyphen(self):
        self.assertEqual(
            extract_property_id("https://x.cl/MLC-123456789-propiedad"),
            "MLC123456789",
        )

    def test_extract_property_id_without_hyphen(self):
        self.assertEqual(extract_property_id("MLC123456789"), "MLC123456789")

    def test_parse_uf_price(self):
        self.assertEqual(parse_price("UF 6.500"), ("UF 6.500", 6500, "UF"))

    def test_parse_decimal_uf_price(self):
        self.assertEqual(parse_price("UF 20,79"), ("UF 20,79", 20.79, "UF"))

    def test_parse_clp_price(self):
        self.assertEqual(parse_price("$ 850.000"), ("$ 850.000", 850000, "CLP"))

    def test_parse_usd_price(self):
        self.assertEqual(parse_price("US$ 2.000"), ("US$ 2.000", 2000, "USD"))

    @patch("portal_source.fetch_properties")
    def test_fetch_all_properties_deduplicates_by_id(self, fetch):
        shared = Property("MLC123456789", "Compartida", "https://example.test/shared")
        unique = Property("MLC987654321", "Única", "https://example.test/unique")
        fetch.side_effect = [[shared], [shared, unique]]

        self.assertEqual(
            fetch_all_properties(("https://search.test/one", "https://search.test/two")),
            [shared, unique],
        )


if __name__ == "__main__":
    unittest.main()
