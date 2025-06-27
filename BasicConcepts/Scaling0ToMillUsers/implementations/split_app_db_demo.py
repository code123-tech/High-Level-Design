"""
Simple demo showing an application layer separated from a (very) lightweight
persistence layer.  The goal is to illustrate the _concept_ of keeping your
business logic (services / handlers) separate from data‐access concerns so
that each can be scaled or swapped independently.

Run the file:
    python split_app_db_demo.py

Expected output:
    Creating user 'alice'  … done.
    Current users in DB: ['alice']

Of course in real life the *Database* class would be a proper repository that
speaks to Postgres / MySQL / DynamoDB etc. and the *UserService* could be an
HTTP endpoint (FastAPI / Flask / Django).  This file keeps everything in-proc
so you can focus on the split.
"""
from __future__ import annotations


class InMemoryDatabase:
    """A toy replacement for a real database – keeps everything in memory."""

    def __init__(self) -> None:
        self._users: list[str] = []

    # — CRUD operations ---------------------------------------------------
    def add_user(self, username: str) -> None:
        if username in self._users:
            raise ValueError(f"user '{username}' already exists")
        self._users.append(username)

    def list_users(self) -> list[str]:
        return list(self._users)


class UserService:
    """Application layer that *depends* on a data-access layer (the DB)."""

    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    # Public API ----------------------------------------------------------
    def signup(self, username: str) -> None:
        print(f"Creating user '{username}'  …", end=" ")
        self._db.add_user(username)
        print("done.")

    def list_users(self) -> list[str]:
        return self._db.list_users()


# ————————————————————————————————————————————————————————————————————
# Demo / manual test harness
# ————————————————————————————————————————————————————————————————————

def main() -> None:
    # Infrastructure layer – could be a connection pool in production.
    db = InMemoryDatabase()

    # Application/service layer – could be an HTTP handler in production.
    user_service = UserService(db)

    # Business flow -------------------------------------------------------
    user_service.signup("alice")
    print("Current users in DB:", user_service.list_users())


if __name__ == "__main__":
    main() 