import random
from math import cos, sin, sqrt, pi
import pygame
import mspringmass as spm

# random obstacles
# orbit obs

class ActorFactory:
    def __init__(self, world, actor_list):
        self.world = world
        self.actor_list = actor_list
        self.obs_list = []

    def create_obstacle(self):
        # radius = 20
        # viscous = 0.01
        # restitution = 0.95
        RED = (188, 39, 50)
        GREEN = (61, 199, 112)
        WHITE = (255, 255, 255)
        self.obs_list.append(spm.FixedPointMass((0,0),  self.world, 60, 0.01,
                              1.5, spm.CircleDrawer(color = WHITE, width=0)))
        self.obs_list.append(spm.FixedPointMass((600,0),  self.world, 60, 0.01,
                              1.5, spm.CircleDrawer(color = WHITE, width=0)))
        self.obs_list.append(spm.FixedPointMass((0,700),  self.world, 40, 0.01,
                              1.5, spm.CircleDrawer(color = WHITE, width=0)))
        self.obs_list.append(spm.FixedPointMass((600,700),  self.world, 40, 0.01,
                              1.5, spm.CircleDrawer(color = WHITE, width=0)))
        
        self.obs_list.append(spm.FixedPointMass((100,100),  self.world, 20, 0.01,
                              0.95, spm.CircleDrawer(color = RED, width=0)))
        self.obs_list.append(spm.FixedPointMass((200,100),  self.world, 20, 0.01,
                              0.95, spm.CircleDrawer(color = RED, width=0)))
        self.obs_list.append(spm.FixedPointMass((300,100),  self.world, 20, 0.01,
                              0.95, spm.CircleDrawer(color = RED, width=0)))
        self.obs_list.append(spm.FixedPointMass((400,100),  self.world, 20, 0.01,
                              0.95, spm.CircleDrawer(color = RED, width=0)))
        self.obs_list.append(spm.FixedPointMass((500,100),  self.world, 20, 0.01,
                              0.95, spm.CircleDrawer(color = RED, width=0)))
        
        self.obs_list.append(spm.FixedPointMass((300,220),  self.world, 50, 0.01,
                              0.5, spm.CircleDrawer(color = GREEN, width=0)))
        
        self.obs_list.append(spm.FixedPointMass((100,300),  self.world, 20, 0.01,
                              0.95, spm.CircleDrawer(color = RED, width=0)))
        self.obs_list.append(spm.FixedPointMass((200,400),  self.world, 20, 0.01,
                              0.95, spm.CircleDrawer(color = RED, width=0)))
        self.obs_list.append(spm.FixedPointMass((300,350),  self.world, 20, 0.01,
                              0.95, spm.CircleDrawer(color = RED, width=0)))
        self.obs_list.append(spm.FixedPointMass((400,400),  self.world, 20, 0.01,
                              0.95, spm.CircleDrawer(color = RED, width=0)))
        self.obs_list.append(spm.FixedPointMass((500,300),  self.world, 20, 0.01,
                              0.95, spm.CircleDrawer(color = RED, width=0)))
        
        return self.obs_list
        
    def create_point_mass(self, pos, vel):
        # vel = (random.uniform(-10, 10), random.uniform(-10, 0))
        mass = 10
        radius = 10
        viscous = 0.01
        restitution = 0.95 
        # if fixed:
        #     color = "gray"
        #     return spm.FixedPointMass(pos,  self.world, radius, viscous,
        #                       restitution, spm.CircleDrawer(color, width=0))
        # else:
        color = "green"
        return spm.PointMass(pos, vel, self.world, radius, mass, viscous,
                             restitution, spm.CircleDrawer(color, width=0))

    # def create_spring(self, p1, p2):
    #     spring_const = 0.01
    #     natural_len = 20
    #     return spm.Spring(p1, p2, self.world, spring_const, natural_len,
    #                       spm.LineDrawer("white", width=2))
        
    def create_collision_resolver(self):
        return spm.countedCollisionResolver(self.world, self.actor_list)

    def create_boundary(self, name):
        width, height = self.world.size
        geometry = {"top": ((0, -1), (0, 0)),
                    "bottom": ((0, 1), (0, height)),
                    "left": ((-1, 0), (0, 0)),
                    "right": ((1, 0), (width, 0))}
        normal, point_included = geometry[name]
        return spm.Boundary(normal, point_included, self.world, self.actor_list)
    
    
class AppMain:
    def __init__(self):
        pygame.init()
        width, height = 600, 700
        pygame.display.set_caption("Charlee Charlee")
        self.screen = pygame.display.set_mode((width, height))

        self.world = spm.World((width, height), dt=1.0, gravity_acc=(0, 0.1))
        self.actor_list = []
        self.factory = ActorFactory(self.world, self.actor_list)
        
        for i in range(len(self.factory.create_obstacle())):
            self.actor_list.append(self.factory.create_obstacle()[i])

        self.actor_list.append(self.factory.create_collision_resolver())
        self.actor_list.append(self.factory.create_boundary("top"))
        # self.actor_list.append(self.factory.create_boundary("bottom"))
        self.actor_list.append(self.factory.create_boundary("left"))
        self.actor_list.append(self.factory.create_boundary("right"))
        
        
        self.point_mass_prev = None
        
        self.player_images = []
        self.player = self.create_player()

    def create_player(self):
        file_path = "../../assets/player/p1_walk{:02}.png"
        player = spm.Player(spm.PgVector(250,500), self.world, file_path, 42)
        self.actor_list.append(player)
        return player
        
    def add_connected_point_mass(self):
        p = self.factory.create_point_mass((300, 0), (random.uniform(-10, 10), random.uniform(-10, 0)))
        self.actor_list.append(p)

        # if self.point_mass_prev is not None:
        #     sp = self.factory.create_spring(p, self.point_mass_prev)
        #     self.actor_list.append(sp)
        # if pygame.key.get_pressed()[pygame.K_SPACE]:
        #     self.point_mass_prev = p

    def update(self):
        for a in self.actor_list:
            a.update()
        self.actor_list[:] = [a for a in self.actor_list if a.is_alive]


    def draw(self, animation_index,player_pos):
        self.screen.fill(pygame.Color("black"))
        self.player.move_player(animation_index, spm.PgVector((player_pos, 633)))
        for a in self.actor_list:
            a.draw(self.screen)
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        player_img = self.player.get_player_images()
        
        
        frame_index = 0
        player_pos = 300
        walk = False
        player_move = 0

        while True:
            frames_per_second = 60
            clock.tick(frames_per_second)
            

            should_quit = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    should_quit = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    should_quit = True
                # elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                #     self.point_mass_prev = None
                # elif event.type == pygame.MOUSEBUTTONDOWN:
                #     sling_x, sling_y = event.pos
                #     tip1 = (player_pos, 550)
                #     tip2 = (-(event.pos[0] - sling_x ), -(event.pos[1] - sling_y))
                #     # for k in range(1,11):
                    
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.add_connected_point_mass()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        player_move = -7
                        walk = True
                        
                    elif event.key == pygame.K_d:
                        player_move = 7
                        walk = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        player_move = 0
                        walk = False
            if should_quit:
                break
            
            player_pos += player_move
            if player_pos <= 90:
                player_pos = 90
            elif player_pos >= 510:
                player_pos = 510
            
            if walk == True:
                frame_index += 1
            else:
                frame_index = 0
            
            animation_period = 3 #This come from trial and error
            animation_index = (frame_index // animation_period % len(player_img))

            self.update()
            self.draw(animation_index, player_pos)

        pygame.quit()


if __name__ == "__main__":
    AppMain().run()