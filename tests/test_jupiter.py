"""Tests for the Jupiter decoder using real transaction data.

Fixture tx: 4Vu4wEKpHqdzxHkPYAQ4JyXnkBwyuGBztpg5auJqkntaQuALB1Qn59LbHifq1MMGLmSwsBFDqVwSZJNdpG6isgN9
A Jupiter v6 Route swap that routes through Orca Whirlpool.
"""

from solexplain.decoders.jupiter import JupiterDecoder


class TestJupiterDecoder:
    def test_can_decode(self, load_fixture):
        tx = load_fixture("jupiter")
        decoder = JupiterDecoder()
        program_ids = set()
        for ix in tx["transaction"]["message"]["instructions"]:
            program_ids.add(ix.get("programId", ""))
        assert decoder.can_decode(program_ids)

    def test_decode_route(self, load_fixture):
        tx = load_fixture("jupiter")
        decoder = JupiterDecoder()
        results = decoder.decode(
            "4Vu4wEKpHqdzxHkPYAQ4JyXnkBwyuGBztpg5auJqkntaQuALB1Qn59LbHifq1MMGLmSwsBFDqVwSZJNdpG6isgN9",
            tx,
        )
        assert len(results) == 1
        assert results[0]["type"] == "jupiter_swap"
        assert results[0]["instruction"] == "Route"

    def test_no_match_on_unrelated_tx(self, load_fixture):
        tx = load_fixture("raydium")
        decoder = JupiterDecoder()
        results = decoder.decode("unrelated", tx)
        assert results == []
