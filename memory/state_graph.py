import sys
import time
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("FleeceStateGraph")


class GraphState:
    """Working state container passed through graph execution nodes."""

    def __init__(self, query: str, task: Optional[str] = None):
        self.query: str = query
        self.task: Optional[str] = task
        self.clean_query: str = ""
        self.is_fast_path_hit: bool = False
        self.fast_path_answer: Optional[str] = None
        self.fast_path_source: Optional[str] = None
        self.index_map: str = ""
        self.matched_sections: List[Dict[str, Any]] = []
        self.unbroken_content_block: str = ""
        self.allocation_before: Dict[str, int] = {}
        self.compaction_occurred: bool = False
        self.reasoning_mode: str = "einstein"
        self.thinking_trace: str = ""
        self.clean_answer: str = ""
        self.response: str = ""
        self.execution_trace: List[Dict[str, Any]] = []

    def trace(self, node_name: str, details: str):
        self.execution_trace.append(
            {
                "node": node_name,
                "timestamp": time.time(),
                "details": details,
            }
        )


class StateGraphMemoryEngine:
    """
    Two-Tier Stateful Graph Memory Engine for Project: Fleece Gamma (Reasoning Edition).
    Tier 1: Fast-Path Living Markdown Dossier (L1 Cache, ~150-250 tokens)
    Tier 2: Deep Vectorless PageIndex (L2 Unbroken Source Retrieval)
    Reasoning Pipeline: Separates <think>...</think> chain-of-thought from final verified answer
    and auto-updates DOSSIER.md with pure synthesized facts.
    """

    def __init__(
        self,
        engine,
        memory_budget,
        markdown_store,
        page_index,
        ingestion_protocols,
        dossier,
    ):
        self.engine = engine
        self.budget = memory_budget
        self.markdown = markdown_store
        self.page_index = page_index
        self.ingestion = ingestion_protocols
        self.dossier = dossier
        self.last_state: Optional[GraphState] = None

    def run(self, user_prompt: str, task_context: Optional[str] = None, stream: bool = True) -> GraphState:
        state = GraphState(query=user_prompt, task=task_context)
        state.reasoning_mode = getattr(self.engine, "reasoning_mode", "einstein")

        # 1. INGEST (Anti-Parsing Protocol)
        self._node_ingest(state)

        # 2. CHECK_DOSSIER_L1 (Fast-Path Check)
        self._node_check_dossier_l1(state)

        if not state.is_fast_path_hit:
            # 3. NAVIGATE_PAGEINDEX_L2 (Deep Vectorless Navigation)
            self._node_navigate_pageindex(state)

            # 4. RETRIEVE_UNBROKEN (Zero-Chunking Document Extraction)
            self._node_retrieve_unbroken(state)

        # 5. BUDGET_ENFORCE (Shield Ingested Content / Evict Dialogue History)
        self._node_budget_enforce(state)

        # 6. EXECUTE (Reasoning Inference with Unbroken Material)
        self._node_execute(state, stream=stream)

        # 7. AUTO_UPDATE_DOSSIER (Consistently Update Dossier with New Discoveries)
        if not state.is_fast_path_hit and state.matched_sections:
            self._node_auto_update_dossier(state)

        # 8. ARCHIVE (Record to Secondary Memory Ledger)
        self._node_archive(state)

        self.last_state = state
        return state

    def _node_ingest(self, state: GraphState):
        state.clean_query = self.ingestion.anti_parse(state.query)
        state.trace(
            "INGEST",
            f"Input sanitized with 100% structure preservation. Length: {len(state.clean_query)} chars.",
        )

    def _node_check_dossier_l1(self, state: GraphState):
        """Tier 1 Check: Evaluates Living Dossier for instant verified answers."""
        is_hit, ans, src = self.dossier.check_fast_path(state.clean_query)
        if is_hit and ans:
            state.is_fast_path_hit = True
            state.fast_path_answer = ans
            state.fast_path_source = src

            dossier_block = f"### [Source: {src}]\n{ans}"
            self.budget.set_protected_ingestion(dossier_block)
            self.budget.add_interaction(role="user", content=state.clean_query)
            state.trace(
                "CHECK_DOSSIER_L1",
                f"Fast-Path HIT! Found verified entry in DOSSIER.md ({src}). Sparing deep file scan.",
            )
        else:
            state.trace(
                "CHECK_DOSSIER_L1",
                "Fast-Path MISS. Escalating to L2 PageIndex for deep unbroken retrieval.",
            )

    def _node_navigate_pageindex(self, state: GraphState):
        state.index_map = self.page_index.get_navigation_map()
        state.trace(
            "NAVIGATE_PAGEINDEX_L2",
            f"PageIndex evaluated with {len(self.page_index.tree)} total sections.",
        )

    def _node_retrieve_unbroken(self, state: GraphState):
        matched = self.page_index.navigate_and_retrieve(state.clean_query, max_sections=2)
        state.matched_sections = matched

        if matched:
            citations = []
            for sec in matched:
                citations.append(f"### [Source: {sec['id']}]\n{sec['unbroken_content']}")
            unbroken_block = "\n\n".join(citations)
            state.unbroken_content_block = unbroken_block
            self.budget.set_protected_ingestion(unbroken_block)
            state.trace(
                "RETRIEVE_UNBROKEN",
                f"Loaded {len(matched)} unbroken sections into protected memory without chunking.",
            )
        else:
            self.budget.clear_protected_ingestion()
            state.trace("RETRIEVE_UNBROKEN", "No external document sections required for this turn.")

        self.budget.add_interaction(role="user", content=state.clean_query)

    def _node_budget_enforce(self, state: GraphState):
        state.allocation_before = self.budget.get_token_allocation()
        compaction = self.budget.enforce_budget(offload_callback=self.markdown.archive_evicted_context)
        state.compaction_occurred = compaction

        allocation_after = self.budget.get_token_allocation()
        headroom = allocation_after["remaining_headroom"]

        if compaction:
            state.trace(
                "BUDGET_ENFORCE",
                "Context repartitioned: evicted dialogue history to shield unbroken ingested document.",
            )
        else:
            state.trace(
                "BUDGET_ENFORCE",
                f"Context safe. Protected doc: {allocation_after['ingested_tokens']} tok. "
                f"Available headroom: {headroom} tok.",
            )

    def _node_execute(self, state: GraphState, stream: bool = True):
        messages = self.budget.build_safe_context()
        formatted_prompt = self.engine.chat_format(messages)
        max_gen = getattr(self.budget, "reserved_completion", 4096)

        if stream:
            full_res = []
            print(f"\n[Fleece Gamma | Mode: {{REASON:{state.reasoning_mode}}}]:\n", flush=True)
            for chunk in self.engine.generate(formatted_prompt, max_tokens=max_gen, stream=True):
                sys.stdout.write(chunk)
                sys.stdout.flush()
                full_res.append(chunk)
            print("\n")
            state.response = "".join(full_res)
        else:
            state.response = self.engine.generate(formatted_prompt, max_tokens=max_gen, stream=False)

        thinking, answer = self.engine.extract_thinking_and_answer(state.response)
        state.thinking_trace = thinking
        state.clean_answer = answer or state.response

        self.budget.add_interaction(role="assistant", content=state.response)
        think_tok = self.engine.count_tokens(thinking) if thinking else 0
        ans_tok = self.engine.count_tokens(state.clean_answer)
        state.trace(
            "EXECUTE",
            f"Reasoning completed in mode '{{REASON:{state.reasoning_mode}}}'. "
            f"Thinking tokens: ~{think_tok} | Answer tokens: ~{ans_tok}.",
        )

    def _node_auto_update_dossier(self, state: GraphState):
        """Tier 1 Continuous Update: Persist new discoveries to DOSSIER.md."""
        source_ids = [s["id"] for s in state.matched_sections]
        try:
            self.dossier.record_discovery(
                query=state.clean_query,
                response=state.clean_answer or state.response,
                source_refs=source_ids,
            )
            self.page_index.rebuild_index()
            state.trace(
                "AUTO_UPDATE_DOSSIER",
                "Consistently updated DOSSIER.md with newly verified fact (thinking trace stripped).",
            )
        except Exception as e:
            logger.error("Failed to update dossier: %s", e)

    def _node_archive(self, state: GraphState):
        record = (
            f"**Mode:** `{{REASON:{state.reasoning_mode}}}`\n"
            f"**User:** {state.clean_query[:100]}...\n"
            f"**Assistant:** {state.clean_answer[:120]}...\n"
        )
        if state.is_fast_path_hit:
            record += f"**Cache Hit:** {state.fast_path_source}\n"
        elif state.matched_sections:
            record += f"**Cited Sections:** {', '.join([s['id'] for s in state.matched_sections])}\n"
        self.markdown.archive_record(record)
        state.trace("ARCHIVE", "State recorded to secondary markdown ledger.")
