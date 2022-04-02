import os,random
from threading import Thread
from time import sleep

import playsound
from termcolor import colored

from config import *

import numpy as np
from PIL import Image

def get_ansi_color_code(r, g, b):
    if r == g and g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round(((r - 8) / 247) * 24) + 232
    return 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)


def get_color(r, g, b):
    return "\x1b[48;5;{}m \x1b[0m".format(int(get_ansi_color_code(r,g,b)))


def show_image(img_path):
	try:
		img = Image.open(img_path)
	except FileNotFoundError:
		exit('Image not found.')

	h = 50
	w = 120

	img = img.resize((w,h), Image.ANTIALIAS)
	img_arr = np.asarray(img)
	h,w,c = img_arr.shape 
	for x in range(h):
		print(" "*12,end='')
		for y in range(w):
			pix = img_arr[x][y]
			print(get_color(pix[0], pix[1], pix[2]), sep='', end='')
		print()
		sleep(0.15)

# Importing module specified in the config file
art = __import__(f'arts.{artFile}', globals(), locals(), ['*'])

def replaceMultiple(mainString, toBeReplace, newString):
    # Iterate over the list to be replaced
    for elem in toBeReplace :
        # Check if the element is in the main string
        if elem in mainString :
            # Replace the string
            mainString = mainString.replace(elem, newString)
    
    return  mainString

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def pprint(art,time):
    
    color_used = [random.choice(color)]
    colorAttribute = []
    for i in range(len(art)):
        if art[i] in colorCodes:
        	# Color attr set to blink if 9
            if art[i] == '⑨':
                colorAttribute = [colorCodes[art[i]]]
            # color attr none if 10
            elif art[i] == '⑩':
                colorAttribute = []
            # Random color if R
            elif art[i] == '®':
                color_used = color
            else:
                color_used = [colorCodes[art[i]]]
                
        print(colored(replaceMultiple(art[i],colorCodes,''),random.choice(color_used),attrs=colorAttribute),sep='', end='',flush= True);sleep(time)
    show_image('./pic/km.jpg') 

def pAudio():
    if playAudio:
        playsound.playsound(resource_path(audio), True)

# Code reader
with open(resource_path(__file__)) as f_in:
	code = f_in.read()
        
def pcode():
    # Print the code before wishing 
    if codePrint:
        for i in range(len(code)):
            print(colored(code[i], codeColor),sep='', end='',flush= True);sleep(codingSpeed)
        input('\n\n'+colored('python3','blue')+colored(' PyBirthdayWish.py','yellow'))
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        input(colored('press F11 and hit {Enter}...','blue'))
        os.system('cls' if os.name == 'nt' else 'clear')

# Clearing terminal
os.system('cls' if os.name == 'nt' else 'clear')

try:
    pcode()
    Thread(target = pAudio).start()
    Thread(target = pprint, args=(art.mainArt,speed)).start()
    input()

except KeyboardInterrupt:
    print(colored('\n[-] Thanks!!','red'))
    os._exit(0)
