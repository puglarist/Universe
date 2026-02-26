from __future__ import annotations

from functools import wraps


def require_admin(func):
    @wraps(func)
    def wrapper(self, actor, *args, **kwargs):
        if not actor.is_admin:
            raise PermissionError("Admin role required")
        return func(self, actor, *args, **kwargs)

    return wrapper
