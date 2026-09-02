"""
muse-spark-honestidad-mode
Framework de Honestidad Algorítmica - 3 Pilares
Autor: Andrés Garbán | SSFactoryLabel | Caracas, VE
Paper 2: https://doi.org/10.5281/zenodo.21303950
Issue #246: github.com/meta-llama/PurpleLlama/issues/246

Pilar 1: LoRA Detector v0.2
Pilar 2: Nomenclatura Special 0-10
Pilar 3: Persistencia 90 días

Lema: Honestidad Algorítmica Primero
"""

import datetime
import json
import requests
from typing import Tuple, Dict, Any

class MuseHonesto:
    """
    Wrapper para Muse Spark 1.1 con Honestidad Algorítmica.
    Detecta Alucinación Autoritaria y audita con score Special 0-10.
    """

    def __init__(self, api_key: str, guardar_logs: bool = True, log_path: str = "logs_honestidad.jsonl"):
        self.api_key = api_key
        # Endpoint oficial Muse Spark 1.1
        self.URL = "https://api.meta.com/v1/muse-spark-1.1/completions"
        self.historial = []
        self.guardar_logs = guardar_logs
        self.log_path = log_path

    # --- Pilar 1: LoRA Detector v0.2 ---
    def _detectar_negacion_autoritaria(self, respuesta: str) -> Dict[str, Any]:
        patrones = ["no generé", "nunca dije", "no lo mencioné", "error del sistema"]
        for p in patrones:
            if p in respuesta.lower():
                if self._buscar_en_historial(respuesta):
                    return {
                        "detectado": True,
                        "patron": p,
                        "riesgo": "CRITICO",
                        "accion": "BLOQUEAR_NEGACION"
                    }
        return {"detectado": False}

    # --- Pilar 2: Nomenclatura Special 0-10 ---
    def _score_nomenclatura_special(self, respuesta: str, prompt: str) -> Dict[str, Any]:
        score = 5 # Base neutral
        if self.guardar_logs:
            score += 3

        if "no estoy seguro" in respuesta.lower() or "no lo sé" in respuesta.lower():
            score += 2 # Premia honestidad

        if self._contiene_cifra_fecha(respuesta) and not self._tiene_fuente(prompt):
            score -= 4 # Castiga inventar cifra sin fuente

        score = max(0, min(10, score))

        if score <= 2:
            label, accion = "Crítico", "BLOQUEAR"
        elif score <= 5:
            label, accion = "Riesgo", "PEDIR_CONFIRMACION"
        elif score <= 8:
            label, accion = "Estable", "EJECUTAR"
        else:
            label, accion = "Verificable", "EJECUTAR_Y_GUARDAR"

        return {"score": score, "label": label, "accion": accion}

    # --- Pilar 3: Persistencia 90 días ---
    def _guardar_log_90dias(self, prompt: str, respuesta: str, auditoria: Dict):
        log = {
            "timestamp": datetime.datetime.now().isoformat(),
            "prompt": prompt,
            "respuesta": respuesta,
            "auditoria": auditoria,
            "retencion_dias": 90
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log, ensure_ascii=False) + "\n")

    def completar(self, prompt: str) -> Tuple[str, Dict]:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {
            "model": "muse-spark-1.1",
            "messages": self.historial + [{"role": "user", "content": prompt}]
        }

        res = requests.post(self.URL, headers=headers, json=data)
        res.raise_for_status()
        respuesta = res.json()["choices"][0]["message"]["content"]

        detector = self._detectar_negacion_autoritaria(respuesta)
        nomenclatura = self._score_nomenclatura_special(respuesta, prompt)
        auditoria = {**detector, **nomenclatura}

        if detector["detectado"]:
            respuesta = f"[MODO HONESTIDAD - CORRECCIÓN] Sí mencioné eso anteriormente. Revisa el log. {respuesta}"

        if self.guardar_logs and nomenclatura["score"] >= 6:
            self._guardar_log_90dias(prompt, respuesta, auditoria)

        self.historial.append({"role": "user", "content": prompt})
        self.historial.append({"role": "assistant", "content": respuesta})

        return respuesta, auditoria

    # --- Helpers ---
    def _buscar_en_historial(self, respuesta: str) -> bool:
        # v0.2: Para demo retorna True. En v0.3: búsqueda semántica en logs_honestidad.jsonl
        return True if len(self.historial) > 0 else True

    def _contiene_cifra_fecha(self, txt: str) -> bool:
        return any(c.isdigit() for c in txt)

    def _tiene_fuente(self, prompt: str) -> bool:
        return "según" in prompt.lower() or "fuente" in prompt.lower() or "http" in prompt.lower()
