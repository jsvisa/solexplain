"""Tests for the Jupiter Products decoder (DCA, Limit, Perps)."""

from solexplain.decoders.jupiter_products import JupiterProductsDecoder


class TestJupiterProductsDecoder:
    def test_can_decode_dca(self, load_fixture):
        tx = load_fixture("jupiter_dca")
        decoder = JupiterProductsDecoder()
        program_ids = {
            ix.get("programId", "")
            for ix in tx["transaction"]["message"]["instructions"]
        }
        assert decoder.can_decode(program_ids)

    def test_decode_dca_open(self, load_fixture):
        tx = load_fixture("jupiter_dca")
        decoder = JupiterProductsDecoder()
        results = decoder.decode("test_dca_tx", tx)
        assert len(results) == 1
        assert results[0]["type"] == "jupiter_dca"
        assert results[0]["instruction"] == "OpenDca"
        assert results[0]["program"] == "Jupiter DCA"

    def test_decode_limit_create_order(self, load_fixture):
        tx = load_fixture("jupiter_limit")
        decoder = JupiterProductsDecoder()
        results = decoder.decode("test_limit_tx", tx)
        assert len(results) == 1
        assert results[0]["type"] == "jupiter_limit"
        assert results[0]["instruction"] == "CreateOrder"
        assert results[0]["program"] == "Jupiter Limit"

    def test_decode_perps_open_position(self, load_fixture):
        tx = load_fixture("jupiter_perps")
        decoder = JupiterProductsDecoder()
        results = decoder.decode("test_perps_tx", tx)
        assert len(results) == 1
        assert results[0]["type"] == "jupiter_perps"
        assert results[0]["instruction"] == "OpenPosition"
        assert results[0]["program"] == "Jupiter Perps"

    def test_format_output_dca(self):
        decoder = JupiterProductsDecoder()
        lines = decoder.format_output(
            {"type": "jupiter_dca", "instruction": "OpenDca", "program": "Jupiter DCA"}
        )
        assert lines == ["  Jupiter DCA: OpenDca"]

    def test_format_output_limit(self):
        decoder = JupiterProductsDecoder()
        lines = decoder.format_output(
            {
                "type": "jupiter_limit",
                "instruction": "CreateOrder",
                "program": "Jupiter Limit",
            }
        )
        assert lines == ["  Jupiter Limit: CreateOrder"]

    def test_format_output_perps(self):
        decoder = JupiterProductsDecoder()
        lines = decoder.format_output(
            {
                "type": "jupiter_perps",
                "instruction": "OpenPosition",
                "program": "Jupiter Perps",
            }
        )
        assert lines == ["  Jupiter Perps: OpenPosition"]

    def test_decode_dca_v1_real_tx(self, load_fixture):
        """Real tx: 2qvPK698...xLYm — Jupiter DCA v1 Deposit + Operator."""
        tx = load_fixture("jupiter_dca_v1")
        decoder = JupiterProductsDecoder()
        program_ids = {
            ix.get("programId", "")
            for ix in tx["transaction"]["message"]["instructions"]
        }
        assert decoder.can_decode(program_ids)
        results = decoder.decode(
            "2qvPK698g8xB3DX8iB34hJoo4xgaYrBmAgM3qbpedMXVdAWR54PXiJUxUFBfH19H8hgkMsb4nZVjCaakgEcYxLYm",
            tx,
        )
        assert len(results) >= 1
        types = {r["type"] for r in results}
        assert "jupiter_dca" in types
        # Should find Deposit from DCA v1
        instructions = [r["instruction"] for r in results]
        assert "Deposit" in instructions

    def test_no_match_on_unrelated_tx(self, load_fixture):
        tx = load_fixture("raydium")
        decoder = JupiterProductsDecoder()
        results = decoder.decode("unrelated", tx)
        assert results == []
