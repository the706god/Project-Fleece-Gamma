# Project: Fleece Gamma

The Crate Motor AI Build (Reasoning Edition) — a deep-thinking, private AI model that reasons through hard problems step by step directly on your own computer. Once set up, it requires zero internet connection and sends zero data to the cloud.

Core Model: Qwen 3.5 9B Instruct (Full Q8_0 Precision)
Reasoning Modes: 10 Switchable plusIQ Modes with Automatic Thought-Stripping
Memory & Acceleration: Native Metal TurboQuant (turbo4/turbo4) with 65,536-token context capacity
Document Stack: Mimir OCR (3-Pass Progressive Optical Sieve) + Two-Tier Vectorless Memory System

---

## Why Fleece Exists: Stop Hiring a Top Lawyer to Check Checkboxes

Frontier reasoning models like OpenAI o1/o3, Claude Extended Thinking, and Gemini Thinking are amazing. But using them for everyday work is like hiring a five-hundred-dollar-an-hour lawyer just to make sure people checked every box on a paper form.

The biggest waste of money in AI today is not one giant math problem. It is having background agents constantly checking rules, auditing documents, cross-referencing lists, and verifying multi-step procedures on expensive cloud systems. Every single thinking token burns through your rate limits and spikes your monthly invoice.

Project Fleece Gamma was built to fix that. It is your local reasoning crate motor. You offload deep logic audits, compliance reviews, and multi-step rule checking to your own computer. You get unlimited deep reasoning for zero dollars per month, zero token bills, zero rate limits, and 100% privacy. You save your expensive cloud models for the rare, world-changing strategies that actually need them.

---

## What Fleece Gamma Is Designed For

Fleece Gamma is the deep thinker of the Fleece suite. It is designed for tasks where speed matters less than walking through hard logic step by step.

Unlike standard text models that guess the next word immediately, Fleece Gamma stops and thinks before it answers. It writes out a hidden scratchpad of logic, tests different angles, catches its own mistakes, and then outputs a clear final answer.

### Updated Technical Specs

- Brain: Qwen 3.5 9B Instruct running at full Q8_0 precision. We removed uncensored fantasy finetunes to keep instruction following and factual output tight and predictable.
- Switchable plusIQ Reasoning: Switch between 10 different thinking depths on the fly:
  - Deep Research Mode (`{REASON:spoon}`): Ponders deeply for maximum thoroughness on hard problems.
  - Multi-Perspective Mode (`{REASON:einstein}`): Analyzes complex arguments from multiple viewpoints before deciding.
  - Standard Thinking Modes (`xhigh`, `medium`, `low`): Balances reasoning depth with speed.
  - Instant Instruct Modes (`ispoon`, `ieinstein`, `ixhigh`, `imedium`, `ilow`): Turns off the scratchpad for lightning-fast standard answers.
- Clean Memory Traces: The engine automatically cleans away temporary scratchpad thoughts (`<think>...</think>`) before saving facts to your memory. Your permanent notes stay clean and your workspace never clogs up.
- TurboQuant KV Cache: Uses high-efficiency 4-bit memory packing (turbo4/turbo4). This cuts memory usage by nearly four times and unlocks a huge 65,536-token workspace on your local machine.
- Memory Fallback Guard: If run on an older machine without TurboQuant, it smoothly steps down to standard q8_0 memory instead of crashing.
- Dedicated Thinking Room: Automatically reserves 4,096 tokens of dedicated thinking space so complex answers never get cut off mid-thought.
- Zero-Destruction Guarantee: Fleece strictly protects your source documents:
  1. Anti-Parsing: Raw text and rule clauses are never scrambled or changed.
  2. Anti-Chunking: Documents are kept whole, never chopped into loose paragraphs.
  3. Anti-Truncating: Information is never cut off mid-sentence.

---

## How Fleece Remembers: Two-Tier Vectorless Memory

Most AI tools use messy vector databases that chop long legal documents and rulebooks into disconnected snippets, losing the overall context. Fleece Gamma uses a clean, unbroken two-tier memory system:

- Tier 1 Memory (Fast Working Memory — The Living Dossier): This is your agent's verified fact book. When Gamma solves a hard logic puzzle or verifies a compliance question, it writes the clean result into `DOSSIER.md`. Next time you ask, it serves the answer immediately without having to re-think the whole problem.
- Tier 2 Memory (Book Index Navigation — The PageIndex Tree): Instead of guessing where rules live, Fleece builds a structured table-of-contents tree in `PAGE_INDEX.json`. Gamma navigates directly to the exact page, section, and line number of every requirement, just like a human auditor using a book index.
- Cold Backup (Secondary Markdown Store): Every ingested document is permanently preserved as clean, whole Markdown files on your local drive.

---

## Bonus Feature: Mimir OCR

Most local reasoning tools force you to build your own document pipeline before you can feed them a single real-world file. We packaged **Mimir OCR**—the proprietary OCR stack from our upcoming **MimirOS** release—directly into Fleece Gamma so you get a complete, multi-purpose local AI tool right out of the box.

