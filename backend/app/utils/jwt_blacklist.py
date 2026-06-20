from datetime import datetime

# in-memory store (replace with Redis in production)
BLACKLIST = set()


def blacklist_token(jti: str):
    BLACKLIST.add(jti)


def is_token_revoked(jti: str) -> bool:
    return jti in BLACKLIST