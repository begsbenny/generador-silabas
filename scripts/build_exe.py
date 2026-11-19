"""Genera el ejecutable de Windows con PyInstaller.

Uso, en Windows y con el entorno virtual activo:
    pip install -e ".[dev]"
    python scripts/build_exe.py             # un solo archivo: dist/GeneradorSilabas.exe
    python scripts/build_exe.py --carpeta   # carpeta dist/GeneradorSilabas/ (abre más rápido)

Incluye el icono y los recursos de assets/, y copia LICENSE y THIRD_PARTY_NOTICES.md junto al
ejecutable. PyInstaller crea el ejecutable del sistema operativo donde se ejecuta, por eso
este script solo funciona en Windows.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

NOMBRE = "GeneradorSilabas"
PAQUETE = "silabas"
RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "src" / PAQUETE / "assets"


def main():
    parser = argparse.ArgumentParser(description="Genera el ejecutable de Generador de Sílabas.")
    parser.add_argument("--carpeta", action="store_true", help="genera una carpeta en lugar de un solo archivo")
    args = parser.parse_args()

    if sys.platform != "win32":
        sys.exit("Este script debe ejecutarse en Windows para generar un .exe.")
    if not (ASSETS / "icon.ico").exists():
        sys.exit(f"Falta el icono: {ASSETS / 'icon.ico'}")

    import PyInstaller.__main__ as pyinstaller

    pyinstaller.run([
        str(RAIZ / "run.py"),
        "--name", NOMBRE,
        "--onedir" if args.carpeta else "--onefile",
        "--noconsole",                                        # Sin ventana negra de consola
        "--icon", str(ASSETS / "icon.ico"),
        "--paths", str(RAIZ / "src"),
        "--collect-all", "customtkinter",                     # Temas y recursos de CustomTkinter
        "--add-data", f"{ASSETS}{os.pathsep}{PAQUETE}/assets",   # Icono y fuentes
        "--distpath", str(RAIZ / "dist"),
        "--workpath", str(RAIZ / "build"),
        "--specpath", str(RAIZ / "build"),
        "--noconfirm",
    ])

    # Las licencias deben acompañar al ejecutable
    destino = RAIZ / "dist" / (NOMBRE if args.carpeta else "")
    for nombre in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
        shutil.copy2(RAIZ / nombre, destino / nombre)


if __name__ == "__main__":
    main()
