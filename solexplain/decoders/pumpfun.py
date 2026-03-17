"""Pump.fun decoder — token launchpad and AMM."""

from .base import BaseDecoder, find_instructions_from_logs

PROGRAM_NAMES = {
    "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P": "Pump.fun",
    "pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA": "Pump.fun AMM",
}


class PumpfunDecoder(BaseDecoder):
    name = "Pump.fun"
    output_types = ["pumpfun"]
    program_ids = list(PROGRAM_NAMES.keys())

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        results = []
        for pid, program_name in PROGRAM_NAMES.items():
            instructions = find_instructions_from_logs(tx_data, {pid})
            for ix in instructions:
                results.append(
                    {
                        "type": "pumpfun",
                        "instruction": ix,
                        "program": program_name,
                    }
                )
        return results

    def format_output(self, d: dict) -> list[str]:
        prog = d.get("program", "Pump.fun")
        return [f"  {prog}: {d.get('instruction', 'unknown')}"]
