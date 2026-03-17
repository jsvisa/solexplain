"""Auto-discover all BaseDecoder subclasses in this package."""

import importlib
import inspect
import pkgutil
import warnings

from .base import BaseDecoder

decoders: list[BaseDecoder] = []
_type_to_decoder: dict[str, BaseDecoder] = {}
_fallback = BaseDecoder()

for _, modname, is_pkg in pkgutil.walk_packages(__path__, prefix=__name__ + "."):
    if is_pkg:
        continue
    try:
        module = importlib.import_module(modname)
    except ImportError as exc:
        warnings.warn(f"Skip decoder {modname}: {exc}")
        continue
    for _, cls in inspect.getmembers(module, inspect.isclass):
        if issubclass(cls, BaseDecoder) and cls is not BaseDecoder:
            instance = cls()
            decoders.append(instance)
            for t in instance.output_types:
                _type_to_decoder[t] = instance


def format_decoder_output(d: dict) -> list[str]:
    """Format a decoder output dict by dispatching to the owning decoder."""
    decoder = _type_to_decoder.get(d.get("type", ""), _fallback)
    return decoder.format_output(d)


__all__ = ["BaseDecoder", "decoders", "format_decoder_output"]
