import pygame
import random
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
        self.radius= radius
        self.color = pygame.Color(color)
        
    def update(self):
        self.vy += self.world.gy * self.world.dt
        self.x += self.vx * self.world.dt
        self.y += self.vy * self.world.dt
        if self.x < 0 or self.x > self.world.width or self.y > self.world.height:
            self.is_alive = False
            
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
class AppMain:
    def __init__(self):
        pygame.init()
        width, height = 600, 400
        self.screen = pygame.display.set_mode((width, height))
        self.world = World(width, height, dt=1.0, gy=0.5)
        self.particle_list = []
    def update(self):
        for p in self.particle_list:
            p.update()
        self.particle_list[:] = [p for p in self.particle_list if p.is_alive]
    def draw(self):
        self.screen.fill(pygame.Color("black"))
        for p in self.particle_list:
            p.draw(self.screen)
        pygame.display.update()

    def add_particle(self, pos, v, button):
        if button == 1:
            vx = v[0]
            vy = v[1]
            rr = random.uniform(5,15)
            color_list = ["red", "green", "blue"]
            p = Particle(pos, (vx, vy), self.world, radius=rr, color = random.choice(color_list))
            self.particle_list.append(p)
            
    def add_multiple_particles(self, pos, button):
        if button == 3:
            for _ in range(random.randint(2,5)):
                vx = random.uniform(-10, 10)
                vy = random.uniform(-10, 0)
                rr = random.uniform(5,15)
                color_list = ["red", "green", "blue"]
                p = Particle(pos, (vx, vy), self.world, radius=rr, color = random.choice(color_list))
                self.particle_list.append(p)
            
    def run(self):
        clock = pygame.time.Clock()
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
                    x,y = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.add_particle(event.pos, (-(event.pos[0]-x)/5, -(event.pos[1]-y)/5), event.button)
                    self.add_multiple_particles(event.pos, event.button)
            if should_quit:
                break
            self.update()
            self.draw()
        pygame.quit()
if __name__ == "__main__":
    app = AppMain()
    app.run()