import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
font = pygame.font.Font(None, 50)
text_img = font.render("hello, pygame", True, pygame.Color("green"))

# For image mouse
img_org = pygame.image.load("../../assets/player/p1_walk01.png")
player_img = img_org.convert()

while True:
    pygame.event.clear()
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_ESCAPE]:
        break
    mouse_pos = pygame.mouse.get_pos()
    
    # fill the screen with the selected color
    # In python, this one is called 'method'
    # the data having method are called 'objects'
    screen.fill(pygame.Color("black"))
    #method to paste image to the mouse position
    screen.blit(player_img, mouse_pos)
    mouse_x, mouse_y = mouse_pos
    screen.blit(text_img, (mouse_x + 100, mouse_y))
    pygame.draw.line(screen, pygame.Color("blue"), mouse_pos, [mouse_x + 600, mouse_y], 4)
    pygame.draw.line(screen, pygame.Color("blue"), mouse_pos, [mouse_x - 600, mouse_y], 4)
    pygame.draw.line(screen, pygame.Color("blue"), mouse_pos, [mouse_x, mouse_y + 400], 4)
    pygame.draw.line(screen, pygame.Color("blue"), mouse_pos, [mouse_x, mouse_y - 400], 4)
    pygame.draw.ellipse(screen, pygame.Color("red"), [mouse_x + 80, mouse_y, 270 , 40], 2)
    pygame.display.update()
    
pygame.quit()
