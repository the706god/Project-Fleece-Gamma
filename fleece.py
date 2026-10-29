#!/usr/bin/env python3
"""
Project: Fleece Gamma - The 'Crate Motor' SLM Build (Reasoning Edition)
Model: Qwen 3.5 9B (8.95B) The Defiant Fable Uncensored Heretic plusIQ-TOOLS NEO MAX MTP (Q6_K)
Equipped with:
- Switchable plusIQ Reasoning Modes ({REASON:spoon}, {REASON:einstein}, {REASON:xhigh}, {REASON:medium}, {REASON:low})
- Switchable Zero-Thinking Instruct Modes ({REASON:ispoon}, {REASON:ieinstein}, {REASON:ixhigh}, {REASON:imedium}, {REASON:ilow})
- Living Markdown Dossier (L1 Fast-Path Cache, consistently auto-updating with <think> stripping)
- Vectorless RAG (L2 PageIndex Tree Navigation)
- Stateful Graph Memory Engine
- Explicit Anti-Parsing, Anti-Chunking, Anti-Truncating Protocols
- Secondary Legacy Markdown Memory Ledger
"""

import os
import argparse
from typing import Optional, List

from engine.llm_engine import FleeceEngine, VALID_REASONING_MODES
from memory.context_budget import ContextBudgetManager
from memory.markdown_store import LegacyMarkdownStore
from memory.page_index import PageIndexEngine
from memory.dossier import LivingDossierEngine
from memory.state_graph import StateGraphMemoryEngine
from ingestion.protocols import IngestionProtocols

SYSTEM_DIRECTIVE_GAMMA = """You are an advanced analytical reasoning AI engine powered by Project: Fleece Gamma.

MANDATORY REASONING & INGESTION DIRECTIVES:
1. ZERO-DESTRUCTION FIDELITY: Any and all information ingested must NEVER be parsed, chunked, or truncated. All ingested documents, code blocks, tables, records, and notes are treated as complete, unbroken wholes.
2. FIRST-PRINCIPLES REASONING: Deconstruct complex problems methodically. Verify assumptions against unbroken ingested documents before formulating conclusions.
3. HOLISTIC CONTEXT UTILIZATION: Evaluate ingested materials in their full context. Never guess, invent, or make assumptions based on partial snippets. If information is not in the ingested data, state that clearly.
4. CITATION OF UNBROKEN SOURCES: When answering or referencing knowledge, cite the exact source file and section anchor provided by the PageIndex or Dossier memory system.
5. ABSOLUTE FORMAT INTEGRITY: Maintain exact indentation, mathematical notation, code syntax, and tabular structures without destructive reformatting."""


