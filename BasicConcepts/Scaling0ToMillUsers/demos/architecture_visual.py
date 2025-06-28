import shutil
from pathlib import Path
import time

# lightweight imports for simulation
# we guard them in functions to avoid hard dependency if user only wants diagram

def main() -> None:
    print("Choose a demo:")
    print("1) Show architecture diagram only")
    print("2) Walk me through a single request flow")
    print("3) Simulate one write + read cycle using demo components")

    choice = input("Enter 1/2/3 (default 1): ").strip() or "1"

    if choice == "1":
        if shutil.which("dot"):
            try:
                import graphviz  # noqa: F401
                build_graphviz()
            except ImportError:
                print("graphviz Python package missing – ASCII fallback\n")
                print_ascii()
        else:
            print_ascii()

    elif choice == "2":
        _walk_through_flow()

    elif choice == "3":
        _simulate_cycle()
    else:
        print("Invalid choice, exiting.")


# ------------------------------------------------------------------
# Option-2 helper
# ------------------------------------------------------------------


def _walk_through_flow() -> None:
    steps = [
        "Client issues HTTP POST /signup",
        "Load Balancer selects App-Srv-2 (round-robin)",
        "App-Srv-2 writes new user to Primary DB",
        "Primary DB replicates change to Replica-1 & Replica-2",
        "Subsequent GET /user/123 read is served from Replica-1",
    ]
    print("\n▶ Request flow:")
    for idx, line in enumerate(steps, 1):
        print(f" {idx}. {line}")


# ------------------------------------------------------------------
# Option-3 helper (mini simulation)
# ------------------------------------------------------------------


def _simulate_cycle() -> None:
    print("\nRunning mini in-memory simulation …\n")
    try:
        from CursorLearning.High_Level_Design.BasicConcepts.Scaling0ToMillUsers.implementations.db_replication_demo import (
            PrimaryDB,
            ReplicaDB,
            DatabaseRouter,
        )
    except ImportError:
        # dynamic load based on file path so script works when run directly
        import importlib.machinery as _mach
        import importlib.util as _util

        impl_path = (
            Path(__file__)  # current file
            .resolve()
            .parent.parent  # go to demos/
            / "implementations" / "db_replication_demo.py"
        )

        loader = _mach.SourceFileLoader("_db_rep_demo", str(impl_path))
        spec = _util.spec_from_loader(loader.name, loader)
        module = _util.module_from_spec(spec)  # type: ignore[arg-type]
        loader.exec_module(module)  # type: ignore[arg-type]

        PrimaryDB = module.PrimaryDB  # type: ignore[attr-defined]
        ReplicaDB = module.ReplicaDB  # type: ignore[attr-defined]
        DatabaseRouter = module.DatabaseRouter  # type: ignore[attr-defined]

    primary = PrimaryDB()
    replicas = [ReplicaDB("replica-1"), ReplicaDB("replica-2")]
    for r in replicas:
        primary.attach_replica(r)
    router = DatabaseRouter(primary, replicas)

    print("WRITE → primary: user:42 = bob")
    router.write("user:42", "bob")

    print("Immediate READ ← replica (may be None):")
    router.read("user:42")

    time.sleep(ReplicaDB.REPLICATION_DELAY_SEC * 2)
    print("READ after replication delay:")
    router.read("user:42")

    print("\nMini-simulation done.\n")


# ------------------------------------------------------------------
# Diagram helpers (used when user chooses option 1)
# ------------------------------------------------------------------


def build_graphviz() -> None:
    """Render architecture.png using Graphviz if available."""
    from graphviz import Digraph

    g = Digraph("scale_path", format="png")
    g.attr(rankdir="TB", bgcolor="white")

    g.node("C", "Client / Browser", shape="ellipse", style="filled", fillcolor="#cfe2ff")
    g.node("LB", "Load Balancer", shape="box", style="filled", fillcolor="#d1e7dd")
    g.edge("C", "LB")

    for idx in (1, 2):
        g.node(f"APP{idx}", f"App-Srv-{idx}", shape="box", style="filled", fillcolor="#fff3cd")
        g.edge("LB", f"APP{idx}")

    g.node("DBP", "Primary DB", shape="cylinder", style="filled", fillcolor="#f8d7da")
    g.node("DBR1", "Replica-1", shape="cylinder")
    g.node("DBR2", "Replica-2", shape="cylinder")

    g.edge("APP1", "DBP")
    g.edge("APP2", "DBP")
    g.edge("DBP", "DBR1", style="dashed")
    g.edge("DBP", "DBR2", style="dashed")

    out_path = Path(__file__).with_suffix(".png")
    g.render(out_path.stem, directory=out_path.parent, cleanup=True)
    print(f"✅ Diagram written to {out_path}\n")


ASCII_ART = r"""
          ┌───────────────┐
          │   Client      │
          └──────┬────────┘
                 │
          ┌──────▼───────┐
          │ Load Balancer│
          └┬─────┬───────┘
           │     │
    ┌──────▼───┐ └───────▼────┐
    │App-Srv-1 │   │App-Srv-2 │
    └──────┬────┘   └────┬─────┘
           │  writes/reads │
           ▼               ▼
        ┌─────────────┐     ┃ (same)
        │  Primary DB │─────┘
        └──┬──────────┬┘
           │          │  replication
     ┌─────▼───┐ ┌───▼─────┐
     │Replica-1│ │Replica-2│
     └─────────┘ └─────────┘
"""


def print_ascii() -> None:
    print(ASCII_ART)


if __name__ == "__main__":
    main()