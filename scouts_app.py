import pygame, sys
import pygame.gfxdraw
import datetime

pygame.init()

X,Y=640,480
size = width, height = X, Y
black = 0, 0, 0
white = 255, 255, 255
purple = 116, 20, 220

screen = pygame.display.set_mode(size)

scoutlogo = pygame.image.load("/home/pi/digital_maker/Scouts_Logo_Horizontal_White.png")
logosmall = pygame.transform.smoothscale(scoutlogo, (226, 69))
logorect = logosmall.get_rect()
logorect.top = 10;
logorect.left = 10;

piechart = pygame.image.load("/home/pi/digital_maker/piechart.png")
piechart.set_colorkey(white)
piechart = pygame.transform.smoothscale(piechart, (200, 200))
pierect = piechart.get_rect()
pierect.center = (400,400)

smallfont = pygame.font.Font('/home/pi/digital_maker/NunitoSans-Light.ttf', 24)
font = pygame.font.Font('/home/pi/digital_maker/NunitoSans-Black.ttf', 32)

text = font.render('1st Histon', True, white, purple)
textRect = text.get_rect()
textRect.center = (Y//2, X//2)
textRect.left = 10
textRect.top = logorect.bottom-10


bigfont = pygame.font.Font('/home/pi/digital_maker/NunitoSans-Black.ttf', 100)

def show_text(afont, x, y, text):
    mytext = afont.render(text, True, white, purple)
    mytextRect = mytext.get_rect()
    mytextRect.center = (x,y)
    screen.blit(mytext, mytextRect)
    
def draw_pie_chart2 (size, x, y, num_segments, segmentnames=None, segmentcols=None):
    pie_angle = 360//num_segments;
    for j in range(0,num_segments):
        pygame.gfxdraw.pie(screen, x, y, size//2, pie_angle*j, pie_angle*(j+1), (0, 255, 128))

def draw_pie_chart(rotation):
    screen.blit(piechart, pierect)

pie_angle = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
    screen.fill(purple)
    screen.blit(logosmall, logorect)
    screen.blit(text, textRect)
    currentDT = datetime.datetime.now()
    
    #text_in_centre(currentDT.hour, currentDT.minute)
    show_text(bigfont, X//2, Y//2, currentDT.strftime("%H:%M"))
    show_text(smallfont, X//4*3, 50, currentDT.strftime("%A, %d %B, %Y"))
    
    #draw_pie_chart(200, 300, 300, 6)
    draw_pie_chart(pie_angle)
    pie_angle = pie_angle + 10
    if pie_angle >=360 :
        pie_angle= 0;
    
    pygame.display.flip()
    
    