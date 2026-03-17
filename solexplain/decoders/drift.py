"""Drift Protocol decoder — perpetuals and spot DEX."""

from .base import BaseDecoder, find_instructions_from_logs


class DriftDecoder(BaseDecoder):
    name = "Drift"
    output_types = ["drift"]
    program_ids = [
        "dRiftyHA39MWEi3m9aunc5MzRF1JYuBsbn6VPcn33UH",
    ]

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        instructions = find_instructions_from_logs(tx_data, set(self.program_ids))
        if not instructions:
            return []
        return [{"type": "drift", "instruction": ix} for ix in instructions]

    def format_output(self, d: dict) -> list[str]:
        return [f"  Drift: {d.get('instruction', 'unknown')}"]
