import pygame as pg
from pygame.locals import *

pg.init() 

global WIDTH, HEIGHT
WIDTH = 1400
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
surface = pg.display.set_mode(SIZE)


FPS = 60
clock = pg.time.Clock()
tile_size = 100

bb = pg.image.load('bakgrunn.png')

def draw_grid():
    for line in range (0, 14):
        pg.draw.line(surface, (225, 255, 255), (0, line * tile_size), (WIDTH, line * tile_size))
        pg.draw.line(surface, (225, 255, 255), (line * tile_size, 0), (line * tile_size, HEIGHT))

class Player():
    def __init__(self, x, y):
        self.image_right = []
        self.image_left = []
        self.index = 0
        self.counter = 0
        for i in range(1,3):
            img_right = pg.image.load(f'Zombie0{i}.png')
            img_right = pg.transform.scale(img_right(100,100))
            img_left = pg.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        
        self.image = self.image_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 0                                      #Vi kan også bruke andre navn på variabelen, så blir det større forskjell

    def update(self):
        #delta x og delta y
        dx = 0
        dy = 0
        walk_cooldown = 20 # Må skje 20 ganger før animasjonen endres(?) ca. 10 min inn i del 3 av tutorialen
        
        key = pg.key.get_pressed()
        if key[pg.K_SPACE] and self.jumped == False:
            self.vel_y  = -15
            self.jumped = True
        if key[pg.K_SPACE] == False:
            self.jumped = False
        if key[pg.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1                                 #Vi kan også bruke andre navn på variabelen, så blir det større forskjell
        if key[pg.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1                                  #Vi kan også bruke andre navn på variabelen, så blir det større forskjell
        #Gjør at det er bildet hvor avataren står stille som vises, dersom han står stille   
        if key[pg.K_LEFT] == False and key[pg.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:                             #Vi kan også bruke andre navn på variabelen, så blir det større forskjell
                self.image = self.images_right[self.index]
            if self.direction == -1:                            #Vi kan også bruke andre navn på variabelen, så blir det større forskjell
                self.image = self.images_left[self.index]
        
        #Animasjon
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
                if self.index >= len(self.images_right):
            self.index = 0
            if self.direction == 1:                             #Vi kan også bruke andre navn på variabelen, så blir det større forskjell
                self.image = self.images_right[self.index]
            if self.direction == -1:                            #Vi kan også bruke andre navn på variabelen, så blir det større forskjell
                self.image = self.images_left[self.index]
        
        #legger til gravitasjon
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        
        dy += self.vel_y
        
        self.rect.x += dx
        self.rect.y += dy
        
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            dy = 0
        
        surface.blit(self.image, self.rect)

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
                
                col_count += 1
            row_count += 1
            
    def draw(self):
        for tile in self.tile_list:
            surface.blit(tile[0], tile[1])
            

world_data =[
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

player = Player(100, HEIGHT - 300)
world = World(world_data)


run = True
while run == True:
    
    clock.tick(FPS)
    
    surface.blit(bb, (0, 0))
    
    world.draw()
    player.update()
    draw_grid()
    
    
    #print(world.tile_list)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    pg.display.update()
            
pg.quit()

