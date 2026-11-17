import os
import re
import sys
import json
import logging
from typing import Generator, List, Dict, Any, Optional, Tuple

# Ensure compiled TurboQuant dylibs are discovered first
TURBOQUANT_LIB_DIR = "/Users/ATLAS/Desktop/CODING/Tools/llama-cpp-turboquant/build/bin"
if os.path.exists(TURBOQUANT_LIB_DIR):
    os.environ.setdefault("LLAMA_CPP_LIB_PATH", TURBOQUANT_LIB_DIR)
    os.environ.setdefault("MTMD_CPP_LIB", TURBOQUANT_LIB_DIR)

KV_CACHE_TYPE_MAP = {
    "f16": 1,
    "q8_0": 8,
    "turbo2": 43,  # GGML_TYPE_TURBO2_0
    "turbo3": 44,  # GGML_TYPE_TURBO3_0
    "turbo4": 47,  # GGML_TYPE_TURBO4_0 (Optimal default on M1 Pro)
    "turbo5": 51,  # GGML_TYPE_TURBO5_0
    "turbo6": 52,  # GGML_TYPE_TURBO6_0
}

logging.basicConfig(level=logging.INFO, format="[Fleece-Gamma] %(levelname)s: %(message)s")
logger = logging.getLogger("FleeceReasoningEngine")

VALID_REASONING_MODES = (
    "spoon",       # Ultra xhigh research chain-of-thought
    "einstein",    # Multi-agent analytical high reasoning
    "xhigh",       # Extended high reasoning
    "medium",      # Balanced standard reasoning
    "low",         # Fast lightweight reasoning
    "ispoon",      # Instruct-only spoon (0 thinking tokens)
    "ieinstein",   # Instruct-only einstein (0 thinking tokens)
    "ixhigh",      # Instruct-only xhigh (0 thinking tokens)
    "imedium",     # Instruct-only medium (0 thinking tokens)
    "ilow",        # Instruct-only low (0 thinking tokens)
)


