import pygame, sys, random
import pygame.gfxdraw
import datetime
from scouts_util import *
from pygame.locals import *
import picamera
import bme680
from subprocess import Popen, PIPE, DEVNULL

# Initialise pygame
pygame.init()
size = width, height = X, Y = 1280, 720

# Load some resources
smallfont, font, bigfont = load_fonts()
logo, logorect = load_logo()
screen = pygame.display.set_mode(size)
piechart, pierect = load_piechart()

# Main loop
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    pygame.event.pump()

# Draw the background
    screen.fill(purple)
    screen.blit(logo, logorect)
    show_text(screen, font, 10, logorect.bottom-10, '1st Histon')
    currentDT = datetime.datetime.now()
    show_text_centre(screen, smallfont, X//4*3, 50, currentDT.strftime("%A, %d %B, %Y"))

# Check if a key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_1]:
       show_text_centre(screen, font, X//2, 300, "Button 1 pressed")
    if key[pygame.K_2]:
       show_text_centre(screen, font, X//2, 300, "Button 2 pressed")
    
# Send the display to the screen
    pygame.display.flip()
    
    