"""Raydium AMM/CLMM/CPMM decoder — extracts swap and liquidity actions."""

from .base import BaseDecoder, find_instructions_from_logs

PROGRAM_NAMES = {
    "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK": "Raydium CLMM",
    "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8": "Raydium AMM v4",
    "routeUGWgWzqBWFcrCfv8tritsqukccJPu3q5GPP3xS": "Raydium Router",
    "CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C": "Raydium CPMM",
}


class RaydiumDecoder(BaseDecoder):
    name = "Raydium"
    program_ids = list(PROGRAM_NAMES.keys())

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        results = []
        for pid, program_name in PROGRAM_NAMES.items():
            instructions = find_instructions_from_logs(tx_data, {pid})
            for ix in instructions:
                results.append(
                    {
                        "type": "raydium",
                        "instruction": ix,
                        "program": program_name,
                    }
                )
        return results
