"""Lending decoder — Marginfi, Solend/Save, Kamino."""

from .base import BaseDecoder, find_instructions_from_logs

LENDING_PROGRAMS = {
    "MFv2hWf31Z9kbCa1snEPYctwafyhdvnV7FZnsebVacA": "Marginfi",
    "So1endDq2YkqhipRh3WViPa8hFMo56cMYwLBYtyHWmD": "Solend/Save",
    "KLend2g3cP87ber8PCj7bvw9RpAhE3z2DRjwMKVpMjJ": "Kamino Lending",
    "6LtLpnUFNByNXLyCoK9wA2MykKAmQNZKBdY8s47dehDc": "Kamino Vaults",
}


class LendingDecoder(BaseDecoder):
    name = "Lending"
    output_types = ["lending"]
    program_ids = list(LENDING_PROGRAMS.keys())

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        results = []
        for pid, protocol in LENDING_PROGRAMS.items():
            instructions = find_instructions_from_logs(tx_data, {pid})
            for ix in instructions:
                results.append(
                    {
                        "type": "lending",
                        "protocol": protocol,
                        "action": ix,
                    }
                )
        return results

    def format_output(self, d: dict) -> list[str]:
        protocol = d.get("protocol", "Lending")
        return [f"  {protocol}: {d.get('action', 'unknown')}"]
