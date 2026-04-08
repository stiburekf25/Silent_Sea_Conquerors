import pygame
pygame.init()
import sys

OKNO_sirka = 1280
OKNO_vyska = 768
okno = pygame.display.set_mode((OKNO_sirka, OKNO_vyska))
fullscreen = False
hra = True 


#Barvy
cervena = 200, 200, 200

# Vlastnosti lode
velikost_lode_x = 100
velikost_lode_y = 200
pozice_lode_x = OKNO_sirka / 2 - velikost_lode_x / 2
pozice_lode_y = OKNO_vyska / 2 - velikost_lode_y / 2
aktualni_rychlost_lode = 2

#Obrazky
mapa_neotevrena_puvodni = pygame.image.load("mapa_puvodni_neotevrena.png")

clock = pygame.time.Clock()
mys_pozice = pygame.mouse.get_pos()

while hra:
    stisknuto = pygame.key.get_pressed()
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
    
    if stisknuto[pygame.K_w]:
        pozice_lode_y -= aktualni_rychlost_lode
    if stisknuto[pygame.K_s]:
        pozice_lode_y += aktualni_rychlost_lode
    if stisknuto[pygame.K_a]:
        pozice_lode_x -= aktualni_rychlost_lode
    if stisknuto[pygame.K_d]:
        pozice_lode_x += aktualni_rychlost_lode

    okno.fill((20, 89, 163))
    pygame.draw.rect(okno, cervena, (pozice_lode_x, pozice_lode_y, velikost_lode_x, velikost_lode_y))
    okno.blit(mapa_neotevrena_puvodni, (OKNO_sirka - 150, 30))
    #pygame.draw.rect(okno, cervena, (OKNO_sirka - 150, 30, 120, 120))
    pygame.display.flip()
    clock.tick(60)
    