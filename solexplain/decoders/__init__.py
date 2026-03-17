"""Auto-discover all BaseDecoder subclasses in this package."""

import importlib
import inspect
import pkgutil
import warnings

from .base import BaseDecoder

decoders: list[BaseDecoder] = []

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
            decoders.append(cls())

__all__ = ["BaseDecoder", "decoders"]
