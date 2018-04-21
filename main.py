import pygame,sys
from pygame.locals import *
import puzzlemap

pygame.init()
fpsClock = pygame.time.Clock()

# window surface object
wsurfo = pygame.display.set_mode((270,270))
pygame.display.set_caption("Puzzle")

# colors
red    = pygame.Color(255,123,123)
blue   = pygame.Color(125,148,224)
yellow = pygame.Color(255,219,127)
backg  = pygame.Color(110,110,110)
line   = pygame.Color(62,62,62)
black  = pygame.Color(0,0,0)
white  = pygame.Color(255, 255, 255)

# base class
class Square(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([26,26])
        self.image.fill(color)

        self.coordx = x
        self.coordy = y

        self.rect = self.image.get_rect()
        self.rect.x = 2 + (30 * x)
        self.rect.y = 2 + (30 * y)

# wall class
class Wall(Square):
    def __init__(self, x, y):
        Square.__init__(self, black, x, y)

class Goal(Square):
    def __init__(self, x, y):
        Square.__init__(self, blue, x, y)

#player class
class Player(Square):
    def __init__(self, x, y):
        Square.__init__(self, red, x, y)

    def update(self, x=None, y=None):
        if x: self.coordx = x
        if y: self.coordy = y
        if self.coordx < 0: self.coordx = 0
        if self.coordy < 0: self.coordy = 0
        if self.coordx > 8: self.coordx = 8
        if self.coordy > 8: self.coordy = 8
        self.rect.x = 2 + (30 * self.coordx)
        self.rect.y = 2 + (30 * self.coordy)

    def move(self, direction):
        if not direction:
            return
        if direction == 'n':
            self.coordy -= 1
        elif direction == 's':
            self.coordy += 1
        elif direction == 'e':
            self.coordx += 1
        elif direction == 'w':
            self.coordx -= 1
        self.update()


# board
def draw_board():
    # each square is 26x26

    #lines
    w = 30
    for i in range(0,10):
        pygame.draw.line(wsurfo, line, (0,i*w-1), (300, i*w-1), 4)
        pygame.draw.line(wsurfo, line, (i*w-1, 0), (i*w-1, 300), 4)        

# pre game
entities = pygame.sprite.Group()
player = ""
#currmap = [row[:] for row in puzzlemap.level1]

# map stuff
x = y = 0
for row in puzzlemap.level1:
    for ent in row:
        if ent == 2:
            wall = Wall(x, y)
            entities.add(wall)
        elif ent == 3:
            goal = Goal(x,y)
            entities.add(goal)
        elif ent == 1:
            player = Player(x, y)
        x += 1
    x = 0
    y += 1


entities.add(player)

move = '' # n, s, e, w

# game loop
while True:
    wsurfo.fill(backg)
    draw_board()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                move = 'n'
            elif event.key == K_DOWN:
                move = 's'
            elif event.key == K_RIGHT:
                move = 'e'
            elif event.key == K_LEFT:
                move = 'w'
    
    player.move(move)
    # check collision
    for ent in entities:
        if ent == player:
            continue
        if (player.coordx, player.coordy) == (ent.coordx, ent.coordy):
            if isinstance(ent, Goal):
                entities.draw(wsurfo)
                pygame.display.update()
                pygame.quit()
                sys.exit()
            elif isinstance(ent, Wall):
                if move=='n': player.move('s')
                elif move=='s': player.move('n')
                elif move=='e': player.move('w')
                elif move=='w': player.move('e')

    move = ''
    entities.draw(wsurfo)
    pygame.display.update()
    fpsClock.tick(30)