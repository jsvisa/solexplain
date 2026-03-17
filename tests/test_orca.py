"""Tests for the Orca decoder using real transaction data.

Fixture tx: 4NJTzecfhvJi5m3be4KnPNz7d5uRDZN3ypov9QEnpwYTE31BANPXg2guke9kjBYShZSsvD1rv9wSRymCAMynFNMC
A direct Orca Whirlpool Swap.

Also tested with the Jupiter fixture which contains an Orca Whirlpool Swap as inner CPI.
"""

from solexplain.decoders.orca import OrcaDecoder


class TestOrcaDecoder:
    def test_can_decode(self, load_fixture):
        tx = load_fixture("orca")
        decoder = OrcaDecoder()
        program_ids = set()
        for ix in tx["transaction"]["message"]["instructions"]:
            program_ids.add(ix.get("programId", ""))
        for inner in tx["meta"].get("innerInstructions") or []:
            for ix in inner.get("instructions", []):
                program_ids.add(ix.get("programId", ""))
        assert decoder.can_decode(program_ids)

    def test_decode_direct_swap(self, load_fixture):
        tx = load_fixture("orca")
        decoder = OrcaDecoder()
        results = decoder.decode(
            "4NJTzecfhvJi5m3be4KnPNz7d5uRDZN3ypov9QEnpwYTE31BANPXg2guke9kjBYShZSsvD1rv9wSRymCAMynFNMC",
            tx,
        )
        assert len(results) >= 1
        assert results[0]["type"] == "orca"
        assert results[0]["instruction"] == "Swap"

    def test_decode_via_jupiter_cpi(self, load_fixture):
        """Orca Whirlpool is invoked as inner CPI inside a Jupiter Route."""
        tx = load_fixture("jupiter")
        decoder = OrcaDecoder()
        results = decoder.decode("jupiter_tx", tx)
        assert len(results) >= 1
        assert results[0]["type"] == "orca"
        assert results[0]["instruction"] == "Swap"

    def test_no_match_on_unrelated_tx(self, load_fixture):
        tx = load_fixture("staking_native")
        decoder = OrcaDecoder()
        results = decoder.decode("unrelated", tx)
        assert results == []
