"""Tests for the Lending decoder using real transaction data.

Fixture tx: ipGoC5WycgpEdG3jrscbTfjkB8vMKbUNkD4FAoFbRs7J9ZbRBZafeHH6zm6uozbken6azmrnFL9QQC6vPJAh3QM
Marginfi LendingAccountStartFlashloan.
"""

from solexplain.decoders.lending import LendingDecoder


class TestLendingDecoder:
    def test_can_decode(self, load_fixture):
        tx = load_fixture("lending_marginfi")
        decoder = LendingDecoder()
        program_ids = set()
        for ix in tx["transaction"]["message"]["instructions"]:
            program_ids.add(ix.get("programId", ""))
        assert decoder.can_decode(program_ids)

    def test_decode_marginfi(self, load_fixture):
        tx = load_fixture("lending_marginfi")
        decoder = LendingDecoder()
        results = decoder.decode(
            "ipGoC5WycgpEdG3jrscbTfjkB8vMKbUNkD4FAoFbRs7J9ZbRBZafeHH6zm6uozbken6azmrnFL9QQC6vPJAh3QM",
            tx,
        )
        assert len(results) >= 1
        result = results[0]
        assert result["type"] == "lending"
        assert result["protocol"] == "Marginfi"
        assert result["action"] == "LendingAccountStartFlashloan"

    def test_no_match_on_unrelated_tx(self, load_fixture):
        tx = load_fixture("jupiter")
        decoder = LendingDecoder()
        results = decoder.decode("unrelated", tx)
        assert results == []
