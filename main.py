import pygame
pygame.init()
import sys
import math

OKNO_sirka = 1280
OKNO_vyska = 768
okno = pygame.display.set_mode((OKNO_sirka, OKNO_vyska))
fullscreen = False
hra = True
shop = False
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
basic_lod = pygame.image.load("basic_lod.png")
pokrocila_lod = pygame.image.load("pokrocila_lod.png")
profesionalni_lod = pygame.image.load("profesionalni_lod.png")

#recty
mapa_neotevrena_puvodni_rect = mapa_neotevrena_puvodni.get_rect(topleft=(OKNO_sirka - 150, 30))
mapa_exit_rect = mapa_exit.get_rect(topleft=(OKNO_sirka - 180, 630))
kompas_rect = kompas_obrazek.get_rect(topleft=(15, 5))
kotva_rect = kotva_obrazek.get_rect(topleft=(OKNO_sirka - 140, 610))
kotva_dole_rect = kotva_dole.get_rect(topleft=(OKNO_sirka - 140, 610))

#fonty

font = pygame.font.Font("pirat_font.ttf", 24)
zlato_font = pygame.font.Font("pirat_font.ttf", 28)
posatky_font = pygame.font.Font("pirat_font.ttf", 28)

# Loď se otáčí podle směru.
lod_surface = basic_lod

# Směr ručičky kompasu: 0 = sever, 90 = východ, 180 = jih, 270 = západ.
uhel_kompasu = 0
kompas_rucicka_offset_y = 20

# Animace moře
cas_animace = 0
rychlost_vln = 0.01  # Velmi pomalý pohyb vln

clock = pygame.time.Clock()


#ostrovy

rozestup_ostrovu = 2000

ostrov_spawn = [
    {"x": 700, "y": 700, "nazev": "lava_ostrov"},
    {"x": -2500, "y": -1500, "nazev": "shop_ostrov"},
    {"x": -4000, "y": -3000, "nazev": "cerv_ostrov"},
    {"x": 3000, "y": -2000, "nazev": "magma_ostrov"},
]


vyber_ostrovu = [
    {
        "nazev": "lava_ostrov",
        "obrazek": pygame.image.load("lava_ostrov.png"),
    },
    {
        "nazev": "shop_ostrov",
        "obrazek": pygame.image.load("shop_ostrov.png"),
    },
    {
        "nazev": "cerv_ostrov",
        "obrazek": pygame.image.load("cerv_ostrov.png"),
    },
    {
        "nazev": "magma_ostrov",
        "obrazek": pygame.image.load("magma_ostrov.png"),
    }
]

#lod statistiky

lod_informace = [
    {
        "nazev": "basic_lod",
        "rychlost": 2,
        "obrazek": basic_lod,
        "maximalni_pocet_posatky": 5,
        "maximalni_unosnost_zlata": 1000,
        "cena": 0,
        "pocet_posatky": 5,
    },
    {
        "nazev": "pokrocila_lod",
        "rychlost": 3,
        "obrazek": pokrocila_lod,
        "maximalni_pocet_posatky": 10,
        "maximalni_unosnost_zlata": 5000,
        "cena": 1000,
        "pocet_posatky": 10,
    },
    {
        "nazev": "profesionalni_lod",
        "rychlost": 4,
        "obrazek": profesionalni_lod,
        "maximalni_pocet_posatky": 15,
        "maximalni_unosnost_zlata": 10000,
        "cena": 5000,
        "pocet_posatky": 15,
    },
]

aktualni_lod = lod_informace[0]
lod_surface = aktualni_lod["obrazek"]
aktualni_rychlost_lode = aktualni_lod["rychlost"]
velikost_lode_x = lod_surface.get_width()
velikost_lode_y = lod_surface.get_height()
maximalni_unosnost_zlata = aktualni_lod["maximalni_unosnost_zlata"]
maximalni_pocet_posatky = aktualni_lod["maximalni_pocet_posatky"]
aktualni_zlato = 10000
aktualni_posatky = aktualni_lod["pocet_posatky"]
zakoupene_lodi = {"basic_lod": True}


