"""Orchestrator: fetch → parse → decode → structured result."""

from dataclasses import dataclass, field

from solexplain.decoders import decoders
from solexplain.parser import (
    DEFAULT_RPC,
    fetch_tx,
    parse_actions,
    parse_info,
    parse_programs,
    parse_sol_transfers,
    parse_token_transfers,
)


@dataclass
class TxExplanation:
    tx_hash: str
    block_time: int | None
    status: str
    fee_lamports: int
    programs: list[dict] = field(default_factory=list)
    actions: list[dict] = field(default_factory=list)
    token_transfers: list[dict] = field(default_factory=list)
    sol_transfers: list[dict] = field(default_factory=list)
    decoder_outputs: list[dict] = field(default_factory=list)


def explain(tx_hash: str, rpc_url: str = DEFAULT_RPC) -> TxExplanation:
    """Fetch, parse, and decode a Solana transaction."""
    tx = fetch_tx(tx_hash, rpc_url)
    info = parse_info(tx)
    programs = parse_programs(tx)
    actions = parse_actions(tx)
    token_transfers = parse_token_transfers(tx)
    sol_transfers = parse_sol_transfers(tx)

    # Run protocol decoders
    tx_program_ids = {p["id"] for p in programs}
    decoder_outputs = []
    for decoder in decoders:
        if decoder.can_decode(tx_program_ids):
            decoder_outputs.extend(decoder.decode(tx_hash, tx))

    return TxExplanation(
        tx_hash=tx_hash,
        block_time=info["block_time"],
        status=info["status"],
        fee_lamports=info["fee"],
        programs=programs,
        actions=actions,
        token_transfers=token_transfers,
        sol_transfers=sol_transfers,
        decoder_outputs=decoder_outputs,
    )
