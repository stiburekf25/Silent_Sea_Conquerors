import pygame
pygame.init()
import sys
import math

OKNO_sirka = 1280
OKNO_vyska = 768
okno = pygame.display.set_mode((OKNO_sirka, OKNO_vyska))
fullscreen = False
hra = True
kotva = False
mapa_otevrena = False


#Barvy
cervena = 200, 200, 200

# Velikost světa.
MAPA_SIRKA = 5000
MAPA_VYSKA = 5000

# Vlastnosti lode
velikost_lode_x = 100
velikost_lode_y = 200
pozice_lode_x =  0
pozice_lode_y = 0
aktualni_rychlost_lode = 2
pomala_rychlost_lode = 1
cas_pomale_jizdy_ms = 5000
cas_vytazeni_kotvy = pygame.time.get_ticks()
rychlost_otaceni_basic = 2

#Obrazky
mapa_neotevrena_puvodni = pygame.image.load("mapa_puvodni_neotevrena.png")
mapa_otevrena_puvodni = pygame.image.load("mapa_puvodni_otevrena.png")
mapa_exit = pygame.image.load("exit_mapa.png")
mapa_background = pygame.image.load("mapa_background.png")
kompas_obrazek = pygame.image.load("compas.png")
mapa_exit_vetsi = pygame.transform.scale(mapa_exit, (mapa_exit.get_width() * 1.2, mapa_exit.get_height() * 1.2))
kotva_obrazek = pygame.image.load("kotva.png")
kotva_vetsi = pygame.transform.scale(kotva_obrazek, (kotva_obrazek.get_width() * 1.1, kotva_obrazek.get_height() * 1.1))
kotva_dole = pygame.image.load("kotva_dole.png")
kotva_dole_vetsi = pygame.transform.scale(kotva_dole, (kotva_dole.get_width() * 1.1, kotva_dole.get_height() * 1.1))
ostorv1 = pygame.image.load("lavovy_ostrov.png")
basic_lod = pygame.image.load("basic_lod.png")

#recty
mapa_neotevrena_puvodni_rect = mapa_neotevrena_puvodni.get_rect(topleft=(OKNO_sirka - 150, 30))
mapa_exit_rect = mapa_exit.get_rect(topleft=(OKNO_sirka - 180, 630))
kompas_rect = kompas_obrazek.get_rect(topleft=(15, 5))
kotva_rect = kotva_obrazek.get_rect(topleft=(OKNO_sirka - 140, 610))
kotva_dole_rect = kotva_dole.get_rect(topleft=(OKNO_sirka - 140, 610))

#fonty
font = pygame.font.SysFont("Arial", 24)

# Loď se otáčí podle směru.
lod_surface = basic_lod

# Směr ručičky kompasu: 0 = sever, 90 = východ, 180 = jih, 270 = západ.
uhel_kompasu = 0
kompas_rucicka_offset_y = 20

# Animace moře
cas_animace = 0
rychlost_vln = 0.01  # Velmi pomalý pohyb vln

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

    if not kotva:
        aktualni_rychlost = 0
    else:
        ubehly_cas_od_vytazeni = pygame.time.get_ticks() - cas_vytazeni_kotvy
        if ubehly_cas_od_vytazeni < cas_pomale_jizdy_ms:
            aktualni_rychlost = pomala_rychlost_lode
        else:
            aktualni_rychlost = aktualni_rychlost_lode
    
    if kotva:
        if stisknuto[pygame.K_a]:
            uhel_kompasu -= rychlost_otaceni_basic
        if stisknuto[pygame.K_d]:
            uhel_kompasu += rychlost_otaceni_basic

    uhel_kompasu %= 360

    radiany_lode = math.radians(uhel_kompasu)
    pozice_lode_x += aktualni_rychlost * math.sin(radiany_lode)
    pozice_lode_y -= aktualni_rychlost * math.cos(radiany_lode)

    # Kamera drží loď uprostřed okna.
    kamera_x = pozice_lode_x + velikost_lode_x / 2 - OKNO_sirka / 2
    kamera_y = pozice_lode_y + velikost_lode_y / 2 - OKNO_vyska / 2

    # Aktualizace animace
    cas_animace += rychlost_vln
    
    
