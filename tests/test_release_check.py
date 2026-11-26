import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("release_check", ROOT / "tools/release_check.py")
POLICY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(POLICY)


class PublicBoundary(unittest.TestCase):
    def test_private_state_is_rejected_even_with_broad_export_pattern(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            errors = POLICY.violations(root, [".private/context.json", "provider.session", ".env"], ["*"])
            self.assertEqual(len(errors), 3)
            self.assertTrue(all("private state" in error for error in errors))

    def test_symlink_cannot_bring_external_source_into_public_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "external.md").symlink_to(root.parent / "not-public")
            errors = POLICY.violations(root, ["external.md"], ["*.md"])
            self.assertEqual(len(errors), 1)
            self.assertIn("symlink", errors[0])

    def test_unreviewed_file_needs_explicit_public_scope(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("public documentation")
            self.assertEqual(POLICY.violations(root, ["README.md"], ["README.md"]), [])
            self.assertIn("outside reviewed", POLICY.violations(root, ["new-file.json"], ["README.md"])[0])

    def test_symlinked_parent_cannot_include_an_external_file(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root, external = base / "candidate", base / "external"
            root.mkdir()
            external.mkdir()
            (external / "record.md").write_text("installation-only fixture")
            (root / "docs").symlink_to(external, target_is_directory=True)
            errors = POLICY.violations(root, ["docs/record.md"], ["docs/*.md"])
            self.assertEqual(len(errors), 1)
            self.assertIn("outside the candidate", errors[0])


if __name__ == "__main__":
    unittest.main()
