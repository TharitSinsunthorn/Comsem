import random
import pygame
import Charlee as chr

class ActorFactory:
    def __init__(self, world, actor_list):
        self.world = world
        self.actor_list = actor_list
        self.obs_list = []

    def create_obstacle(self):
        # RED = (188, 39, 50)
        # GREEN = (61, 199, 112)
        WHITE = (255, 255, 255)
        PURPLE = (210, 145, 255)
        RUST = (212, 198, 178)
        
        # White planet at corner
        self.obs_list.append(chr.FixedPointMass((0,0),  self.world, 60, 0.01,
                              1.5, chr.CircleDrawer(color = WHITE, width=0, glow=(100, 7))))
        self.obs_list.append(chr.FixedPointMass((600,0),  self.world, 60, 0.01,
                              1.5, chr.CircleDrawer(color = WHITE, width=0, glow=(100, 7))))
        self.obs_list.append(chr.FixedPointMass((0,750),  self.world, 40, 0.01,
                              1.5, chr.CircleDrawer(color = WHITE, width=0, glow=(100, 7))))
        self.obs_list.append(chr.FixedPointMass((600,750),  self.world, 40, 0.01,
                              1.5, chr.CircleDrawer(color = WHITE, width=0, glow=(100, 7))))
        
        # Purple planet
        self.obs_list.append(chr.FixedPointMass((80,130),  self.world, 20, 0.01,
                              0.95, chr.CircleDrawer(color = PURPLE, width=0, glow=(100, 6))))
        self.obs_list.append(chr.FixedPointMass((200,110),  self.world, 20, 0.01,
                              0.95, chr.CircleDrawer(color = PURPLE, width=0, glow=(100, 6))))
        self.obs_list.append(chr.FixedPointMass((400,110),  self.world, 20, 0.01,
                              0.95, chr.CircleDrawer(color = PURPLE, width=0, glow=(100, 6))))
        self.obs_list.append(chr.FixedPointMass((520,130),  self.world, 20, 0.01,
                              0.95, chr.CircleDrawer(color = PURPLE, width=0, glow=(100, 6))))
        self.obs_list.append(chr.FixedPointMass((100,300),  self.world, 20, 0.01,
                              0.95, chr.CircleDrawer(color = PURPLE, width=0, glow=(100, 6))))
        self.obs_list.append(chr.FixedPointMass((200,400),  self.world, 20, 0.01,
                              0.95, chr.CircleDrawer(color = PURPLE, width=0, glow=(100, 6))))
        self.obs_list.append(chr.FixedPointMass((300,350),  self.world, 20, 0.01,
                              0.95, chr.CircleDrawer(color = PURPLE, width=0, glow=(100, 6))))
        self.obs_list.append(chr.FixedPointMass((400,400),  self.world, 20, 0.01,
                              0.95, chr.CircleDrawer(color = PURPLE, width=0, glow=(100, 6))))
        self.obs_list.append(chr.FixedPointMass((500,300),  self.world, 20, 0.01,
                              0.95, chr.CircleDrawer(color = PURPLE, width=0, glow=(100, 6))))
        
        # Sun
        self.obs_list.append(chr.FixedPointMass((300,220),  self.world, 50, 0.01,
                              0.2, chr.CircleDrawer(color = RUST, width=0, glow = (100, 7))))
        
        return self.obs_list
        
    def create_point_mass(self, pos, vel):
        mass = 10
        radius = 10
        viscous = 0.02
        restitution = 1.05
        AQUA = (160,216,199)
        return chr.PointMass(pos, vel, self.world, radius, mass, viscous,
                             restitution, chr.CircleDrawer(AQUA, width=0))
    
    def create_player(self):
        file_path = "../../assets/player/p1_walk{:02}.png"
        return chr.Player((0,0), self.world, file_path, 42)
    
    def create_collision_resolver(self):
        return chr.countedCollisionResolver(self.world, self.actor_list)
    
    def create_gfield(self, p1, p2, G):
        return chr.GravitationalForce(p1, p2, self.world, G, chr.LineDrawer("white", width=1))

    def create_boundary(self, name):
        width, height = self.world.size
        geometry = {"top": ((0, -1), (0, 0)),
                    "bottom": ((0, 1), (0, height)),
                    "left": ((-1, 0), (0, 0)),
                    "right": ((1, 0), (width, 0))}
        normal, point_included = geometry[name]
        return chr.Boundary(normal, point_included, self.world, self.actor_list)
    
    
