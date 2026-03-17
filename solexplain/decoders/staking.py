"""Staking decoder — native stake + liquid staking (Marinade, Jito)."""

from .base import BaseDecoder, find_instructions_from_logs

NATIVE_STAKE_PID = "Stake11111111111111111111111111111111111111"

LIQUID_STAKING_PROGRAMS = {
    "MarBmsSgKXdrN1egZf5sqe1TMai9K1rChYNDJgjq7aD": "Marinade Finance",
    "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn": "Jito Staking",
    "jitoVjT9jRUyeXmi8dEfEXBCacqnphn41Rkjwkm7FJq": "Jito Tip Router",
}


class StakingDecoder(BaseDecoder):
    name = "Staking"
    program_ids = [NATIVE_STAKE_PID] + list(LIQUID_STAKING_PROGRAMS.keys())

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        results = []
        results.extend(self._decode_native_stake(tx_data))
        results.extend(self._decode_liquid_staking(tx_data))
        return results

    def _decode_native_stake(self, tx_data: dict) -> list[dict]:
        """Parse native stake instructions from jsonParsed data."""
        results = []
        all_instructions = self._collect_instructions(tx_data)

        for ix in all_instructions:
            if ix.get("programId") != NATIVE_STAKE_PID:
                continue
            parsed = ix.get("parsed")
            if not isinstance(parsed, dict):
                continue
            action = parsed.get("type", "")
            if not action:
                continue
            info = parsed.get("info", {})
            result = {
                "type": "stake",
                "protocol": "Native Stake",
                "action": action,
            }
            stake_account = info.get("stakeAccount", "")
            if stake_account:
                result["stake_account"] = stake_account
            results.append(result)

        return results

    def _decode_liquid_staking(self, tx_data: dict) -> list[dict]:
        """Parse liquid staking instructions from log messages."""
        results = []
        for pid, protocol in LIQUID_STAKING_PROGRAMS.items():
            instructions = find_instructions_from_logs(tx_data, {pid})
            for ix in instructions:
                results.append(
                    {
                        "type": "stake",
                        "protocol": protocol,
                        "action": ix,
                    }
                )
        return results

    @staticmethod
    def _collect_instructions(tx_data: dict) -> list[dict]:
        """Collect all instructions (top-level + inner) from the transaction."""
        instructions = []
        message = tx_data.get("transaction", {}).get("message", {})
        instructions.extend(message.get("instructions", []))
        for inner in tx_data.get("meta", {}).get("innerInstructions", []) or []:
            instructions.extend(inner.get("instructions", []))
        return instructions
