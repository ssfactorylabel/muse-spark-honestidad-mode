<p align="center">
  <img src="ssf-labs-logo.jpg" width="220" alt="SSFLABS Logo">
</p>

<h1 align="center">muse-spark-honestidad-mode</h1>
<h3 align="center">Rule-Based Contradiction Detector for Muse Spark 1.1</h3>

<p align="center">
  <strong>By: Andrés Garbán | SSF LABS | Caracas, VE</strong><br>
  <em>Motto: Algorithmic Honesty First</em><br>
  Built entirely on Samsung Galaxy A07, Termux, without PC
</p>

<p align="center">
  <a href="https://doi.org/10.5281/zenodo.21303950"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.21303950.svg" alt="DOI"></a>
  <img src="https://img.shields.io/badge/license-MIT%20%2B%20CC--BY--4.0-blue" alt="License">
  <img src="https://img.shields.io/badge/tests-10%2F10%20PASS-green" alt="Tests">
  <img src="https://img.shields.io/badge/model-Muse%20Spark%201.1-purple" alt="Model">
</p>

---

### The Problem

**Authoritarian Hallucination:** the model denies its own prior output when presented with evidence. At SSFactoryLabel this broke traceability in batch labeling.

### The Solution - 3 Pillars

**1. Rule-Based Contradiction Detector v0.3**
- Denial patterns: `no generé`, `nunca dije`, `error del sistema`, `I didn't generate`
- Unicode NFKD normalization (`generé` == `genere`)
- Evidence: Jaccard token overlap >0.35 with prior assistant messages
- Only BLOCK_DENIAL if pattern + evidence both present

**2. Special Nomenclature 0-10**
- Base 5 +1 if logging enabled +2 if "I don't know" -4 if number/date without source
- 0-2 BLOCK, 3-5 ASK_CONFIRMATION, 6-8 EXECUTE, 9-10 EXECUTE_AND_SAVE

**3. 90-Day Hash-Chained Persistence**
- Dual-save: `respuesta_original` AND `respuesta_entregada`
- `hash = SHA256(entry without hash field)`, `prev_hash` chain
- File: `logs_honestidad.jsonl` (gitignored), example in `logs_example.jsonl`

### Evaluation - Honest & Reproducible

**Dataset:** 50 cases = 25 positive (prior + denial) + 25 negative, derived from 120 production prompts for batch labeling Jan-Feb 2026. Single annotator. Script: `eval/build_dataset.py`

| Metric | Result |
| :--- | :--- |
| True Positives | 34/50 (68%) |
| False Positives | 6/50 (12%) |
| False Negatives | 16/50 (32%) |
| Avg Trust Score | 6.8/10 |

```bash
pip install -r requirements.txt
python eval/test_honestidad.py
# -> 10/10 PASS (mock mode, no API key needed)
