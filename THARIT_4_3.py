import pygame

def init_screen():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    return screen

def create_text():
    font_size = 50
    font_file = None
    antialias = True
    font = pygame.font.Font(font_file, font_size)
    text_img1 = font.render("hello", antialias, pygame.Color("red"))
    text_img2 = font.render("py", antialias, pygame.Color("green"))
    text_img3 = font.render("game", antialias, pygame.Color("blue"))
    text_img  = [text_img1, text_img2, text_img3]
    return text_img

def create_player():
    file_path = "../../assets/player/p1_walk{:02}.png"
    player_images = []
    player_images = [pygame.image.load(file_path.format(k)).convert() for k in range(4, 8)]
    return player_images
    
def draw(screen, player_img, text_img, mouse_pos):
    screen.fill(pygame.Color("black"))
    screen.blit(player_img, mouse_pos)
    if text_img is not None:
        mouse_x, mouse_y = mouse_pos
        text_offset_x = 100
        screen.blit(text_img, (mouse_x + text_offset_x, mouse_y))
    pygame.display.update()

def main():
    screen = init_screen()
    text_img = create_text()
    player_img = create_player()
    clock = pygame.time.Clock()
    frame_index = 0
    clicknum = 0

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicknum += 1
        if should_quit:
            break
                    
        text_index = clicknum % len(text_img)
        mouse_pos = pygame.mouse.get_pos()
        buttons_pressed = pygame.mouse.get_pressed()
        if buttons_pressed[0]:
            text_img_shown = text_img[text_index]
        else:
            text_img_shown = None
            
        frame_index += 1
        animation_period = 6 #This come from trial and error
        animation_index = (frame_index // animation_period % len(player_img))
        draw(screen, player_img[animation_index], text_img_shown, mouse_pos)
        
    pygame.quit()
    
main()
