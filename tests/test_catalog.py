import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CatalogContract(unittest.TestCase):
    def invoke(self, *arguments, catalog=None):
        with tempfile.TemporaryDirectory() as directory:
            command = [sys.executable, str(ROOT / "tools/catalog.py")]
            if catalog is not None:
                path = Path(directory) / "catalog.json"
                path.write_text(json.dumps(catalog))
                command += ["--catalog", str(path)]
            return subprocess.run(command + list(arguments), capture_output=True, text=True, timeout=10)

    def source(self):
        return json.loads((ROOT / "registry/components.json").read_text())

    def test_plan_requires_tasks_but_does_not_enable_optional_devices(self):
        result = self.invoke("plan", "orchestration", "notifications")
        self.assertEqual(result.returncode, 0, result.stderr)
        value = json.loads(result.stdout)
        self.assertEqual([c["id"] for c in value["ordered_components"]],
                         ["tasks", "orchestration", "notifications"])
        self.assertEqual(value["execution"], "none")
        self.assertEqual(value["independent_acceptance"], "not_established_by_plan")
        self.assertIn("orchestration", value["availability_gaps"])

    def test_unknown_component_has_actionable_error(self):
        result = self.invoke("plan", "unknown-piece")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown component: unknown-piece", result.stderr)

    def test_metadata_cannot_masquerade_as_live_probe(self):
        catalog = self.source()
        catalog["components"][0]["live_status"] = "ready"
        result = self.invoke("list", catalog=catalog)
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot assert live readiness", result.stderr)

    def test_rejects_dependency_cycle_before_reporting_plan(self):
        catalog = self.source()
        index = {c["id"]: c for c in catalog["components"]}
        index["tasks"]["requires"] = ["orchestration"]
        index["tasks"]["optional"] = []
        result = self.invoke("plan", "orchestration", catalog=catalog)
        self.assertEqual(result.returncode, 2)
        self.assertIn("dependency cycle", result.stderr)


if __name__ == "__main__":
    unittest.main()
