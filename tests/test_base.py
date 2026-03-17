"""Tests for the base decoder helper: find_instructions_from_logs."""

from solexplain.decoders.base import BaseDecoder, find_instructions_from_logs


def _make_tx(log_messages):
    return {"meta": {"logMessages": log_messages, "innerInstructions": []}}


class TestFindInstructionsFromLogs:
    def test_single_matching_program(self):
        tx = _make_tx([
            "Program AAA invoke [1]",
            "Instruction: Swap",
            "Program AAA success",
        ])
        assert find_instructions_from_logs(tx, {"AAA"}) == ["Swap"]

    def test_ignores_non_matching_program(self):
        tx = _make_tx([
            "Program BBB invoke [1]",
            "Instruction: Swap",
            "Program BBB success",
        ])
        assert find_instructions_from_logs(tx, {"AAA"}) == []

    def test_multiple_instructions(self):
        tx = _make_tx([
            "Program AAA invoke [1]",
            "Instruction: Route",
            "Program BBB invoke [2]",
            "Instruction: Transfer",
            "Program BBB success",
            "Program AAA success",
        ])
        assert find_instructions_from_logs(tx, {"AAA"}) == ["Route"]
        assert find_instructions_from_logs(tx, {"BBB"}) == ["Transfer"]
        assert find_instructions_from_logs(tx, {"AAA", "BBB"}) == [
            "Route",
            "Transfer",
        ]

    def test_nested_invocations(self):
        tx = _make_tx([
            "Program AAA invoke [1]",
            "Instruction: SharedAccountsRoute",
            "Program BBB invoke [2]",
            "Instruction: Swap",
            "Program BBB success",
            "Program CCC invoke [2]",
            "Instruction: Swap",
            "Program CCC success",
            "Program AAA success",
        ])
        result = find_instructions_from_logs(tx, {"AAA"})
        assert result == ["SharedAccountsRoute"]

    def test_empty_logs(self):
        tx = _make_tx([])
        assert find_instructions_from_logs(tx, {"AAA"}) == []

    def test_none_logs(self):
        tx = {"meta": {"logMessages": None}}
        assert find_instructions_from_logs(tx, {"AAA"}) == []

    def test_missing_meta(self):
        assert find_instructions_from_logs({}, {"AAA"}) == []

    def test_failed_program(self):
        tx = _make_tx([
            "Program AAA invoke [1]",
            "Instruction: Swap",
            "Program AAA failed: custom error",
        ])
        assert find_instructions_from_logs(tx, {"AAA"}) == ["Swap"]


class TestBaseDecoder:
    def test_can_decode_matches(self):
        dec = BaseDecoder()
        dec.program_ids = ["AAA", "BBB"]
        assert dec.can_decode({"AAA", "CCC"}) is True

    def test_can_decode_no_match(self):
        dec = BaseDecoder()
        dec.program_ids = ["AAA"]
        assert dec.can_decode({"BBB"}) is False

    def test_decode_returns_empty(self):
        dec = BaseDecoder()
        assert dec.decode("hash", {}) == []
