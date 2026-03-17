"""Tests for the Drift decoder."""

from solexplain.decoders.drift import DriftDecoder


class TestDriftDecoder:
    def test_can_decode(self, load_fixture):
        tx = load_fixture("drift")
        decoder = DriftDecoder()
        program_ids = {
            ix.get("programId", "")
            for ix in tx["transaction"]["message"]["instructions"]
        }
        assert decoder.can_decode(program_ids)

    def test_decode_place_and_take(self, load_fixture):
        tx = load_fixture("drift")
        decoder = DriftDecoder()
        results = decoder.decode("test_drift_tx", tx)
        assert len(results) == 1
        assert results[0]["type"] == "drift"
        assert results[0]["instruction"] == "PlaceAndTakePerpOrder"

    def test_format_output(self):
        decoder = DriftDecoder()
        lines = decoder.format_output(
            {"type": "drift", "instruction": "PlaceAndTakePerpOrder"}
        )
        assert lines == ["  Drift: PlaceAndTakePerpOrder"]

    def test_no_match_on_unrelated_tx(self, load_fixture):
        tx = load_fixture("raydium")
        decoder = DriftDecoder()
        results = decoder.decode("unrelated", tx)
        assert results == []
