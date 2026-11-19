"""Pruebas de metadatos y empaquetado de silabas."""

import os
import re
import subprocess
import sys
from pathlib import Path

import silabas

RAIZ = Path(__file__).resolve().parents[1]


def test_version_tiene_formato_x_y_z():
    assert re.fullmatch(r"\d+\.\d+\.\d+", silabas.__version__)


def test_fecha_tiene_formato_iso():
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", silabas.__date__)


def test_copyright_incluye_autor_y_rango_de_anios():
    assert silabas.__author__ in silabas.__copyright__
    assert silabas.__date__[:4] in silabas.__copyright__


def test_changelog_documenta_la_version_actual():
    changelog = (RAIZ / "CHANGELOG.md").read_text(encoding="utf-8")
    assert f"## [{silabas.__version__}]" in changelog


def test_importar_el_paquete_no_carga_librerias_visuales():
    # En un subproceso, para que no dependa de lo que importen otros tests
    codigo = (
        "import sys, silabas; "
        "assert 'tkinter' not in sys.modules and 'customtkinter' not in sys.modules"
    )
    entorno = {**os.environ, "PYTHONPATH": str(RAIZ / "src")}
    r = subprocess.run([sys.executable, "-c", codigo], env=entorno, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def test_licencia_mit_a_nombre_del_autor():
    licencia = (RAIZ / "LICENSE").read_text(encoding="utf-8")
    assert licencia.startswith("MIT License")
    assert silabas.__author__ in licencia
    assert silabas.__license__ == "MIT"


def _archivos_publicos():
    return [*(RAIZ / "src").rglob("*.py"), RAIZ / "README.md", RAIZ / "pyproject.toml", RAIZ / "CHANGELOG.md"]


def test_no_hay_correos_en_el_codigo_publicado():
    patron = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
    for archivo in _archivos_publicos():
        assert not patron.search(archivo.read_text(encoding="utf-8")), archivo


def test_no_quedan_textos_de_derechos_reservados():
    for archivo in _archivos_publicos():
        assert "derechos reservados" not in archivo.read_text(encoding="utf-8").lower(), archivo
