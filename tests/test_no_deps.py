import importlib
import json
import os
import shutil
import sys
import unittest
from pathlib import Path


class NoDepsModeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_root = Path("tests/tmp_no_deps").resolve()
        if self.tmp_root.exists():
            shutil.rmtree(self.tmp_root)
        self.tmp_root.mkdir(parents=True)

        self.addCleanup(self._cleanup_environment)

    def _cleanup_environment(self) -> None:
        shutil.rmtree(self.tmp_root, ignore_errors=True)
        for key in ("NO_DEPS", "AFI_OUTPUT_DIR"):
            os.environ.pop(key, None)
        for module_name in ("editor_video", "environment"):
            sys.modules.pop(module_name, None)

    def test_dummy_artifacts_created(self) -> None:
        output_dir = (self.tmp_root / "output").resolve()
        os.environ["NO_DEPS"] = "1"
        os.environ["AFI_OUTPUT_DIR"] = str(output_dir)

        sys.modules.pop("environment", None)
        sys.modules.pop("editor_video", None)

        editor = importlib.import_module("editor_video")
        importlib.reload(editor)

        target_path = self.tmp_root / "output" / "custom.mp4"
        sucesso = editor.executar_modo_simulado(
            str(target_path),
            origem="input_video.mp4",
            musica="music.mp3",
            texto="demo text",
        )

        self.assertTrue(sucesso)

        dummy_mp4 = editor.SETTINGS.output_dir / "dummy_arquivo.mp4"
        dummy_json = editor.SETTINGS.output_dir / "dummy_arquivo.json"

        self.assertTrue(dummy_mp4.exists(), "dummy_arquivo.mp4 nao foi criado")
        self.assertTrue(dummy_json.exists(), "dummy_arquivo.json nao foi criado")
        self.assertTrue(target_path.exists(), "arquivo de destino solicitado nao foi gerado")

        payload = json.loads(dummy_json.read_text(encoding="utf-8"))
        self.assertEqual(payload.get("status"), "simulado")
        self.assertEqual(
            Path(payload.get("destino_solicitado")).resolve(),
            target_path.resolve(),
        )


if __name__ == "__main__":
    unittest.main()
