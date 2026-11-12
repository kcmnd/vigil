import argparse
import random

from vigil.display import plot_history
from vigil.models import Observation, Target, Vec2
from vigil.sensor import scan
from vigil.simulation import step
from vigil.tracker import Tracker

DURATION = 10


def run() -> None:
    print("Starting Vigil…")
    # targets start spread out and pass within 2-3 m of each other near (0, 0) at t=5
    targets = [
        Target("t0", Vec2(-10, -5), Vec2(2, 1)),
        Target("t1", Vec2(5, -3), Vec2(-1, 1)),
        Target("t2", Vec2(-3, 10), Vec2(1, -2)),
    ]
    rng = random.Random(42)
    tracker = Tracker()

    truth_history: dict[str, list[Target]] = {target.target_id: [] for target in targets}
    scans: list[list[Observation]] = []

    for t in range(DURATION + 1):
        for target in targets:  # ground truth for plotting
            truth_history[target.target_id].append(target)

        observations = scan(targets, observed_at=t, rng=rng)
        tracker.update(observations)
        scans.append(observations)

        targets = step(targets)

    plot_history(list(truth_history.values()), scans, tracker.tracks)


def main() -> None:
    parser = argparse.ArgumentParser(prog="vigil")
    commands = parser.add_subparsers(dest="command")

    commands.add_parser("run", help="Run the tracker simulation")

    args = parser.parse_args()

    if args.command == "run":
        run()
    else:
        parser.print_help()
