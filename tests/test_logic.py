"""Pruebas de silabas.logic (Python puro, no abren ninguna ventana)."""

import pytest

from silabas import config, logic

OPCIONES = ["m", "s", "qu", "gu", "cr"] + list(logic.VOCALES)


def _vocales_de_silabas(palabra):
    """Vocales de una palabra ignorando la 'u' muda de qu/gu."""
    limpia = palabra.replace("qu", "q").replace("gu", "g")
    return [c for c in limpia if c in logic.VOCALES]


# --- generar_palabra ---------------------------------------------------

def test_longitud_segun_cantidad_de_silabas():
    palabra = logic.generar_palabra(3, ["m"], modo_balanceado=False)
    assert len(palabra) == 6                       # 3 sílabas CV
    assert palabra[0::2] == "mmm"


def test_modo_balanceado_no_repite_vocales():
    for _ in range(1000):
        vocales = _vocales_de_silabas(logic.generar_palabra(5, OPCIONES, True))
        assert len(vocales) == 5 and len(set(vocales)) == 5


def test_qu_y_gu_solo_con_e_o_i():
    for _ in range(500):
        palabra = logic.generar_palabra(4, ["qu", "gu"], False)
        silabas = [palabra[i:i + 3] for i in range(0, len(palabra), 3)]
        assert all(s in ("que", "qui", "gue", "gui") for s in silabas)


def test_no_repite_la_ultima_palabra():
    for _ in range(300):
        assert logic.generar_palabra(1, ["m"], False, ultima_palabra="ma") != "ma"


def test_vocales_solas_aparecen_sin_consonante():
    palabra = logic.generar_palabra(5, list(logic.VOCALES), True)
    assert sorted(palabra) == sorted(logic.VOCALES)


@pytest.mark.parametrize("n, opciones", [(0, ["m"]), (-2, ["m"]), (3, [])])
def test_argumentos_invalidos(n, opciones):
    with pytest.raises(ValueError):
        logic.generar_palabra(n, opciones, True)


# --- segmentar ---------------------------------------------------------

@pytest.mark.parametrize("texto, esperado", [
    ("ma",    [("m", "a"), ("a", "a")]),
    ("a",     [("a", "a")]),
    ("cro",   [("cr", "o"), ("o", "o")]),
    ("chi",   [("ch", "i"), ("i", "i")]),
    ("que",   [("qu", "e"), ("e", "e")]),
    ("gui",   [("gu", "i"), ("i", "i")]),
    ("masa",  [("m", "a"), ("a", "a"), ("s", "a"), ("a", "a")]),
    ("ch",    [("ch", None)]),                      # consonante sin vocal al final
    ("",      []),
])
def test_segmentar(texto, esperado):
    assert logic.segmentar(texto) == esperado


def test_segmentar_reconstruye_la_palabra():
    for _ in range(500):
        palabra = logic.generar_palabra(4, OPCIONES, False)
        assert "".join(g for g, _ in logic.segmentar(palabra)) == palabra


def test_logic_no_depende_de_librerias_visuales():
    import sys
    assert "tkinter" not in sys.modules
    assert "customtkinter" not in sys.modules


def test_la_paleta_tiene_un_color_por_vocal():
    assert set(config.colores_vocales) == set(logic.VOCALES)


def test_las_consonantes_se_generan_y_se_reconocen_todas():
    # Cada consonante configurada produce palabras que se segmentan empezando por ella
    for consonante in config.CONSONANTES:
        for _ in range(20):
            palabra = logic.generar_palabra(1, [consonante], modo_balanceado=False)
            primer_grupo, vocal = logic.segmentar(palabra)[0]
            assert primer_grupo == consonante, (consonante, palabra)
            assert vocal in logic.VOCALES


def test_modo_balanceado_con_mas_silabas_que_vocales_no_falla():
    palabra = logic.generar_palabra(8, ["m", "s"], modo_balanceado=True)
    assert len(palabra) == 16                              # 8 sílabas consonante + vocal


def test_la_palabra_solo_contiene_letras_configuradas():
    permitidas = set("".join(config.CONSONANTES)) | set(logic.VOCALES)
    for _ in range(300):
        palabra = logic.generar_palabra(4, config.CONSONANTES + list(logic.VOCALES), True)
        assert set(palabra) <= permitidas