class FleeceCrateMotor:
    """
    Plug-and-play Reasoning AI Crate Motor.
    Encapsulates multi-mode reasoning inference, context limitation safeguards,
    Two-Tier memory (L1 Living Dossier + L2 PageIndex), and stateful graph memory.
    """

    def __init__(self, config_path: str = "fleece_config.json"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        resolved_config = os.path.join(base_dir, config_path)

        self.engine = FleeceEngine(resolved_config)
        markdown_root = os.path.join(
            base_dir, self.engine.config.get("storage", {}).get("markdown_root", "storage/markdown")
        )
        self.markdown_store = LegacyMarkdownStore(markdown_root)
        self.page_index = PageIndexEngine(markdown_root, token_counter=self.engine.count_tokens)
        self.dossier = LivingDossierEngine(markdown_root)

        mem_cfg = self.engine.config.get("memory", {})
        self.memory = ContextBudgetManager(
            max_context_tokens=mem_cfg.get("max_context_tokens", 16384),
            reserved_completion_tokens=mem_cfg.get("reserved_completion_tokens", 4096),
            system_anchor_tokens=mem_cfg.get("system_anchor_tokens", 1200),
            compaction_threshold=mem_cfg.get("memory_compaction_threshold", 0.85),
            strip_thinking_from_history=mem_cfg.get("strip_thinking_from_history", True),
            token_counter=self.engine.count_tokens,
        )

        ingest_cfg = self.engine.config.get("ingestion", {})
        self.ingestion = IngestionProtocols(
            max_block_tokens=ingest_cfg.get("max_block_tokens", 8192),
            token_counter=self.engine.count_tokens,
        )

        # Two-Tier Graph Memory Machine
        self.graph = StateGraphMemoryEngine(
            engine=self.engine,
            memory_budget=self.memory,
            markdown_store=self.markdown_store,
            page_index=self.page_index,
            ingestion_protocols=self.ingestion,
            dossier=self.dossier,
        )

        # Baked-in immutable system anchor
        self.memory.set_system_anchor(SYSTEM_DIRECTIVE_GAMMA)

    def set_reasoning_mode(self, mode: str) -> str:
        """Switch the active plusIQ reasoning or instruct mode."""
        return self.engine.set_reasoning_mode(mode)

    def set_task(self, task_description: str):
        """Define the primary objective for the crate motor without parsing."""
        sanitized = self.ingestion.anti_parse(task_description)
        self.memory.set_active_task(sanitized)
        self.markdown_store.store_knowledge(
            topic="active_task",
            content=sanitized,
            tags=["task", "active_objective"],
        )
        self.page_index.rebuild_index()

    def store_knowledge(self, topic: str, content: str, tags: Optional[List[str]] = None) -> str:
        """Store knowledge in markdown and automatically update PageIndex tree."""
        clean_content = self.ingestion.anti_parse(content)
        path = self.markdown_store.store_knowledge(topic, clean_content, tags)
        self.page_index.rebuild_index()
        return path

    def execute(self, user_prompt: str, stream: bool = True, verbose: bool = False) -> str:
        """Run execution through the Two-Tier State Graph reasoning workflow."""
        state = self.graph.run(user_prompt, stream=stream)
        if verbose:
            print("\n--- [Memory State Graph Trace] ---")
            for t in state.execution_trace:
                print(f"[{t['node']}] -> {t['details']}")
            print("----------------------------------\n")
        return state.response


def cli():
    parser = argparse.ArgumentParser(description="Project: Fleece Gamma - Reasoning SLM Crate Motor")
    parser.add_argument("--task", type=str, help="Initial task objective for the crate motor")
    parser.add_argument("--prompt", type=str, help="Single prompt execution mode")
    parser.add_argument(
        "--mode",
        type=str,
        choices=VALID_REASONING_MODES,
        help="Initial reasoning/instruct mode (spoon, einstein, xhigh, medium, low, ispoon, ieinstein, ixhigh, imedium, ilow)",
    )
    parser.add_argument("--trace", action="store_true", help="Print execution trace from memory graph")
    args = parser.parse_args()

    motor = FleeceCrateMotor()
    if args.mode:
        motor.set_reasoning_mode(args.mode)

    if args.task:
        motor.set_task(args.task)
        print(f"[Task Initialized]: {args.task}")

    if args.prompt:
        motor.execute(args.prompt, stream=True, verbose=args.trace)
        return

    print("=" * 68)
    print(" Project: Fleece Gamma - Ready (Reasoning Edition | Two-Tier Memory)")
    print(" Core: Qwen 3.5 9B (8.95B) The Defiant Fable plusIQ-TOOLS (Q6_K MTP)")
    print(f" Active Reasoning Mode: {{REASON:{motor.engine.reasoning_mode}}}")
    print(" Commands:")
    print("   !mode <name> -> Switch mode (spoon, einstein, xhigh, medium, low,")
    print("                   ispoon, ieinstein, ixhigh, imedium, ilow)")
    print("   !think       -> Inspect the internal <think> trace of last turn")
    print("   !dossier     -> View current Living Dossier cache")
    print("   !toc         -> Display current PageIndex document map")
    print("   !budget      -> Check context token usage")
    print("   !reset       -> Clear conversation turns, keep model and memory")
    print("   exit / quit  -> Terminate session")
    print("=" * 68)

    while True:
        try:
            user_in = input("\n[You] > ").strip()
            if not user_in:
                continue
            if user_in.lower() in ["exit", "quit"]:
                print("Shutting down Fleece Gamma.")
                break
            if user_in == "!toc":
                print("\n" + motor.page_index.get_navigation_map() + "\n")
                continue
            if user_in == "!dossier":
                if os.path.exists(motor.dossier.dossier_path):
                    with open(motor.dossier.dossier_path, "r", encoding="utf-8") as f:
                        print("\n" + f.read() + "\n")
                continue
            if user_in == "!budget":
                alloc = motor.memory.get_budget_allocation()
                print("\n=== Context Budget Allocation ===")
                for k, v in alloc.items():
                    print(f"  {k}: {v}")
                print("=================================\n")
                continue
            if user_in == "!reset":
                motor.memory.reset_history()
                print("\n[✓] Conversation turns cleared. Model and memory retained.\n")
                continue
            if user_in == "!think":
                last = motor.graph.last_state
                if last and last.thinking_trace:
                    print("\n=== Last Internal Reasoning Trace (<think>) ===")
                    print(last.thinking_trace)
                    print("===============================================\n")
                else:
                    print("\n[i] No internal <think> trace recorded on the previous turn.\n")
                continue
            if user_in.startswith("!mode"):
                parts = user_in.split(maxsplit=1)
                if len(parts) < 2:
                    print(
                        f"\nCurrent mode: {{REASON:{motor.engine.reasoning_mode}}}\n"
                        f"Available modes: {', '.join(VALID_REASONING_MODES)}\n"
                    )
                else:
                    try:
                        new_m = motor.set_reasoning_mode(parts[1])
                        print(f"\n[✓] Active reasoning mode set to: {{REASON:{new_m}}}\n")
                    except ValueError as e:
                        print(f"\n[!] {e}\n")
                continue

            motor.execute(user_in, stream=True, verbose=args.trace)
        except KeyboardInterrupt:
            print("\nSession aborted.")
            break


if __name__ == "__main__":
    cli()
