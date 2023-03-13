import pygame as pg
from pygame.locals import *
import pickle


pg.init() 


global WIDTH, HEIGHT
WIDTH = 1400
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
surface = pg.display.set_mode(SIZE)
font_score = pg.font.SysFont('Bauhaus 93', 30)


FPS = 60
clock = pg.time.Clock()
tile_size = 70 # Deler inn skjermen i mange kvadrater, hver av sidene i kvadratene har lengde 70
game_over = 0 # Lager en funksjon som brukes når avataren dør
start_menu = True # Definerer start_menu som True, slik at vi får opp startmenyen når man kjører koden


bb = pg.image.load('background.png')
restart_img = pg.image.load('restart.png') # Hentet fra https://opengameart.org/content/ultimate-timeracer-button-pack
start_img = pg.image.load('start.png') # Hentet fra https://opengameart.org/content/ultimate-timeracer-button-pack
exit_img = pg.image.load('exit.png') # Hentet fra https://opengameart.org/content/ultimate-timeracer-button-pack
#level = 1
score = 0
white = (255, 255, 255)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surface.blit(img, (x,y))


def draw_grid():
    for line in range (0, 20): # Definerer antallet kolonner med blokker vi vil dele inn skjermen i
        pg.draw.line(surface, (225, 255, 255), (0, line * tile_size), (WIDTH, line * tile_size))
        pg.draw.line(surface, (225, 255, 255), (line * tile_size, 0), (line * tile_size, HEIGHT))


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        
        
    def draw(self):
        action = False
        
        # Tegner knappen
        surface.blit(self.image, self.rect)
        
        # Henter musen sin posisjon
        pos = pg.mouse.get_pos()
        
        # Sjekker om musen er over og trykker på knappen
        if self.rect.collidepoint(pos):
            
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        
        # Null betyr at tasten er sluppet igjen
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return action
                
    
class Player():
    def __init__(self, x, y):
        self.reset(x, y)                                    


    def update(self, game_over): # Legger inn game_over som et argument i update-funksjonen, siden det er en global variabel
        # Delta x og delta yx
        dx = 0
        dy = 0
        walk_cooldown = 10 # Bestemmer hvor fort bildene skifter
        
        
        if game_over == 0:
            # Legger inn bevegelse for tastene
            key = pg.key.get_pressed()
            
            if key[pg.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y  = -15
                self.jumped = True
            
            if key[pg.K_SPACE] == False:
                self.jumped = False
            
            if key[pg.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1                                 
            
            if key[pg.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1                                  
            
            # Gjør at det er bildet hvor avataren står stille som vises, dersom han står stille   
            if key[pg.K_LEFT] == False and key[pg.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                
                if self.direction == 1:                             
                    self.image = self.image_right[self.index]
                
                if self.direction == -1:                            
                    self.image = self.image_left[self.index]

            # Animasjon
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                
                if self.index >= len(self.image_right):
                    self.index = 0
                
                if self.direction == 1:                             
                    self.image = self.image_right[self.index]
                
                if self.direction == -1:                           
                    self.image = self.image_left[self.index]

            # Legger til gravitasjonskraft
            self.vel_y += 0.75
            
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
            
            self.in_air = True 
            # Sjekker for kollisjoner mellom avataren og blokkene
            for tile in world.tile_list:

                # Man må sjekke for kollisjon i x- og i y-retning hver for seg for å få ønskelig resultat
                # Sjekker for kollisjon i x-retningen
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height): # dx er x-avstanden avataren skal flytte seg
                    dx = 0 # Dersom avataren kolliderer med en blokk i x-retning, blir farten lik 0, så man ikke kan gå gjennom blokken

                # Sjekker for kollisjon i y-retningen
                # Bruker colliderect()-funksjonen fordi alle objektene er rektangler
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): # dy er y-avstanden avataren skal flytte seg
                    # Sjekker om avataren treffer blokken fra oversiden eller undersiden

                    if self.vel_y < 0:# Hvis avataren har en negativ y-fart, betyr det at den hopper opp og treffer blokken fra undersiden
                        # dy, avstanden avataren kan flytte seg før det blir en kollisjon, må være avstanden mellom avatarens hode og bunnen av blokken
                        dy = tile[1].bottom - self.rect.top 
                        self.vel_y = 0 # Endrer y-farten til 0 så avataren faller rett ned igjen, og ikke blir "hengende" i lufta

                    elif self.vel_y >= 0:# Hvis avataren har en positiv y-fart, betyr det at den faller ned og treffer blokken fra oversiden
                        # Her er dy avstanden mellom avatarens bein og toppen av blokken
                        dy = tile[1].top - self.rect.bottom
                        self.in_air = False


            # Sjekker for kollisjon mellom spilleren (self) og hver av lava-blokkene (som alle ligger i lava-group)
            if pg.sprite.spritecollide(self, lava_group, False):
                game_over -= 1
                # print(game_over) Brukte dette i starten for å se koden fungerte, og kollisjonene ble registrert

            self.rect.x += dx
            self.rect.y += dy
            
            if pg.sprite.spritecollide(self, exit_group, False):
                game_over = 1
            
        elif game_over == -1: # Hvis game_over = -1, betyr det at man har dødd
            self.image = self.dead_image # I såfall er det et annet bilde av avataren som vises
            if self.rect.y > -800:
                self.rect.y -= 5 # Avataren "flyter" opp til toppen av skjermen og ut av bildet

# Kanskje det skal skje noe annet med ham når han dør?
# I videoen blir avataren et spøkelse, så da passer det jo fint at han "flyter" til toppen
            
            """if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
                dy = 0""" # Brukte denne i starten, så ikke avataren skulle falle ned gjennom bunnen av skjermen 
        
        surface.blit(self.image, self.rect)
        pg.draw.rect(surface, (255, 255, 255), self.rect, 2)# Tegner rektangelet som utgjør omrisset rundt spillavataren, synliggjør kollisjonene
        
        return game_over # Returnerer en evt. ny verdi for game_over-variablen, som hvis avataren treffer lavaen
        
        
    def reset(self, x, y):
        self.image_right = []
        self.image_left = []
        self.index = 0
        self.counter = 0
        
        for i in range(1,3):
            img_right = pg.image.load(f'Zombie0{i}.png')
            img_right = pg.transform.scale(img_right, (100,100))
            img_left = pg.transform.flip(img_right, True, False)
            self.image_right.append(img_right)
            self.image_left.append(img_left)
        
        self.dead_image = pg.image.load('Dead_Zombie01.png') # Fant dette bildet på https://opengameart.org/content/zombie-character
        self.image = self.image_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width() 
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True # Kan ikke hoppe flere ganger på rad
       
       
class World():
    def __init__(self, data):
        
        self.tile_list = []

        jordblokk = pg.image.load('dirt_tile_08.png')
        gress = pg.image.load('dirt_tile_06.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            
            for tile in row:
                if tile == 1:
                    img = pg.transform.scale(jordblokk, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count*tile_size
                    img_rect.y = row_count*tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                
                if tile == 2:
                    img = pg.transform.scale(gress, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count*tile_size
                    img_rect.y = row_count*tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                
                if tile == 3:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size//2)) # Pluss for at den skal ligge på bunnen
                    lava_group.add(lava)
                
                if tile == 4:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size))
                    exit_group.add(exit)
                
                if tile == 5:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size//2)) 
                    coin_group.add(coin)
                col_count += 1
            row_count += 1
            
            
    def draw(self):
        for tile in self.tile_list:
            surface.blit(tile[0], tile[1])
            pg.draw.rect(surface, (255, 255, 255), tile[1], 2) # Tegner omrisset rundt alle blokkene, synliggjør kollisjoner
            
    
class Lava(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self) # Legger til objekter i spill
        img = pg.image.load('Lava.png') # Hentet fra https://opengameart.org/content/2-seamless-lava-tiles 
        self.image = pg.transform.scale(img, (tile_size, tile_size//2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        
class Coin(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self) # Legger til objekter i spill
        img = pg.image.load('coin.png') # Hentet fra https://opengameart.org/content/2-seamless-lava-tiles 
        self.image = pg.transform.scale(img, (tile_size//2, tile_size//2))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y) #gjør at vi posisjonerer fra midtpunktet av mynten


class Exit(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self) # Legger til objekter i spill
        img = pg.image.load('next.png') # Hentet fra https://opengameart.org/content/2-seamless-lava-tiles 
        self.image = pg.transform.scale(img, (tile_size + tile_size//2, int(tile_size * 2)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# 0 = tom
# 1 = dirt-kloss
# 2 = dirt-kloss med gress
# 3 = lava
# 4 = dør
# 5 = mynter

world_data =[
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 4, 0],
[2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 3, 3, 3, 3, 2, 0, 0, 0, 2, 2],
[2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1],
]


player = Player(100, HEIGHT - 300)
lava_group = pg.sprite.Group()
coin_group = pg.sprite.Group()
exit_group = pg.sprite.Group()


# Vi kan bruke dette senere når vi skal lage flere leveler
# Henter data fra mappen med leveler
# Pickle_in = open(caroline1_data, 'rb')
# World_data = pickle.load(pickle_in)
world = World(world_data) 


# Lager knappene
restart_button = Button(WIDTH //2 - 550, HEIGHT // 4 , restart_img)
start_button = Button(WIDTH //2 - 550, HEIGHT // 4, start_img)
exit_button = Button(WIDTH //2 + 175, HEIGHT // 4, exit_img)


run = True
while run == True:
    
    clock.tick(FPS)
    
    surface.blit(bb, (0, 0))
    
    if start_menu == True:
        
        if exit_button.draw() == True:
            run = False
        
        if start_button.draw() == True:
            start_menu = False
    
    else: 
        world.draw()
        
        lava_group.draw(surface)
        coin_group.draw(surface)
        exit_group.draw(surface)
        
        if game_over == 0:                                                                 
            
            #sjekker om en mynt har blitt tatt
            if pg.sprite.spritecollide(player, coin_group, True):
                score += 1
            draw_text('Poeng: ' + str(score), font_score, white, tile_size - 10, 10)
        
        gamer_over = player.update(game_over)
        
        # Hvis avataren dør
        if game_over == -1:
            
            if exit_button.draw() == True: # Tegner exit-knappen for å kunne avslutte spillet
                run = False # Hvis knappen trykkes på, endres run-variablen til False, og spillet avsluttes
            
            if restart_button.draw() == True: # Tegner reset-knappen så man kan starte spillet på nytt
                player.reset(100, HEIGHT - 300)
                game_over = 0 # Endrer game_over-variablen til 0 igjen, så spillet kjøres fra begynnelsen
                score = 0
        
        #Hvis spiller har gjort ferdig ett level
        if game_over == 1:
            #level += 1
            run = False
            
        """
            if level <= max_levels:
                pass
            else:
                pass
        """ 
        game_over = player.update(game_over) # Ny verdi for game_over-funksjonen
        draw_grid()
    
    
    #print(world.tile_list)
    
    for event in pg.event.get():
        
        if event.type == pg.QUIT:
            run = False
    pg.display.update()
    
    
pg.quit()
