import pygame, sys
import pygame.gfxdraw
import datetime
import picamera
import io
from subprocess import call, Popen, PIPE, DEVNULL
black = 0, 0, 0
white = 255, 255, 255
purple = 116, 20, 220


def show_text(screen, afont, x, y, text):
    mytext = afont.render(text, True, white, purple)
    mytextRect = mytext.get_rect()
    mytextRect.left = x
    mytextRect.top = y
    screen.blit(mytext, mytextRect)

def show_text_centre(screen, afont, x, y, text):
    mytext = afont.render(text, True, white, purple)
    mytextRect = mytext.get_rect()
    mytextRect.center = (x, y)
    screen.blit(mytext, mytextRect)

def load_fonts():
    smallfont = pygame.font.Font('/home/pi/digital_maker/fonts/NunitoSans-Light.ttf', 24)
    font = pygame.font.Font('/home/pi/digital_maker/fonts/NunitoSans-Black.ttf', 32)
    bigfont = pygame.font.Font('/home/pi/digital_maker/fonts/NunitoSans-Black.ttf', 100)
    return [smallfont, font, bigfont]

def load_logo():
    scoutlogo = pygame.image.load("/home/pi/digital_maker/Scouts_Logo_Horizontal_White.png")
    logosmall = pygame.transform.smoothscale(scoutlogo, (226, 69))
    logorect = logosmall.get_rect()
    logorect.top = 10;
    logorect.left = 10;
    return [logosmall, logorect]

def load_piechart():
    piechart = pygame.image.load("/home/pi/digital_maker/piechart3.png")
#     piechart.convert_alpha()
    piechart = pygame.transform.smoothscale(piechart, (200, 200))
    pierect = piechart.get_rect()
    print(piechart.get_at((10,10)))
    pierect.center = (400,400)
    return [piechart, pierect]
    
def basic_screen(screen):
    screen.fill(purple)
    screen.blit(logosmall, logorect)
    screen.blit(text, textRect)
    currentDT = datetime.datetime.now()
    show_text(smallfont, X//4*3, 50, currentDT.strftime("%A, %d %B, %Y"))

def get_mode(mode):
    key = pygame.key.get_pressed()
    if key[pygame.K_1]: mode = "time"
    if key[pygame.K_2]: mode = "countdown"
    if key[pygame.K_3]: mode = "gamepicker"
    if key[pygame.K_4]: mode = "temperature"
    if key[pygame.K_5]: mode = "scouts-var"
    if key[pygame.K_q]: mode = "quit"
    return mode

def draw_pie_chart2 (size, x, y, num_segments, segmentnames=None, segmentcols=None):
    pie_angle = 360//num_segments;
    for j in range(0,num_segments):
        pygame.gfxdraw.pie(screen, x, y, size//2, pie_angle*j, pie_angle*(j+1), (0, 255, 128))

def draw_pie_chart(rotation, screen):
    screen.blit(piechart, pierect)
    
def write_video_file(stream, filename):
    print('Writing video!')
    with stream.lock:
        # Find the first header frame in the video
        for frame in stream.frames:
            if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break
        # Write the rest of the stream to disk
        with io.open(filename, 'wb') as output:
            output.write(stream.read())
 
def playfile(filename):
    process = call(['omxplayer',  filename], stdin=PIPE,
                             stdout=DEVNULL, close_fds=True, bufsize=0)

