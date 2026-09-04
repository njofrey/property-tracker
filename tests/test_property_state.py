import json
import tempfile
import unittest
from pathlib import Path

from property_state import PropertyState


class PropertyStateTests(unittest.TestCase):
    def test_persists_baseline_and_items(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            state = PropertyState(str(path))
            item = {"id": "MLC123456789", "price_value": 500000}

            state.save_item(item)
            state.mark_seen(item["id"])
            state.mark_initialized()
            self.assertTrue(state.flush())

            restored = PropertyState(str(path))
            self.assertTrue(restored.initialized())
            self.assertEqual(restored.seen_ids(), {item["id"]})
            self.assertEqual(restored.get_item(item["id"]), item)
            self.assertFalse(restored.flush())

    def test_rejects_invalid_state_instead_of_resetting_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            path.write_text(json.dumps({"version": 99}), encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "Estado inválido"):
                PropertyState(str(path))


if __name__ == "__main__":
    unittest.main()
