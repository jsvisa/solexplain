"""Wormhole bridge decoder — enriches transactions with destination chain info."""

import json
import urllib.request

from .base import BaseDecoder

WORMHOLESCAN_API = "https://api.wormholescan.io/api/v1/operations"

CHAIN_NAMES = {
    1: "Solana",
    2: "Ethereum",
    3: "Terra",
    4: "BSC",
    5: "Polygon",
    6: "Avalanche",
    7: "Oasis",
    10: "Fantom",
    13: "Klaytn",
    14: "Celo",
    16: "Moonbeam",
    23: "Arbitrum",
    24: "Optimism",
    30: "Base",
}


def _normalize_address(addr: str) -> str:
    """Strip Wormhole zero-padding from EVM addresses (32-byte -> 20-byte)."""
    if addr.startswith("0x") and len(addr) == 66:
        if addr[2:26] == "0" * 24:
            return "0x" + addr[26:]
    return addr


class WormholeDecoder(BaseDecoder):
    name = "Wormhole Bridge"
    program_ids = [
        "worm2ibMTQZMhU6MaEFR53xnxfLq7E6GR3FIsrjiXvq",  # Core Bridge
        "worm2ZoG2kUd4vFXhvjh93UUH596ayRfgQ2MgjNMTth",  # Core Bridge v2
        "wormDTUJ6AWPNvk59vGQbDvGJmqbDTdgWgAqcLBCgUb",  # Token Bridge
        "3u8hJUVTA4jH1wYAyUur7FFZVQ8H635K3tSHHF4ssjQ5",  # Token Bridge Relayer
        "tbr7Qje6qBzPwfM52csL5KFi8ps5c5vDyiVVBLYVdRf",  # Token Bridge Relayer v2
    ]

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        try:
            return [self._lookup(tx_hash)]
        except Exception:
            return []

    def _lookup(self, tx_hash: str) -> dict:
        url = f"{WORMHOLESCAN_API}?txHash={tx_hash}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())

        ops = data.get("operations", [])
        if not ops:
            return {"type": "wormhole", "error": "No operation found"}

        op = ops[0]
        content = op.get("content", {})
        payload = content.get("payload", {})
        target_chain = op.get("targetChain", {})
        source_chain = op.get("sourceChain", {})

        return {
            "type": "wormhole_bridge",
            "source_chain": CHAIN_NAMES.get(
                source_chain.get("chainId"), source_chain.get("chainId")
            ),
            "source_tx": source_chain.get("transaction", {}).get("txHash"),
            "symbol": op.get("data", {}).get("symbol"),
            "amount": payload.get("amount"),
            "destination_chain": CHAIN_NAMES.get(
                target_chain.get("chainId"), target_chain.get("chainId")
            ),
            "destination_address": _normalize_address(
                payload.get("toAddress", "")
            ),
            "destination_tx": target_chain.get("transaction", {}).get("txHash"),
        }
