"""Jupiter DCA, Limit Order, and Perps decoder."""

from .base import BaseDecoder, find_instructions_from_logs

JUPITER_PROGRAMS = {
    "DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M": (
        "jupiter_dca",
        "Jupiter DCA",
    ),
    "jupoNjAxXgZ4rjzxzPMP4oxduvQsQtZzyknqvzYNrNu": (
        "jupiter_limit",
        "Jupiter Limit",
    ),
    "PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu": (
        "jupiter_perps",
        "Jupiter Perps",
    ),
}


class JupiterProductsDecoder(BaseDecoder):
    name = "Jupiter Products"
    output_types = ["jupiter_dca", "jupiter_limit", "jupiter_perps"]
    program_ids = list(JUPITER_PROGRAMS.keys())

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        results = []
        for pid, (output_type, label) in JUPITER_PROGRAMS.items():
            instructions = find_instructions_from_logs(tx_data, {pid})
            for ix in instructions:
                results.append(
                    {
                        "type": output_type,
                        "instruction": ix,
                        "program": label,
                    }
                )
        return results

    def format_output(self, d: dict) -> list[str]:
        prog = d.get("program", "Jupiter")
        return [f"  {prog}: {d.get('instruction', 'unknown')}"]
