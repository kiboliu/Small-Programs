import pygame, sys, os
from pygame.locals import *

def move_box(level, i):
    if level[i] == '-' or level[i] == '@':
        level[i] = '$'
    else:
        level[i] = '*'

def move_man(level, i):
    if level[i] == '-' or level[i] == '$':
        level[i] = '@'
    else:
        level[i] = '+'

def move_floor(level, i):
    if level[i] == '@' or level[i] == '$':
        level[i] = '-'
    else:
        level[i] = '.'

def get_offset(d, width):
    offset_map = {'l': -1, 'u': -width, 'r': 1, 'd': width}
    return offset_map[d.lower()]

#game map
class Sokoban:

    def __init__(self):
        #set a map:
        #"-" for space, "#" for wall, "@" for player
        #"$" for box, "." for target, "+" for player reach target, "*" for box reach target
        self.level = list(
            "----#####----------"
            "----#---#----------"
            "----#$--#----------"
            "--###--$##---------"
            "--#--$-$-#---------"
            "###-#-##-#---######"
            "#---#-##-#####--..#"
            "#-$--$----------..#"
            "#####-###-#@##--..#"
            "----#-----#########"
            "----#######--------")
        #column and row of map
        self.w = 19
        self.h = 11
        #initial staring point of player
        self.man = 163
        #record each move, for undo
        self.solution = []
        #record times of moving box
        self.push = 0
        #record undo, for redo
        self.todo = []

    #draw the map
    def draw(self, screen, skin):
        w = skin.get_width() / 4
        for i in range(0, self.w):
            for j in range(0, self.h):
                item = self.level[j * self.w + i]
                
                if item == '#':
                    screen.blit(skin, (i * w, j * w), (0, 2 * w, w, w))
                elif item == '-':
                    screen.blit(skin, (i * w, j * w), (0, 0, w, w))
                elif item == '@':
                    screen.blit(skin, (i * w, j * w), (w, 0, w, w))
                elif item == '$':
                    screen.blit(skin, (i * w, j * w), (2 * w, 0, w, w))
                elif item == '.':
                    screen.blit(skin, (i * w, j * w), (0, w, w, w))
                elif item == '+':
                    screen.blit(skin, (i * w, j * w), (w, w, w, w))
                elif item == '*':
                    screen.blit(skin, (i * w, j * w), (2 * w, w, w, w))
    
    #when move
    def move(self, d):
        self._move(d)
        #reset the redo list to empty, because redo can only be executed after redo
        self.todo = []
        
    #update each items after move
    def _move(self, d):
        
        h = get_offset(d, self.w)
        
        if self.level[self.man + h] == '-' or self.level[self.man + h] == '.':
            move_man(self.level, self.man + h)
            move_floor(self.level, self.man)
            self.man += h
            self.solution += d
            
        elif self.level[self.man + h] == '*' or self.level[self.man + h] == '$':
            #next place of box
            h2 = h * 2
            if self.level[self.man + h2] == '-' or self.level[self.man + h2] == '.':
                move_box(self.level, self.man + h2)
                move_man(self.level, self.man + h)
                move_floor(self.level, self.man)
                self.man += h
                #upper case show that box is being moved
                self.solution += d.upper()
                self.push += 1
    
    #undo a move
    def undo(self):
        if self.solution.__len__() > 0:
            #store the move action in the todo list
            self.todo.append(self.solution[-1])
            #delete
            self.solution.pop()
            
            h = get_offset(self.todo[-1], self.w) * -1
            
            # just a move of player
            if self.todo[-1].islower():
                move_man(self.level, self.man + h)
                move_floor(self.level, self.man)
                self.man += h
            # box is also moved
            else:
                move_floor(self.level, self.man - h)
                move_box(self.level, self.man)
                move_man(self.level, self.man + h)
                self.man += h
                self.push -= 1
    
    #redo a move
    def redo(self):
        if self.todo.__len__ > 0:
            self._move(self.todo[-1].lower())
            self.todo.pop()

def main():
    
    pygame.init()
    
    #set the windown sizec
    screen = pygame.display.set_mode((400,300))
    
    #load the image
    skinfilename = os.path.join('borgar.png')
    
    try:
        skin = pygame.image.load(skinfilename)
    except pygame.error as msg:
        print('cannot load skin')
        raise SystemExit(msg)
    
    skin = skin.convert()
    
    #set the background color
    screen.fill(skin.get_at((0,0)))
    
    #set the title
    pygame.display.set_caption('Sokoban')
    
    #set the game object and initialize the game
    skb = Sokoban()
    skb.draw(screen, skin)
    
    #set the time for repeating operation
    clock = pygame.time.Clock()
    pygame.key.set_repeat(200,50)
    
    #game loop
    while True:
        clock.tick(60)
    
        #get the event from keyboard
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    skb.move('l')
                    skb.draw(screen, skin)
                elif event.key == K_UP:
                    skb.move('u')
                    skb.draw(screen, skin)
                elif event.key == K_RIGHT:
                    skb.move('r')
                    skb.draw(screen, skin)
                elif event.key == K_DOWN:
                    skb.move('d')
                    skb.draw(screen, skin)
                elif event.key == K_BACKSPACE:
                    skb.undo()
                    skb.draw(screen, skin)
                elif event.key == K_SPACE:
                    skb.redo()
                    skb.draw(screen, skin)
        #update the game after each event
        pygame.display.update()
        
        pygame.display.set_caption(skb.solution.__len__().__str__() + '/' + skb.push.__str__() + ' - Sokoban')

if __name__ == '__main__':
    main()
    
            