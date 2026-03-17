"""Base class for protocol-specific transaction decoders."""


class BaseDecoder:
    """Subclass this to add protocol-specific enrichment."""

    program_ids: list[str] = []
    name: str = ""

    def can_decode(self, tx_programs: set[str]) -> bool:
        """Return True if this decoder is relevant to the transaction."""
        return bool(set(self.program_ids) & tx_programs)

    def decode(self, tx_hash: str, tx_data: dict) -> list[dict]:
        """Return extra enrichment dicts for this protocol.

        Each dict should have at least a 'type' key describing the enrichment.
        """
        return []
