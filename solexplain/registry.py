"""Program ID → (name, category) mapping for well-known Solana programs."""

PROGRAMS: dict[str, tuple[str, str]] = {
    # System
    "11111111111111111111111111111111": ("System Program", "system"),
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA": ("Token Program", "system"),
    "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb": ("Token-2022", "system"),
    "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL": (
        "Associated Token Account",
        "system",
    ),
    "ComputeBudget111111111111111111111111111111": ("Compute Budget", "system"),
    "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr": ("Memo v1", "system"),
    "Memo1UhkJBfCR6MNhJeRaqYk5kfprAPBiqKnAk5WTnN": ("Memo v2", "system"),
    "SysvarRent111111111111111111111111111111111": ("Sysvar Rent", "system"),
    "SysvarC1ock11111111111111111111111111111111": ("Sysvar Clock", "system"),
    # DeFi — Jupiter
    "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4": ("Jupiter v6", "dex"),
    "JUP4Fb2cqiRUcaTHdrPC8h2gNsA2ETXiPDD33WcGuJB": ("Jupiter v4", "dex"),
    # DeFi — Raydium
    "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK": ("Raydium CLMM", "dex"),
    "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8": ("Raydium AMM v4", "dex"),
    "routeUGWgWzqBWFcrCfv8tritsqukccJPu3q5GPP3xS": ("Raydium Router", "dex"),
    "CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C": ("Raydium CPMM", "dex"),
    # DeFi — Orca
    "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc": ("Orca Whirlpool", "dex"),
    # DeFi — Meteora
    "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo": ("Meteora DLMM", "dex"),
    "Eo7WjKq67rjJQSZxS6z3YkapzY3eMj6Xy8X5EQVn5UaB": ("Meteora Pools", "dex"),
    # DeFi — OpenBook / Serum
    "srmqPvymJeFKQ4zGQed1GFppgkRHL9kaELCbyksJtPX": ("Serum v3", "dex"),
    "opnb2LAfJYbRMAHHvqjCwQxanZn7ReEHp1k81EohpZb": ("OpenBook v2", "dex"),
    # Bridges — Wormhole
    "worm2ibMTQZMhU6MaEFR53xnxfLq7E6GR3FIsrjiXvq": ("Wormhole Core Bridge", "bridge"),
    "wormDTUJ6AWPNvk59vGQbDvGJmqbDTdgWgAqcLBCgUb": (
        "Wormhole Token Bridge",
        "bridge",
    ),
    "3u8hJUVTA4jH1wYAyUur7FFZVQ8H635K3tSHHF4ssjQ5": (
        "Wormhole Token Bridge Relayer",
        "bridge",
    ),
    "tbr7Qje6qBzPwfM52csL5KFi8ps5c5vDyiVVBLYVdRf": (
        "Wormhole Token Bridge Relayer v2",
        "bridge",
    ),
    "worm2ZoG2kUd4vFXhvjh93UUH596ayRfgQ2MgjNMTth": (
        "Wormhole Core Bridge v2",
        "bridge",
    ),
    "execXUrAsMnqMmTHj5m7N1YQgsDz3cwGLYCYyuDRciV": (
        "Wormhole Executor",
        "bridge",
    ),
    # Bridges — Others
    "src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4": ("deBridge", "bridge"),
    "FC4eXxkKAJCzs3cfhgSrqhCRbWLqSMmRSSbwukHC44SJ": ("Mayan Finance", "bridge"),
    "BrdgN2RPzEMWF96ZbnnJaUtQDQx7VRXYaHHbYCBvceWB": ("Allbridge Core", "bridge"),
    # Staking
    "Stake11111111111111111111111111111111111111": ("Native Stake", "staking"),
    "MarBmsSgKXdrN1egZf5sqe1TMai9K1rChYNDJgjq7aD": ("Marinade Finance", "staking"),
    "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn": ("Jito Staking", "staking"),
    "jitoVjT9jRUyeXmi8dEfEXBCacqnphn41Rkjwkm7FJq": ("Jito Tip Router", "staking"),
    # Lending
    "MFv2hWf31Z9kbCa1snEPYctwafyhdvnV7FZnsebVacA": ("Marginfi", "lending"),
    "So1endDq2YkqhipRh3WViPa8hFMo56cMYwLBYtyHWmD": ("Solend/Save", "lending"),
    "KLend2g3cP87ber8PCj7bvw9RpAhE3z2DRjwMKVpMjJ": ("Kamino Lending", "lending"),
    "6LtLpnUFNByNXLyCoK9wA2MykKAmQNZKBdY8s47dehDc": ("Kamino Vaults", "lending"),
    # Oracles
    "FsJ3A3u2vn5cTVofAjvy6y5kwABJAqYWpe4975bi2epH": ("Pyth Oracle", "oracle"),
    "SW1TCH7qEPTdLsDHRgPuMQjbQxKdH2aBStViMFnt64f": ("Switchboard v2", "oracle"),
    # Governance
    "GovER5Lthms3bLBqWub97yVrMmEogzX7xNjdXpPPCVZw": ("SPL Governance", "governance"),
    "voTpe3tHQ7AjQHMapgSue2HJFAh2cGsdokqN3XqmVSj": ("Voter Stake Registry", "governance"),
}


def lookup_program(program_id: str) -> tuple[str, str]:
    """Return (name, category) for a program ID, or a truncated fallback."""
    if program_id in PROGRAMS:
        return PROGRAMS[program_id]
    return (f"Unknown ({program_id[:8]}...)", "unknown")
