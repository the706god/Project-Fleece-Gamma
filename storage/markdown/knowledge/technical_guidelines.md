# Technical Architecture Guidelines
date: 2026-11-18
tags: architecture, crate-motor, reasoning, engineering

## Crate Motor Design Principles
A crate motor is a drop-in local AI build that requires zero external cloud setup.
The engine is completely self-contained within its repository folder, including bundled Native Metal TurboQuant libraries.
Hardware detection occurs dynamically across Apple Silicon Metal, CUDA, and CPU fallback.

## Reasoning Modes (plusIQ Protocol)
Fleece Gamma runs Qwen 3.5 9B Instruct (Full Q8_0 Precision) with 10 switchable modes:
- Reasoning modes (with compacted `<think>...</think>` chain-of-thought): `spoon`, `einstein`, `xhigh`, `medium`, `low`
- Instruct modes (zero thinking tokens): `ispoon`, `ieinstein`, `ixhigh`, `imedium`, `ilow`

## Ingestion Protocol Specifications
The ingestion engine strictly adheres to three unbreakable protocols:
1. Anti-Parsing: Preserves raw markdown tables, syntax trees, and indentation verbatim.
2. Anti-Chunking: Never splits code blocks or document sections across arbitrary token slices.
3. Anti-Truncating: Never truncates ingested documents; evicts older conversational turns first to protect document integrity.

## Context Budget Limits
The working context capacity is set to 65,536 tokens via Native Metal TurboQuant (turbo4/turbo4 KV cache, with automatic q8_0 fallback), with 4,096 tokens reserved for chain-of-thought completion.
When memory usage exceeds 85% of capacity, the engine offloads older dialogue turns to the secondary markdown store and strips historical `<think>...</think>` traces so reasoning never starves unbroken documents.
