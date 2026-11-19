"""Lógica pura del Generador de Sílabas.

Este módulo no depende de tkinter ni de CustomTkinter: solo genera texto plano.
La interfaz se encarga de dibujarlo.
"""

import random

from silabas import config

# Vocales del idioma y reglas de combinación
VOCALES = ("a", "e", "i", "o", "u")
DIGRAFOS_E_I = ("qu", "gu")      # Solo se combinan con 'e' o 'i'
VOCALES_QU_GU = ("e", "i")

MAX_INTENTOS = 100               # Intentos para evitar repetir la última palabra


def _vocales_base(opcion):
    """Vocales con las que puede combinarse una consonante."""
    return VOCALES_QU_GU if opcion in DIGRAFOS_E_I else VOCALES


def _tiene_vocal_libre(opcion, vocales_usadas):
    """Indica si una opción puede aportar una vocal aún no usada en la palabra."""
    if opcion in VOCALES:
        return opcion not in vocales_usadas
    return any(v not in vocales_usadas for v in _vocales_base(opcion))


def _elegir_opcion(opciones, vocales_usadas, modo_balanceado):
    """Elige una opción (consonante o vocal sola) al azar.

    En modo balanceado prioriza las que aún pueden aportar una vocal sin usar.
    Si ninguna puede, vuelve a considerar todas las opciones.
    """
    if modo_balanceado:
        filtradas = [op for op in opciones if _tiene_vocal_libre(op, vocales_usadas)]
        return random.choice(filtradas or opciones)
    return random.choice(opciones)


def _elegir_vocal(consonante, vocales_usadas, modo_balanceado):
    """Elige la vocal que acompañará a una consonante."""
    base = _vocales_base(consonante)
    if modo_balanceado:
        libres = [v for v in base if v not in vocales_usadas]
        if libres:
            return random.choice(libres)
    return random.choice(base)


def generar_silaba(opciones, vocales_usadas, modo_balanceado):
    """Genera una sílaba. Devuelve (texto_de_la_silaba, vocal_usada)."""
    elem = _elegir_opcion(opciones, vocales_usadas, modo_balanceado)
    if elem in VOCALES:
        return elem, elem
    vocal = _elegir_vocal(elem, vocales_usadas, modo_balanceado)
    return elem + vocal, vocal


def _construir_palabra(n, opciones, modo_balanceado):
    """Une n sílabas generadas al azar en una sola palabra."""
    partes = []
    vocales_usadas = set()
    for _ in range(n):
        silaba, vocal = generar_silaba(opciones, vocales_usadas, modo_balanceado)
        partes.append(silaba)
        vocales_usadas.add(vocal)
    return "".join(partes)


def generar_palabra(n, opciones, modo_balanceado, ultima_palabra=None):
    """Genera una palabra de n sílabas y la devuelve en texto plano.

    Args:
        n: cantidad de sílabas (entero > 0).
        opciones: lista de consonantes y/o vocales solas permitidas.
        modo_balanceado: si es True, evita repetir vocales dentro de la palabra
            mientras sea posible.
        ultima_palabra: palabra anterior; se intenta no repetirla.

    Raises:
        ValueError: si n no es positivo o no hay opciones.
    """
    if n <= 0:
        raise ValueError("La cantidad de sílabas debe ser mayor que 0.")
    if not opciones:
        raise ValueError("Debe haber al menos una opción seleccionada.")

    palabra = ""
    for _ in range(MAX_INTENTOS):
        palabra = _construir_palabra(n, opciones, modo_balanceado)
        if palabra != ultima_palabra:
            break
    return palabra


def _buscar_consonante(texto, i):
    """Devuelve la consonante (simple o compuesta) que empieza en texto[i], o None."""
    for c in config.CONSONANTES_ORDENADAS:
        if texto.startswith(c, i):
            if c in DIGRAFOS_E_I:
                # 'qu' / 'gu' solo cuentan como grupo si les sigue 'e' o 'i'
                sig = i + len(c)
                if sig < len(texto) and texto[sig].lower() in VOCALES_QU_GU:
                    return c
            else:
                return c
    return None


def segmentar(texto):
    """Divide una palabra en grupos para dibujarla: [(grupo, vocal), ...].

    `vocal` es la letra que decide el color del grupo; toda la sílaba
    (consonante + vocal) comparte la misma. Es None si el grupo no tiene
    vocal asociada (consonante al final de la palabra).

    Ejemplo: "quema" -> [("qu","e"), ("e","e"), ("m","a"), ("a","a")]
    """
    grupos = []
    i = 0
    while i < len(texto):
        # Vocal sola
        if texto[i].lower() in VOCALES:
            grupos.append((texto[i], texto[i]))
            i += 1
            continue

        cons = _buscar_consonante(texto, i)
        if cons:
            fin = i + len(cons)
            if fin < len(texto):
                voc = texto[fin]
                grupos.append((texto[i:fin], voc))
                grupos.append((voc, voc))
                i = fin + 1
            else:
                grupos.append((texto[i:fin], None))
                i = fin
        elif i + 1 < len(texto):
            voc = texto[i + 1]
            grupos.append((texto[i], voc))
            grupos.append((voc, voc))
            i += 2
        else:
            grupos.append((texto[i], None))
            i += 1
    return grupos
