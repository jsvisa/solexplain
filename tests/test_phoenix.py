"""Tests for the Phoenix decoder."""

from solexplain.decoders.phoenix import PhoenixDecoder


class TestPhoenixDecoder:
    def test_can_decode(self, load_fixture):
        tx = load_fixture("phoenix")
        decoder = PhoenixDecoder()
        program_ids = {
            ix.get("programId", "")
            for ix in tx["transaction"]["message"]["instructions"]
        }
        assert decoder.can_decode(program_ids)

    def test_decode_swap(self, load_fixture):
        tx = load_fixture("phoenix")
        decoder = PhoenixDecoder()
        results = decoder.decode("test_phoenix_tx", tx)
        assert len(results) == 1
        assert results[0]["type"] == "phoenix"
        assert results[0]["instruction"] == "Swap"

    def test_format_output(self):
        decoder = PhoenixDecoder()
        lines = decoder.format_output({"type": "phoenix", "instruction": "Swap"})
        assert lines == ["  Phoenix: Swap"]

    def test_no_match_on_unrelated_tx(self, load_fixture):
        tx = load_fixture("raydium")
        decoder = PhoenixDecoder()
        results = decoder.decode("unrelated", tx)
        assert results == []
