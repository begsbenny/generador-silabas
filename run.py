"""Lanzador para desarrollo y para PyInstaller: `python run.py`."""

import sys
from pathlib import Path

# Permite ejecutar sin instalar el paquete (layout src/)
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from silabas.__main__ import main

if __name__ == "__main__":
    main()
