# Project: Fleece Gamma 🐑🧠

**The "Crate Motor" SLM build (Reasoning Edition)** — a self-contained, uncensored reasoning AI model you run **completely offline, on your own machine**. No internet needed.

**Core model:** Qwen 3.5 9B (`8.95B` parameters) The Defiant Fable Uncensored Heretic plusIQ-TOOLS NEO MAX MTP (`Q6_K` GGUF, bundled inside `models/`)

---

## What "local reasoning agent" means here

Fleece Gamma is a **tool for offloading deep analytical, mathematical, architectural, and logical reasoning from frontier (cloud) agents so it can live locally**. You give it a task, it reasons step-by-step using compacted `<think>...</think>` blocks, dynamically adjusts its reasoning depth via 10 switchable `plusIQ` modes, serves verified answers, and keeps its own notes — all without calling anything to a server.

- **No internet required.** Everything runs locally, with the physical `8.16 GB` GGUF model bundled directly inside `models/`.
- **No cloud API keys.** No `OPENAI_API_KEY`, no `ANTHROPIC_API_KEY`, no external calls.
- **No vector databases, embeddings, or chunking.** Retrieval is by direct file search over plain markdown.
- **Dynamic Reasoning Depth (`plusIQ`).** Switch on the fly between deep research reasoning (`{REASON:spoon}`), multi-perspective analytical reasoning (`{REASON:einstein}`), standard reasoning (`xhigh`, `medium`, `low`), or zero-thinking instant instruct modes (`ispoon`, `ieinstein`, `ixhigh`, `imedium`, `ilow`).
- **Self-contained.** Everything the project needs sits in one folder.

---

## What's inside the crate

1. **GGUF Reasoning SLM core (`engine/llm_engine.py`)** — pre-configured for Apple Silicon (Metal), NVIDIA (CUDA), or CPU fallback, with native `plusIQ` mode switching and `<think>...</think>` trace extraction.
2. **Bundled Physical Model (`models/`)**
   - `Qwen3.5-9B-The-Defiant-Fable-Uncnr-Heretic-plusIQ-TOOLS-NEO-MAX-MTP-Q6_K.gguf` (`8.16 GB` physical file + local `model.gguf` alias).
3. **Two-tier living memory (`memory/`)**
   - **Tier 1 — Living Dossier (`DOSSIER.md`):** a fast-path cache. Frequently asked questions and verified answers are served instantly (with internal `<think>` traces stripped so the cache stays pure).
   - **Tier 2 — Vectorless PageIndex (`PAGE_INDEX.json`):** a plain table-of-contents tree over the markdown knowledge files. Zero embeddings, zero chunking.
4. **Reasoning-aware context safeguard (`memory/context_budget.py`)** — reserves dedicated completion headroom (`4,096` tokens) for chain-of-thought reasoning, strips historical `<think>` traces from prior turns so multi-turn chats never bloat the context window, and offloads older conversation first to keep ingested documents intact.
5. **Ingestion protocols (`ingestion/protocols.py`)** — three guarantees:
   - **Anti-Parsing:** raw text is never rewritten or reformatted.
   - **Anti-Chunking:** documents are treated as complete wholes.
   - **Anti-Truncating:** content is never cut off mid-sentence.

---

## Quickstart

### 1. Verify the bundled model (optional)

```bash
python -m pip install -r requirements.txt
python setup_models.py
```

### 2. Run

```bash
./run.sh
```

### 3. Use inside the interactive shell

- `!mode <name>` — switch active reasoning mode (`spoon`, `einstein`, `xhigh`, `medium`, `low`, `ispoon`, `ieinstein`, `ixhigh`, `imedium`, `ilow`).
- `!think` — inspect the internal `<think>...</think>` reasoning trace from the previous turn.
- `!dossier` — view the living dossier.
- `!toc` — view the table-of-contents index.
- `!budget` — check context token usage.
- `!reset` — clear conversation turns, keep the model and memory.

### 4. Run as a Python crate motor

```python
from fleece import FleeceCrateMotor

motor = FleeceCrateMotor()
motor.set_reasoning_mode("einstein")
motor.set_task("Audit system architecture for concurrency bottlenecks")
response = motor.execute("What are the three unbreakable Ingestion Protocol Specifications?")
print(response)
```