class AppMain:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("../../assets/sound/bg.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.03)
        
        width, height = 600, 750
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Charlee Charlee")
        
        #Build world
        self.world = chr.World((width, height), dt=1.0, gravity_acc=(0, 0.09))
        self.actor_list = []
        self.factory = ActorFactory(self.world, self.actor_list)
        
        # Build obstacles
        for i in range(len(self.factory.create_obstacle())):
            self.actor_list.append(self.factory.create_obstacle()[i])

        # Build boundary
        self.actor_list.append(self.factory.create_collision_resolver())
        self.actor_list.append(self.factory.create_boundary("top"))
        self.actor_list.append(self.factory.create_boundary("left"))
        self.actor_list.append(self.factory.create_boundary("right"))
        
        #Build player
        self.player_images = []
        self.player = self.factory.create_player()
        self.actor_list.append(self.player)
        
    def add_gravitational_point_mass(self):
        # Add moving point mass
        p = self.factory.create_point_mass((random.uniform(100,500), 0), (random.uniform(-10, 10), random.uniform(-8, -5)))
        self.actor_list.append(p)

        # Determine center of gravitational force
        s1 = self.factory.create_obstacle()[-1]
        gf1 = self.factory.create_gfield(p, s1, G = -15)
        self.actor_list.append(gf1)

    def update(self):
        for a in self.actor_list:
            a.update()
        self.actor_list[:] = [a for a in self.actor_list if a.is_alive]

    def decorate(self):
        planet_list = []
        path1 = "../../assets/planet/purple1.png"
        planet = pygame.image.load(path1).convert_alpha()
        planet = pygame.transform.scale(planet, (80,53))
 
        planet_list.append(planet.get_rect(center=(78,130)))
        planet_list.append(planet.get_rect(center=(198,110)))
        planet_list.append(planet.get_rect(center=(398,110)))
        planet_list.append(planet.get_rect(center=(518,130)))
        planet_list.append(planet.get_rect(center=(298,350)))
        planet_list.append(planet.get_rect(center=(98,300)))
        planet_list.append(planet.get_rect(center=(498,300)))
        planet_list.append(planet.get_rect(center=(198,400)))
        planet_list.append(planet.get_rect(center=(398,400)))
        for i in range(len(planet_list)):
            self.screen.blit(planet, planet_list[i])
    
    def background(self):
        file_path = "../../assets/bg/space4.jpg"
        bg = pygame.image.load(file_path).convert_alpha()
        bg = pygame.transform.scale(bg, (600, 750))
        self.screen.blit(bg, (0, 0))

    def draw(self, animation_index,player_pos, game_over, start):
        self.background()
        self.player.move_player(animation_index, chr.PgVector((player_pos, 683)))
        for a in self.actor_list:
            a.draw(self.screen)

        if game_over == True:
            self.gameover()
            
        self.decorate()
        self.startscreen(start)
        pygame.display.update()
        
    def gameover(self):
        font = pygame.font.Font(None, 90)
        font2 = pygame.font.Font(None, 30)
        font3 = pygame.font.Font(None, 20)
        
        text_img = font.render("GAME OVER", True, pygame.Color("white"))
        text_img2 = font2.render("Press R to restart", True, pygame.Color("white"))
        text_img3 = font3.render("Press ESC to say bye Charlee", True, pygame.Color("white"))
        
        text_rect = text_img.get_rect(center=(600/2, 450/2))
        text_rect2 = text_img2.get_rect(center=(600/2, 550/2))
        text_rect3 = text_img3.get_rect(center=(600/2, 600/2))
        
        self.screen.blit(text_img, text_rect)
        self.screen.blit(text_img2, text_rect2)
        self.screen.blit(text_img3, text_rect3)
        
    def restart(self):
        for a in self.actor_list:
            a.restart()
        
    def startscreen(self, start):
        if not start:
            font = pygame.font.Font(None, 100)
            font2 = pygame.font.Font(None, 30)
            font3 = pygame.font.Font(None, 20)
            
            text_img = font.render("Press", True, pygame.Color("white"))
            text_img2 = font2.render("SPACEBAR to START", True, pygame.Color("white"))
            text_img3 = font3.render("use A&D to move Charlee", True, pygame.Color("white"))
            
            text_rect = text_img.get_rect(center=(600/2, 450/2))
            text_rect2 = text_img2.get_rect(center=(600/2, 550/2))
            text_rect3 = text_img3.get_rect(center=(600/2, 600/2))
            
            self.screen.blit(text_img, text_rect)
            self.screen.blit(text_img2, text_rect2)
            self.screen.blit(text_img3, text_rect3)
            
            
    def run(self):
        clock = pygame.time.Clock()
        should_quit = False
        
        player_img = self.player.get_player_images()
        frame_index = 0
        player_pos = 300
        walk = False
        player_move = 0
    
        start = False
        game_over = False
        life = True
        
        gameover_sound = pygame.mixer.Sound("../../assets/sound/gameover.wav")
        sad = pygame.mixer.Sound("../../assets/sound/sadchild.wav")
        
        while True:
            self.startscreen(life)
            frames_per_second = 60
            clock.tick(frames_per_second)
            for a in self.actor_list:
                if type(a) is chr.PointMass and a.pos.y > 760:
                    gameover_sound.play()
                    gameover_sound.set_volume(0.05)
                        
                    sad.play()
                    sad.set_volume(0.04)
                    
                    game_over = True
                    self.actor_list.remove(a)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    should_quit = True
                    
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    should_quit = True
                    
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                    game_over = False
                    self.restart()
                    self.run()
                    
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and life:
                    self.add_gravitational_point_mass()
                    life = False
                    start = True
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        player_move = -8 
                        walk = True
    
                    elif event.key == pygame.K_d:
                        player_move = 8
                        walk = True
                        
                    elif event.key == pygame.K_a and pygame.K_d:
                        player_move = 0
                        walk = False
                        
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or pygame.K_d:
                        player_move = 0
                        walk = False
                        
            if should_quit:
                break
                
            player_pos += player_move
            if player_pos <= 80:
                player_pos = 80
            elif player_pos >= 520:
                player_pos = 520
                
            if walk == True:
                frame_index += 1
            else:
                frame_index = 0
                
                
            animation_period = 1
            animation_index = (frame_index // animation_period % len(player_img))

            self.update()
            self.draw(animation_index, player_pos, game_over, start)
            
        pygame.quit()


if __name__ == "__main__":
    AppMain().run()
