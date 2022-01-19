import pygame


class World:
    def __init__(self, width, height, dt, gy):
        self.width = width
        self.height = height
        self.dt = dt
        self.gravity_acc = pygame.math.Vector2(0, gy)


class Particle:
    def __init__(self, pos, vel, world, radius=10, color="green"):
        self.is_alive = True
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(vel)
        self.world = world
        self.radius = radius
        self.color = pygame.Color(color)

    def update(self):
        self.vel += self.world.gravity_acc * self.world.dt
        self.pos += self.vel * self.world.dt
        self.update_after_move()
            
    def update_after_move(self):
        if self.x < 0 or self.x > self.world.width or self.y > self.world.height:
            self.is_alive = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        
    @property
    def x(self):
        return self.pos.x
    
    @property
    def y(self):
        return self.pos.y
    
class ConfinedParticle(Particle):
    def update_after_move(self):
        e = 0.95
        if self.pos.x < 0 + self.radius or self.pos.x > self.world.width - self.radius:
            self.vel.x *= -e
        if self.pos.y > self.world.height - self.radius:
            self.vel.y *= -e