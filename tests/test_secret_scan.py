import importlib.util
import io
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("secret_scan", ROOT / "tools/secret_scan.py")
SCANNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCANNER)


class ScannerIntegrity(unittest.TestCase):
    def test_modified_download_is_rejected_before_archive_or_execution(self):
        with patch("sys.argv", ["secret_scan.py", "--download"]), \
             patch.object(SCANNER.platform, "system", return_value="Linux"), \
             patch.object(SCANNER.platform, "machine", return_value="x86_64"), \
             patch.object(SCANNER.urllib.request, "urlopen", return_value=io.BytesIO(b"modified binary")), \
             patch.object(SCANNER, "scan") as execute:
            with self.assertRaisesRegex(SystemExit, "integrity check failed"):
                SCANNER.main()
            execute.assert_not_called()


if __name__ == "__main__":
    unittest.main()
