import random

from vigil.models import Observation, Target, Vec2


def observe(
    target: Target,
    observed_at: int,
    rng: random.Random,
) -> Observation:
    noise_std = 1.0  # metres

    return Observation(
        observed_at=observed_at,
        source="simulated-sensor",
        position=Vec2(
            target.position.x + rng.gauss(0, noise_std),
            target.position.y + rng.gauss(0, noise_std),
        ),
    )


def scan(targets: list[Target], observed_at: int, rng: random.Random) -> list[Observation]:
    """one sensor sweep: a noisy observation of each target"""
    observations = [observe(target, observed_at, rng) for target in targets]
    rng.shuffle(observations)
    return observations
