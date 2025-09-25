"""Runtime compatibility helpers for Python version differences."""
from __future__ import annotations

import inspect
from typing import ForwardRef

_PATCH_ATTR = "__card_science_forwardref_patched__"


def ensure_forwardref_recursive_guard_default() -> None:
    """Monkey patch typing.ForwardRef for Python 3.13 compatibility.

    Python 3.13 introduced a required ``recursive_guard`` keyword-only argument on
    :meth:`typing.ForwardRef._evaluate`. Pydantic v1 still invokes this private
    method using the older positional signature which leads to ``TypeError``
    during application startup. The shim below restores the previous calling
    convention by injecting a wrapper that accepts positional arguments and
    forwards them with an explicit ``recursive_guard`` default.
    """

    current = getattr(ForwardRef, _PATCH_ATTR, False)
    if current:
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


__all__ = ["ensure_forwardref_recursive_guard_default"]
