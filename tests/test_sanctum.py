"""Tests for the Sanctum decoder."""

from solexplain.decoders.sanctum import SanctumDecoder


class TestSanctumDecoder:
    def test_can_decode(self, load_fixture):
        tx = load_fixture("sanctum")
        decoder = SanctumDecoder()
        program_ids = {
            ix.get("programId", "")
            for ix in tx["transaction"]["message"]["instructions"]
        }
        assert decoder.can_decode(program_ids)

    def test_decode_swap_via_stake(self, load_fixture):
        tx = load_fixture("sanctum")
        decoder = SanctumDecoder()
        results = decoder.decode("test_sanctum_tx", tx)
        assert len(results) == 1
        assert results[0]["type"] == "sanctum"
        assert results[0]["instruction"] == "SwapViaStake"
        assert results[0]["program"] == "Sanctum Router"

    def test_format_output(self):
        decoder = SanctumDecoder()
        lines = decoder.format_output(
            {
                "type": "sanctum",
                "instruction": "SwapViaStake",
                "program": "Sanctum Router",
            }
        )
        assert lines == ["  Sanctum Router: SwapViaStake"]

    def test_no_match_on_unrelated_tx(self, load_fixture):
        tx = load_fixture("raydium")
        decoder = SanctumDecoder()
        results = decoder.decode("unrelated", tx)
        assert results == []
