"""Fetch and parse Solana transactions via JSON-RPC."""

import json
import re
import urllib.request

from solexplain.registry import lookup_program

DEFAULT_RPC = "https://api.mainnet-beta.solana.com"


def fetch_tx(tx_hash: str, rpc_url: str = DEFAULT_RPC) -> dict:
    """Fetch a transaction from Solana RPC with jsonParsed encoding."""
    payload = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [
                tx_hash,
                {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0},
            ],
        }
    ).encode()
    req = urllib.request.Request(
        rpc_url,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    if "error" in data:
        raise RuntimeError(f"RPC error: {data['error']}")
    result = data.get("result")
    if result is None:
        raise RuntimeError(f"Transaction not found: {tx_hash}")
    return result


def parse_info(tx: dict) -> dict:
    """Extract basic transaction metadata."""
    meta = tx.get("meta", {})
    return {
        "block_time": tx.get("blockTime"),
        "slot": tx.get("slot"),
        "status": "success" if meta.get("err") is None else "failed",
        "fee": meta.get("fee", 0),
    }


def parse_programs(tx: dict) -> list[dict]:
    """Extract all invoked programs from instructions and inner instructions."""
    seen = set()
    programs = []
    message = tx.get("transaction", {}).get("message", {})

    for ix in message.get("instructions", []):
        pid = ix.get("programId", "")
        if pid and pid not in seen:
            seen.add(pid)
            name, category = lookup_program(pid)
            programs.append({"id": pid, "name": name, "category": category})

    for inner in tx.get("meta", {}).get("innerInstructions", []) or []:
        for ix in inner.get("instructions", []):
            pid = ix.get("programId", "")
            if pid and pid not in seen:
                seen.add(pid)
                name, category = lookup_program(pid)
                programs.append({"id": pid, "name": name, "category": category})

    return programs


def _extract_token_transfer(ix: dict) -> dict | None:
    """Extract a token transfer from a parsed instruction, or None."""
    parsed = ix.get("parsed")
    if not isinstance(parsed, dict):
        return None
    ix_type = parsed.get("type", "")
    info = parsed.get("info", {})

    if ix_type == "transferChecked":
        token_amount = info.get("tokenAmount", {})
        return {
            "type": "transfer",
            "mint": info.get("mint", ""),
            "amount": token_amount.get("amount", "0"),
            "decimals": token_amount.get("decimals", 0),
            "ui_amount": token_amount.get("uiAmountString", "0"),
            "from": info.get("source", ""),
            "to": info.get("destination", ""),
        }
    elif ix_type == "burn" or ix_type == "burnChecked":
        token_amount = info.get("tokenAmount", {})
        if not token_amount:
            return {
                "type": "burn",
                "mint": info.get("mint", ""),
                "amount": str(info.get("amount", "0")),
                "decimals": 0,
                "ui_amount": str(info.get("amount", "0")),
                "from": info.get("account", ""),
                "to": "",
            }
        return {
            "type": "burn",
            "mint": info.get("mint", ""),
            "amount": token_amount.get("amount", "0"),
            "decimals": token_amount.get("decimals", 0),
            "ui_amount": token_amount.get("uiAmountString", "0"),
            "from": info.get("account", ""),
            "to": "",
        }
    elif ix_type == "mintTo" or ix_type == "mintToChecked":
        token_amount = info.get("tokenAmount", {})
        if not token_amount:
            return {
                "type": "mint",
                "mint": info.get("mint", ""),
                "amount": str(info.get("amount", "0")),
                "decimals": 0,
                "ui_amount": str(info.get("amount", "0")),
                "from": "",
                "to": info.get("account", ""),
            }
        return {
            "type": "mint",
            "mint": info.get("mint", ""),
            "amount": token_amount.get("amount", "0"),
            "decimals": token_amount.get("decimals", 0),
            "ui_amount": token_amount.get("uiAmountString", "0"),
            "from": "",
            "to": info.get("account", ""),
        }
    return None


def parse_token_transfers(tx: dict) -> list[dict]:
    """Extract token transfers from all instructions (top-level + inner)."""
    transfers = []
    message = tx.get("transaction", {}).get("message", {})

    for ix in message.get("instructions", []):
        t = _extract_token_transfer(ix)
        if t:
            transfers.append(t)

    for inner in tx.get("meta", {}).get("innerInstructions", []) or []:
        for ix in inner.get("instructions", []):
            t = _extract_token_transfer(ix)
            if t:
                transfers.append(t)

    return transfers


def parse_sol_transfers(tx: dict) -> list[dict]:
    """Extract SOL transfers from system program transfer instructions."""
    transfers = []
    message = tx.get("transaction", {}).get("message", {})

    def _check(ix):
        parsed = ix.get("parsed")
        if not isinstance(parsed, dict):
            return
        if parsed.get("type") == "transfer" and ix.get("programId") == "11111111111111111111111111111111":
            info = parsed.get("info", {})
            transfers.append(
                {
                    "from": info.get("source", ""),
                    "to": info.get("destination", ""),
                    "lamports": info.get("lamports", 0),
                }
            )

    for ix in message.get("instructions", []):
        _check(ix)
    for inner in tx.get("meta", {}).get("innerInstructions", []) or []:
        for ix in inner.get("instructions", []):
            _check(ix)

    return transfers


_INVOKE_RE = re.compile(r"Program (\w+) invoke \[(\d+)\]")
_INSTRUCTION_RE = re.compile(r"Instruction: (.+)")


def parse_actions(tx: dict) -> list[dict]:
    """Parse log messages to extract program invoke / instruction pairs."""
    logs = tx.get("meta", {}).get("logMessages", []) or []
    actions = []
    program_stack = []

    for line in logs:
        m = _INVOKE_RE.search(line)
        if m:
            program_stack.append(m.group(1))
            continue
        m = _INSTRUCTION_RE.search(line)
        if m and program_stack:
            pid = program_stack[-1]
            name, _ = lookup_program(pid)
            actions.append({"program": name, "instruction": m.group(1)})
            continue
        if "success" in line or "failed" in line:
            if program_stack:
                program_stack.pop()

    return actions
