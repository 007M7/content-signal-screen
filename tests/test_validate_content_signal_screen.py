import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALIDATOR = os.path.join(ROOT, "scripts", "validate_content_signal_screen.py")
SIGNALS = [
    "concrete_takeaway",
    "source_specificity",
    "author_footprint",
    "cognitive_progress",
]


def valid_artifact(risk="medium", coverage="sampled_content", inspected=None):
    if inspected is None:
        inspected = ["opening", "sampled_body"] if coverage != "metadata_only" else []
    return {
        "schema_version": "0.1",
        "run_id": "test-001",
        "created_at": "2026-07-15T00:00:00Z",
        "source": {
            "title": "Example article",
            "path_or_url": "https://example.com/article",
            "source_type": "article",
            "sensitivity": "public",
        },
        "slop_risk": risk,
        "basis": "The sample provides enough material for a bounded quality-risk screen.",
        "input_coverage": coverage,
        "inspected_sections": inspected,
        "signals": {
            name: {
                "rating": "mixed",
                "evidence": f"Observed bounded evidence for {name}.",
                "confidence": "medium",
            }
            for name in SIGNALS
        },
        "uncertainty": "The screen is heuristic and does not verify facts or authorship.",
        "not_inferred": "The result is not a claim that the content is AI-generated or worthless.",
        "recommended_next_gate": "Perform human review or source verification before acting on the result.",
        "writeback_status": "none",
    }


def run_validator(artifact):
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "artifact.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(artifact, handle)
        result = subprocess.run(
            [sys.executable, VALIDATOR, path], capture_output=True, text=True, check=False
        )
        return result.returncode, json.loads(result.stdout)


class TestValidateContentSignalScreen(unittest.TestCase):
    def test_valid_medium(self):
        code, result = run_validator(valid_artifact())
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")

    def test_valid_indeterminate_metadata_only(self):
        code, result = run_validator(valid_artifact("indeterminate", "metadata_only", []))
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")

    def test_missing_signal_invalid(self):
        artifact = valid_artifact()
        del artifact["signals"]["author_footprint"]
        code, result = run_validator(artifact)
        self.assertEqual(code, 2)
        self.assertIn("missing signals", " ".join(result["errors"]))

    def test_empty_inspection_invalid_for_sample(self):
        code, result = run_validator(valid_artifact("medium", "sampled_content", []))
        self.assertEqual(code, 2)
        self.assertIn("inspected_sections", " ".join(result["errors"]))

    def test_ai_detector_field_forbidden(self):
        artifact = valid_artifact()
        artifact["ai_generated"] = True
        code, result = run_validator(artifact)
        self.assertEqual(code, 2)
        self.assertIn("forbidden", " ".join(result["errors"]))

    def test_v02_rejected(self):
        artifact = valid_artifact()
        artifact["schema_version"] = "0.2"
        code, result = run_validator(artifact)
        self.assertEqual(code, 2)
        self.assertIn("schema_version", " ".join(result["errors"]))

    def test_wrong_root_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "artifact.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(["not", "an", "object"], handle)
            result = subprocess.run(
                [sys.executable, VALIDATOR, path], capture_output=True, text=True, check=False
            )
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["status"], "invalid")


if __name__ == "__main__":
    unittest.main()
