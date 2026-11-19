# Guía para agentes — Generador de Sílabas

App de escritorio en Python (CustomTkinter). Layout `src/`, paquete `silabas`.

## Mapa: qué archivo tocar
| Quiero cambiar… | Archivo |
|---|---|
| Versión, autor, fecha, licencia | `src/silabas/__init__.py` |
| Historial de cambios | `CHANGELOG.md` |
| Colores, tamaños y zoom, valores por defecto, tema, nombre de la fuente | `src/silabas/config.py` |
| Cómo se carga la fuente Andika y el icono | `src/silabas/recursos.py` |
| Archivos de la fuente y del icono | `src/silabas/assets/` |
| Lógica de generación (sin interfaz) | `src/silabas/logic.py` |
| Widgets, layout, dibujo, zoom, eventos | `src/silabas/gui.py` |
| Arranque de la app | `src/silabas/__main__.py` |
| Generar el .exe (solo en Windows) | `scripts/build_exe.py` |

## Reglas
- `logic.py` es Python puro: **nunca** importar tkinter ni customtkinter (ni en `config.py` ni en `__init__.py` a nivel de módulo).
- `__init__.py` solo contiene el docstring y los metadatos; no importa nada del paquete.
- Sin variables globales: el estado vive en atributos de `SilabasApp` (`self.ultima_palabra`, `self.font_size`).
- Todo valor configurable (colores, límites, textos fijos) va en `config.py`, no en línea.
- No romper el cálculo de ancho con `canvas.bbox` en `mostrar_palabra` ni el zoom (`<MouseWheel>`, `<Button-4/5>`).
- No depender de fuentes instaladas en el equipo: las fuentes se cargan desde `assets/fonts`.
- No incluir datos personales de contacto (correos, teléfonos) en el código ni en la interfaz.
- La única fuente incluida es Andika (Regular y Bold) con su `OFL.txt`. No añadir otras sin anotar su licencia en `THIRD_PARTY_NOTICES.md`.
- Los recursos viven en `src/silabas/assets/`, dentro del paquete (así viajan en el `.exe`).
- El `.exe` solo se genera en Windows (`python scripts/build_exe.py`).
- Licencia MIT: no añadir textos de «derechos reservados»; si se añade una dependencia, anotar su licencia en `THIRD_PARTY_NOTICES.md`.
- Todo cambio en `logic.py` debe llevar su test en `tests/test_logic.py`.
- Al publicar una versión: actualizar `__version__` y `__date__` en `__init__.py` y añadir su entrada `## [X.Y.Z]` en `CHANGELOG.md` (un test lo comprueba).

## Comandos
- Instalar: `pip install -e ".[dev]"`
- Probar: `pytest`
- Ejecutar: `python run.py`
- Compilar .exe (solo Windows): `python scripts/build_exe.py` (o `--carpeta`)

## Nota
La GUI no tiene tests automáticos; verificarla abriendo la app (generar, zoom con rueda, redimensionar, modo coloreado).
