import pygame

def init_screen():
    pygame.init()
    width, height = 600, 700
    screen = pygame.display.set_mode((width, height))
    return screen

def create_player():
    file_path = "../../assets/player/p1_walk{:02}.png"
    player_images = []
    player_images = [pygame.image.load(file_path.format(k)).convert() for k in range(2, 8)]
    return player_images
    
def draw(screen, player_img, pos):
    screen.fill(pygame.Color("black"))
    screen.blit(player_img, pos)
    #mouse_x, mouse_y = player_pos
    pygame.display.update()

def main():
    screen = init_screen()
    player_img = create_player()
    clock = pygame.time.Clock()
    frame_index = 0
    player_pos = 250
    
    walk = False
    player_move = 0

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
                elif event.key == pygame.K_b:
                    pass
                elif event.key == pygame.K_a:
                    player_move = -7
                    walk = True
                    # frame_index += 1
                elif event.key == pygame.K_d:
                    player_move = 7
                    walk = True
                    # frame_index += 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player_move = 0
                    walk = False

        if should_quit:
            break
                    
        player_pos += player_move
        if player_pos <= 0:
            player_pos = 0
        elif player_pos >= 530:
            player_pos = 530
            
        if walk == True:
            frame_index += 1
        else:
            frame_index = 0
            
        animation_period = 3 #This come from trial and error
        animation_index = (frame_index // animation_period % len(player_img))
        draw(screen, player_img[animation_index], (player_pos, 500))
        pygame.draw.circle(screen, "green", (250,500, 70, self.width)
    pygame.quit()
    
if __name__ == "__main__":

    main()

