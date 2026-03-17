"""Jupiter aggregator decoder — extracts swap route instruction type."""

from .base import BaseDecoder, find_instructions_from_logs


class JupiterDecoder(BaseDecoder):
    name = "Jupiter"
    program_ids = [
        "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4",  # v6
        "JUP4Fb2cqiRUcaTHdrPC8h2gNsA2ETXiPDD33WcGuJB",  # v4
    ]

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        instructions = find_instructions_from_logs(tx_data, set(self.program_ids))
        if not instructions:
            return []
        return [
            {"type": "jupiter_swap", "instruction": ix} for ix in instructions
        ]
