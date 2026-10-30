# Project: Fleece Gamma 🐑🧠

**The "Crate Motor" SLM build (Reasoning Edition)** — a self-contained, uncensored reasoning AI model equipped with **Mimir OCR** that you run **completely offline, on your own machine**. No internet needed.

**Core model:** Qwen 3.5 9B (`8.95B` parameters) The Defiant Fable Uncensored Heretic plusIQ-TOOLS NEO MAX MTP (`Q6_K` GGUF, bundled inside `models/`)
**Ingestion & Memory Stack:** **Mimir OCR** (3-Pass Progressive Optical Sieve with Coordinate Delta-Masking + Two-Tier Vectorless Memory)

---

## What "local reasoning agent" means here

Fleece Gamma is a **tool for offloading deep analytical, mathematical, architectural, and document reasoning from frontier (cloud) agents so it can live locally**. You give it a task or a degraded multi-page PDF/scan, **Mimir OCR** extracts and grounds every text block to normalized `[x0, y0, x1, y1]` coordinates, and the engine reasons step-by-step using compacted `<think>...</think>` blocks via 10 switchable `plusIQ` modes — all without calling anything to a server.

- **No internet required.** Everything runs locally, with the physical `8.16 GB` GGUF model bundled directly inside `models/`.
- **No cloud API keys.** No `OPENAI_API_KEY`, no `ANTHROPIC_API_KEY`, no AWS Textract.
- **Mimir OCR Stack.** Combines the **3-Pass Progressive Optical Sieve with Coordinate Delta-Masking** (`sieve_ocr.py`) and the **Two-Tier Vectorless Memory System** (`DOSSIER.md` L1 + `PAGE_INDEX.json` L2). Zero embeddings, zero chunking.
- **Dynamic Reasoning Depth (`plusIQ`).** Switch on the fly between deep research reasoning (`{REASON:spoon}`), multi-perspective analytical reasoning (`{REASON:einstein}`), standard reasoning (`xhigh`, `medium`, `low`), or zero-thinking instant instruct modes (`ispoon`, `ieinstein`, `ixhigh`, `imedium`, `ilow`).
- **Self-contained.** Everything the project needs sits in one folder.

---

## What's inside the crate

1. **GGUF Reasoning SLM core (`engine/llm_engine.py`)** — pre-configured for Apple Silicon (Metal), NVIDIA (CUDA), or CPU fallback, with native `plusIQ` mode switching and `<think>...</think>` trace extraction.
2. **Bundled Physical Model (`models/`)**
   - `Qwen3.5-9B-The-Defiant-Fable-Uncnr-Heretic-plusIQ-TOOLS-NEO-MAX-MTP-Q6_K.gguf` (`8.16 GB` physical file + local `model.gguf` alias).
3. **Mimir OCR (`sieve_ocr.py` & `memory/`)**
   - **3-Pass Progressive Optical Sieve with Coordinate Delta-Masking (`engine/sieve_ocr.py`):**
     - **Pass 1 (OS-Native OCR):** Apple Vision / Windows OCR clears ~85% of clean text in `<150ms/page`.
     - **Coordinate Delta-Masking:** Locks in `>= 0.85` confidence blocks and crops only `< 0.85` bounding boxes (`12px` margin at `200 DPI`).
     - **Pass 2 (Targeted `RapidOCR` ONNX):** Runs on delta-masked sub-crops (~12%: faded print, stamps, tables) and projects coordinates back to full-page `[0.0000, 1.0000]` space.
     - **Pass 3 (In-Process Local VLM via `MiniCPM-V 2.6`):** Escalates stubborn cursive/marginalia crops (~3%) at `temperature=0.0` with Gate 3 quarantine (`needs_human_review = True` if `< 0.85` or `[?]`).
   - **Tier 1 — Mimir Living Dossier (`DOSSIER.md`):** a fast-path cache. Frequently asked questions and verified answers are served instantly (with internal `<think>` traces stripped so the cache stays pure).
   - **Tier 2 — Mimir Vectorless PageIndex (`PAGE_INDEX.json`):** a plain table-of-contents tree over the markdown knowledge files. Zero embeddings, zero chunking.
4. **Reasoning-aware context safeguard (`memory/context_budget.py`)** — reserves dedicated completion headroom (`4,096` tokens) for chain-of-thought reasoning, strips historical `<think>` traces from prior turns so multi-turn chats never bloat the context window, and offloads older conversation first to keep ingested documents intact.
5. **Ingestion protocols (`ingestion/protocols.py`)** — three guarantees:
   - **Anti-Parsing:** raw text is never rewritten or reformatted.
   - **Anti-Chunking:** documents are treated as complete wholes.
   - **Anti-Truncating:** content is never cut off mid-sentence.

---

## Quickstart

### 1. Verify the bundled models (optional)

```bash
python -m pip install -r requirements.txt
python setup_models.py
```

### 2. Run Mimir OCR Benchmark or Launch Shell

```bash
python test_sieve_ocr.py
./run.sh
```

### 3. Use inside the interactive shell

- `!audit /path/to/skill` — audit an agent or skill for sovereign Fleece compatibility.
- `!ocr /path/to/document.pdf` — ingest a PDF or image via the Mimir 3-Pass Progressive Optical Sieve.
- `!mode <name>` — switch active reasoning mode (`spoon`, `einstein`, `xhigh`, `medium`, `low`, `ispoon`, `ieinstein`, `ixhigh`, `imedium`, `ilow`).
- `!think` — inspect the internal `<think>...</think>` reasoning trace from the previous turn.
- `!dossier` — view the Mimir living dossier.
- `!toc` — view the Mimir table-of-contents index.
- `!budget` — check context token usage.
- `!reset` — clear conversation turns, keep the model and memory.

### 4. Run as a Python crate motor

```python
from fleece import FleeceCrateMotor

motor = FleeceCrateMotor()
motor.set_reasoning_mode("einstein")
motor.ingest_document("contract_scan.pdf")
response = motor.execute("Audit the contract clauses and cite normalized bounding boxes.")
print(response)
```

---

## Auditing Frontier Agents & Skills (`AUDIT_PLAYBOOK.md`)

Fleece includes an automated compatibility auditor to evaluate whether skills and agents designed for Frontier platforms (OpenAI, Claude, Antigravity, LangChain, CrewAI) can run sovereignly on Fleece SLM Crate Motors.

```bash
# Audit any agent script, prompt, or skill folder:
./audit_agent.py /path/to/my_skill/

# Generate Markdown audit report:
./audit_agent.py /path/to/my_skill/ --format markdown --output AUDIT_REPORT.md

# Audit directly from the interactive shell:
[You] > !audit /path/to/my_skill
```

See [`AUDIT_PLAYBOOK.md`](AUDIT_PLAYBOOK.md) for the complete 6-Pillar Audit Rubric and platform-by-platform conversion instructions.