How you use it is completely up to you. Whether your workflow touches medical, legal, financial, administrative, or everyday files, Mimir OCR is built to read whatever documents and forms you feed it with fidelity and accuracy—offline and under your control.

Under the hood, it runs a 3-pass pipeline (OS-native reading first, RapidOCR on low-confidence boxes, and a sleeping Chandra-OCR-2 fallback only for tough scans) without chopping or cutting off your pages. Combined with Fleece Gamma's portable deep reasoning, you can read tough paperwork offline and walk through complex logic on your own machine anywhere in the world.

---

## Real-World Possibilities (Industry-Agnostic)

You control what documents you check and how you use the results. You do not need to be a software engineer to get practical value out of Fleece Gamma:

- Contract and Policy Cross-Auditing: Feed in a 50-page employee handbook, supplier agreement, or lease. Gamma checks step by step if clause 12 contradicts clause 47, highlighting the exact page and sentence.
- Multi-Document Business Rule Verification: Provide a purchase order, a shipping receipt, and a billing invoice. Gamma verifies line by line whether quantities match, math adds up, and payment terms comply with company rules.
- Complex Schedule and Project Conflict Checks: Ingest a detailed project schedule with multiple teams and deadlines. Gamma analyzes dependencies and spots hidden bottlenecks—such as two teams scheduled to use the same equipment on the same morning.
- Multi-Step Standard Operating Procedure (SOP) Compliance: Check field reports against safety manuals to verify that every mandatory safety step was documented in the correct sequence.
- Software Logic and Architecture Auditing: Review codebases and database rules to ensure user permissions are verified before sensitive customer records are modified.

---

## Ideal System Specifications

Running a 9-billion parameter model at full Q8_0 precision with 65,536 tokens of memory requires a capable workstation:

### Mac (Apple Silicon)
- Best: Any Mac with M1 Pro, M1 Max, M2 Pro, M2 Max, M3 Pro, M3 Max, M4, or Mac Studio with 32 GB or more Unified Memory.
- Minimum: Apple Silicon Mac with 16 GB Unified Memory (runs comfortably with shorter working documents).
- Operating System: macOS 13 (Ventura) or later.

### Windows PC
- Best: 8-core modern CPU (Intel Core i7/i9 12th gen+ or AMD Ryzen 7/9) with 32 GB system RAM and an NVIDIA GPU (RTX 3080, 4070, 4080, 4090 with 12 GB+ VRAM).
- Minimum: 8-core CPU with 32 GB system RAM (can run on CPU alone).
- Operating System: Windows 10 or 11 (64-bit).

### Linux
- Best: Modern x86_64 or ARM64 workstation with 32 GB RAM and an NVIDIA GPU (CUDA support).
- Minimum: 8-core modern CPU with 32 GB RAM.

---

## What to Expect for Response Speeds

- On Apple Silicon Mac (M1 Pro / M2 / M3 32 GB): 18 to 32 words per second. Thoughtful, steady, and consistent. You will see it deliberate and then output clear, verified conclusions.
- On Windows / Linux with NVIDIA GPU: 20 to 35 words per second.
- On Standard CPU Only (No GPU): 5 to 10 words per second (best for background overnight jobs and deep audits).
- Document Reading Speed (Mimir OCR): Less than 1 second per page for 85%+ of standard documents.

---

## Quickstart Guide

### 1. Set Up the Environment

```bash
python -m pip install -r requirements.txt
python setup_models.py
```

### 2. Test Document Reading or Start the Shell

```bash
# Run the built-in document reading test:
python test_sieve_ocr.py

# Launch the interactive terminal:
./run.sh
```

### 3. Useful Commands Inside the Shell

- `!audit /path/to/skill` — Check if an outside prompt or agent skill can run locally on Fleece Gamma.
- `!ocr /path/to/file.pdf` — Read a document and store it in permanent, unbroken memory.
- `!reason <mode>` — Change your reasoning mode (e.g., `!reason spoon`, `!reason einstein`, `!reason ispoon`).
- `!dossier` — View your verified fact book.
- `!toc` — View the document table of contents tree.
- `!budget` — Check how much of your 65,536-token workspace is currently in use.
- `!reset` — Clear active conversation turns while keeping all loaded documents intact.

### 4. Use Inside Python Scripts

```python
from fleece import FleeceCrateMotor

# 1. Start the reasoning motor
motor = FleeceCrateMotor()

# 2. Ingest compliance manuals or contracts
motor.ingest_document("vendor_contract_2026.pdf")
motor.ingest_document("company_procurement_policy.pdf")

# 3. Ask for a multi-step logic audit
query = "{REASON:einstein} Does section 4.2 of the vendor contract comply with our procurement payment policy?"
answer = motor.execute(query)
print(answer)
```

---

## Auditing Outside Agents and Skills

Fleece Gamma includes a built-in reasoning auditor. It evaluates external agent skills and prompt chains, verifying if they can be moved from cloud models (like OpenAI o1 or Claude Extended Thinking) to run offline on Gamma without losing logical rigor.

```bash
./audit_agent.py /path/to/my_reasoning_skill/
```
