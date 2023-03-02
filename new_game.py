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
        img = pg.image.load('spiller.png')
        self.image = pg.transform.scale(img, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
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

#Hello, ser du dette?
#NO
