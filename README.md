# Generador de Sílabas

Genera palabras con sílabas al azar (consonante + vocal) para proyectarlas en pantalla grande.

Está pensado para talleres de lectoescritura con personas adultas sin escolaridad previa: varias personas pueden participar sin que alguien tenga que escribir las sílabas en la pizarra. La dificultad se ajusta eligiendo qué consonantes se usan.

## Uso

- **Cantidad de sílabas:** cuántas sílabas tiene cada palabra (por defecto, 3).
- **Consonantes:** marca las que quieres practicar. Hay 35 opciones: simples, `ch`, `ll`, `ñ`, `qu`, `gu` y grupos como `cr`, `fr` o `tr`. Con pocas consonantes el ejercicio es más fácil. `qu` y `gu` siempre van con `e` o `i`. Si no marcas ninguna ni la vocal sola, se usa `m`.
- **Vocal sola (`a`):** además de consonante + vocal, pueden salir vocales sueltas.
- **Modo balanceado** (activo por defecto): dentro de una palabra evita repetir vocales mientras sea posible.
- **Modo coloreado** (activo por defecto): cada sílaba toma el color de su vocal (a azul, e rojo, i naranja, o verde, u morado). Apagado, el texto se muestra en blanco.
- **Generar:** botón o tecla Enter. Evita repetir la palabra anterior.
- **Zoom:** rueda del ratón para agrandar o reducir el texto (tamaño inicial 150).

La palabra se dibuja con la fuente Andika, que viaja dentro del programa: no hace falta instalarla.

**Privacidad:** el programa funciona sin conexión y no guarda ni envía datos de quienes participan.

## Instalación y ejecución

Pensado para Windows. Requiere Python 3.10 o superior para ejecutarlo desde el código.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
python run.py                   # o: python -m silabas
```

## Tests

```bash
pytest
```

## Generar el ejecutable (Windows)

PyInstaller crea el ejecutable del sistema operativo donde se ejecuta, por eso debe hacerse en Windows:

```bash
python scripts/build_exe.py             # un solo archivo: dist/GeneradorSilabas.exe
python scripts/build_exe.py --carpeta   # carpeta dist/GeneradorSilabas/ (abre más rápido)
```

El script incluye el icono y los recursos, y copia `LICENSE` y `THIRD_PARTY_NOTICES.md` junto al ejecutable.
Si compartes el ejecutable, entrégalo con esos dos archivos. Los ejecutables sin firma digital pueden
provocar el aviso de Windows SmartScreen o de algunos antivirus; es habitual en programas hechos con PyInstaller.

## Estructura

```
src/silabas/
├── __init__.py   Versión, autor y fecha
├── config.py     Constantes, colores, tema y valores por defecto
├── logic.py      Generación de palabras y segmentación (Python puro)
├── gui.py        Clase SilabasApp (CustomTkinter)
├── recursos.py   Carga de la fuente Andika y del icono
├── __main__.py   Arranque
└── assets/       Icono y fonts/ (Andika Regular y Bold, con su licencia)
tests/            Pruebas
scripts/          build_exe.py
run.py            Lanzador (desarrollo y PyInstaller)
CHANGELOG.md · LICENSE · THIRD_PARTY_NOTICES.md · AGENTS.md
```

## Licencia

Código publicado bajo licencia [MIT](LICENSE). Los iconos son obra de este proyecto y llevan la misma licencia.
El programa incluye la fuente Andika, © SIL International, bajo la SIL Open Font License 1.1 (`src/silabas/assets/fonts/OFL.txt`).
Las bibliotecas de terceros que usa están en [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Se ofrece «tal cual» y sin garantías (ver `LICENSE`). Es una herramienta de apoyo didáctico; no es un servicio
ni un dispositivo de salud.

## Autor

Benny Ronaldo Rojas Villadeza
