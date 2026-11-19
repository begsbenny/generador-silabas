"""Recursos incluidos con el programa: fuente Andika e icono de la ventana.

Las librerías gráficas se importan dentro de las funciones, así este módulo se puede importar sin ellas.
"""

import sys
import warnings
from pathlib import Path

from silabas import config

# Funciona igual en desarrollo y dentro del .exe de PyInstaller
RUTA_ASSETS = Path(__file__).resolve().parent / "assets"
RUTA_FUENTES = RUTA_ASSETS / "fonts"


def cargar_fuente(ventana):
    """Carga Andika desde assets/fonts y devuelve el nombre de la fuente a usar.

    La fuente se registra solo para este programa (no se instala en el equipo). Si no se puede cargar,
    avisa y devuelve la fuente de respaldo, para que la proyección nunca falle.
    Requiere que la ventana ya esté creada.
    """
    from tkinter import font as tkfont

    if sys.platform == "win32":
        import ctypes

        gdi32 = ctypes.windll.gdi32
        gdi32.AddFontResourceExW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p]
        gdi32.AddFontResourceExW.restype = ctypes.c_int

        for archivo in config.ARCHIVOS_FUENTE:
            try:
                gdi32.AddFontResourceExW(str(RUTA_FUENTES / archivo), 0x10, None)
            except Exception:
                pass   # se detecta abajo al comprobar la familia
    else:
        import customtkinter as ctk

        for archivo in config.ARCHIVOS_FUENTE:
            try:
                ctk.FontManager.load_font(str(RUTA_FUENTES / archivo))
            except Exception:
                pass   # se detecta abajo al comprobar la familia

    if config.FUENTE_PALABRA in tkfont.families(ventana):
        return config.FUENTE_PALABRA
    warnings.warn(f"No se pudo cargar la fuente {config.FUENTE_PALABRA}; se usa {config.FUENTE_PALABRA_RESPALDO}.")
    return config.FUENTE_PALABRA_RESPALDO


def aplicar_icono(ventana):
    """Pone el icono del programa en la ventana (barra de título y barra de tareas)."""
    ruta = RUTA_ASSETS / config.ARCHIVO_ICONO

    def poner():
        try:
            ventana.iconbitmap(str(ruta))
        except Exception:
            pass   # sistemas sin soporte de .ico: se deja el icono por defecto

    # CustomTkinter pone su propio icono unos 200 ms después de abrir la ventana: se reemplaza justo después
    ventana.after(300, poner)