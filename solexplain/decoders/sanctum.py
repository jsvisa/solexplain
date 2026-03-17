"""Sanctum LST decoder — liquid staking token infrastructure and swaps."""

from .base import BaseDecoder, find_instructions_from_logs

PROGRAM_NAMES = {
    "stkitrT1Uoy18Dk1fTrgPw8W6MVzoCfYoAFT4MLsmhq": "Sanctum Router",
    "unpXTU2Ndrc7WWNyEhQWe4udTzSibLPi25SXv2xbCHQ": "Sanctum Unstake",
}


class SanctumDecoder(BaseDecoder):
    name = "Sanctum"
    output_types = ["sanctum"]
    program_ids = list(PROGRAM_NAMES.keys())

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        results = []
        for pid, program_name in PROGRAM_NAMES.items():
            instructions = find_instructions_from_logs(tx_data, {pid})
            for ix in instructions:
                results.append(
                    {
                        "type": "sanctum",
                        "instruction": ix,
                        "program": program_name,
                    }
                )
        return results

    def format_output(self, d: dict) -> list[str]:
        prog = d.get("program", "Sanctum")
        return [f"  {prog}: {d.get('instruction', 'unknown')}"]
