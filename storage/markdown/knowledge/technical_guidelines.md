# Technical Architecture Guidelines
date: 2026-10-29
tags: architecture, crate-motor, reasoning, engineering

## Crate Motor Design Principles
A crate motor is a drop-in component that requires zero external setup.
The engine must be completely self-contained within its repo folder, including its physical GGUF reasoning weights.
Hardware detection must occur dynamically without requiring manual flag tuning.

## Reasoning Modes (plusIQ Protocol)
Fleece Gamma uses Qwen 3.5 9B (8.95B) The Defiant Fable Uncensored Heretic plusIQ-TOOLS (Q6_K MTP) with 10 switchable modes:
- Reasoning modes (with compacted `<think>...</think>` chain-of-thought): `spoon`, `einstein`, `xhigh`, `medium`, `low`
- Instruct modes (zero thinking tokens): `ispoon`, `ieinstein`, `ixhigh`, `imedium`, `ilow`

## Ingestion Protocol Specifications
The ingestion engine strictly adheres to three unbreakable protocols:
1. Anti-Parsing: Preserves raw markdown tables, syntax trees, and indentation.
2. Anti-Chunking: Never splits code blocks or paragraphs across arbitrary token limits.
3. Anti-Truncating: Never truncates prompts abruptly; utilizes head-and-tail compaction with explicit continuation notices.

## Context Budget Limits
The default working context is set to 16,384 tokens (expandable up to 262,144 native tokens).
When memory usage exceeds 85% of capacity, the engine triggers automated offloading to the secondary markdown store.
Internal `<think>...</think>` traces from prior turns are stripped from history so reasoning never starves unbroken documents.
