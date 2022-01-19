import pytest
import particle

@pytest.mark.parametrize("x0, y0, vx0, vy0, expected", [
    (300, 200, 5, 10, True),
    (300, 200, -5, -10, True),
    (599, 200, 5, 10, False),
    (300, 399, 5, 10, False),
    (-1, 399, 5, 10, False),
    (0, 0, 5, 10, True),
    (0, 0, -5, 10, False),
])
def test_particle_liveness_after_move(x0, y0, vx0, vy0, expected):
    width, height = 600, 400
    dt, g = 1, 0.5
    w = particle.World(width, height, dt, g)
    p = particle.Particle((x0, y0), (vx0, vy0), w)
    p.update()
    assert p.is_alive == expected