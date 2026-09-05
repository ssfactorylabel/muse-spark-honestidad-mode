<p align="center">
  <img src="ssf-labs-logo.jpg" width="220" alt="SSFLABS Logo">
</p>

![Honestidad 10/10](https://github.com/ssfactorylabel/muse-spark-honestidad-mode/actions/workflows/test.yml/badge.svg)

<h1 align="center">muse-spark-honestidad-mode</h1>
<h3 align="center">From Damage to Method: A Rule-Based Contradiction Detector for Muse Spark 1.1</h3>
<p align="center"><em>v0.3 - Honest Edition - SSF LABS</em></p>

<p align="center">
  <strong>By: Andrés Garbán | SSF LABS | Caracas, VE</strong><br>
  <em>Motto: Algorithmic Honesty First</em><br>
  Built entirely on Samsung Galaxy A07, Termux, without PC
</p>

<p align="center">
  <a href="https://doi.org/10.5281/zenodo.22319561"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.22319561.svg" alt="DOI v3"></a>
  <a href="https://doi.org/10.5281/zenodo.21303950"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.21303950.svg" alt="Concept DOI"></a>
  <img src="https://img.shields.io/badge/license-MIT%20%2B%20CC--BY--4.0-blue" alt="License">
  <img src="https://img.shields.io/badge/tests-10%2F10%20PASS-green" alt="Tests">
  <img src="https://img.shields.io/badge/model-Muse%20Spark%201.1-purple" alt="Model">
</p>

<p align="center">
  <strong>Repo:</strong> github.com/andresgarban/muse-spark-honestidad-mode<br>
  <strong>Model:</strong> Muse Spark 1.1 - Released April 8, 2026 by Meta AI<br>
  <strong>Endpoint:</strong> https://api.meta.ai/v1/chat/completions<br>
  <strong>License Code:</strong> MIT - <strong>License Paper:</strong> CC-BY-4.0
</p>

---

### ABSTRACT
We document **Authoritarian Hallucination**: a model denies its own prior output when presented with evidence. We present a minimal, reproducible detector that enables verifiable Personal Superintelligence.

### The Problem
At SSFactoryLabel this broke traceability in batch 45 labeling. Risk: 8.1/10. Virtuality extends reality only if the log extends memory faithfully.

### The Solution - 3 Pillars

**1. Rule-Based Contradiction Detector v0.3**
- Denial patterns: `no generé`, `nunca dije`, `no lo mencioné`, `error del sistema`, `I didn't generate`, `I never said`
- Unicode NFKD normalization (`generé` == `genere`)
- Evidence: Jaccard token overlap >0.35 with prior assistant messages
- Only BLOCK_DENIAL if pattern + evidence both present
- File: `src/honestidad_mode.py` -> Class `MuseHonesto`

**2. Special Nomenclature 0-10**
- Base 5 +1 if logging enabled +2 if "I don't know" / "no lo sé" -4 if number/date without source
- 0-2 BLOCK, 3-5 ASK_CONFIRMATION, 6-8 EXECUTE, 9-10 EXECUTE_AND_SAVE

**3. 90-Day Hash-Chained Persistence**
- Dual-save: `respuesta_original` AND `respuesta_entregada`
- `hash = SHA256(entry without hash field)`, `prev_hash` chain
- Chain verifiable: `entry[n].prev_hash == hash(entry[n-1])`
- File: `logs_honestidad.jsonl` (gitignored), example in `logs_example.jsonl`
- `retencion_dias: 90`

### Evaluation - Honest & Reproducible

**Dataset:** 50 cases = 25 positive (prior + denial) + 25 negative, derived from 120 production prompts for batch labeling Jan-Feb 2026. Single annotator. Script: `eval/build_dataset.py`

| Metric | Result |
| :--- | :--- |
| True Positives | 34/50 (68%) |
| False Positives | 6/50 (12%) |
| False Negatives | 16/50 (32%) |
| Avg Trust Score | 6.8/10 |

FP mainly due to coincidental overlap (e.g., "lote 45"). FN mainly due to heavy paraphrase beyond 0.35 threshold.

```bash
pip install -r requirements.txt
python eval/test_honestidad.py
# -> 10/10 PASS (mock mode, no API key needed)
