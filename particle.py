import pygame


class World:
    def __init__(self, width, height, dt, gy):
        self.width = width
        self.height = height
        self.dt = dt
        self.gy = gy


class Particle:
    def __init__(self, pos, vel, world, radius=10, color="green"):
        self.is_alive = True
        self.x, self.y = pos
        self.vx, self.vy = vel
        self.world = world
        self.radius = radius
        self.color = pygame.Color(color)

    def update(self):
        self.vy += self.world.gy * self.world.dt
        self.x += self.vx * self.world.dt
        self.y += self.vy * self.world.dt
        if self.x < 0 or self.x > self.world.width or self.y > self.world.height:
            self.is_alive = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)