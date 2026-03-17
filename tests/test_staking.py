"""Tests for the Staking decoder using real transaction data.

Native stake fixture: bw4RTvFqz9tBG5nHkcVoRjmW3fxCydYPEbhHs4QRSEQLrAWUXcLNBjN8wyVZKwmfhy3eBTcUKBtn9CiHR9yn9nv
  Initialize + DelegateStake with stake account 7BAQFMppAZPEKgCK2x62QJvfriXc1g8Yza11ErffRRwB

Marinade fixture: 2UvCpfCLi7KJ5C7mfKzqo1gHXTWiWpyvGXMeyo8eANiwKFPjA7xkxpa5vUPHhcSNa8PXuFVHyV9nnWS1RbTbdeZH
  Marinade Finance Deposit
"""

from solexplain.decoders.staking import StakingDecoder


class TestStakingDecoderNative:
    def test_can_decode(self, load_fixture):
        tx = load_fixture("staking_native")
        decoder = StakingDecoder()
        program_ids = set()
        for ix in tx["transaction"]["message"]["instructions"]:
            program_ids.add(ix.get("programId", ""))
        assert decoder.can_decode(program_ids)

    def test_decode_native_stake(self, load_fixture):
        tx = load_fixture("staking_native")
        decoder = StakingDecoder()
        results = decoder.decode(
            "bw4RTvFqz9tBG5nHkcVoRjmW3fxCydYPEbhHs4QRSEQLrAWUXcLNBjN8wyVZKwmfhy3eBTcUKBtn9CiHR9yn9nv",
            tx,
        )
        assert len(results) == 2

        init = results[0]
        assert init["type"] == "stake"
        assert init["protocol"] == "Native Stake"
        assert init["action"] == "initialize"
        assert init["stake_account"] == "7BAQFMppAZPEKgCK2x62QJvfriXc1g8Yza11ErffRRwB"

        delegate = results[1]
        assert delegate["type"] == "stake"
        assert delegate["protocol"] == "Native Stake"
        assert delegate["action"] == "delegate"
        assert (
            delegate["stake_account"] == "7BAQFMppAZPEKgCK2x62QJvfriXc1g8Yza11ErffRRwB"
        )


class TestStakingDecoderMarinade:
    def test_can_decode(self, load_fixture):
        tx = load_fixture("staking_marinade")
        decoder = StakingDecoder()
        program_ids = set()
        for ix in tx["transaction"]["message"]["instructions"]:
            program_ids.add(ix.get("programId", ""))
        assert decoder.can_decode(program_ids)

    def test_decode_marinade_deposit(self, load_fixture):
        tx = load_fixture("staking_marinade")
        decoder = StakingDecoder()
        results = decoder.decode(
            "2UvCpfCLi7KJ5C7mfKzqo1gHXTWiWpyvGXMeyo8eANiwKFPjA7xkxpa5vUPHhcSNa8PXuFVHyV9nnWS1RbTbdeZH",
            tx,
        )
        assert len(results) >= 1
        deposit = results[0]
        assert deposit["type"] == "stake"
        assert deposit["protocol"] == "Marinade Finance"
        assert deposit["action"] == "Deposit"

    def test_no_match_on_unrelated_tx(self, load_fixture):
        tx = load_fixture("raydium")
        decoder = StakingDecoder()
        results = decoder.decode("unrelated", tx)
        assert results == []
