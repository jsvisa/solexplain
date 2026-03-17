"""Meteora DLMM/Pools decoder — extracts swap and liquidity actions."""

from .base import BaseDecoder, find_instructions_from_logs

PROGRAM_NAMES = {
    "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo": "Meteora DLMM",
    "Eo7WjKq67rjJQSZxS6z3YkapzY3eMj6Xy8X5EQVn5UaB": "Meteora Pools",
}


class MeteoraDecoder(BaseDecoder):
    name = "Meteora"
    program_ids = list(PROGRAM_NAMES.keys())

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        results = []
        for pid, program_name in PROGRAM_NAMES.items():
            instructions = find_instructions_from_logs(tx_data, {pid})
            for ix in instructions:
                results.append(
                    {
                        "type": "meteora",
                        "instruction": ix,
                        "program": program_name,
                    }
                )
        return results
