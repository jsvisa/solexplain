"""Jupiter Lend Earn decoder — deposits/withdrawals into lending vaults."""

from ..tokens import mint_symbol
from .base import BaseDecoder, find_instructions_from_logs

JUPITER_LEND_PROGRAMS = {
    "jup3YeL8QhtSx1e253b2FDvsMNC87fDrgQZivbrndc9": "Jupiter Lend",
    "jupeiUmn818Jg1ekPURTpr4mFo29p46vygyykFJ3wZC": "Jupiter Lend Liquidity",
}


def _find_transfer_info(tx_data: dict) -> dict | None:
    """Find the first transferChecked in innerInstructions and return its info."""
    for group in tx_data.get("meta", {}).get("innerInstructions", []):
        for ix in group.get("instructions", []):
            parsed = ix.get("parsed")
            if not parsed:
                continue
            if parsed.get("type") == "transferChecked":
                return parsed.get("info")
    return None


def _format_amount(amount_str: str, decimals: int) -> str:
    """Format a raw token amount with thousands separators."""
    raw = int(amount_str)
    whole = raw // (10**decimals)
    frac = raw % (10**decimals)
    if frac == 0:
        return f"{whole:,}"
    frac_str = str(frac).zfill(decimals).rstrip("0")
    return f"{whole:,}.{frac_str}"


class JupiterLendDecoder(BaseDecoder):
    name = "Jupiter Lend"
    output_types = ["jupiter_lend"]
    program_ids = list(JUPITER_LEND_PROGRAMS.keys())

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        # Only match when the top-level program is Jupiter Lend
        top_pid = "jup3YeL8QhtSx1e253b2FDvsMNC87fDrgQZivbrndc9"
        instructions = find_instructions_from_logs(tx_data, {top_pid})
        if not instructions:
            return []

        action = instructions[0]  # e.g. "Deposit", "Withdraw"

        # Extract amount and token from inner transferChecked
        transfer = _find_transfer_info(tx_data)
        amount = None
        token = None
        if transfer and "tokenAmount" in transfer:
            ta = transfer["tokenAmount"]
            amount = _format_amount(ta["amount"], ta["decimals"])
            token = mint_symbol(transfer.get("mint", ""))

        return [
            {
                "type": "jupiter_lend",
                "action": action,
                "amount": amount,
                "token": token,
            }
        ]

    def format_output(self, d: dict) -> list[str]:
        action = d.get("action", "unknown")
        amount = d.get("amount")
        token = d.get("token")
        if amount and token:
            return [f"  Jupiter Lend: {action} {amount} {token} into lending vault"]
        return [f"  Jupiter Lend: {action}"]
