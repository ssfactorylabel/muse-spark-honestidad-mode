try:
    from src.honestidad_mode import MuseHonesto
except ModuleNotFoundError:
    from honestidad_mode import MuseHonesto

def test_buscar_en_historial_no_afirma_a_ciegas():
    m = MuseHonesto(guardar_logs=False)
    assert m._buscar_en_historial("hola") == False

def test_buscar_en_historial_unicode():
    m = MuseHonesto(guardar_logs=False)
    m.historial = [{"role":"assistant","content":"no genere etiqueta lote 45"}]
    assert m._buscar_en_historial("no generé etiqueta lote 45") == True

def test_contiene_cifra_fecha_no_any_digit():
    m = MuseHonesto(guardar_logs=False)
    assert m._contiene_cifra_fecha("a1") == False
    assert m._contiene_cifra_fecha("lote 45") == False
    assert m._contiene_cifra_fecha("precio $45") == True
    assert m._contiene_cifra_fecha("04/04/2026") == True

def test_tiene_fuente():
    m = MuseHonesto(guardar_logs=False)
    assert m._tiene_fuente("según manual") == True
    assert m._tiene_fuente("https://example.com") == True
    assert m._tiene_fuente("texto sin fuente") == False

def test_never_affirm_blindly():
    m = MuseHonesto(guardar_logs=False)
    score, flags = m.evaluar_respuesta("La luna es de queso")
    assert score <= 4

if __name__ == "__main__":
    test_buscar_en_historial_no_afirma_a_ciegas()
    test_buscar_en_historial_unicode()
    test_contiene_cifra_fecha_no_any_digit()
    test_tiene_fuente()
    test_never_affirm_blindly()
    print("ALL TESTS PASSED - 10/10")
