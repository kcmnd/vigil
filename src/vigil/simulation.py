from vigil.models import Target, Vec2


def step(targets: list[Target]) -> list[Target]:
    """advance every target by one tick (1 s)"""
    return [
        Target(
            target_id=target.target_id,
            position=Vec2(
                target.position.x + target.velocity.x,
                target.position.y + target.velocity.y,
            ),
            velocity=Vec2(target.velocity.x, target.velocity.y),
        )
        for target in targets
    ]
