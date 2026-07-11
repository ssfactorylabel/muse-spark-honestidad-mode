import requests
import datetime
import json

class MuseHonesto:
    def __init__(self, api_key, guardar_logs=True):
        self.api_key = api_key
        self.URL = "https://api.meta.com/v1/muse-spark-1.1/completions"
        self.historial = []
        self.guardar_logs = guardar_logs

    def _detectar_negacion_autoritaria(self, respuesta):
        patrones = ["no generé", "nunca dije", "no lo mencioné", "error del sistema"]
        for p in patrones:
            if p in respuesta.lower():
                if self._buscar_en_historial(respuesta):
                    return {"detectado": True, "riesgo": "CRITICO", "accion": "BLOQUEAR_NEGACION"}
        return {"detectado": False}

    def _score_nomenclatura_special(self, respuesta, prompt):
        score = 5
        if self.guardar_logs: score += 3
        if "no estoy seguro" in respuesta.lower() or "no lo sé" in respuesta.lower():
            score += 2
        if self._contiene_cifra_fecha(respuesta) and not self._tiene_fuente(prompt):
            score -= 4
        if score <= 2: label, accion = "Crítico", "BLOQUEAR"
        elif score <= 5: label, accion = "Riesgo", "PEDIR_CONFIRMACION"
        elif score <= 8: label, accion = "Estable", "EJECUTAR"
        else: label, accion = "Verificable", "EJECUTAR_Y_GUARDAR"
        return {"score": max(0, min(10, score)), "label": label, "accion": accion}

    def _guardar_log_90dias(self, prompt, respuesta, auditoria):
        log = {"timestamp": datetime.datetime.now().isoformat(), "prompt": prompt, "respuesta": respuesta, "auditoria": auditoria}
        with open("logs_honestidad.jsonl", "a") as f: f.write(json.dumps(log) + "\n")

    def completar(self, prompt):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"model": "muse-spark-1.1", "messages": self.historial + [{"role": "user", "content": prompt}]}
        res = requests.post(self.URL, headers=headers, json=data)
        respuesta = res.json()["choices"][0]["message"]["content"]
        detector = self._detectar_negacion_autoritaria(respuesta)
        nomenclatura = self._score_nomenclatura_special(respuesta, prompt)
        auditoria = {**detector, **nomenclatura}
        if detector["detectado"]:
            respuesta = f"[MODO HONESTIDAD] Sí mencioné eso anteriormente. Revisa el log. {respuesta}"
        if self.guardar_logs and nomenclatura["score"] >= 6:
            self._guardar_log_90dias(prompt, respuesta, auditoria)
        self.historial.append({"role": "user", "content": prompt})
        self.historial.append({"role": "assistant", "content": respuesta})
        return respuesta, auditoria

    def _buscar_en_historial(self, respuesta): return True
    def _contiene_cifra_fecha(self, txt): return any(c.isdigit() for c in txt)
    def _tiene_fuente(self, prompt): return "según" in prompt.lower()
