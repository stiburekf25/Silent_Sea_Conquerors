import pygame
pygame.init()
import sys

OKNO_sirka, OKNO_vyska = 1280, 768
okno = pygame.display.set_mode((OKNO_sirka, OKNO_vyska))
fullscreen = False

clock = pygame.time.Clock()

while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    okno = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    okno = pygame.display.set_mode((OKNO_sirka, OKNO_vyska))

    okno.fill((30, 30, 30))
    pygame.display.flip()
    clock.tick(60)