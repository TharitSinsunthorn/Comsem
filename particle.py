import pygame
import random

class World:
    def __init__(self, width, height, dt, gy):
        self.width = width
        self.height = height
        self.dt = dt
        self.gy = gy

class Particle:
    def __init__(self, pos, vel, world):
        self.is_alive = True
        self.x, self.y = pos
        self.vx, self.vy = vel
        self.world = world
        
    def update(self):
        self.vy += self.world.gy * self.world.dt
        self.x += self.vx * self.world.dt
        self.y += self.vy * self.world.dt
        if self.x < 0 or self.x > self.world.width or self.y > self.world.height:
            self.is_alive = False
            
    def draw(self, screen):
        radius = 10
        pygame.draw.circle(screen, pygame.Color("green"), (self.x, self.y), radius)
    
def main():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    
    world = World(width, height, dt=1.0, gy=0.5)
    particle_list = []
    
    while True:
        frames_per_second = 60
        clock.tick(frames_per_second)
        
        should_quit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    should_quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    
                    vx = random.uniform(-10, 10)
                    vy = random.uniform(-10, 0)
                    p = Particle(event.pos, (vx, vy), world)
                    particle_list.append(p)
        if should_quit:
            break
        
        for p in particle_list:
            p.update()
        
        particle_list[:] = {p for p in particle_list if p.is_alive}
        
        screen.fill(pygame.Color("black"))
        for p in particle_list:
            p.draw(screen)
        pygame.display.update()
        
    pygame.quit()
    
if __name__ == "__main__":
    main()