class FleeceEngine:
    """
    Core reasoning execution engine for Project: Fleece Gamma.
    Wraps llama.cpp GGUF inference for Qwen 3.5 9B with native TurboQuant KV caching (turbo4/turbo4),
    automated Metal acceleration, and dynamic reasoning mode control.
    """

    def __init__(self, config_path: str = "fleece_config.json"):
        self.base_dir = os.path.dirname(os.path.abspath(config_path))
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        raw_model_path = self.config.get("model_path", "models/model.gguf")
        self.model_path = os.path.normpath(os.path.join(self.base_dir, raw_model_path))

        # Fallback to models/model.gguf if raw path doesn't exist directly
        alt_model_path = os.path.normpath(os.path.join(self.base_dir, "models/model.gguf"))
        if not os.path.exists(self.model_path) and os.path.exists(alt_model_path):
            self.model_path = alt_model_path

        is_broken_link = os.path.islink(self.model_path) and not os.path.exists(self.model_path)
        is_missing_or_empty = not os.path.exists(self.model_path) or os.path.getsize(self.model_path) < 1_000_000

        if is_broken_link or is_missing_or_empty:
            logger.info("Model file not found locally. Initiating automated first-run setup...")
            sys.path.insert(0, self.base_dir)
            from setup_models import download_model
            self.model_path = download_model()

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at: {self.model_path}")

        engine_cfg = self.config.get("engine", {})
        self.n_ctx = engine_cfg.get("n_ctx", 65536)
        self.n_threads = engine_cfg.get("n_threads", os.cpu_count() or 4)
        self.n_gpu_layers = engine_cfg.get("n_gpu_layers", -1)
        self.default_temp = engine_cfg.get("temperature", 0.6)
        self.default_top_p = engine_cfg.get("top_p", 0.95)
        self.default_top_k = engine_cfg.get("top_k", 20)
        self.repeat_penalty = engine_cfg.get("repeat_penalty", 1.0)
        self.reasoning_mode = engine_cfg.get("default_reasoning_mode", "einstein")
        self.flash_attn = engine_cfg.get("flash_attn", True)
        self.kv_cache_type_k = engine_cfg.get("kv_cache_type_k", "turbo4")
        self.kv_cache_type_v = engine_cfg.get("kv_cache_type_v", "turbo4")
        self.kv_fallback_type = engine_cfg.get("kv_fallback_type", "q8_0")
        self.turbo_sparse_v = engine_cfg.get("turbo_sparse_v", True)
        self.turbo_auto_asymmetric = engine_cfg.get("turbo_auto_asymmetric", True)

        self.llm = None
        self._init_backend()

    def _init_backend(self):
        if self.turbo_sparse_v:
            os.environ.setdefault("TURBO_SPARSE_V", "1")
        if self.turbo_auto_asymmetric:
            os.environ.setdefault("TURBO_AUTO_ASYMMETRIC", "1")
        if self.kv_cache_type_v == "turbo2":
            os.environ.setdefault("TURBO_LAYER_ADAPTIVE", "7")

        k_code = KV_CACHE_TYPE_MAP.get(self.kv_cache_type_k.lower(), 47)
        v_code = KV_CACHE_TYPE_MAP.get(self.kv_cache_type_v.lower(), 47)

        try:
            from llama_cpp import Llama
            logger.info(
                "Initializing llama_cpp backend with GGUF: %s (n_ctx=%d, flash_attn=%s, type_k=%s, type_v=%s)",
                self.model_path, self.n_ctx, self.flash_attn, self.kv_cache_type_k, self.kv_cache_type_v
            )
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=self.n_ctx,
                n_threads=self.n_threads,
                n_gpu_layers=self.n_gpu_layers,
                type_k=k_code,
                type_v=v_code,
                flash_attn=self.flash_attn,
                verbose=False,
            )
            logger.info(
                "Reasoning model loaded into memory. Context capacity: %d tokens | Active Mode: {REASON:%s}",
                self.n_ctx,
                self.reasoning_mode,
            )
        except Exception as e:
            fallback_k = KV_CACHE_TYPE_MAP.get(self.kv_fallback_type.lower(), 8)
            fallback_v = KV_CACHE_TYPE_MAP.get(self.kv_fallback_type.lower(), 8)
            logger.warning(
                "TurboQuant KV cache initialization error: %s. Falling back to %s/%s KV cache...",
                e, self.kv_fallback_type, self.kv_fallback_type
            )
            try:
                from llama_cpp import Llama
                self.llm = Llama(
                    model_path=self.model_path,
                    n_ctx=self.n_ctx,
                    n_threads=self.n_threads,
                    n_gpu_layers=self.n_gpu_layers,
                    type_k=fallback_k,
                    type_v=fallback_v,
                    flash_attn=self.flash_attn,
                    verbose=False,
                )
                logger.info("Fallback reasoning model loaded successfully. Context capacity: %d tokens", self.n_ctx)
            except Exception as e2:
                logger.error("Failed to initialize llama_cpp engine: %s", e2)
                logger.warning("Ensure llama-cpp-python is installed with matching system architecture.")
                raise

    def set_reasoning_mode(self, mode: str) -> str:
        """Switch active reasoning/instruct mode on the fly."""
        clean_mode = mode.strip().lower()
        if clean_mode not in VALID_REASONING_MODES:
            raise ValueError(
                f"Invalid reasoning mode '{mode}'. Choose from: {', '.join(VALID_REASONING_MODES)}"
            )
        self.reasoning_mode = clean_mode
        logger.info("Switched active reasoning mode to: {REASON:%s}", self.reasoning_mode)
        return self.reasoning_mode

    def is_instruct_only_mode(self) -> bool:
        """Returns True if current mode uses zero thinking tokens (prefixed with 'i')."""
        return self.reasoning_mode.startswith("i")

    @staticmethod
    def extract_thinking_and_answer(raw_response: str) -> Tuple[str, str]:
        """
        Separates internal <think>...</think> chain-of-thought from final answer.
        Handles both explicit <think>...</think> blocks and implicit '... </think>' blocks.
        """
        if not raw_response:
            return "", ""

        text = raw_response.strip()

        # Case 1: Explicit <think>...</think> tag pair
        explicit_match = re.search(r"<think>(.*?)</think>(.*)", text, flags=re.DOTALL)
        if explicit_match:
            return explicit_match.group(1).strip(), explicit_match.group(2).strip()

        # Case 2: Prompt opened <think> implicitly, model closed with </think>
        if "</think>" in text:
            parts = text.split("</think>", 1)
            return parts[0].replace("<think>", "").strip(), parts[1].strip()

        # Case 3: Unclosed <think> (hit token limit mid-thought) or instruct mode
        if text.startswith("<think>"):
            return text.replace("<think>", "", 1).strip(), ""

        return "", text

    def count_tokens(self, text: str) -> int:
        """Accurately count tokens using the model's native tokenizer."""
        if not self.llm:
            return len(text.split()) * 4 // 3
        tokens = self.llm.tokenize(text.encode("utf-8"))
        return len(tokens)

    def generate(
        self,
        prompt: str,
        max_tokens: int = 4096,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        stop: Optional[List[str]] = None,
        stream: bool = False,
    ) -> Any:
        """Run inference on a pre-budgeted prompt."""
        if not self.llm:
            raise RuntimeError("Engine not initialized.")

        temp = temperature if temperature is not None else self.default_temp
        tp = top_p if top_p is not None else self.default_top_p
        tk = top_k if top_k is not None else self.default_top_k
        stop_tokens = stop or ["<|im_end|>", "<|endoftext|>"]

        if stream:
            return self._stream_response(prompt, max_tokens, temp, tp, tk, stop_tokens)

        response = self.llm(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temp,
            top_p=tp,
            top_k=tk,
            repeat_penalty=self.repeat_penalty,
            stop=stop_tokens,
        )
        return response["choices"][0]["text"]

    def _stream_response(
        self, prompt: str, max_tokens: int, temp: float, tp: float, tk: int, stop_tokens: List[str]
    ) -> Generator[str, None, None]:
        stream = self.llm(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temp,
            top_p=tp,
            top_k=tk,
            repeat_penalty=self.repeat_penalty,
            stop=stop_tokens,
            stream=True,
        )
        for chunk in stream:
            delta = chunk["choices"][0]["text"]
            if delta:
                yield delta

    def chat_format(self, messages: List[Dict[str, str]]) -> str:
        """
        Apply ChatML format native to Qwen 3.5.
        Injects the active {REASON:<mode>} control directive into the latest user turn
        unless an inline {REASON:...} directive was already provided by the caller.
        """
        formatted = ""
        last_user_idx = -1
        for i in range(len(messages) - 1, -1, -1):
            if messages[i].get("role") == "user":
                last_user_idx = i
                break

        for idx, msg in enumerate(messages):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if idx == last_user_idx and self.reasoning_mode and "{REASON:" not in content:
                content = f"{{REASON:{self.reasoning_mode}}} {content}"
            formatted += f"<|im_start|>{role}\n{content}<|im_end|>\n"

        formatted += "<|im_start|>assistant\n"
        return formatted
