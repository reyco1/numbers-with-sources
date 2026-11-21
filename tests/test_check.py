import tempfile
import unittest
from pathlib import Path

from numbers_with_sources.check import check_claim

CSV = "key,value\n2026-01,100\n2026-02,200\n"


class CheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        Path(self.tmp.name, "visits.csv").write_text(CSV)

    def run_claim(self, value, source, **kw):
        return check_claim({"claim": "x", "value": value, "source": source},
                           self.tmp.name, **kw)

    def test_verified(self):
        self.assertEqual(self.run_claim(100, "visits.csv:2026-01")["status"], "Verified")

    def test_tolerance(self):
        self.assertEqual(self.run_claim(100.4, "visits.csv:2026-01")["status"], "Mismatch")
        r = self.run_claim(100.4, "visits.csv:2026-01", tolerance=0.5)
        self.assertEqual(r["status"], "Verified")

    def test_mismatch_shows_both(self):
        r = self.run_claim(150, "visits.csv:2026-02")
        self.assertEqual(r["status"], "Mismatch")
        self.assertIn("150", r["note"])
        self.assertIn("200", r["note"])

    def test_no_source(self):
        self.assertEqual(self.run_claim(5, None)["status"], "Not verified")

    def test_missing_row(self):
        r = self.run_claim(100, "visits.csv:2030-01")
        self.assertEqual(r["status"], "Not verified")

    def test_missing_file(self):
        r = self.run_claim(100, "nope.csv:2026-01")
        self.assertEqual(r["status"], "Not verified")
        self.assertIn("file not found", r["note"])

    def test_path_outside_data_folder(self):
        r = self.run_claim(100, "../visits.csv:2026-01")
        self.assertEqual(r["status"], "Not verified")


if __name__ == "__main__":
    unittest.main()
