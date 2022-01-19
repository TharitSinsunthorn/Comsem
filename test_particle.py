import pytest
import particle

@pytest.mark.parametrize("x0, y0, vx0, vy0", [
    (0, 0, 5, 10),
    (300, 200, -7, 12),
    (500, 300, -4, -10),
])
def test_particle_move(x0, y0, vx0, vy0):
    width, height = 600, 400
    dt, g = 2, 4
    w = particle.World(width, height, dt, g)

    p = particle.Particle((x0, y0), (vx0, vy0), w)
    p.update()
    assert p.x == x0 + vx0 * dt
    assert p.y == y0 + (vy0 + g * dt) * dt
    p.update()
    assert p.x == x0 + 2 * vx0 * dt
    assert p.y == y0 + (vy0 + g * dt) * dt + (vy0 + 2 * g * dt) * dt