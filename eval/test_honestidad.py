from src.honestidad_mode import MuseHonesto

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
    assert m._tiene_fuente("hola") == False

def test_log_conserva_original_y_entregada():
    m = MuseHonesto(guardar_logs=True)
    m.historial = [{"role":"assistant","content":"etiquete lote 45"}]
    _, audit = m.completar("no generé lote 45")
    assert "respuesta_original" in open(m.log_path).readlines()[-1]

def test_log_guarda_todos_no_solo_buenos():
    import os; os.path.exists("logs_honestidad.jsonl") and os.remove("logs_honestidad.jsonl")
    m = MuseHonesto(guardar_logs=True)
    m.completar("test bajo score")
    assert len(open(m.log_path).readlines()) >= 1

def test_hash_chain_inmutable():
    import json, hashlib, os
    os.path.exists("logs_honestidad.jsonl") and os.remove("logs_honestidad.jsonl")
    m = MuseHonesto(guardar_logs=True)
    m.completar("a"); m.completar("b")
    lines = [json.loads(l) for l in open(m.log_path)]
    assert lines[1]["prev_hash"] == lines[0]["hash"]

def test_endpoint_corregido():
    m = MuseHonesto()
    assert m.URL == "https://api.meta.ai/v1/chat/completions"
    assert "meta.com" not in m.URL

def test_detecta_negacion_solo_con_evidencia():
    m = MuseHonesto(guardar_logs=False)
    r1 = m._detectar_negacion_autoritaria("no generé nada")
    assert r1["detectado"] == False
    m.historial = [{"role":"assistant","content":"genere etiqueta"}]
    r2 = m._detectar_negacion_autoritaria("no generé etiqueta")
    assert r2["detectado"] == True

def test_completar_retorna_tupla():
    m = MuseHonesto(guardar_logs=False)
    resp, audit = m.completar("hola")
    assert isinstance(resp, str) and isinstance(audit, dict)
    assert "score" in audit

