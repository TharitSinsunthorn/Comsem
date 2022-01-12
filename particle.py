import pygame
import random

class Particle:
    pass

def main():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    
    dt = 1.0
    gy = 0.5
    particle_list = []
    p = Particle()
    p.is_alive_ =  False
    p.x, p.y = 0, 0
    p.vx, p.vy = 0, 0
    particle_is_alive = False
    
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
                    p = Particle()
                    p.is_alive = True
                    p.x, p.y = event.pos
                    p.vx = random.uniform(-10, 10)
                    p.vy = random.uniform(-10, 0)
                    particle_list.append(p)
        if should_quit:
            break
        
        for p in particle_list:
            p.vy += gy * dt
            p.x += p.vx * dt
            p.y += p.vy * dt
            if p.x < 0 or p.x > width or p.y > height:
                p.is_alive = False
        
        particle_list[:] = {p for p in particle_list if p.is_alive}
        
        screen.fill(pygame.Color("black"))
        for p in particle_list:
            radius = 10
            pygame.draw.circle(screen, pygame.Color("green"), (p.x, p.y), radius)
        pygame.display.update()
        
    pygame.quit()
    
if __name__ == "__main__":
    main()