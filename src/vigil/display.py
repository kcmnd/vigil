import matplotlib.pyplot as plt

from vigil.models import Observation, Target
from vigil.tracker import Track


def plot_history(
    truth_history: list[list[Target]],
    scans: list[list[Observation]],
    tracks: dict[str, Track],
) -> None:
    for i, history in enumerate(truth_history):
        xs = [target.position.x for target in history]
        ys = [target.position.y for target in history]

        (line,) = plt.plot(
            xs,
            ys,
            marker="*",
            label=history[0].target_id,
        )

        # ring each target's starting point so the direction of travel is clear
        plt.scatter(
            xs[0],
            ys[0],
            s=150,
            facecolors="none",
            edgecolors=line.get_color(),
            linewidths=1.5,
            label="start" if i == 0 else None,
        )

    observation_xs = [observation.position.x for scan in scans for observation in scan]
    observation_ys = [observation.position.y for scan in scans for observation in scan]

    plt.scatter(
        observation_xs,
        observation_ys,
        marker="x",
        color="gray",
        alpha=0.7,
        label="sensor observations",
    )

    # the tracker's estimate of each path: the observations it associated with each track
    for track_id, track in tracks.items():
        xs = [observation.position.x for observation in track.observations]
        ys = [observation.position.y for observation in track.observations]

        (line,) = plt.plot(
            xs,
            ys,
            linestyle="--",
            marker="o",
            markersize=3,
            label=f"track {track_id} ({track.status.value})",
        )

        # label each track point with the scan it came from
        for observation in track.observations:
            plt.annotate(
                f"{observation.observed_at:g}",
                (observation.position.x, observation.position.y),
                xytext=(3, 3),
                textcoords="offset points",
                fontsize=7,
                color=line.get_color(),
            )

    plt.title("Vigil: simulated target paths and tracks")
    plt.xlabel("x position (m)")
    plt.ylabel("y position (m)")
    plt.grid()
    plt.legend()
    plt.axis("equal")
    plt.show()
