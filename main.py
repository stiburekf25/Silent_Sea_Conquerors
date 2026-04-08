import pygame
pygame.init()
import sys

OKNO_sirka = 1280
OKNO_vyska = 768
okno = pygame.display.set_mode((OKNO_sirka, OKNO_vyska))
fullscreen = False
hra = True 

cervena = 200, 200, 200

velikost_lode_x = 100
velikost_lode_y = 200
pozice_lode_x = OKNO_sirka / 2 - velikost_lode_x / 2
pozice_lode_y = OKNO_vyska / 2 - velikost_lode_y / 2

clock = pygame.time.Clock()

while hra:
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
        
        

    okno.fill((20, 89, 163))
    pygame.draw.rect(okno, cervena, (pozice_lode_x, pozice_lode_y, velikost_lode_x, velikost_lode_y))
    pygame.display.flip()
    clock.tick(60)