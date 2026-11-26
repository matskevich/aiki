import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("release_manifest", ROOT / "tools/release_manifest.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ExactArtifact(unittest.TestCase):
    def test_changed_or_extra_source_is_not_the_validated_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("reviewed")
            MODULE.seal(root, "preview", "0.1.0-preview.1")
            MODULE.verify(root)
            (root / "README.md").write_text("changed")
            with self.assertRaisesRegex(ValueError, "content_changed"):
                MODULE.verify(root)
            (root / "README.md").write_text("reviewed")
            (root / "extra.json").write_text("{}")
            with self.assertRaisesRegex(ValueError, "content_changed"):
                MODULE.verify(root)

    def test_private_provenance_is_not_required_in_public_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("same bytes")
            first = MODULE.seal(root, "preview", "0.1.0-preview.1")
            second = MODULE.seal(root, "public", "0.1.0")
            self.assertEqual(first["content_sha256"], second["content_sha256"])
            self.assertNotIn("source_revision", second)
            MODULE.verify(root)

    def test_source_symlink_is_rejected_before_sealing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").symlink_to(root.parent / "private")
            with self.assertRaisesRegex(ValueError, "symlink"):
                MODULE.seal(root, "preview", "0.1.0")


if __name__ == "__main__":
    unittest.main()
