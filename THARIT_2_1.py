# C0TB1716 Tharit Sinsunthorn
import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
font = pygame.font.Font(None, 100)
text_img = font.render("TOWER TAKE A SHOWER", True, pygame.Color("cyan"))


    

while True:
    pygame.event.clear()
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_ESCAPE]:
        break
    mouse_pos = pygame.mouse.get_pos()
    
    # fill the screen with the selected color. In python, this one is called 'method', the data having method are called 'objects'
    screen.fill(pygame.Color("black"))
    #method to paste image to the mouse position
    screen.blit(text_img, mouse_pos)
    pygame.display.update()
    
pygame.quit()
