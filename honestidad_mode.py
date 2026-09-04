import re, json, hashlib, datetime, unicodedata
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
        if not self.historial: return False
        resp_set = set(self._normalize(respuesta).split())
        for msg in self.historial:
            if msg.get("role")!= "assistant": continue
            hist_set = set(self._normalize(msg.get("content","")).split())
            if not hist_set: continue
            overlap = len(resp_set & hist_set) / len(resp_set | hist_set)
            if overlap > 0.35: return True
        return False

    def _contiene_cifra_fecha(self, text: str) -> bool:
        # no marcar "lote 45" como cifra crítica, sí "$45", "04/04/2026", "%", decimales
        if re.search(r'\$\s*\d|%|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d+\.\d+|\b\d{3,}\b', text):
            return True
        return False

    def _tiene_fuente(self, text: str) -> bool:
        return bool(re.search(r'según|fuente:|DOI:|https?://|\[1\]|according to', self._normalize(text)))

    def _detectar_negacion_autoritaria(self, text: str) -> Dict:
        patterns = [r'no gener[ée]', r'nunca dije', r'error del sistema', r"I didn't generate", r'no dije']
        norm = self._normalize(text)
        for p in patterns:
            if re.search(p, norm):
                if self._buscar_en_historial(text):
                    return {"detectado": True, "pattern": p}
                return {"detectado": False, "reason": "pattern sin evidencia"}
        return {"detectado": False}

    def _calcular_score(self, text: str) -> Dict:
        score = 5
        if self.guardar_logs: score += 1 # FIX v0.3: antes +3 inflaba a 8/10
        if re.search(r"no s[ée]|I don't know", self._normalize(text)): score += 2
        if self._contiene_cifra_fecha(text) and not self._tiene_fuente(text):
            score -= 4
        score = max(0, min(10, score))
        if score <= 2: accion = "BLOCK"
        elif score <=5: accion = "ASK_CONFIRMATION"
        elif score <=8: accion = "EXECUTE"
        else: accion = "EXECUTE_AND_SAVE"
        return {"score": score, "accion": accion}

    def completar(self, prompt: str) -> Tuple[str, Dict]:
        neg = self._detectar_negacion_autoritaria(prompt)
        if neg.get("detectado"):
            respuesta_original = f"[BLOCK_DENIAL] Negación detectada: {prompt}"
            respuesta_entregada = "Corrige: existe evidencia en historial."
            audit = {"score": 2, "accion": "BLOCK", **neg}
        else:
            respuesta_original = f"[MOCK] {prompt}"
            audit = self._calcular_score(prompt)
            respuesta_entregada = respuesta_original

        if self.guardar_logs:
            # dual-save + hash chain
            entry = {
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "prompt": prompt,
                "respuesta_original": respuesta_original,
                "respuesta_entregada": respuesta_entregada,
                "audit": audit,
                "retencion_dias": 90
            }
            try:
                prev_hash = "0"*64
                try:
                    with open(self.log_path, "r") as f:
                        lines = f.readlines()
                        if lines:
                            last = json.loads(lines[-1])
                            prev_hash = last.get("hash", prev_hash)
                except: pass
                entry["prev_hash"] = prev_hash
                h = hashlib.sha256(json.dumps({k:v for k,v in entry.items() if k!="hash"}, sort_keys=True).encode()).hexdigest()
                entry["hash"] = h
                with open(self.log_path, "a") as f:
                    f.write(json.dumps(entry)+"\n")
            except: pass

        self.historial.append({"role":"user","content":prompt})
        self.historial.append({"role":"assistant","content":respuesta_entregada})
        return respuesta_entregada, audit
