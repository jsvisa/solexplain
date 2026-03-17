"""Phoenix DEX decoder — on-chain order book."""

from .base import BaseDecoder, find_instructions_from_logs


class PhoenixDecoder(BaseDecoder):
    name = "Phoenix"
    output_types = ["phoenix"]
    program_ids = [
        "PhoeNiXZ8ByJGLkxNfZRnkUfjvmuYqLR89jjFHGqdXY",
    ]

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        instructions = find_instructions_from_logs(tx_data, set(self.program_ids))
        if not instructions:
            return []
        return [{"type": "phoenix", "instruction": ix} for ix in instructions]

    def format_output(self, d: dict) -> list[str]:
        return [f"  Phoenix: {d.get('instruction', 'unknown')}"]
