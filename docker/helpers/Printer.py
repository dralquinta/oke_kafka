from datetime import datetime
from termcolor import colored
from inspect import getframeinfo, stack
import os.path


def get_current_date():
    return str("["+datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"]")

def debug(msg, color=None):
    frame = getframeinfo(stack()[1][0])
    filename = os.path.splitext(os.path.basename(frame.filename))[0]
    lineno = str(frame.lineno)    

    debug_exp = get_current_date()+" DEBUG: "+filename+".py:"+lineno+" - "+str(msg)

    if (color == "red"):
        print(turn_red(debug_exp), flush=True)
    elif (color == "green"):
        print(turn_green(debug_exp), flush=True)
    elif (color == "yellow"):
        print(turn_yellow(debug_exp), flush=True)
    elif (color == "blue"):
        print(turn_blue(debug_exp), flush=True)
    elif (color == "magenta"):
        print(turn_magenta(debug_exp), flush=True)
    elif (color == "cyan"):
        print(turn_cyan(debug_exp), flush=True)
    elif (color == "grey"):
        print(turn_grey(debug_exp), flush=True)
    else:
        print(turn_white(debug_exp), flush=True)

def turn_red(msg):
    return colored(msg, 'red')

def turn_green(msg):
    return colored(msg, 'green')

def turn_yellow(msg):
    return colored(msg, 'yellow')

def turn_blue(msg):
    return colored(msg, 'blue')

def turn_magenta(msg):
    return colored(msg, 'magenta')

def turn_cyan(msg):
    return colored(msg, 'cyan')

def turn_white(msg):
    return colored(msg, 'white')

def turn_grey(msg):
    return colored(msg, 'grey')