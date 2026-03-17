"""Tests for the Meteora decoder using real transaction data.

Fixture tx: JVoxTRifFdCj37MQkBNRbbFXkqmHvk5QJTXLcC1etE1xXigCT9akvF8LmxRf8pKo4eCYkuzyMhJ2p4Y7AZwHGHk
A Meteora DLMM Swap2.
"""

from solexplain.decoders.meteora import MeteoraDecoder


class TestMeteoraDecoder:
    def test_can_decode(self, load_fixture):
        tx = load_fixture("meteora")
        decoder = MeteoraDecoder()
        program_ids = set()
        for ix in tx["transaction"]["message"]["instructions"]:
            program_ids.add(ix.get("programId", ""))
        for inner in tx["meta"].get("innerInstructions") or []:
            for ix in inner.get("instructions", []):
                program_ids.add(ix.get("programId", ""))
        assert decoder.can_decode(program_ids)

    def test_decode_dlmm_swap(self, load_fixture):
        tx = load_fixture("meteora")
        decoder = MeteoraDecoder()
        results = decoder.decode(
            "JVoxTRifFdCj37MQkBNRbbFXkqmHvk5QJTXLcC1etE1xXigCT9akvF8LmxRf8pKo4eCYkuzyMhJ2p4Y7AZwHGHk",
            tx,
        )
        assert len(results) >= 1
        swap = results[0]
        assert swap["type"] == "meteora"
        assert swap["instruction"] == "Swap2"
        assert swap["program"] == "Meteora DLMM"

    def test_no_match_on_unrelated_tx(self, load_fixture):
        tx = load_fixture("staking_native")
        decoder = MeteoraDecoder()
        results = decoder.decode("unrelated", tx)
        assert results == []
