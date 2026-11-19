"""Pruebas de los recursos incluidos: fuente Andika, icono y empaquetado."""

import struct
from pathlib import Path

from silabas import config

RAIZ = Path(__file__).resolve().parents[1]          # No depende de la carpeta desde la que se ejecute pytest
ASSETS = RAIZ / "src" / "silabas" / "assets"
FUENTES = ASSETS / "fonts"
PATRONES_PAQUETE = ("assets/*", "assets/fonts/*")


def test_la_fuente_de_la_palabra_es_andika():
    assert config.FUENTE_PALABRA == "Andika"
    assert all(nombre.startswith("Andika-") for nombre in config.ARCHIVOS_FUENTE)


def test_solo_se_incluye_andika_regular_y_bold_con_su_licencia():
    assert {p.name for p in FUENTES.iterdir()} == set(config.ARCHIVOS_FUENTE) | {"OFL.txt"}


def test_las_fuentes_son_archivos_ttf_de_andika():
    for nombre in config.ARCHIVOS_FUENTE:
        datos = (FUENTES / nombre).read_bytes()
        assert datos[:4] == b"\x00\x01\x00\x00"                  # firma TrueType
        assert len(datos) > 50_000
        assert b"Andika" in datos or "Andika".encode("utf-16-be") in datos


def test_la_licencia_de_la_fuente_esta_incluida_y_avisada():
    ofl = (FUENTES / "OFL.txt").read_text(encoding="utf-8")
    assert "SIL OPEN FONT LICENSE" in ofl.upper() and "Andika" in ofl
    avisos = (RAIZ / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    assert "Andika" in avisos and "SIL Open Font License" in avisos


def test_no_quedan_recursos_sueltos_fuera_del_paquete():
    assert not (RAIZ / "src" / "assets").exists()


def test_el_icono_es_un_ico_valido_con_los_tamanos_necesarios():
    datos = (ASSETS / config.ARCHIVO_ICONO).read_bytes()
    reservado, tipo, cantidad = struct.unpack("<HHH", datos[:6])
    assert (reservado, tipo) == (0, 1)                       # firma de un archivo .ico
    tamanos = {datos[6 + 16 * i] or 256 for i in range(cantidad)}
    assert {16, 32, 48, 256} <= tamanos


def test_los_datos_del_paquete_incluyen_los_recursos():
    pyproject = (RAIZ / "pyproject.toml").read_text(encoding="utf-8")
    assert "[tool.setuptools.package-data]" in pyproject
    for patron in PATRONES_PAQUETE:
        assert f'"{patron}"' in pyproject


def test_el_script_del_ejecutable_incluye_icono_y_recursos():
    script = (RAIZ / "scripts" / "build_exe.py").read_text(encoding="utf-8")
    assert "--icon" in script and "--add-data" in script
    assert "LICENSE" in script and "THIRD_PARTY_NOTICES.md" in script
