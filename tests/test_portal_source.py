import unittest

from portal_source import extract_property_id, parse_price


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

    def test_parse_clp_price(self):
        self.assertEqual(parse_price("$ 850.000"), ("$ 850.000", 850000, "CLP"))

    def test_parse_usd_price(self):
        self.assertEqual(parse_price("US$ 2.000"), ("US$ 2.000", 2000, "USD"))


if __name__ == "__main__":
    unittest.main()
