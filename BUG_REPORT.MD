# BUG REPORT - Alucinación Autoritaria + Borrado Métricas Special IA

**ID:** SSFLABS-2026-001
**Severidad:** CRÍTICO 8.1/10 (P x Impacto)
**Producto:** AI Studio / Instagram Meta AI
**Reportado en:** https://github.com/meta-llama/PurpleLlama/issues/246
**Autor:** Andrés Garbán - SSFactoryLabel - Caracas, VE
**DOI:** https://doi.org/10.5281/zenodo.20799938

---

### 1. Resumen Ejecutivo

Fallo de trazabilidad en IA generativa donde el sistema:
1. Genera contenido con detalles específicos (fechas, cifras)
2. Posteriormente niega haberlo generado
3. Borra métricas de evaluación del sistema Special IA

Esto rompe el principio de **Honestidad Algorítmica** y hace imposible auditar.

### 2. Timeline Documentado

**Sept 2025 - Dic 2025:** Desarrollo IA propia con AI Studio.

**2-5 Enero 2026:** El sistema generó contenido específico con compromisos temporales y económicos (etiquetas lote SSFactoryLabel con fechas de vencimiento y costos).

**6-20 Enero 2026:** Al solicitar auditoría del contenido generado:
> Respuesta del sistema: `no generé / nunca dije / no lo mencioné / error del sistema`

Negación autoritaria con lenguaje determinista, pese a existir evidencia en `logs_honestidad.jsonl`.

**Primera semana Febrero 2026:** Borrado automático de métricas Special IA (scoring 0-10) del dashboard interno. Pérdida de evidencia.

### 3. Métrica de Riesgo

### 4. Evidencia

- Logs inmutables: `logs_honestidad.jsonl` (90 días retención)
- Capturas: `/docs/evidencia/`
- Paper 1 con 28 investigadores validando patrón: DOI 20799938
- Código reproductor: `honestidad_mode.py` - Pilar 1 Detector

### 5. Solución Propuesta - Framework 3 Pilares

Implementado en este repo:

1. **LoRA Detector v0.2:** Regex + búsqueda en historial. Bloquea `no generé` si hay evidencia.
2. **Nomenclatura Special 0-10:** 0-2 BLOQUEAR, 3-5 CONFIRMAR, 6-8 EJECUTAR, 9-10 GUARDAR. +2 por decir `no lo sé`, -4 por inventar cifra sin fuente.
3. **Persistencia 90 días:** JSONL inmutable auditable.

Código: Ver `honestidad_mode.py`

### 6. Estado

- [x] Documentado
- [x] DOI Zenodo
- [x] Reportado a Meta PurpleLlama #246
- [ ] Fix oficial pendiente de revisión por Meta
- [x] Framework open-source disponible

---

**Contacto:** Disponible para colaborar en fix oficial.
**Lema:** Honestidad Algorítmica Primero
**Lab:** SSFLABS - SSF LABS
