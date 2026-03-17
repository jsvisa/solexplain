"""Base class for protocol-specific transaction decoders."""

import re

_INVOKE_RE = re.compile(r"Program (\w+) invoke \[(\d+)\]")
_INSTRUCTION_RE = re.compile(r"Instruction: (.+)")


def find_instructions_from_logs(tx_data: dict, program_ids: set[str]) -> list[str]:
    """Extract instruction names from log messages for the given program IDs.

    Scans meta.logMessages for 'Program <pid> invoke' followed by
    'Instruction: <name>' pairs and returns instruction names matching
    the given program_ids.
    """
    logs = tx_data.get("meta", {}).get("logMessages", []) or []
    instructions = []
    program_stack = []

    for line in logs:
        m = _INVOKE_RE.search(line)
        if m:
            program_stack.append(m.group(1))
            continue
        m = _INSTRUCTION_RE.search(line)
        if m and program_stack:
            if program_stack[-1] in program_ids:
                instructions.append(m.group(1))
            continue
        if "success" in line or "failed" in line:
            if program_stack:
                program_stack.pop()

    return instructions


def short_addr(addr: str, n: int = 8) -> str:
    """Shorten a base58 address for display."""
    if len(addr) <= n * 2 + 3:
        return addr
    return f"{addr[:n]}...{addr[-n:]}"


class BaseDecoder:
    """Subclass this to add protocol-specific enrichment."""

    program_ids: list[str] = []
    name: str = ""
    output_types: list[str] = []

    def can_decode(self, tx_programs: set[str]) -> bool:
        """Return True if this decoder is relevant to the transaction."""
        return bool(set(self.program_ids) & tx_programs)

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        """Return extra enrichment dicts for this protocol.

        Each dict should have at least a 'type' key describing the enrichment.
        """
        return []

    def format_output(self, d: dict) -> list[str]:
        """Format a single decoder output dict as display lines.

        Override in subclasses for protocol-specific formatting.
        Default: key-value pairs (skipping 'type').
        """
        return [f"  {k}: {v}" for k, v in d.items() if k != "type"]
