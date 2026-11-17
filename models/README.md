# Model Directory: Project Fleece Gamma

This folder holds the local AI model reasoning brain files for Project Fleece Gamma.

Once these files are downloaded to your computer, Fleece Gamma runs completely offline. It never sends your sensitive contracts, audits, or proprietary data to the internet.

---

## What Is in This Folder

1. Core Reasoning Model (`model.gguf` / `Qwen3.5-9B_TQ-Q8_0.gguf`)
   - Brain: Qwen 3.5 9B Instruct.
   - Precision: Full Q8_0 precision (clean, uncompromised math and logic weights).
   - What It Does: Solves hard problems, tests its own logic step by step, and audits long documents.
   - Dynamic Thinking: Supports 10 switchable plusIQ reasoning modes (such as spoon, einstein, and instant modes) with automatic thought-stripping so working memory stays tidy.
   - Memory Speed: Uses TurboQuant 4-bit memory packing (turbo4/turbo4) to unlock 65,536 tokens of working memory. If TurboQuant is not supported on your system, it automatically steps down to standard q8_0 memory so it never crashes.

2. Optical Sieve Specialists (Mimir OCR Pass 3)
   - Specialist Brain: `chandra-ocr-2.Q6_K.gguf`
   - Specialist Eyes: `chandra-ocr-2.mmproj-f16.gguf`
   - What They Do: These files sleep until you feed Gamma a complex, degraded, or handwritten scan that passes 1 and 2 cannot verify. It wakes up on demand, decodes the tough text, and immediately sleeps again to save memory for reasoning.

---

## How to Download and Verify the Models

You can download and verify all the necessary model files with one command from the project root folder:

```bash
python setup_models.py
```

This script checks whether the models are already on your computer. If they are missing or damaged, it downloads them automatically and tests their file size.

---

## Model Specifications

- Core Brain File: `model.gguf` (aliased to `Qwen3.5-9B_TQ-Q8_0.gguf`)
- Architecture: Qwen 3.5 (9 Billion Parameters)
- Quantization: Q8_0 (8-bit quantization)
- KV Cache Mode: turbo4/turbo4 (with automatic q8_0 fallback)
- Context Window: 65,536 tokens
- Reserved Thinking Buffer: 4,096 tokens
- Default Source: Hugging Face (`unsloth/Qwen3.5-9B-GGUF`)
- OCR Fallback Model: `chandra-ocr-2.Q6_K.gguf` + `chandra-ocr-2.mmproj-f16.gguf`
