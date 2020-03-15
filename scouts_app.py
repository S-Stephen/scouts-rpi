import pygame, sys, random
import pygame.gfxdraw
import datetime
from scouts_util import *
from pygame.locals import *
import picamera
import bme680
from subprocess import Popen, PIPE, DEVNULL


pygame.init()

size = width, height = X, Y = 1280, 720
black = 0, 0, 0
white = 255, 255, 255
purple = 116, 20, 220

smallfont, font, bigfont = load_fonts()
screen = pygame.display.set_mode(size)
logo, logorect = load_logo()

def show_text(afont, x, y, text):
    mytext = afont.render(text, True, white, purple)
    mytextRect = mytext.get_rect()
    mytextRect.left = x
    mytextRect.top = y
    screen.blit(mytext, mytextRect)

def show_text_centre(afont, x, y, text):
    mytext = afont.render(text, True, white, purple)
    mytextRect = mytext.get_rect()
    mytextRect.center = (x, y)
    screen.blit(mytext, mytextRect)

piechart, pierect = load_piechart()

pie_angle = 0
pie_speed = 0
start_time = 0
i=0
count = disp = 7200
mode = "time"
patrol=""
camera = picamera.PiCamera()
cam_filename = ""
cam_start_time = 0

sensor = bme680.BME680()
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    pygame.event.pump()

    screen.fill(purple)
    screen.blit(logo, logorect)
    show_text(font, 10, logorect.bottom-10, '1st Histon')
    currentDT = datetime.datetime.now()
    show_text_centre(smallfont, X//4*3, 50, currentDT.strftime("%A, %d %B, %Y"))

    mode=get_mode(mode)
    key = pygame.key.get_pressed()
    if mode != "scouts-var": camera.stop_preview()
    if mode == "quit": sys.exit()

    if mode=="time":
        show_text_centre(font, X//2, 150, "Current time in Histon is....")
        show_text_centre(bigfont, X//2, Y//2, currentDT.strftime("%H:%M:%S"))
        day=currentDT.weekday()
        if (day==0):
            show_text_centre(font, X//2, Y//2+70, "Monday Scouts starts at 7.30pm")
        elif (day==3):
            show_text_centre(font, X//2, Y//2+70, "Thursday Scouts starts at 7.30pm")  
        show_text(smallfont, X//6, 650, "Instructions: Just read the time! q: quit programme")
    elif mode=="countdown":
        show_text_centre(font, X//2, 150, "Timer countdown")
        key = pygame.key.get_pressed()
        if key[pygame.K_r]: count = disp = 7200; start_time = 0;
        if key[pygame.K_g]: start_time = datetime.datetime.now()
        if key[pygame.K_s]: start_time = 0; count = disp
        if start_time != 0:
            disp = count-(datetime.datetime.now()-start_time).seconds
        show_text_centre(bigfont, X//2, Y//2, "%d"%disp)
        show_text(smallfont, X//6, 650, "Instructions: r: reset timer to 7200s; g: start timing; s: stop/pause timing;  q: quit programme")
    elif mode=="gamepicker":
        show_text_centre(font, X//2, 150, "Which patrol picks the game...")
        rotpie = pygame.transform.rotate(piechart,pie_angle)
        pierect = rotpie.get_rect()
        pierect.center = (X//2-100,300)
        if key[pygame.K_g]:
            pie_speed = 100
            pie_angle = random.randint(0,359)
            i=0
        if pie_speed > 0:
            pie_angle += pie_speed//10
        i += 1
        if (i%20 == 0):
            if pie_speed > 0:
                pie_speed -= max(pie_speed//5,1);
        pie_angle += pie_speed
        ang = pie_angle%360
        segment = 360/6
        if   ang<1*segment: patrol="Falcons"
        elif ang<2*segment: patrol="Eagles"
        elif ang<3*segment: patrol="Hawks"
        elif ang<4*segment: patrol="Another"
        elif ang<5*segment: patrol="Yet another"
        else: patrol="The other one"
        screen.blit(rotpie, pierect)
        show_text_centre(font, X//2+120, 300, patrol)
        show_text(smallfont, X//6, 650, "Instructions: g: start spinner;  q: quit programme")
    elif mode=="temperature":
#         if (sensor.get_sensor_data()):
            sensor.get_sensor_data()
            show_text_centre(font, X//2, 150, "Scouts Sensor")
            space = 200;
            show_text(smallfont, X//4, 200, "Temperature:")
            show_text(smallfont, X//4+space, 200, "%.2f C"%sensor.data.temperature)
            show_text(smallfont, X//4, 250, "Pressure:")
            show_text(smallfont, X//4+space, 250, "%.2f hPa"%sensor.data.pressure)
            show_text(smallfont, X//4, 300, "Humidity:")
            show_text(smallfont, X//4+space, 300, "%.2f %%"%sensor.data.humidity)        
            show_text(smallfont, X//4, 350, "Air Quality:")
            if (sensor.data.heat_stable):
                show_text(smallfont, X//4+space, 350, "%d Ohms"%sensor.data.gas_resistance)
            show_text(smallfont, X//6, 650, "Instructions: Just read the values;  q: quit programme")
      
        
    elif mode=="scouts-var":
        show_text_centre(font, X//2, 150, "Scouts VAR")
        if key[pygame.K_g]:
            if cam_start_time == 0:
                stream = picamera.PiCameraCircularIO(camera, seconds=20)
                camera.start_preview(fullscreen=False, window=(300,300,600,600))
                camera.start_recording(stream, format='h264')
                cam_start_time = datetime.datetime.now()
    #             camera.start_recording(cam_start_time.strftime("myfile-%H:%M.h264"))
                camera.wait_recording(1)
            
        if key[pygame.K_s]:
            if cam_start_time != 0:
                camera.wait_recording(1)
                cam_start_time = datetime.datetime.now()
                camera.stop_preview()
                camera.stop_recording()
                cam_filename = cam_start_time.strftime("myfile-%H:%M.h264")
                write_video_file(stream, cam_filename)
                cam_start_time = 0
                
        if key[pygame.K_p]:
            playfile(cam_filename)

        if cam_start_time != 0:
            camera.wait_recording(0.1)

        show_text(smallfont, X//8, 650, "Instructions: g: start camera; s: stop camera (event has occurred!); p: playback stored video; q: quit programme;")
       

    pygame.display.flip()
    
    