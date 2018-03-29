#!/bin/bash/py
import sys
import select
import tty
import termios

sys.stdin = open('/dev/rfcomm0', 'r')

def isData():
	return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

old_settings = termios.tcgetattr(sys.stdin)

try:
	tty.setcbreak(sys.stdin.fileno())

	while 1:

		if isData() :
			c = sys.stdin.read(1)
			if c == "C":
				print("YES\n")
			if c == "1":
				break
finally:
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

