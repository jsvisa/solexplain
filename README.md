# solexplain

Explain Solana transactions in human-readable form. Fetches a transaction via JSON-RPC, parses programs, token transfers, SOL transfers, and runs pluggable protocol decoders to extract protocol-specific details.

## Install

```bash
pip install -e .

# with dev tools (pytest, black, isort, flake8)
pip install -e ".[dev]"
```

## Usage

```bash
solexplain <tx_signature>
solexplain <tx_signature> --rpc https://your-rpc-url.com
```

Example output:

```
Transaction: 4Vu4wEKp...isgN9
Time:        2025-03-15 12:34:56 UTC
Status:      success
Fee:         0.000005000 SOL

Programs:
  - Compute Budget [system]
  - Jupiter v6 [dex]
  - Orca Whirlpool [dex]
  - Token Program [system]

Actions:
  - Jupiter v6: Route
  - Orca Whirlpool: Swap

Token Transfers:
  12.500000 (mint:So11111...1111112)  8xKpQ9n...4jRkVHe → 3xMy7pQ...9nRkZHf

Protocol Details:
  Jupiter: Route swap
  Orca Whirlpool: Swap
```

## Supported Protocol Decoders

| Decoder | Protocols | Output Type |
|---------|-----------|-------------|
| **Jupiter** | Jupiter v6, v4 | Swap route instruction (`Route`, `SharedAccountsRoute`, `ExactOutRoute`) |
| **Jupiter Products** | DCA, Limit Order, Perps | DCA/limit/perps actions (`OpenDca`, `CreateOrder`, `OpenPosition`) |
| **Raydium** | CLMM, AMM v4, Router, CPMM | Swap/liquidity instruction with program label |
| **Meteora** | DLMM, Pools | Swap/liquidity instruction |
| **Orca** | Whirlpool | Swap/liquidity instruction |
| **Drift** | Drift Protocol | Perps/spot DEX actions (`PlaceAndTakePerpOrder`, `Deposit`, etc.) |
| **Phoenix** | Phoenix DEX | On-chain order book actions (`Swap`, `PlaceLimitOrder`, etc.) |
| **Sanctum** | Sanctum Router, Sanctum Unstake | LST swaps (`SwapViaStake`, `Unstake`) |
| **Pump.fun** | Pump.fun, Pump.fun AMM | Token launchpad actions (`Buy`, `Sell`, `Create`) |
| **Staking** | Native Stake, Marinade, Jito Staking, Jito Tip Router | Stake action with account info |
| **Lending** | Marginfi, Solend/Save, Kamino Lending, Kamino Vaults | Lending action (deposit, withdraw, borrow, etc.) |
| **Wormhole** | Core Bridge, Token Bridge, Relayer | Bridge details via WormholeScan API |

Decoders are auto-discovered — drop a new `BaseDecoder` subclass into `solexplain/decoders/` and it registers automatically.

## Adding a New Decoder

Create `solexplain/decoders/myprotocol.py`:

```python
from .base import BaseDecoder, find_instructions_from_logs

class MyProtocolDecoder(BaseDecoder):
    name = "My Protocol"
    program_ids = ["MyProgram111111111111111111111111111111111"]

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        instructions = find_instructions_from_logs(tx_data, set(self.program_ids))
        return [{"type": "my_protocol", "instruction": ix} for ix in instructions]
```

Then add a formatting case in `cli.py`'s `format_explanation()` and a test in `tests/`.

## Architecture

```
solexplain/
├── cli.py              # CLI entry point and output formatting
├── explainer.py        # Orchestrator: fetch → parse → decode
├── parser.py           # Solana RPC fetch and transaction parsing
├── registry.py         # Program ID → name/category mapping
└── decoders/
    ├── base.py         # BaseDecoder class + find_instructions_from_logs helper
    ├── jupiter.py      # Jupiter aggregator
    ├── jupiter_products.py  # Jupiter DCA/Limit/Perps
    ├── raydium.py      # Raydium AMM/CLMM/CPMM
    ├── meteora.py      # Meteora DLMM/Pools
    ├── orca.py         # Orca Whirlpool
    ├── drift.py        # Drift Protocol perps/spot
    ├── phoenix.py      # Phoenix on-chain order book
    ├── sanctum.py      # Sanctum LST infrastructure
    ├── pumpfun.py      # Pump.fun token launchpad
    ├── staking.py      # Native + liquid staking
    ├── lending.py      # Marginfi/Solend/Kamino
    └── wormhole.py     # Wormhole bridge (external API)
tests/
├── conftest.py         # Shared fixtures
├── fixtures/           # Real transaction data (JSON)
├── test_base.py
├── test_cli.py
├── test_jupiter.py
├── test_jupiter_products.py
├── test_raydium.py
├── test_meteora.py
├── test_orca.py
├── test_drift.py
├── test_phoenix.py
├── test_sanctum.py
├── test_pumpfun.py
├── test_staking.py
└── test_lending.py
```

## Development

```bash
# run tests
make test

# format code
make format

# lint (black --check, isort --check, flake8)
make lint

# lint + test
make check

# build package
make build

# publish to PyPI
make publish
```

## Requirements

- Python 3.10+
- `base58` (runtime)
- `pytest`, `black`, `isort`, `flake8` (dev)
