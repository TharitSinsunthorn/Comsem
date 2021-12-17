import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
font = pygame.font.Font(None, 50)
text_img = font.render("Hello, pygame", True, pygame.Color("green"))

# For image mouse
img_org = pygame.image.load("../../assets/player/p1_walk01.png")
player_img = img_org.convert()

while True:
    pygame.event.clear()
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_ESCAPE]:
        break
    mouse_pos = pygame.mouse.get_pos()
    
    # fill the screen with the selected color. In python, this one is called 'method', the data having method are called 'objects'
    screen.fill(pygame.Color("black"))
    #method to paste image to the mouse position
    screen.blit(player_img, mouse_pos)
    mouse_x, mouse_y = mouse_pos
    screen.blit(text_img, (mouse_x + 100, mouse_y))
    # For red circle
    # pygame.draw.circle(screen, pygame.Color("red"), pygame.mouse.get_pos(), 30)
    pygame.display.update()
    
pygame.quit()
#########################
