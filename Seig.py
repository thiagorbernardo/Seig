import sys     # let  python use your file system
import os      # help python identify your OS
import pygame  # load pygame keywords
import random

#Objects

##############################################################################################
class Player(pygame.sprite.Sprite): #Spawn Players
    def __init__(self):
        self.health = 100
        self.score = 1
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.images = []
        for i in range(1,3):
            img = pygame.image.load(os.path.join('images','hero' + str(i) + '.png')).convert()
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            self.images.append(img)
            self.image = self.images[0]
            self.rect  = self.image.get_rect()

    def control(self,x,y):
        '''
        control player movement
        '''
        self.movex += x
        aux = self.movey
        self.movey += y
        if(aux>= self.movey):
            self.gravity()

    def update(self):
        '''
        Update sprite position
        '''

        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        # moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame >= 2*CYCLES:
                self.frame = 0
            self.image = self.images[self.frame//CYCLES]

        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame >= 2*CYCLES:
                self.frame = 0
            self.image = self.images[self.frame//CYCLES]

        #COLLISIONS
        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in hit_list:
            self.health -= 1
            self.isAlive()
        
        ground_hit_list = pygame.sprite.spritecollide(self, ground_list, False)
        for g in ground_hit_list:
            self.health -= 1
            self.isAlive()
            print(self.health)

    def isAlive(self):
        if(self.health == 0):
                print('YOU LOSE')
                pygame.quit()
                sys.exit()
                main = False
                print(self.health)

        
    def gravity(self):
        self.movey += 0.03 # how fast player falls
        if self.rect.y > WORLDY/2 and self.movey >= 0:
            self.movey = 0
            self.rect.y = WORLDY/2

class Enemy(pygame.sprite.Sprite):
    '''
    Spawn an enemy
    '''
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images',img))
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0 # counter variable

    def move(self):
        '''
        enemy movement
        '''
        distance = 30
        speed = 1

        if self.counter >= 0 and self.counter <= distance:
            self.rect.x += speed
        elif self.counter >= distance and self.counter <= distance*2:
            self.rect.x -= speed
        else:
            self.counter = 0

        self.counter += 1

class Level():
    def bad(lvl,eloc):
        if lvl == 1:
            enemy = Enemy(eloc[0],eloc[1],'enemy.png') # spawn enemy
            enemy_list = pygame.sprite.Group() # create enemy group
            enemy_list.add(enemy)              # add enemy to group
        if lvl == 2:
            print("Level " + str(lvl) )

        return enemy_list
    def loot(lvl,lloc):
        print(lvl)

    def ground(lvl,gloc,tx,ty):
        ground_list = pygame.sprite.Group()
        i=0
        if lvl == 1:
            while i < len(gloc):
                ground = Platform(gloc[i],WORLDY-ty,tx,ty,'ground.png')
                ground_list.add(ground)
                i=i+1

        if lvl == 2:
            print("Level " + str(lvl) )

        return ground_list

    def platform(lvl,tx,ty):
        plat_list = pygame.sprite.Group()
        ploc = []
        i=0
        if lvl == 1:
            """ploc.append((0,WORLDY-ty-128,3))
            ploc.append((300,WORLDY-ty-256,3))
            ploc.append((500,WORLDY-ty-128,4))"""

            while i < len(ploc):
                j=0
                while j <= ploc[i][2]:
                    plat = Platform((ploc[i][0]+(j*tx)),ploc[i][1],tx,ty,'ground.png')
                    plat_list.add(plat)
                    j=j+1
                print('run' + str(i) + str(ploc[i]))
                i=i+1

        if lvl == 2:
            print("Level " + str(lvl) )

        return plat_list #isso aqui eu faço quando tiver o mapa completo

class Platform(pygame.sprite.Sprite):
    # x location, y location, img width, img height, img file    
    def __init__(self,xloc,yloc,imgw,imgh,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images',img)).convert()
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc
####################################################################################################
#Setup

ALPHA = (255, 255, 255)
WORLDX = 800
WORLDY = 600

FPS = 60        # frame rate
CYCLES = 3       # animation CYCLES
CLOCK = pygame.time.Clock()
pygame.init()
main = True

WORLD = pygame.display.set_mode([WORLDX,WORLDY])
BACKDROP = pygame.image.load(os.path.join('images','stage.png')).convert()
BACKDROPBOX = WORLD.get_rect()

player = Player()   # spawn player
player.rect.x = WORLDX/2
player.rect.y = WORLDY/2
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 3     # how fast to move

eloc = []
eloc = [WORLDX/2 + 100,WORLDY/2]
gloc = []

tx = 64 #tile size
ty = 64 #tile size

i=0
while i <= (WORLDX/tx)+tx:
    gloc.append(i*tx)
    i=i+1

enemy_list = Level.bad( 1, eloc )
ground_list = Level.ground( 1,gloc,tx,ty )
plat_list = Level.platform( 1,tx,ty )
##################################################################################################
'''
Main loop
'''
while main == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   
            pygame.quit()
            sys.exit()
            main = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-steps,0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(steps,0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.control(0,-steps)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(steps,0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-steps,0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.control(0,steps)
            if event.key == ord('m'):
                pygame.quit()
                sys.exit()
                main = False

    WORLD.blit(BACKDROP, BACKDROPBOX)
    player.gravity() # check gravity
    player.update()
    player_list.draw(WORLD) #refresh player position
    enemy_list.draw(WORLD)  # refresh enemies
    ground_list.draw(WORLD)
    plat_list.draw(WORLD)
    for e in enemy_list:
        e.move()
    pygame.display.flip()
    CLOCK.tick(FPS)