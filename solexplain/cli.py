"""CLI entry point for solexplain."""

import argparse
import datetime

from solexplain.explainer import TxExplanation, explain
from solexplain.parser import DEFAULT_RPC


def _short(addr: str, n: int = 8) -> str:
    if len(addr) <= n * 2 + 3:
        return addr
    return f"{addr[:n]}...{addr[-n:]}"


def format_explanation(r: TxExplanation) -> str:
    lines = []
    lines.append(f"Transaction: {r.tx_hash}")
    if r.block_time:
        dt = datetime.datetime.fromtimestamp(r.block_time, tz=datetime.timezone.utc)
        lines.append(f"Time:        {dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    lines.append(f"Status:      {r.status}")
    lines.append(f"Fee:         {r.fee_lamports / 1e9:.9f} SOL")
    lines.append("")

    # Programs
    lines.append("Programs:")
    for p in r.programs:
        cat = f" [{p['category']}]" if p["category"] != "unknown" else ""
        lines.append(f"  - {p['name']}{cat}")
    lines.append("")

    # Actions
    if r.actions:
        lines.append("Actions:")
        for a in r.actions:
            lines.append(f"  - {a['program']}: {a['instruction']}")
        lines.append("")

    # Token transfers
    if r.token_transfers:
        lines.append("Token Transfers:")
        for t in r.token_transfers:
            direction = t["type"]
            if direction == "transfer":
                lines.append(
                    f"  {t['ui_amount']} (mint:{_short(t['mint'])})"
                    f"  {_short(t['from'])} → {_short(t['to'])}"
                )
            elif direction == "burn":
                lines.append(
                    f"  BURN {t['ui_amount']} (mint:{_short(t['mint'])})"
                    f"  from {_short(t['from'])}"
                )
            elif direction == "mint":
                lines.append(
                    f"  MINT {t['ui_amount']} (mint:{_short(t['mint'])})"
                    f"  to {_short(t['to'])}"
                )
        lines.append("")

    # SOL transfers
    if r.sol_transfers:
        lines.append("SOL Transfers:")
        for t in r.sol_transfers:
            sol = t["lamports"] / 1e9
            lines.append(f"  {sol:.9f} SOL  {_short(t['from'])} → {_short(t['to'])}")
        lines.append("")

    # Decoder outputs
    if r.decoder_outputs:
        lines.append("Protocol Details:")
        for d in r.decoder_outputs:
            dtype = d.get("type", "unknown")
            if dtype == "wormhole_bridge":
                lines.append(f"  Wormhole Bridge:")
                lines.append(f"    Source:      {d.get('source_chain')}")
                lines.append(f"    Token:       {d.get('symbol') or 'unknown'}")
                lines.append(f"    Amount:      {d.get('amount')}")
                lines.append(f"    Dest chain:  {d.get('destination_chain')}")
                lines.append(f"    Dest addr:   {d.get('destination_address')}")
                lines.append(
                    f"    Dest tx:     {d.get('destination_tx') or 'pending'}"
                )
            else:
                for k, v in d.items():
                    if k != "type":
                        lines.append(f"  {k}: {v}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Explain a Solana transaction in human-readable form"
    )
    parser.add_argument("tx_hash", help="Solana transaction signature")
    parser.add_argument(
        "--rpc",
        default=DEFAULT_RPC,
        help=f"Solana RPC URL (default: {DEFAULT_RPC})",
    )
    args = parser.parse_args()

    result = explain(args.tx_hash, args.rpc)
    print(format_explanation(result))


if __name__ == "__main__":
    main()
