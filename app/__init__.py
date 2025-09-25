from .utils.compat import ensure_forwardref_recursive_guard_default

ensure_forwardref_recursive_guard_default()

from .main import app

__all__ = ["app"]
