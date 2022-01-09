import pygame

def init_screen():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    return screen

def create_text(text, color):
    font_size = 50
    font_file = None
    antialias = True
    font = pygame.font.Font(font_file, font_size)
    text_img = font.render("Hello, pygame", antialias, pygame.Color("green"))
    text_img2 = font.render(text, antialias, pygame.Color(color))
    return text_img, text_img2

def draw(screen, player_img, text_img, mouse_pos):
    # fill the screen with the selected color. 
    # In python, this one is called 'method', 
    # the data having method are called 'objects'
    screen.fill(pygame.Color("black"))
    #method to paste image to the mouse position
    screen.blit(player_img, mouse_pos)
    mouse_x, mouse_y = mouse_pos
    text_offset_x = 100
    screen.blit(text_img, (mouse_x + text_offset_x, mouse_y))
    # For red circle
    # pygame.draw.circle(screen, pygame.Color("red"), pygame.mouse.get_pos(), 30)
    pygame.display.update()

def main():
    screen = init_screen()
    text_img, text_img2 = create_text("Hello pygame", "yellow")
    # For image mouse
    img_org = pygame.image.load("../../assets/player/p1_walk01.png")
    player_img = img_org.convert()

    while True:
        should_quit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    should_quit = True
                # elif event.key == pygame.K_b:
                #     pass
        if should_quit:
            break
        mouse_pos = pygame.mouse.get_pos()
        
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            draw(screen, player_img, text_img2, mouse_pos)
        else:
            draw(screen, player_img, text_img, mouse_pos)
        
    pygame.quit()
    
main()
