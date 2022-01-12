import pygame
import random

class Particle:
    def __init__(self, pos, vel):
        self.is_alive = True
        self.x, self.y = pos
        self.vx, self.vy = vel
        
    def update(self, width, height, dt, gy):
        self.vy += gy * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.x < 0 or self.x > width or self.y > height:
            self.is_alive = False
            
    def draw(self, screen):
        radius = 10
        pygame.draw.circle(screen, pygame.Color("green"), (self.x, self.y), radius)
    
def main():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    
    dt = 1.0
    gy = 0.5
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
                    p = Particle(event.pos, (vx, vy))
                    particle_list.append(p)
        if should_quit:
            break
        
        for p in particle_list:
            p.update(width, height, dt, gy)
        
        particle_list[:] = {p for p in particle_list if p.is_alive}
        
        screen.fill(pygame.Color("black"))
        for p in particle_list:
            p.draw(screen)
        pygame.display.update()
        
    pygame.quit()
    
if __name__ == "__main__":
    main()