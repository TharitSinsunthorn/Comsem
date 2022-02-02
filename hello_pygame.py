import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.draw.circle(screen, pygame.Color("red"), (300,200), 30)
pygame.display.update()
pygame.time.wait(5000)
pygame.quit()
