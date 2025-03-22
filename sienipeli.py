import pygame
import sys
import random
import os

# Alustetaan Pygame
pygame.init()

# Näytön koko
naytto = pygame.display.set_mode((1920, 1000))
pygame.display.set_caption("Sienipeli")

# Eri kokosia fontteja
ohje_fontti = pygame.font.SysFont("comic sans ms", 20)
laskuri_fontti = pygame.font.SysFont("comic sans ms", 30)
fontti = pygame.font.SysFont("comic sans ms", 40)

# Määritä kuvien polku
kuvat_kansio = os.path.join(os.path.dirname(__file__), 'kuvat')

# Ladataan kuvat
kanttarelli = pygame.image.load(os.path.join(kuvat_kansio, 'kanttarelli.png'))
tatti = pygame.image.load(os.path.join(kuvat_kansio, 'tatti.png'))
kori = pygame.image.load(os.path.join(kuvat_kansio, 'kori.png'))
tuhkelo = pygame.image.load(os.path.join(kuvat_kansio, 'tuhkelo.png'))
myrkky = pygame.image.load(os.path.join(kuvat_kansio, 'kärpässieni.png'))
tausta = pygame.image.load(os.path.join(kuvat_kansio, 'tausta.png'))

# Haetaan suorakulmiot
kanttarelli_rect = kanttarelli.get_rect()
tatti_rect = tatti.get_rect()
kori_rect = kori.get_rect()
tuhkelo_rect = tuhkelo.get_rect()
myrkky_rect = myrkky.get_rect()

kello = pygame.time.Clock()

# Korin alku koordinaatit
kori_x = 0
kori_y = 1000 - kori_rect.height

# Alustus korin liikkeelle
oikealle = False
vasemmalle = False

# Pelin tila
peli_kaynnissa = True
peli_voitto = False

# Ohjeet näkyville
ohjeet_nakyy = False

# Pisteet
pisteet = 0
taso_pisteet = 500

# Taso
taso = 1
max_taso = 10

# Sienille Luokka
class Sieni:
    def __init__(self, kuva, rect, pisteet, vaikeus):
        self.kuva = kuva
        self.rect = rect.copy()
        self.rect.x = random.randint(0, 1920 - self.rect.width)
        self.rect.y = 0
        self.nopeus = random.choice([-2, 2])
        self.osunut_maahan = False
        self.pisteet = pisteet
        self.vaikeus = vaikeus
        
    # Sienten liike
    def liiku(self):
        if not self.osunut_maahan:
            self.rect.y += 2 + self.vaikeus * 0.5  # Lisää nopeutta vaikeuden mukaan
            if self.rect.y + self.rect.height >= 1000:
                return False  # Sieni poistetaan, kun se osuu maahan
        return True  
    
class MyrkkySieni(Sieni):
    def __init__(self, kuva, rect, vaikeus):
        super().__init__(kuva, rect, 0, vaikeus)

# Yhdistetty muuttujat että saadaan uusi peli helpommin alustettua 
def uusi_peli():
    global kori_x, kori_y, oikealle, vasemmalle, sienet, kanttarelli_laskuri, tatti_laskuri, tuhkelo_laskuri, myrkky_laskuri, pisteet, peli_kaynnissa, taso, taso_pisteet
    kori_x = 0
    kori_y = 1000 - kori_rect.height
    oikealle = False
    vasemmalle = False
    
    sienet = []
    
    kanttarelli_laskuri = 0
    tatti_laskuri = 0
    tuhkelo_laskuri = 0
    myrkky_laskuri = 0
    
    pisteet = 0
    taso = 1

    taso_pisteet = 500
    
    peli_kaynnissa = True
    peli_voitto = False
    
    ohjeet_nakyy = False

   
