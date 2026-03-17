"""Tests for the Jupiter Lend Earn decoder."""

from solexplain.decoders.jupiter_lend import JupiterLendDecoder


class TestJupiterLendDecoder:
    def test_can_decode(self, load_fixture):
        tx = load_fixture("jupiter_lend")
        decoder = JupiterLendDecoder()
        program_ids = {
            ix.get("programId", "")
            for ix in tx["transaction"]["message"]["instructions"]
        }
        assert decoder.can_decode(program_ids)

    def test_decode_deposit(self, load_fixture):
        """Real tx: 2qvPK698...xLYm — Deposit 21,211 USDT into lending vault."""
        tx = load_fixture("jupiter_lend")
        decoder = JupiterLendDecoder()
        results = decoder.decode(
            "2qvPK698g8xB3DX8iB34hJoo4xgaYrBmAgM3qbpedMXVdAWR54PXiJUxUFBfH19H8hgkMsb4nZVjCaakgEcYxLYm",
            tx,
        )
        assert len(results) == 1
        r = results[0]
        assert r["type"] == "jupiter_lend"
        assert r["action"] == "Deposit"
        assert r["amount"] == "21,211"
        assert r["token"] == "USDT"

    def test_format_output_with_amount(self):
        decoder = JupiterLendDecoder()
        lines = decoder.format_output(
            {
                "type": "jupiter_lend",
                "action": "Deposit",
                "amount": "21,211",
                "token": "USDT",
            }
        )
        assert lines == ["  Jupiter Lend: Deposit 21,211 USDT into lending vault"]

    def test_format_output_without_amount(self):
        decoder = JupiterLendDecoder()
        lines = decoder.format_output(
            {
                "type": "jupiter_lend",
                "action": "Withdraw",
                "amount": None,
                "token": None,
            }
        )
        assert lines == ["  Jupiter Lend: Withdraw"]

    def test_no_match_on_unrelated_tx(self, load_fixture):
        tx = load_fixture("raydium")
        decoder = JupiterLendDecoder()
        results = decoder.decode("unrelated", tx)
        assert results == []
