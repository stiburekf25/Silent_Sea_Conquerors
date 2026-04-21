import pygame
pygame.init()
import sys
import math

OKNO_sirka = 1280
OKNO_vyska = 768
okno = pygame.display.set_mode((OKNO_sirka, OKNO_vyska))
fullscreen = False
hra = True 
mapa_otevrena = False


#Barvy
cervena = 200, 200, 200

# Velikost světa.
MAPA_SIRKA = 5000
MAPA_VYSKA = 5000

# Vlastnosti lode
velikost_lode_x = 100
velikost_lode_y = 200
pozice_lode_x = MAPA_SIRKA / 2 - velikost_lode_x / 2
pozice_lode_y = MAPA_VYSKA / 2 - velikost_lode_y / 2
aktualni_rychlost_lode = 2

#Obrazky
mapa_neotevrena_puvodni = pygame.image.load("mapa_puvodni_neotevrena.png")
mapa_otevrena_puvodni = pygame.image.load("mapa_puvodni_otevrena.png")
mapa_exit = pygame.image.load("exit_mapa.png")
mapa_background = pygame.image.load("mapa_background.png")
kompas_obrazek = pygame.image.load("compas.png")
mapa_exit_vetsi = pygame.transform.scale(mapa_exit, (mapa_exit.get_width() * 1.2, mapa_exit.get_height() * 1.2))
ostorv1 = pygame.image.load("lavovy_ostrov.png")

#recty
mapa_neotevrena_puvodni_rect = mapa_neotevrena_puvodni.get_rect(topleft=(OKNO_sirka - 150, 30))
mapa_exit_rect = mapa_exit.get_rect(topleft=(OKNO_sirka - 180, 630))
kompas_rect = kompas_obrazek.get_rect(topleft=(15, 5))

# Směr ručičky kompasu: 0 = sever, 90 = východ, 180 = jih, 270 = západ.
uhel_kompasu = 0
kompas_rucicka_offset_y = 20

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

    # Kamera drží loď uprostřed okna.
    kamera_x = pozice_lode_x + velikost_lode_x / 2 - OKNO_sirka / 2
    kamera_y = pozice_lode_y + velikost_lode_y / 2 - OKNO_vyska / 2

    smer_x = int(stisknuto[pygame.K_d]) - int(stisknuto[pygame.K_a])
    smer_y = int(stisknuto[pygame.K_s]) - int(stisknuto[pygame.K_w])

    # Aktualizace směru kompasu jen pokud se loď opravdu pohybuje.
    if smer_x != 0 or smer_y != 0:
        uhel_kompasu = math.degrees(math.atan2(smer_x, -smer_y))
    
    
    
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

    okno.fill((13, 55, 102))

    # Vykreslení mapy posunuté kamerou.
    pygame.draw.rect(okno, (20, 89, 163), (-kamera_x, -kamera_y, MAPA_SIRKA, MAPA_VYSKA))

    lod_na_obrazovce_x = pozice_lode_x - kamera_x
    lod_na_obrazovce_y = pozice_lode_y - kamera_y
    pygame.draw.rect(okno, cervena, (lod_na_obrazovce_x, lod_na_obrazovce_y, velikost_lode_x, velikost_lode_y))
    if not mapa_neotevrena_puvodni_rect.collidepoint(mys_pozice) and not mapa_otevrena:
        okno.blit(mapa_neotevrena_puvodni, (OKNO_sirka - 150, 30))
    if mapa_neotevrena_puvodni_rect.collidepoint(mys_pozice) and not mapa_otevrena:
        okno.blit(mapa_otevrena_puvodni, (OKNO_sirka - 150, 30))
    if not mapa_otevrena:
        okno.blit(kompas_obrazek, kompas_rect.topleft)

        delka_rucicky = min(kompas_rect.width, kompas_rect.height) * 0.26
        stred_x = kompas_rect.centerx
        stred_y = kompas_rect.centery + kompas_rucicka_offset_y
        radiany = math.radians(uhel_kompasu)

        konec_x = stred_x + delka_rucicky * math.sin(radiany)
        konec_y = stred_y - delka_rucicky * math.cos(radiany)

        pygame.draw.line(okno, (220, 30, 30), (stred_x, stred_y), (konec_x, konec_y), 5)
        pygame.draw.circle(okno, (30, 30, 30), (stred_x, stred_y), 6)
    if mapa_otevrena:
        okno.blit(mapa_background, (50, 50))
        okno.blit(mapa_exit, (OKNO_sirka - 180, 630))
        if mapa_exit_rect.collidepoint(mys_pozice):
            okno.blit(mapa_exit_vetsi, (OKNO_sirka - 185, 625))

    pygame.display.flip()
    clock.tick(60)
    