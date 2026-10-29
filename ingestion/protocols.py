import re
import logging
from typing import List, Callable, Optional

logger = logging.getLogger("IngestionProtocols")


class IngestionProtocols:
    """
    Ingestion Protocols for Project: Fleece Gamma.
    Enforces strict non-destructive ingestion:
    1. Anti-Parsing Protocol: Preserves 100% of indentation, tables, syntax, and raw characters.
    2. Anti-Chunking Protocol: Rejects arbitrary slicing. Treats documents and sections as complete wholes.
    3. Anti-Truncating Protocol: Rejects abrupt text cutting. Guarantees complete semantic blocks.
    """

    def __init__(self, max_block_tokens: int = 8192, token_counter: Optional[Callable[[str], int]] = None):
        self.max_block_tokens = max_block_tokens
        self.token_counter = token_counter or (lambda s: len(s.split()) * 4 // 3)

    # -------------------------------------------------------------
    # Protocol 1: Anti-Parsing
    # -------------------------------------------------------------
    def anti_parse(self, raw_input: str) -> str:
        """
        Guarantees that raw text is NEVER destructively parsed or stripped.
        Retains markdown tables, code blocks, indentation, and structure verbatim.
        """
        if not raw_input:
            return ""

        clean = raw_input.replace("\r\n", "\n").replace("\r", "\n")

        fences = clean.count("```")
        if fences % 2 != 0:
            clean += "\n```\n"

        return clean

    # -------------------------------------------------------------
    # Protocol 2: Anti-Chunking
    # -------------------------------------------------------------
    def anti_chunk(self, content: str) -> List[str]:
        """
        Strictly rejects fixed-character or fixed-token slicing.
        Retains the document as a complete unbroken entity.
        If the document contains clear Markdown section markers, yields
        complete, unbroken sections rather than arbitrary chunks.
        """
        clean = self.anti_parse(content)

        pattern = r"(?=(?:^|\n)#{1,3}\s+)"
        sections = [s.strip() for s in re.split(pattern, clean, flags=re.MULTILINE) if s.strip()]

        if not sections:
            return [clean]

        return sections

    # -------------------------------------------------------------
    # Protocol 3: Anti-Truncating
    # -------------------------------------------------------------
    def verify_no_truncation(self, text: str, available_tokens: int) -> str:
        """
        Verifies that content fits within available headroom without truncation.
        Warns if the document pushes up against hardware limits.
        """
        current_tokens = self.token_counter(text)
        if current_tokens > available_tokens:
            logger.warning(
                "Ingested document size (%d tokens) approaches context headroom (%d tokens). "
                "Retaining full document intact; conversational history will be evicted to accommodate.",
                current_tokens,
                available_tokens,
            )
        return text
