from typing import Dict

FakeDB = Dict[str, dict]

_db: FakeDB = {}


def get_db() -> FakeDB:
    return _db
