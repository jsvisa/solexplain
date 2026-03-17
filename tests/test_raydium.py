"""Tests for the Raydium decoder using real transaction data.

Fixture tx: 2mMCbovia2Wv7LfjmRP5HAoRHhJE8f5ScUHZwAJFqHL6HFVP6BEd9XfHDMYAeei3AGmKxDVTRrpn8C2aimoqZ3ed
A Raydium CLMM Swap.
"""

from solexplain.decoders.raydium import RaydiumDecoder


class TestRaydiumDecoder:
    def test_can_decode(self, load_fixture):
        tx = load_fixture("raydium")
        decoder = RaydiumDecoder()
        program_ids = set()
        for ix in tx["transaction"]["message"]["instructions"]:
            program_ids.add(ix.get("programId", ""))
        for inner in tx["meta"].get("innerInstructions") or []:
            for ix in inner.get("instructions", []):
                program_ids.add(ix.get("programId", ""))
        assert decoder.can_decode(program_ids)

    def test_decode_clmm_swap(self, load_fixture):
        tx = load_fixture("raydium")
        decoder = RaydiumDecoder()
        results = decoder.decode(
            "2mMCbovia2Wv7LfjmRP5HAoRHhJE8f5ScUHZwAJFqHL6HFVP6BEd9XfHDMYAeei3AGmKxDVTRrpn8C2aimoqZ3ed",
            tx,
        )
        assert len(results) >= 1
        swap = results[0]
        assert swap["type"] == "raydium"
        assert swap["instruction"] == "Swap"
        assert swap["program"] == "Raydium CLMM"

    def test_no_match_on_unrelated_tx(self, load_fixture):
        tx = load_fixture("staking_native")
        decoder = RaydiumDecoder()
        results = decoder.decode("unrelated", tx)
        assert results == []
