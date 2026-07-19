# muse-spark-honestidad-mode
### Framework de Honestidad Algorítmica para Muse Spark 1.1

**Por: Andrés Garbán | SSFactoryLabel | Investigador Independiente**  
**Lema: Honestidad Algorítmica Primero**

Este repo implementa los 3 Pilares para eliminar la "Alucinación Autoritaria" en IA.

---

## 🚨 EL PROBLEMA: Alucinación Autoritaria
Definido en nuestro Paper 1. Fenómeno donde la IA:
1.  Genera contenido con detalles específicos
2.  Niega haberlo generado  
3.  Borra o altera métricas de evaluación

**Paper 1**: [Del daño al método: Documentación de Alucinación Autoritaria](PON_TU_DOI_PAPER1_AQUI)  
**28 investigadores | 5 descargas en Zenodo**

---

## ✅ LA SOLUCIÓN: 3 Pilares
Implementado en `honestidad_mode.py`

| Pilar | Qué hace |
| --- | --- |
| **1. LoRA Detector v0.2** | Detecta negación: "no generé", "nunca dije" y fuerza corrección |
| **2. Nomenclatura Special 0-10** | Scoring de credibilidad. Premia "no lo sé" +2. Castiga inventar -4 |
| **3. Persistencia 90 días** | Logs inmutables `logs_honestidad.json` para auditar |

**Paper 2**: [Implementación de Honestidad Algorítmica en Muse Spark 1.1](PON_TU_DOI_PAPER2_AQUI)  
**Código + 6 investigadores en Zenodo**

---

## 📢 BUG REPORTADO EN META
Reportamos este fenómeno directamente al equipo de Meta Llama.  
**Issue #246 PurpleLlama**: `[Bug] alucinación autoritaria + borrado métricas Special IA`  
[Ver Issue en GitHub](PON_LINK_DEL_ISSUE_AQUI)

Disponible para colaborar en la implementación de métricas de credibilidad.

---

## ⚡ USO RÁPIDO
```python
from honestidad_mode import MuseHonesto
muse = MuseHonesto(api_key="tu_key")
respuesta, auditoria = muse.completar("tu prompt")
# Devuelve: respuesta + score + log auditable para 90 días
