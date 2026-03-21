import tempfile
import unittest
from pathlib import Path

from compose.detector import detect_signals


class TestComposeDetector(unittest.TestCase):
    def test_detect_signals_finds_python_and_github_actions(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "requirements.txt").write_text("pyyaml", encoding="utf-8")
            (root / "app.py").write_text("print('hi')", encoding="utf-8")
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "ci.yml").write_text("name: ci", encoding="utf-8")

            detected = detect_signals(root)

        self.assertIn("python", detected)
        self.assertIn("ci_github_actions", detected)

    def test_detect_signals_scans_subdirectories_for_monorepo_union(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            backend = root / "services" / "backend"
            frontend = root / "apps" / "web"
            backend.mkdir(parents=True)
            frontend.mkdir(parents=True)
            (backend / "service.py").write_text("print('backend')", encoding="utf-8")
            (frontend / "package.json").write_text('{"name":"web"}', encoding="utf-8")
            (frontend / "ui.ts").write_text("export const x = 1;", encoding="utf-8")

            detected = detect_signals(root)

        self.assertIn("python", detected)
        self.assertIn("typescript", detected)

    def test_detect_signals_uses_pyproject_as_python_signal(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")

            detected = detect_signals(root)

        self.assertIn("python", detected)


if __name__ == "__main__":
    unittest.main()