uusi_peli()
# Pääsilmukka
while True:
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # Näppäinten tapahtumat 
        if peli_kaynnissa:
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    oikealle = True
                if tapahtuma.key == pygame.K_i:
                    ohjeet_nakyy = True
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    oikealle = False
                if tapahtuma.key == pygame.K_i:
                    ohjeet_nakyy = False
        else:
            if tapahtuma.type == pygame.KEYDOWN and tapahtuma.key == pygame.K_RETURN:
                uusi_peli()

    if peli_kaynnissa:
        # Tason & pisteiden tarkastelu & kirjaus
        if pisteet >= taso_pisteet:
            taso_pisteet += 500
            taso += 1
            pisteet = 0
            if taso > max_taso:
                peli_kaynnissa = False  # Lopeta peli, jos maksimitaso saavutetaan
                peli_voitto = True  # Pelaaja voitti pelin
                
        # Kanttarellien ilmestyminen
        kanttarelli_laskuri += 1
        if kanttarelli_laskuri >= 60 + taso * 10:  # Säädä ilmestymistiheyttä tason mukaan
            sienet.append(Sieni(kanttarelli, kanttarelli_rect, 100, taso))
            kanttarelli_laskuri = 0

        # Tattien ilmestyminen
        tatti_laskuri += 1
        if tatti_laskuri >= 40 + taso * 10:  # Säädä ilmestymistiheyttä tason mukaan
            sienet.append(Sieni(tatti, tatti_rect, 50, taso))
            tatti_laskuri = 0

        # Tuhkeloiden ilmestyminen
        tuhkelo_laskuri += 1
        if tuhkelo_laskuri >= 30 + taso * 10:  # Säädä ilmestymistiheyttä tason mukaan
            sienet.append(Sieni(tuhkelo, tuhkelo_rect, 20, taso))
            tuhkelo_laskuri = 0

        # Myrkkysienten ilmestyminen
        myrkky_laskuri += 1
        if myrkky_laskuri >= 150 - taso * 12:  # Säädä ilmestymistiheyttä tason mukaan
            sienet.append(MyrkkySieni(myrkky, myrkky_rect, taso))
            myrkky_laskuri = 0

        # Poistetaan sienet, jotka menevät alareunan yli
        sienet = [sieni for sieni in sienet if sieni.liiku()]

        # Tarkistetaan, osuuko kori sieneen
        kori_rect.x = kori_x
        kori_rect.y = kori_y
        for sieni in sienet[:]:
            if kori_rect.colliderect(sieni.rect):
                if isinstance(sieni, MyrkkySieni):
                    peli_kaynnissa = False
                else:
                    pisteet += sieni.pisteet
                    sienet.remove(sieni)

        # Korin liike ruudun rajoissa
        if oikealle and kori_x + kori.get_width() < 1920:
            kori_x += 10
        if vasemmalle and kori_x > 0:
            kori_x -= 10
            
    # Ohjeet
    ohjeet_tuhkelo = ohje_fontti.render(f"Tuhkelo = 20 pistettä", True, (55, 245, 5)) 
    ohjeet_tatti = ohje_fontti.render(f"Tatti = 50 pistettä", True, (55, 245, 5))
    ohjeet_kanttarelli = ohje_fontti.render(f"Kanttarelli = 100 pistettä", True, (55, 245, 5))
    ohjeet_myrkky = ohje_fontti.render(f"Myrkkysieni = Häviät pelin", True, (255, 0, 0))
    ohjeet_taso = ohje_fontti.render(f"Taso (ja vaikeus) nousee pisteiden myötä", True, (55, 245, 5))
    ohjeet_info = ohje_fontti.render(f"Info (i) ", True, (55, 245, 5))
    ohjeet_liike = ohje_fontti.render(f"Liikuta koria <- & -> näppäimillä", True, (55, 245, 5))
    
    # Näyttö, tausta, kori & sienet piirretään
    naytto.fill((0, 0, 0))
    naytto.blit(tausta, (0, 0))
    naytto.blit(kori, (kori_x, kori_y))
    for sieni in sienet:
        naytto.blit(sieni.kuva, sieni.rect)
        
    # Ohjeet pelin aikana näkyviin (i)
    if ohjeet_nakyy:
            naytto.blit(ohjeet_liike, (0, 280 ))
            naytto.blit(ohjeet_tuhkelo, (0, 0 ))
            naytto.blit(tuhkelo, (220, 0))
            naytto.blit(ohjeet_tatti, (0, 50 ))
            naytto.blit(tatti, (190, 50))
            naytto.blit(ohjeet_kanttarelli, (0, 100 ))
            naytto.blit(kanttarelli, (250, 100))
            naytto.blit(ohjeet_myrkky, (0, 170 ))
            naytto.blit(myrkky, (260, 150 ))
            naytto.blit(ohjeet_taso, (0, 230 ))
    else:
        naytto.blit(ohjeet_info, (0, 0 ))

            
       

    # Näytetään pisteet & taso
    pisteet_teksti = laskuri_fontti.render(f"Pisteet: {pisteet}", True, (55, 245, 5))
    taso_teksti = laskuri_fontti.render(f"Taso: {taso}", True, (55, 245, 5))
    naytto.blit(pisteet_teksti, (1750, 0))
    naytto.blit(taso_teksti, (1750, 30))
    
    # Voitto & häviö tekstit
    if not peli_kaynnissa:
        if peli_voitto:
            peli_loppui_teksti = fontti.render("Onnittelut! Voitit pelin!", True, ((55, 245, 5)))
        else:
            peli_loppui_teksti = fontti.render("Peli päättyi! Keräsit myrkkysienen. Paina Enter aloittaaksesi uudelleen.", True, (255, 0, 0))
        naytto.blit(peli_loppui_teksti, (300, 450))

    pygame.display.flip()
    kello.tick(60)