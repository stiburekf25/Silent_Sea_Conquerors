import pygame
pygame.init()
import sys

OKNO_sirka = 1280
OKNO_vyska = 768
okno = pygame.display.set_mode((OKNO_sirka, OKNO_vyska))
fullscreen = False
hra = True 
mapa_otevrena = False


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
mapa_otevrena_puvodni = pygame.image.load("mapa_puvodni_otevrena.png")
mapa_exit = pygame.image.load("exit_mapa.png")
mapa_background = pygame.image.load("mapa_background.png")
kompas_obrazek = pygame.image.load("compas.png")

#recty
mapa_neotevrena_puvodni_rect = mapa_neotevrena_puvodni.get_rect(topleft=(OKNO_sirka - 150, 30))
mapa_exit_rect = mapa_exit.get_rect(topleft=(OKNO_sirka - 120, 630))

clock = pygame.time.Clock()

while hra:
    mouse_click = False

    mys_pozice = pygame.mouse.get_pos()
    stisknuto = pygame.key.get_pressed()
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if udalost.type == pygame.MOUSEBUTTONDOWN and udalost.button == 1:
            mouse_click = True
    
    if stisknuto[pygame.K_w]:
        pozice_lode_y -= aktualni_rychlost_lode
    if stisknuto[pygame.K_s]:
        pozice_lode_y += aktualni_rychlost_lode
    if stisknuto[pygame.K_a]:
        pozice_lode_x -= aktualni_rychlost_lode
    if stisknuto[pygame.K_d]:
        pozice_lode_x += aktualni_rychlost_lode
    
    
    
#Cursor

    if mapa_neotevrena_puvodni_rect.collidepoint(mys_pozice) and not mapa_otevrena:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif mapa_exit_rect.collidepoint(mys_pozice) and mapa_otevrena:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

#Otevření mapy
    if mapa_neotevrena_puvodni_rect.collidepoint(mys_pozice) and mouse_click and not mapa_otevrena:
        mapa_otevrena = True

#zavrení mapy
    if mapa_exit_rect.collidepoint(mys_pozice) and mouse_click and mapa_otevrena:
        mapa_otevrena = False

    okno.fill((20, 89, 163))
    pygame.draw.rect(okno, cervena, (pozice_lode_x, pozice_lode_y, velikost_lode_x, velikost_lode_y))
    if not mapa_neotevrena_puvodni_rect.collidepoint(mys_pozice) and not mapa_otevrena:
        okno.blit(mapa_neotevrena_puvodni, (OKNO_sirka - 150, 30))
    if mapa_neotevrena_puvodni_rect.collidepoint(mys_pozice) and not mapa_otevrena:
        okno.blit(mapa_otevrena_puvodni, (OKNO_sirka - 150, 30))
    if not mapa_otevrena:
        okno.blit(kompas_obrazek, (50, 50))
    if mapa_otevrena:
        okno.blit(mapa_background, (50, 50))
        okno.blit(mapa_exit, (OKNO_sirka - 120, 630))

    pygame.display.flip()
    clock.tick(60)
    