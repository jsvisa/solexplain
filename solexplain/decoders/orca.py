"""Orca Whirlpool decoder — extracts swap and liquidity actions."""

from .base import BaseDecoder, find_instructions_from_logs


class OrcaDecoder(BaseDecoder):
    name = "Orca Whirlpool"
    output_types = ["orca"]
    program_ids = [
        "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc",
    ]

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        instructions = find_instructions_from_logs(tx_data, set(self.program_ids))
        if not instructions:
            return []
        return [{"type": "orca", "instruction": ix} for ix in instructions]

    def format_output(self, d: dict) -> list[str]:
        return [f"  Orca Whirlpool: {d.get('instruction', 'unknown')}"]
