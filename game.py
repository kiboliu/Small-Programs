import pygame

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

#set the time for repeating operation
clock = pygame.time.Clock()
pygame.key.set_repeat(200,50)

#game loop
while True:
    clock.tick(60)
    pass

#get the event from keyboard
for event in pygame.event.get():
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == KEYDOWN:
        if event.key == K_LEFT:
            pass
        elif event.key == K_UP:
            pass
        elif event.key == K_RIGHT:
            pass
        elif event.key == K_DOWN:
            pass
        elif event.key == K_BACKSPACE:
            pass
        elif event.key == K_SPACE:
            pass
c
#game map
class Sokoban:

    def __init__(self):
        pass
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

    #draw the map
    def draw(self, screen, skin):
        w = skin.get_width() / 4
        for i in range(0, self.w)
            for j in range(0, self.h)
