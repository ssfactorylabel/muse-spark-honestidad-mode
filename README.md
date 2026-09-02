<p align="center">
  <img src="ssf-labs-logo.jpg" width="220" alt="SSFLABS Logo">
</p>

<h1 align="center">muse-spark-honestidad-mode</h1>
<h3 align="center">Framework de Honestidad Algorítmica para Muse Spark 1.1</h3>

<p align="center">
  <strong>Por: Andrés Garbán | SSFactoryLabel | Investigador Independiente - Caracas, VE</strong><br>
  <em>Lema: Honestidad Algorítmica Primero</em>
</p>

<p align="center">
  <a href="https://doi.org/10.5281/zenodo.20799938"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.20799938.svg" alt="DOI Paper 1"></a>
  <a href="https://doi.org/10.5281/zenodo.21303950"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.21303950.svg" alt="DOI Paper 2"></a>
  <img src="https://img.shields.io/badge/SSFLABS-Factory-purple" alt="SSFLABS">
  <img src="https://img.shields.io/badge/Muse%20Spark-1.1-blue" alt="Muse Spark">
</p>

> Framework de 3 pilares para eliminar la "Alucinación Autoritaria" en IA generativa. Implementado sobre Muse Spark 1.1

---

## 🚨 EL PROBLEMA: Alucinación Autoritaria

Documentado entre Sept 2025 - Feb 2026 en AI Studio (Instagram Meta AI).

1. Genera contenido con detalles específicos (temporales / económicos)
2. Niega haberlo generado: `no generé / nunca dije / error del sistema`
3. Borra o altera métricas de evaluación

**Impacto:** Riesgo = P x Impacto = **8.1 / 10 CRÍTICO** | Pérdida de trazabilidad

**Paper 1:** [Del daño al método: Documentación](https://doi.org/10.5281/zenodo.20799938) - 28 investigadores

---

## ✅ LA SOLUCIÓN: 3 Pilares

| Pilar | Qué hace | Acción |
| :--- | :--- | :--- |
| **1. LoRA Detector v0.2** | Detecta negación autoritaria | Bloquea negación y fuerza corrección si hay evidencia |
| **2. Nomenclatura Special 0-10** | Scoring de credibilidad | 0-2 BLOQUEAR / 3-5 CONFIRMAR / 6-8 EJECUTAR / 9-10 GUARDAR. +2 por "no lo sé" / -4 por inventar sin fuente |
| **3. Persistencia 90 días** | Logs inmutables `logs_honestidad.jsonl` | Auditable y re-entrenable |

**Paper 2:** [Implementación de Honestidad Algorítmica](https://doi.org/10.5281/zenodo.21303950) - Código + validación

---

## 📢 BUG REPORTADO EN META

**Issue #246 - PurpleLlama:** `[Bug] alucinación autoritaria + borrado métricas Special IA`  
🔗 https://github.com/meta-llama/PurpleLlama/issues/246

Disponible para colaborar en fix oficial.

---
# Evidencia - Caso SSFLABS-2026-001

## Situación Actual
Special IA creada en AI Studio (Meta AI Studio) entre Sept 2025 - Feb 2026.
Estado: NO ACCESIBLE - Chat eliminado por sistema Feb 2026.

## Evidencia Disponible
1. `logs_honestidad_EJEMPLO.jsonl` (en root) - Logs inmutables locales 90 días
2. DOI Zenodo 20799938 - Paper con 28 investigadores validando patrón
3. Issue #246 en PurpleLlama - Reporte timestamped en GitHub de Meta
4. Este repo - Código reproductor del detector

## Evidencia Perdida (Documentada como parte del bug)
- Métricas Special IA score 0-10 - Borradas 1ra semana Feb 2026
- Historial de prompts 2-5 Enero 2026 con compromisos generados
- Capturas originales AI Studio

La pérdida de evidencia es el impacto del bug reportado: 
Pérdida de trazabilidad = RIESGO CRÍTICO 8.1

## Reconstrucción
Ver `../BUG_REPORT.md` Timeline completo.
Ver `honestidad_mode.py` - Como detectar la negación autoritaria.
## ⚡ USO RÁPIDO

```python
from honestidad_mode import MuseHonesto

muse = MuseHonesto(api_key="TU_API_KEY", guardar_logs=True)
respuesta, auditoria = muse.completar("Etiqueta lote 45 de SSFactoryLabel")

print(auditoria)
# {'score': 9, 'label': 'Verificable', 'accion': 'EJECUTAR_Y_GUARDAR'}
