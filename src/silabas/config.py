"""Configuración del Generador de Sílabas: constantes, colores, tema y valores por defecto.

Los metadatos (versión, autor, fecha) están en silabas/__init__.py
y el historial de cambios en CHANGELOG.md.
"""

# --- Tema de CustomTkinter ---
APARIENCIA = "dark"      # "dark" o "light"
TEMA_COLOR = "blue"      # "blue", "green", "dark-blue"


def aplicar_tema():
    """Aplica el tema de CustomTkinter. Llamar antes de crear la ventana.

    customtkinter se importa aquí (y no arriba) para que este módulo, y por
    tanto logic.py y los tests, no dependan de ninguna librería visual.
    """
    import customtkinter as ctk

    ctk.set_appearance_mode(APARIENCIA)
    ctk.set_default_color_theme(TEMA_COLOR)


# --- Ventana ---
ARCHIVO_ICONO = "icon.ico"   # En assets/; se usa en la ventana y en el ejecutable
VENTANA_ALTO = 520

# --- Texto / zoom ---
FONT_SIZE_INICIAL = 150
FONT_SIZE_MIN = 80
FONT_SIZE_MAX = 280
FONT_SIZE_PASO = 10
FUENTE_PALABRA = "Andika"
FUENTE_PALABRA_RESPALDO = "Verdana"
ARCHIVOS_FUENTE = ("Andika-Regular.ttf", "Andika-Bold.ttf")

# --- Generación ---
SILABAS_INICIAL = 3
CONSONANTE_POR_DEFECTO = "m"   # Se activa si no hay ninguna opción seleccionada

# --- Canvas ---
CANVAS_BG_OSCURO = "#2b2b2b"
CANVAS_BG_CLARO = "#d9d9d9"
COLOR_TEXTO_NEUTRO = "white"   # Color de las letras cuando el modo coloreado está apagado

# --- Paleta de colores para vocales ---
colores_vocales = {
    'a': '#0074D9',  # Azul
    'e': '#FF4136',  # Rojo
    'i': '#FF851B',  # Naranja
    'o': '#2ECC40',  # Verde
    'u': '#6F42C1',  # Morado oscuro
}

# --- Consonantes disponibles ---
CONSONANTES = [
    'm', 's', 'p', 'l', 'r', 't', 'c', 'd', 'f', 'b', 'n', 'z', 'v', 'g', 'h',
    'ch', 'k', 'j', 'qu', 'gu', 'll', 'y', 'ñ',
    'cr', 'fr', 'pl', 'gr', 'br', 'tr', 'bl', 'cl', 'dr', 'fl', 'gl', 'pr',
]

# Mismas consonantes, de mayor a menor longitud (para reconocer 'ch', 'cr', 'qu'... antes que 'c', 'q'...)
CONSONANTES_ORDENADAS = sorted(CONSONANTES, key=len, reverse=True)

# Distribución de los checkboxes de consonantes en la interfaz
MAX_POR_FILA = 12
