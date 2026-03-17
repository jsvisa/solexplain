"""Tests for CLI formatting of new decoder types."""

from solexplain.cli import format_explanation
from solexplain.explainer import TxExplanation


class TestFormatExplanation:
    def _make_explanation(self, decoder_outputs):
        return TxExplanation(
            tx_hash="test_hash",
            block_time=None,
            status="success",
            fee_lamports=5000,
            decoder_outputs=decoder_outputs,
        )

    def test_format_jupiter(self):
        exp = self._make_explanation(
            [
                {"type": "jupiter_swap", "instruction": "SharedAccountsRoute"},
            ]
        )
        output = format_explanation(exp)
        assert "Jupiter: SharedAccountsRoute swap" in output

    def test_format_raydium(self):
        exp = self._make_explanation(
            [
                {"type": "raydium", "instruction": "SwapV2", "program": "Raydium CLMM"},
            ]
        )
        output = format_explanation(exp)
        assert "Raydium CLMM: SwapV2" in output

    def test_format_meteora(self):
        exp = self._make_explanation(
            [
                {"type": "meteora", "instruction": "Swap", "program": "Meteora DLMM"},
            ]
        )
        output = format_explanation(exp)
        assert "Meteora DLMM: Swap" in output

    def test_format_orca(self):
        exp = self._make_explanation(
            [
                {"type": "orca", "instruction": "Swap"},
            ]
        )
        output = format_explanation(exp)
        assert "Orca Whirlpool: Swap" in output

    def test_format_native_stake(self):
        exp = self._make_explanation(
            [
                {
                    "type": "stake",
                    "protocol": "Native Stake",
                    "action": "delegate",
                    "stake_account": "7BAQFMppAZPEKgCK2x62QJvfriXc1g8Yza11ErffRRwB",
                },
            ]
        )
        output = format_explanation(exp)
        assert "Native Stake: delegate" in output
        assert "stake account:" in output
        assert "7BAQFMpp" in output

    def test_format_marinade(self):
        exp = self._make_explanation(
            [
                {"type": "stake", "protocol": "Marinade Finance", "action": "Deposit"},
            ]
        )
        output = format_explanation(exp)
        assert "Marinade Finance: Deposit" in output

    def test_format_lending(self):
        exp = self._make_explanation(
            [
                {"type": "lending", "protocol": "Marginfi", "action": "Deposit"},
            ]
        )
        output = format_explanation(exp)
        assert "Marginfi: Deposit" in output

    def test_format_unknown_type_fallback(self):
        exp = self._make_explanation(
            [
                {"type": "some_new_thing", "foo": "bar"},
            ]
        )
        output = format_explanation(exp)
        assert "foo: bar" in output
