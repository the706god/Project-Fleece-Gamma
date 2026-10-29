# Reasoning Model Directory

This directory houses the GGUF model weights for **Project: Fleece Gamma (Reasoning Edition)**.

### Bundled Physical Weights
A complete, self-contained physical copy of the GGUF model lives directly inside this directory:
- **Filename:** `Qwen3.5-9B-The-Defiant-Fable-Uncnr-Heretic-plusIQ-TOOLS-NEO-MAX-MTP-Q6_K.gguf` (also aliased locally as `model.gguf`)
- **Size:** 8.16 GB (`8,758,814,912` bytes)

### Automated Setup / Verification
You can verify or re-fetch the weights at any time by running from the repository root:
```bash
python setup_models.py
```

### Model Specifications
- **Model:** Qwen 3.5 9B (`8.95B` parameters) The Defiant Fable Uncensored Heretic plusIQ TOOLS NEO MAX MTP
- **Quantization:** `Q6_K` (NEO Imatrix + 16-bit output tensor + Q8_0 MTP tensors)
- **Native Context Capacity:** 262,144 tokens (256K)
- **Switchable Modes:**
  - Reasoning (`<think>...</think>`): `spoon`, `einstein`, `xhigh`, `medium`, `low`
  - Instruct (zero thinking tokens): `ispoon`, `ieinstein`, `ixhigh`, `imedium`, `ilow`
- **Source:** Hugging Face (`DavidAU/Qwen3.5-9B-The-Defiant-Fable-Uncensored-Heretic-NEO-IMATRIX-MAX-MTP-GGUF`)
