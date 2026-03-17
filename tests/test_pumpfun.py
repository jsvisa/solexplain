"""Tests for the Pump.fun decoder."""

from solexplain.decoders.pumpfun import PumpfunDecoder


class TestPumpfunDecoder:
    def test_can_decode(self, load_fixture):
        tx = load_fixture("pumpfun")
        decoder = PumpfunDecoder()
        program_ids = {
            ix.get("programId", "")
            for ix in tx["transaction"]["message"]["instructions"]
        }
        assert decoder.can_decode(program_ids)

    def test_decode_buy(self, load_fixture):
        tx = load_fixture("pumpfun")
        decoder = PumpfunDecoder()
        results = decoder.decode("test_pumpfun_tx", tx)
        assert len(results) == 1
        assert results[0]["type"] == "pumpfun"
        assert results[0]["instruction"] == "Buy"
        assert results[0]["program"] == "Pump.fun"

    def test_format_output(self):
        decoder = PumpfunDecoder()
        lines = decoder.format_output(
            {"type": "pumpfun", "instruction": "Buy", "program": "Pump.fun"}
        )
        assert lines == ["  Pump.fun: Buy"]

    def test_no_match_on_unrelated_tx(self, load_fixture):
        tx = load_fixture("raydium")
        decoder = PumpfunDecoder()
        results = decoder.decode("unrelated", tx)
        assert results == []