#Cursor

    if mapa_neotevrena_puvodni_rect.collidepoint(mys_pozice) and not mapa_otevrena:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif mapa_exit_rect.collidepoint(mys_pozice) and mapa_otevrena:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif kotva_rect.collidepoint(mys_pozice) and not mapa_otevrena and kotva:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif kotva_dole_rect.collidepoint(mys_pozice) and not mapa_otevrena and not kotva:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

#Otevření mapy
    if mapa_neotevrena_puvodni_rect.collidepoint(mys_pozice) and mouse_click and not mapa_otevrena:
        mapa_otevrena = True

#zavrení mapy
    if mapa_exit_rect.collidepoint(mys_pozice) and mouse_click and mapa_otevrena:
        mapa_otevrena = False

#kotva
    if kotva_dole_rect.collidepoint(mys_pozice) and mouse_click and not mapa_otevrena and not kotva:
        kotva = True
        cas_vytazeni_kotvy = pygame.time.get_ticks()
    elif kotva_rect.collidepoint(mys_pozice) and mouse_click and not mapa_otevrena and kotva:
        kotva = False
    okno.fill((13, 55, 102))

    # Jemná textura moře z kroutících se čar
    for radek_index, y in enumerate(range(-30, OKNO_vyska + 30, 22)):
        start_x = -60
        faze_radku = radek_index * 0.45 + cas_animace * 0.12
        while start_x < OKNO_sirka + 60:
            strida = (int(start_x / 40) + radek_index) % 2
            if strida == 0:
                delka = 16 + int((math.sin(start_x * 0.03 + y * 0.02 + faze_radku) + 1) * 5)
            else:
                delka = 28 + int((math.sin(start_x * 0.03 + y * 0.02 + faze_radku) + 1) * 9)

            x1 = int(start_x)
            x2 = int(start_x + delka)
            y1 = int(y + math.sin((start_x * 0.018 + y * 0.01 + cas_animace * 0.25 + radek_index * 0.2)) * 6)
            y2 = int(y + math.sin(((start_x + delka) * 0.018 + y * 0.01 + cas_animace * 0.25 + radek_index * 0.2)) * 6)
            pygame.draw.line(okno, (26, 86, 138), (x1, y1), (x2, y2), 2)
            start_x += 42 if strida == 0 else 48

    lod_stred_x = pozice_lode_x + velikost_lode_x / 2 - kamera_x
    lod_stred_y = pozice_lode_y + velikost_lode_y / 2 - kamera_y
    otocena_lod = pygame.transform.rotate(lod_surface, -uhel_kompasu)
    otocena_lod_rect = otocena_lod.get_rect(center=(lod_stred_x, lod_stred_y))
    okno.blit(otocena_lod, otocena_lod_rect)

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
        distance_text = font.render(f"Position: ({int(-pozice_lode_x)}, {int(-pozice_lode_y)})", True, (255, 255, 255))
        okno.blit(distance_text, (20, kompas_rect.bottom + 10))

        if kotva:
            if kotva_rect.collidepoint(mys_pozice):
                okno.blit(kotva_vetsi, (OKNO_sirka - 145, 600))
            else:
                okno.blit(kotva_obrazek, kotva_rect)
        else:
            if kotva_dole_rect.collidepoint(mys_pozice):
                okno.blit(kotva_dole_vetsi, (OKNO_sirka - 145, 600))
            else:
                okno.blit(kotva_dole, kotva_dole_rect)
    

    if mapa_otevrena:
        okno.blit(mapa_background, (50, 50))
        okno.blit(mapa_exit, (OKNO_sirka - 180, 630))
        if mapa_exit_rect.collidepoint(mys_pozice):
            okno.blit(mapa_exit_vetsi, (OKNO_sirka - 185, 625))
    
    

    pygame.display.flip()
    clock.tick(60)
    