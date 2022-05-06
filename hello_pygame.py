import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
# screen = pygame.Surface((600,400), pygame.SRCALPHA)
pygame.draw.circle(screen, (255,255,255), (100,100), 30)
screen.blit(screen, (0,0))
pygame.display.update()
pygame.time.wait(1000)
pygame.quit()
