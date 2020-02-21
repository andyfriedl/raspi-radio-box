'''
raspi radio box v.0.1.0

'''
import random
import sys
import termios
import time
import tty
import urllib.request
from decimal import Decimal
from time import sleep
from urllib.error import URLError

import RPi.GPIO as GPIO
import vlc
from Adafruit_LED_Backpack import AlphaNum4
from google_connect import get_stream_data
from sevensegment import *

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)
seg = sevensegment(device)

def get_key_pressed():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

system_sounds = [
    "/home/pi/path-to-media-folder/beep.wav",
    "/home/pi/path-to-media-folder/atari_error.wav",
    "/home/pi/path-to-media-folder/deathstar.mp3",
    "/home/pi/path-to-media-folder/beep2.wav",
    "/home/pi/path-to-media-folder/error.wav",
    "/home/pi/path-to-media-folder/computerbeep_3.mp3",
    "/home/pi/path-to-media-folder/computerbeep_31.mp3",
    "/home/pi/path-to-media-folder/alert16.mp3",
    ]

button_delay = 0.5
player = vlc.MediaPlayer()
volume = 50
player.audio_set_volume(volume)
# Setup gpio pins
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(11, GPIO.OUT, initial=GPIO.HIGH)  # Power
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)  # Pause
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)  # Mute
pause_led = mute_led = True
indexing_stream = 10
# Setup VLC players
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
player = instance.media_player_new()
beep_player = instance.media_player_new()
current_stream = ''
GPIO.output(11, True)  # Power led on

print("VLC Audio Stream player ready.\n----- CONTROLS -----")
print("\n(1 - 9) Play a stream.")
print("(- +) Volume \n(m) Mute \n(s) Stop \n(p) Pause\n(q) Quit")
print("\n -- Waiting for input --  Choose a staion (0 - 9)")

stream_data = get_stream_data()
number_of_rows = stream_data[1]

def play_stream(num):
    play_system_sound(30, system_sounds[5])
    print('\n' + 'preset: ' + num)
    time.sleep(button_delay)
    stream_num = int(Decimal(num) - 1)
    url = stream_data[0][stream_num][1]
    station = stream_data[0][stream_num][0]
    city = stream_data[0][stream_num][2]
    state = stream_data[0][stream_num][3]
    seg.text = '________'
    time.sleep(.1)
    seg.text = '========'
    time.sleep(.1)
    seg.text = '********'
    time.sleep(.1)
    seg.text = '========'
    time.sleep(.1)
    seg.text = '________'
    time.sleep(.1)
    seg.text = num + ' ' + station[:6]
    print('Now playing => ' + station + ' from ' + city + ', ' + state + '\n')
    media = instance.media_new(url)
    player.set_media(media)
    player.audio_set_volume(volume)
    time.sleep(1)
    player.play()

def play_system_sound(volume, play_sound):
    beep_player.audio_set_volume(volume)
    media = instance.media_new(play_sound)
    beep_player.set_media(media)
    beep_player.play()
    time.sleep(.3)

def show_led_message(device, msg, delay=0.1):
    # Implemented with virtual viewport
    width = device.width
    padding = " " * width
    msg = padding + msg + padding
    n = len(msg)

    virtual = viewport(device, width=n, height=8)
    sevensegment(virtual).text = msg
    for i in reversed(list(range(n - width))):
        virtual.set_position((i, 0))
        time.sleep(delay)

seg.text = 'READY...'
play_system_sound(50, system_sounds[6])

while True:

    key_pressed = get_key_pressed()

    if (key_pressed == "/"):
        # ------- Pause player

        GPIO.output(8, pause_led)
        print("\nPaused " + str(pause_led))
        player.pause()
        play_system_sound(40, system_sounds[3])
        pause_led = not pause_led

    if (key_pressed == "*"):
        # ------- Mute player

        print("\nMute " + str(mute_led))
        player.audio_toggle_mute()
        GPIO.output(13, mute_led)
        play_system_sound(40, system_sounds[3])
        mute_led = not mute_led

    if (key_pressed == "="):
        # ------- Exit player

        print("\nExiting player ....")
        show_led_message(device, "EXITING PLAYER")
        player.stop()
        play_system_sound(60, system_sounds[7])
        GPIO.output(11, False)
        time.sleep(5)
        seg.text = ''
        GPIO.cleanup()
        exit(0)

    if (key_pressed == "+"):
        # ------- Volume up

        if volume < 100:
            volume += 5
            print(volume)
            player.audio_set_volume(volume)
        else:
            play_system_sound(100, system_sounds[5])
            print("Beep! Max volume.")

    if (key_pressed == "-"):
        # ------- Volume down

        if volume > 0:
            volume -= 5
            print(volume)
            player.audio_set_volume(volume)
        else:
            play_system_sound(60, system_sounds[5])
            print("Beep! Min volume.")

    if (key_pressed == "1" and current_stream != key_pressed):
        current_stream = key_pressed
        play_stream("9")

    if (key_pressed == "2" and current_stream != key_pressed):
        current_stream = key_pressed
        play_stream("6")

    if (key_pressed == "3" and current_stream != key_pressed):
        current_stream = key_pressed
        play_stream("3")

    if (key_pressed == "4" and current_stream != key_pressed):
        current_stream = key_pressed
        play_stream("8")

    if (key_pressed == "5" and current_stream != key_pressed):
        current_stream = key_pressed
        play_stream("5")

    if (key_pressed == "6" and current_stream != key_pressed):
        current_stream = key_pressed
        play_stream("2")

    if (key_pressed == "7" and current_stream != key_pressed):
        current_stream = key_pressed
        play_stream("7")

    if (key_pressed == "8" and current_stream != key_pressed):
        current_stream = key_pressed
        play_stream("4")

    if (key_pressed == "9" and current_stream != key_pressed):
        current_stream = key_pressed
        play_stream("1")

    if (key_pressed == "0"):
        # Play a random stream from playlist Google spreadsheet greater than sream 9
        random_stream_number = random.randint(10, int(number_of_rows))
        print(random_stream_number)
        current_stream = key_pressed
        play_stream(str(random_stream_number))

    if (key_pressed == "."):
        # Index through streams from playlist Google spreadsheet greater than sream 9
        current_stream = key_pressed
        indexing_stream += 1
        if indexing_stream > int(number_of_rows):
            indexing_stream = 10
        play_stream(str(indexing_stream))