def nastav_aktualni_lod(nova_lod):
    global aktualni_lod, lod_surface, aktualni_rychlost_lode, velikost_lode_x, velikost_lode_y
    global maximalni_unosnost_zlata, maximalni_pocet_posatky, aktualni_posatky

    aktualni_lod = nova_lod
    lod_surface = nova_lod["obrazek"]
    aktualni_rychlost_lode = nova_lod["rychlost"]
    velikost_lode_x = lod_surface.get_width()
    velikost_lode_y = lod_surface.get_height()
    maximalni_unosnost_zlata = nova_lod["maximalni_unosnost_zlata"]
    maximalni_pocet_posatky = nova_lod["maximalni_pocet_posatky"]
    aktualni_posatky = nova_lod["pocet_posatky"]




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
    posun_vzoru_x = kamera_x * 0.03
    posun_vzoru_y = kamera_y * 0.02
    for radek_index, y in enumerate(range(-30, OKNO_vyska + 30, 22)):
        start_x = -60
        faze_radku = radek_index * 0.35 + cas_animace * 0.08 + posun_vzoru_y
        while start_x < OKNO_sirka + 60:
            hladka_strida = math.sin((start_x + posun_vzoru_x) * 0.045 + radek_index * 0.8 + faze_radku)
            delka = 20 + int((math.sin(start_x * 0.03 + y * 0.02 + faze_radku) + 1) * 8)
            delka += int(hladka_strida * 4)

            x1 = int(start_x - posun_vzoru_x * 0.15)
            x2 = int(start_x + delka - posun_vzoru_x * 0.15)
            vlna_posun = math.sin(start_x * 0.018 + y * 0.01 + cas_animace * 0.12 + radek_index * 0.18 + posun_vzoru_x * 0.006)
            y1 = int(y + vlna_posun * 5)
            y2 = int(y + math.sin((start_x + delka) * 0.018 + y * 0.01 + cas_animace * 0.12 + radek_index * 0.18 + posun_vzoru_x * 0.006) * 5)
            pygame.draw.line(okno, (26, 86, 138), (x1, y1), (x2, y2), 2)
            start_x += 42

    lod_stred_x = pozice_lode_x + velikost_lode_x / 2 - kamera_x
    lod_stred_y = pozice_lode_y + velikost_lode_y / 2 - kamera_y
    otocena_lod = pygame.transform.rotate(lod_surface, -uhel_kompasu)
    otocena_lod_rect = otocena_lod.get_rect(center=(lod_stred_x, lod_stred_y))
    okno.blit(otocena_lod, otocena_lod_rect)

    for ostrov in ostrov_spawn:
        nazev = ostrov["nazev"]
        data_ostrovu = next((o for o in vyber_ostrovu if o["nazev"] == nazev), None)
        if data_ostrovu:
            obrazek_ostrovu = data_ostrovu["obrazek"]
            pozice_x = ostrov["x"] - kamera_x - obrazek_ostrovu.get_width() / 2
            pozice_y = ostrov["y"] - kamera_y - obrazek_ostrovu.get_height() / 2
            
            # Střed ostrova na obrazovce
            stred_x = int(ostrov["x"] - kamera_x)
            stred_y = int(ostrov["y"] - kamera_y)
            
            # Elipsa kolem ostrova
            sirka_elipsy = 800
            vyska_elipsy = 800
            
            # Detekce kolize - vzdálenost mezi lodí a ostrovem
            dx = ostrov["x"] - (pozice_lode_x + velikost_lode_x / 2)
            dy = ostrov["y"] - (pozice_lode_y + velikost_lode_y / 2)
            vzdalenost = math.hypot(dx, dy)
            
            # Poloměr kolize (průměr elipsy)
            polomer_kolize = (sirka_elipsy + vyska_elipsy) / 4
            
            # Změní se barva elipsy podle kolize
            if vzdalenost < polomer_kolize + 50:
                if nazev == "shop_ostrov":
                    barva_elipsy = (0, 255, 0)  # Zelená u shopu když je blízko
                else:
                    barva_elipsy = (255, 0, 0)  # Červená u ostatních ostrovů když je blízko
            else:
                barva_elipsy = (100, 150, 200)  # Modrá normálně
            
            pygame.draw.ellipse(okno, barva_elipsy, (stred_x - sirka_elipsy // 2, stred_y - vyska_elipsy // 2, sirka_elipsy, vyska_elipsy), 2)
            
            # Obrázek ostrova
            okno.blit(obrazek_ostrovu, (pozice_x, pozice_y))


        if vzdalenost < polomer_kolize + 50 and nazev == "shop_ostrov":
            text_shop = font.render("Press E to enter shop", True, (255, 255, 255))
            okno.blit(text_shop, (stred_x - text_shop.get_width() // 2, stred_y - vyska_elipsy // 2 - 30))
        
        if vzdalenost < polomer_kolize + 50 and nazev == "shop_ostrov":
            if stisknuto[pygame.K_e]:
                hra = False
                shop = True


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
        zlato_text = zlato_font.render(f"Gold: {aktualni_zlato}/{maximalni_unosnost_zlata}", True, (255, 215, 0))
        okno.blit(zlato_text, (20, 720))
        posatky_text = posatky_font.render(f"Crew: {aktualni_posatky}/{maximalni_pocet_posatky}", True, (255, 255, 255))
        okno.blit(posatky_text, (200, 720))

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
        # Podklad mapy a její hranice
        mapa_x_offset = 50
        mapa_y_offset = 50
        mapa_sirka = mapa_background.get_width()
        mapa_vyska = mapa_background.get_height()
        mapa_inset = 100
        mapa_rect = pygame.Rect(
            mapa_x_offset + mapa_inset,
            mapa_y_offset + mapa_inset,
            mapa_sirka - mapa_inset * 2,
            mapa_vyska - mapa_inset * 2,
        )
        stred_mapa_x = mapa_rect.centerx
        stred_mapa_y = mapa_rect.centery
        
        okno.blit(mapa_background, (mapa_x_offset, mapa_y_offset))
        
        # Modrá plocha je přímo na obrázku mapy, ne pod ním
        pygame.draw.rect(okno, (13, 55, 102), mapa_rect)
        
        # Všechny prvky mapy kreslit jen uvnitř mapového panelu
        predchozi_clip = okno.get_clip()
        okno.set_clip(mapa_rect)
        
        # Škálování - mapa je 5000x5000 světových jednotek
        skala_x = mapa_rect.width / MAPA_SIRKA
        skala_y = mapa_rect.height / MAPA_VYSKA
        
        # Vykreslení ostrovů na mapě
        for ostrov in ostrov_spawn:
            nazev = ostrov["nazev"]
            data_ostrovu = next((o for o in vyber_ostrovu if o["nazev"] == nazev), None)
            if data_ostrovu:
                # Ostrovy se pohybují podle pozice lodě, hráč zůstává uprostřed mapy
                mapa_ostrov_x = stred_mapa_x + (ostrov["x"] - pozice_lode_x) * skala_x
                mapa_ostrov_y = stred_mapa_y + (ostrov["y"] - pozice_lode_y) * skala_y
                
                # Zvětšený obraz ostrova na mapě (30% původní velikosti)
                obrazek_ostrovu_mala = data_ostrovu["obrazek"]
                sirka_ostrova = int(obrazek_ostrovu_mala.get_width() * 0.3)
                vyska_ostrova = int(obrazek_ostrovu_mala.get_height() * 0.3)
                
                if sirka_ostrova > 0 and vyska_ostrova > 0:
                    obrazek_ostrovu_scaled = pygame.transform.scale(obrazek_ostrovu_mala, (sirka_ostrova, vyska_ostrova))
                    okno.blit(obrazek_ostrovu_scaled, (mapa_ostrov_x - sirka_ostrova // 2, mapa_ostrov_y - vyska_ostrova // 2))
        
        # Vykreslení šipky hráče v centru mapy
        # Šipka ukazuje stejný směr jako loď v herním okně
        sirka_sipky = 15
        vyska_sipky = 25
        radiany = math.radians(uhel_kompasu)
        cos_a = math.cos(radiany)
        sin_a = math.sin(radiany)
        
        bod1 = (stred_mapa_x + sin_a * vyska_sipky, stred_mapa_y - cos_a * vyska_sipky)  # Špička
        bod2 = (stred_mapa_x - sin_a * 5 - cos_a * sirka_sipky / 2, stred_mapa_y + cos_a * 5 - sin_a * sirka_sipky / 2)
        bod3 = (stred_mapa_x - sin_a * 5 + cos_a * sirka_sipky / 2, stred_mapa_y + cos_a * 5 + sin_a * sirka_sipky / 2)
        
        pygame.draw.polygon(okno, (220, 30, 30), [bod1, bod2, bod3])  # Červená šipka
        pygame.draw.circle(okno, (255, 255, 255), (int(stred_mapa_x), int(stred_mapa_y)), 3)  # Bílý střed
        
        okno.set_clip(predchozi_clip)
        
        okno.blit(mapa_exit, (OKNO_sirka - 180, 630))
        if mapa_exit_rect.collidepoint(mys_pozice):
            okno.blit(mapa_exit_vetsi, (OKNO_sirka - 185, 625))
    
    

    pygame.display.flip()
    clock.tick(60)
    

    while shop:
        mouse_click_shop = False
        mys_pozice_shop = pygame.mouse.get_pos()
        stisknuto_shop = pygame.key.get_pressed()
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if udalost.type == pygame.MOUSEBUTTONDOWN and udalost.button == 1:
                mouse_click_shop = True

        if stisknuto_shop[pygame.K_ESCAPE]:
            shop = False
            hra = True

        okno.fill((17, 24, 35))

        prekryv = pygame.Surface((OKNO_sirka, OKNO_vyska), pygame.SRCALPHA)
        prekryv.fill((0, 0, 0, 120))
        okno.blit(prekryv, (0, 0))

        ramec = pygame.Rect(70, 40, OKNO_sirka - 140, OKNO_vyska - 80)
        pygame.draw.rect(okno, (33, 45, 60), ramec, border_radius=18)
        pygame.draw.rect(okno, (179, 145, 73), ramec, 4, border_radius=18)

        titul = pygame.font.Font("pirat_font.ttf", 40).render("Shipyard Shop", True, (245, 232, 198))
        okno.blit(titul, (OKNO_sirka // 2 - titul.get_width() // 2, 58))

        podtitul = font.render("Buy stronger ships and upgrade your crew capacity", True, (220, 220, 220))
        okno.blit(podtitul, (OKNO_sirka // 2 - podtitul.get_width() // 2, 108))

        stav_text = zlato_font.render(f"Gold: {aktualni_zlato}", True, (255, 215, 0))
        okno.blit(stav_text, (100, 155))
        lod_text = font.render(f"Current ship: {aktualni_lod['nazev']}", True, (255, 255, 255))
        okno.blit(lod_text, (100, 190))

        shop_lodi = [lod_informace[1], lod_informace[2]]
        karta_sirka = 470
        karta_vyska = 460
        zacatek_x = 110
        mezera = 80
        karta_y = 250

        for index, lod in enumerate(shop_lodi):
            karta_x = zacatek_x + index * (karta_sirka + mezera)
            karta = pygame.Rect(karta_x, karta_y, karta_sirka, karta_vyska)
            pygame.draw.rect(okno, (25, 34, 48), karta, border_radius=16)
            pygame.draw.rect(okno, (110, 92, 48), karta, 3, border_radius=16)

            nazev = zlato_font.render(lod["nazev"].replace("_", " ").title(), True, (245, 232, 198))
            okno.blit(nazev, (karta.centerx - nazev.get_width() // 2, karta.y + 18))

            obrazek = pygame.transform.scale(lod["obrazek"], (180, 180))
            okno.blit(obrazek, (karta.centerx - obrazek.get_width() // 2, karta.y + 55))

            ceny_text = font.render(f"Price: {lod['cena']} gold", True, (255, 215, 0))
            okno.blit(ceny_text, (karta.x + 22, karta.y + 250))

            staty = [
                f"Speed: {lod['rychlost']}",
                f"Crew: {lod['pocet_posatky']} / {lod['maximalni_pocet_posatky']}",
                f"Gold hold: {lod['maximalni_unosnost_zlata']}",
            ]

            for radek_index, radek in enumerate(staty):
                stat_text = font.render(radek, True, (230, 230, 230))
                okno.blit(stat_text, (karta.x + 22, karta.y + 285 + radek_index * 28))

            if lod["nazev"] == aktualni_lod["nazev"]:
                btn_text = "Active"
                btn_barva = (70, 140, 90)
            elif zakoupene_lodi.get(lod["nazev"], False):
                btn_text = "Use ship"
                btn_barva = (95, 120, 170)
            elif aktualni_zlato >= lod["cena"]:
                btn_text = "Buy"
                btn_barva = (160, 120, 40)
            else:
                btn_text = "Not enough gold"
                btn_barva = (110, 70, 70)

            btn = pygame.Rect(karta.x + 22, karta.bottom - 62, karta.width - 44, 42)
            pygame.draw.rect(okno, btn_barva, btn, border_radius=10)
            btn_label = font.render(btn_text, True, (255, 255, 255))
            okno.blit(btn_label, (btn.centerx - btn_label.get_width() // 2, btn.centery - btn_label.get_height() // 2))

            if mouse_click_shop and btn.collidepoint(mys_pozice_shop):
                if lod["nazev"] == aktualni_lod["nazev"]:
                    pass
                elif not zakoupene_lodi.get(lod["nazev"], False) and aktualni_zlato >= lod["cena"]:
                    aktualni_zlato -= lod["cena"]
                    zakoupene_lodi[lod["nazev"]] = True
                    nastav_aktualni_lod(lod)
                elif zakoupene_lodi.get(lod["nazev"], False):
                    nastav_aktualni_lod(lod)

        info = font.render("ESC = back to sea", True, (230, 230, 230))
        okno.blit(info, (OKNO_sirka - info.get_width() - 110, OKNO_vyska - 60))

        pygame.display.flip()
        clock.tick(60)