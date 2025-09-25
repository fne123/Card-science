"""Interpreter customization hooks.

This module is imported automatically by Python (when present on the import
path) before any user code runs. We take advantage of that behaviour to apply
the ForwardRef compatibility shim required for Python 3.13 + Pydantic v1.

Placing the shim here ensures that *any* import of FastAPI/Pydantic – even if
it happens before our application package is loaded – will see the patched
behaviour, eliminating the `recursive_guard` startup crash.
"""
from __future__ import annotations

import inspect
from typing import ForwardRef

_PATCH_ATTR = "__card_science_forwardref_patched__"


def _patch_forwardref_evaluate() -> None:
    """Backport the legacy ForwardRef._evaluate signature."""

    if getattr(ForwardRef, _PATCH_ATTR, False):
        return

    signature = inspect.signature(ForwardRef._evaluate)
    recursive_guard = signature.parameters.get("recursive_guard")

    needs_patch = (
        recursive_guard is not None
        and recursive_guard.kind is inspect.Parameter.KEYWORD_ONLY
        and recursive_guard.default is inspect._empty
    )

    if not needs_patch:
        setattr(ForwardRef, _PATCH_ATTR, True)
        return

    original = ForwardRef._evaluate

    def _evaluate(self, globalns, localns, *args, **kwargs):
        if "recursive_guard" in kwargs:
            return original(self, globalns, localns, *args, **kwargs)

        type_params = None
        remaining_args = list(args)

        if remaining_args:
            if len(remaining_args) == 1:
                recursive = remaining_args.pop(0)
                return original(
                    self,
                    globalns,
                    localns,
                    None,
                    *remaining_args,
                    recursive_guard=recursive,
                )

            type_params = remaining_args.pop(0)
            recursive = remaining_args.pop(0)
            return original(
                self,
                globalns,
                localns,
                type_params,
                *remaining_args,
                recursive_guard=recursive,
            )

        return original(
            self,
            globalns,
            localns,
            type_params,
            recursive_guard=set(),
        )

    ForwardRef._evaluate = _evaluate  # type: ignore[assignment]
    setattr(ForwardRef, _PATCH_ATTR, True)


_patch_forwardref_evaluate()

