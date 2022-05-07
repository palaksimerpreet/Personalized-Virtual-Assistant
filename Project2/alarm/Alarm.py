# Original Author : Vasudev Ram
# Modified by     : Giga Blitz

import os, string
from time import sleep
from playsound import playsound

thepath = os.path.dirname(os.path.abspath(__file__))
file = open(rf'{thepath}\alarm_time.txt', 'r')
reading = file.readlines()

try:
    minutes = float(reading[0])
except ValueError:
    print ("Invalid numeric value (%s) for minutes" % sa[1])
    print ("Should be a number greater than 0")
    exit(2)

if minutes < 0:
    print ("Invalid value for minutes, should be greater than 0")
    exit(2)

print("\nMinimize this window and carry on.")

seconds = minutes * 60

if minutes == 1:
    unit_word = " minute"
else:
    unit_word = " minutes"

try:
    if minutes > 0:
        print ("Sleeping for " + str(minutes) + unit_word + "\n")
        sleep (seconds)
    print ("W            W     A      K  K  EEEEE      U    U  PPPP ")
    print (" W          W     A A     K K   E          U    U  P   P")
    print ("  W        W     AAAAA    KK    EEEEE      U    U  PPPP ")
    print ("   W  WW  W     A     A   K K   E          U    U  P    ")
    print ("    WW  WW     A       A  K  K  EEEEE       UUUU   P    ")
    playsound(rf'{thepath}\tone.mp3')
    sleep(7)
except KeyboardInterrupt:
    print ("Interrupted by user")
    exit(2)