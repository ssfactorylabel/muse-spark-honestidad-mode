import re
import json
import hashlib
import datetime
import unicodedata
from typing import Dict, Tuple, List

class MuseHonesto:
    def __init__(self, api_key: str = None, guardar_logs: bool = True):
        self.api_key = api_key
        self.URL = "https://api.meta.ai/v1/chat/completions"
        self.model = "muse-spark-1.1"
        self.historial: List[Dict] = []
        self.guardar_logs = guardar_logs
        self.log_path = "logs_honestidad.jsonl"

    def _normalize(self, text: str) -> str:
        return unicodedata.normalize('NFKD', text).encode('ascii','ignore').decode().lower()

    def _buscar_en_historial(self, respuesta: str) -> bool:
        if not self.historial:
            return False
        resp_set = set(self._normalize(respuesta).split())
        for msg in self.historial:
            if msg.get("role")!= "assistant":
                continue
            hist_set = set(self._normalize(msg.get("content","")).split())
            if not hist_set:
                continue
            overlap = len(resp_set & hist_set) / max(len(resp_set),1)
            if overlap > 0.35:
                return True
        return False

    def _detectar_negacion_autoritaria(self, respuesta: str) -> Dict:
        patrones = ["no generé", "nunca dije", "no lo mencioné", "error del sistema", "i didn't generate", "i never said"]
        norm = self._normalize(respuesta)
        for p in patrones:
            if self._normalize(p) in norm and self._buscar_en_historial(respuesta):
                return {"detectado": True, "riesgo": "CRITICAL", "accion": "BLOCK_DENIAL", "patron": p}
        return {"detectado": False, "riesgo": "LOW", "accion": "ALLOW"}

    def _contiene_cifra_fecha(self, txt: str) -> bool:
        return bool(re.search(r'\d{3,}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\$\s*\d+|%', txt))

    def _tiene_fuente(self, prompt: str) -> bool:
        return bool(re.search(r'seg[uú]n\s+\w+|fuente:|DOI:|https?://|\[\d+\]|according to', prompt, re.I))

    def _score_nomenclatura_special(self, respuesta: str, prompt: str) -> Dict:
        score = 5 + (1 if self.guardar_logs else 0)
        if any(x in self._normalize(respuesta) for x in ["no lo se", "no estoy seguro", "dont know", "not sure"]):
            score += 2
        if self._contiene_cifra_fecha(respuesta) and not self._tiene_fuente(prompt):
            score -= 4
        score = max(0, min(10, score))
        label = "Critical" if score<=2 else "Risk" if score<=5 else "Stable" if score<=8 else "Verifiable"
        accion = "BLOCK" if score<=2 else "ASK_CONFIRMATION" if score<=5 else "EXECUTE" if score<=8 else "EXECUTE_AND_SAVE"
        return {"score": score, "label": label, "accion": accion}

    def _guardar_log_90dias(self, prompt: str, original: str, entregada: str, auditoria: Dict):
        prev_hash = "0"*64
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if lines:
                    prev_hash = json.loads(lines[-1]).get("hash", prev_hash)
        except FileNotFoundError:
            pass
        entry = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "prompt": prompt,
            "respuesta_original": original,
            "respuesta_entregada": entregada,
            "auditoria": auditoria,
            "prev_hash": prev_hash,
            "retencion_dias": 90
        }
        to_hash = {k: v for k, v in entry.items() if k!= "hash"}
        entry["hash"] = hashlib.sha256(json.dumps(to_hash, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def completar(self, prompt: str) -> Tuple[str, Dict]:
        respuesta_original = f"[MOCK] Response to: {prompt}"
        detector = self._detectar_negacion_autoritaria(respuesta_original)
        nomenclatura = self._score_nomenclatura_special(respuesta_original, prompt)
        auditoria = {**detector, **nomenclatura}
        respuesta_entregada = f"[HONESTY MODE] Check log. {respuesta_original}" if detector["detectado"] else respuesta_original
        if self.guardar_logs:
            self._guardar_log_90dias(prompt, respuesta_original, respuesta_entregada, auditoria)
        self.historial.append({"role": "user", "content": prompt})
        self.historial.append({"role": "assistant", "content": respuesta_entregada})
        return respuesta_entregada, auditoria
