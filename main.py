import pygame
pygame.init()
import sys

OKNO_sirka = 1280
OKNO_vyska = 768
okno = pygame.display.set_mode((OKNO_sirka, OKNO_vyska))
fullscreen = False

cervena = 200, 200, 200

velikost_lode_x = 100
velikost_lode_y = 200

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
    pygame.draw.rect(okno, cervena, (OKNO_sirka / 2 - velikost_lode_x / 2, OKNO_vyska / 2 - velikost_lode_y / 2, velikost_lode_x, velikost_lode_y))
    pygame.display.flip()
    clock.tick(60)