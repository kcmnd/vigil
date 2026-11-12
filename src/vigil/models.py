from dataclasses import dataclass


@dataclass
class Vec2:
    x: float
    y: float


@dataclass
class Target:
    """Ground truth for one simulated object. Only the simulator and sensors see it, never the tracker.

    Subclass this for specific kinds of objects (e.g. `Aircraft`, `Vessel`) once they need their own
    fields or behaviour.
    """

    target_id: str
    position: Vec2
    velocity: Vec2


@dataclass
class Observation:
    observed_at: float
    source: str
    position: Vec2
