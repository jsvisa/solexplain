---
name: solexplain
description: Use when explaining Solana transactions in human-readable form, decoding protocol-specific actions, or adding new protocol decoders to solexplain.
---

# solexplain

CLI tool that fetches a Solana transaction and explains it in human-readable form — programs involved, SOL/token transfers, and protocol-specific actions.

## How to Run

Always use the CLI via Bash — never use a browser or Playwright.

Default RPC is `https://api.mainnet-beta.solana.com`. Override with `--rpc` or the `SOLANA_RPC` environment variable:

```bash
# default RPC
solexplain <tx_signature>

# custom RPC via flag
solexplain <tx_signature> --rpc https://your-rpc-url.com

# custom RPC via env
SOLANA_RPC=https://your-rpc-url.com solexplain <tx_signature>
```

**Output includes:**
- Transaction status, timestamp, fee
- Programs involved (with protocol labels)
- SOL and token transfers
- Protocol-specific decoded actions (swap routes, lending ops, perps, etc.)

## Supported Protocols

| Category | Protocols |
|----------|-----------|
| DEX | Jupiter v4/v6, Raydium CLMM/AMM/CPMM, Meteora DLMM/Pools, Orca Whirlpool, Phoenix |
| Jupiter Products | DCA, Limit Order, Perps |
| Lending | Marginfi, Solend/Save, Kamino Lending, Kamino Vaults, Jupiter Lend |
| Staking | Native Stake, Marinade, Jito Staking, Jito Tip Router |
| Launchpad | Pump.fun, Pump.fun AMM |
| Bridge | Wormhole (Core, Token Bridge, Relayer) |
| Other | Sanctum Router/Unstake, Drift |

## Install

```bash
pip install solexplain
# or from source
pip install -e .
```

## Adding a New Decoder

Drop a file in `solexplain/decoders/myprotocol.py` — it auto-registers:

```python
from .base import BaseDecoder, find_instructions_from_logs

class MyProtocolDecoder(BaseDecoder):
    name = "My Protocol"
    program_ids = ["MyProgram111111111111111111111111111111111"]

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        instructions = find_instructions_from_logs(tx_data, set(self.program_ids))
        return [{"type": "my_protocol", "instruction": ix} for ix in instructions]
```

`BaseDecoder` subclasses in `solexplain/decoders/` are discovered automatically via `registry.py` — no registration step needed.

## Key Files

| File | Purpose |
|------|---------|
| `solexplain/cli.py` | Entry point (`solexplain` command) |
| `solexplain/explainer.py` | Orchestrates fetch → parse → decode |
| `solexplain/parser.py` | Parses raw RPC response into transfers/programs |
| `solexplain/registry.py` | Auto-discovers and registers decoders |
| `solexplain/decoders/base.py` | `BaseDecoder` base class |
| `solexplain/tokens.py` | Token mint → symbol/decimals lookup |
