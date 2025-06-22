#!/usr/bin/env python3
"""
CQRS Pattern – Minimal Hands-On Demo
====================================
This interactive toy program illustrates **Command Query Responsibility
Segregation (CQRS)**: writes go through a *command* layer that appends events
into an event-store (the *write model*), while reads query an optimised view
(the *read model*) that is refreshed asynchronously.

Design choices for the demo:
• Pure std-lib (no external DB) – event store is an in-memory list.
• Read-model is a dict rebuilt by a *projector* that you trigger manually to
  mimic eventual consistency lag.
• Domain object: a tiny *BlogPost* with fields `id`, `title`, `content`.

You will be able to:
1. Create / update posts via commands (writes).
2. Read posts from the read-model (queries).
3. Inspect raw events.
4. Sync the read-model to catch up with events – demonstrating the separation.
"""

from __future__ import annotations

import datetime as _dt
import itertools
import sys
from typing import Dict, List

# ──────────────────────────────────────────────────────────────────────────────
# Write model – event store & commands
# ──────────────────────────────────────────────────────────────────────────────

class Event:  # simple value object
    _ids = itertools.count(1)

    def __init__(self, type_: str, payload: dict):
        self.id: int = next(self._ids)
        self.type = type_
        self.payload = payload
        self.ts = _dt.datetime.utcnow()

    def __repr__(self) -> str:  # pretty print for debugging
        return f"<Event {self.id} {self.type} {self.payload} @ {self.ts:%H:%M:%S}>"


event_store: List[Event] = []  # append-only log – the WRITE model


# Command handlers ------------------------------------------------------------

def cmd_create_post(title: str, content: str) -> None:
    event_store.append(Event("PostCreated", {"title": title, "content": content}))
    print("✅  PostCreated event appended (WRITE model)")


def cmd_update_post(post_id: int, content: str) -> None:
    event_store.append(Event("PostUpdated", {"post_id": post_id, "content": content}))
    print("✅  PostUpdated event appended (WRITE model)")


# ──────────────────────────────────────────────────────────────────────────────
# Read model – projection
# ──────────────────────────────────────────────────────────────────────────────

read_model: Dict[int, Dict[str, str]] = {}
last_synced_event_id = 0  # marker so projector knows where to resume


def project_new_events() -> None:
    """Apply *new* events to the read model to simulate projector lag."""
    global last_synced_event_id
    new_events = [e for e in event_store if e.id > last_synced_event_id]
    if not new_events:
        print("🕑  Read-model already up-to-date.")
        return

    for ev in new_events:
        if ev.type == "PostCreated":
            post_id = ev.id  # use event id as synthetic PK
            read_model[post_id] = {
                "id": post_id,
                "title": ev.payload["title"],
                "content": ev.payload["content"],
            }
        elif ev.type == "PostUpdated":
            pid = ev.payload["post_id"]
            if pid in read_model:
                read_model[pid]["content"] = ev.payload["content"]
        last_synced_event_id = ev.id

    print(f"🔄  Projector applied {len(new_events)} event(s). Read-model synced.")


def query_post(post_id: int) -> None:
    post = read_model.get(post_id)
    if post:
        print(f"\n📖  Post {post_id}\nTitle   : {post['title']}\nContent : {post['content']}\n")
    else:
        print("❌  Post not found in READ model (maybe projector lag?).")


# ──────────────────────────────────────────────────────────────────────────────
# CLI boilerplate
# ──────────────────────────────────────────────────────────────────────────────

MENU = """
What would you like to do?
1. Create post (COMMAND)
2. Update post (COMMAND)
3. Query post (QUERY)
4. Sync read-model (Projector)
5. View raw events
6. Exit
"""


def main() -> None:
    print("\n" + "=" * 80)
    print("🔄  CQRS DEMO – COMMAND vs QUERY separation")
    print("=" * 80)

    while True:
        print(MENU)
        choice = input("🔢  Enter choice (1-6): ").strip()

        if choice == "1":
            title = input("Title   : ")
            content = input("Content : ")
            cmd_create_post(title, content)

        elif choice == "2":
            pid = int(input("Post id to update : "))
            new_content = input("New content       : ")
            cmd_update_post(pid, new_content)

        elif choice == "3":
            pid = int(input("Post id to query : "))
            query_post(pid)

        elif choice == "4":
            project_new_events()

        elif choice == "5":
            print("\n🗂️  Raw events (WRITE model):")
            for ev in event_store:
                print(f"  {ev}")
            print()

        elif choice == "6":
            print("\n👋  Exiting CQRS demo – until next command!")
            break

        else:
            print("❌  Invalid choice. Please pick 1-6.")

        input("\n⏎  Press Enter to continue…")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\n👋  Interrupted.") 