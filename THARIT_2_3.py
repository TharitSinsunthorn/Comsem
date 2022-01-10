# C0TB1716 Tharit Sinsunthorn
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
font = pygame.font.Font(None, 50)
text_img = font.render("Hello, pygame", True, pygame.Color("green"))

# For image mouse
img_org = pygame.image.load("../../assets/player/p1_walk01.png")
player_img = img_org.convert()
Pwidth = player_img.get_width()
Pheight = player_img.get_height()

while True:
    pygame.event.clear()
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_ESCAPE]:
        break
    mouse_pos = pygame.mouse.get_pos()
    
    screen.fill(pygame.Color("black"))
    #method to paste image to the mouse position
    mouse_x, mouse_y = mouse_pos
    
    screen.blit(player_img, [mouse_x - Pwidth/2, mouse_y - Pheight/2])
    screen.blit(text_img, (mouse_x + 100 - Pwidth/2, mouse_y - Pheight/2))
    pygame.display.update()
    
pygame.quit()
