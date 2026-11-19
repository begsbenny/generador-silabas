# Historial de cambios

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).
Las versiones siguen [SemVer](https://semver.org/lang/es/).

## [1.2.1] - 2026-11-19

### Corregido
- Coloreado de los grupos `qu` y `gu`: ahora se dibujan junto a su vocal (`e` o `i`) con el color de esa vocal.
- Con el modo coloreado apagado, el texto se muestra en blanco (antes en negro, casi invisible sobre el fondo oscuro).

### Cambiado
- Valores por defecto ajustados.
- La palabra se muestra con la fuente Andika, incluida con el programa (no depende de fuentes instaladas).
- Código reorganizado como paquete (`src/silabas/`) con `config`, `logic`, `gui` (clase `SilabasApp`), `recursos` y arranque, sin variables globales.
- Versión, autor y fecha pasan a `silabas/__init__.py`; el historial, a este archivo.
- Se quitó el correo de contacto de la ventana «Acerca de», que ahora indica la licencia.
- El autor figura con su nombre completo (Benny Ronaldo Rojas Villadeza).

### Añadido
- Icono de la aplicación, en la ventana y en el ejecutable.
- Licencia MIT (`LICENSE`) y avisos de licencias de terceros (`THIRD_PARTY_NOTICES.md`), incluida la de la fuente Andika.
- Pruebas automáticas con pytest.
- Script para generar el ejecutable en Windows (`scripts/build_exe.py`), README y AGENTS.md.

## [1.2.0] - 2026-11-06

### Cambiado
- Migración a CustomTkinter: interfaz moderna con bordes redondeados y tema visual agradable.

## [1.1.0] - 2025-10-25

### Añadido
- Modo coloreado.

### Cambiado
- Se evita repetir la última palabra generada.

## [1.0.0] - 2025-10-11

### Añadido
- Primera versión estable: generador de sílabas CV y CCV.
- Zoom dinámico con la rueda del ratón.
