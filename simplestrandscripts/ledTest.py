import RPi.GPIO as GPIO
import time 
import readline
import os
from threading import Thread

LedPin = 11

STOP 	= 1
RUN 	= 2
QUIT 	= 3
SETUP 	= 4

currentCommand = STOP
blinkList = [500,500]

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LedPin, GPIO.OUT)
	GPIO.output(LedPin, GPIO.LOW)

def tearDown():
	GPIO.output(LedPin, GPIO.LOW)
	GPIO.cleanup()

def loop():
	setup()

	while currentCommand == RUN:
		for idx, val in enumerate(blinkList):
			ms =  val / float(1000)
			if idx % 2 is 0:
				GPIO.output(LedPin, GPIO.HIGH)
			else:
				GPIO.output(LedPin, GPIO.LOW)
			time.sleep(ms)
	
	tearDown()

def runLoop():
	thread = Thread(target = loop, args = ())
	thread.start()	

def getNum(list):
	num = list.strip()
	return int(num) 

def displayInputPrompt():
	global blinkList
	blinkList = []
	while True:
		os.system('clear')
		print 'Type milleseconds'
		print 'Example: 500 [enter] 500 [enter] q'
		print 'Stop with a -1 , quit or q'
		print 'Clear list with c or clear'
		print 'Current List: [on/off]  ' + str(blinkList)

		raw = raw_input('\n:\\') 
		if raw == 'quit' or raw == 'q' or raw == '-1':
			break
		if raw == 'c' or raw == 'clear':
			blinkList = []
			continue
		num = getNum(raw)
		blinkList.append(num)
			

def displayCommandPrompt():
	os.system('clear')
	print 'Christmas Lights BETA .001b'
	print 'Running Status: ' + str(currentCommand == RUN)
	print 'Type stop to stop'
	print 'Type run to run'
	print 'Type setup to setup blink'
	print 'Type quit to quit'
	command = raw_input('|\\')
	processCommand(command.strip())

def processCommand(command):
	global currentCommand
	if command == 'stop' and currentCommand is not STOP:
		animateCommand(command)
		currentCommand = STOP
	if command == 'run' and currentCommand is not RUN:
		animateCommand(command)
		currentCommand = RUN
		runLoop()
	if command == 'quit':
		animateCommand(command)
		os.system('clear')
		print 'YOU CAN\'T QUIT ME, BECUASE i CAN\'T QUIT YOU!!!'
		time.sleep(2)
		currentCommand = QUIT
	if command == 'setup':
		animateCommand(command)
		displayInputPrompt()

def animateCommand(command):
	for i in range(16):
		os.system('clear')
		x = "*" * i
		o = "-" * (16 - i)
		print 'Preparing to ' + command + ' |' + str(x) + str(o) + '|'
		time.sleep(.1)

if __name__ == '__main__':

	try:
		while currentCommand is not QUIT:
			displayCommandPrompt()
	except (KeyboardInterrupt, SystemExit):
		print 'Good bye!!!'

	os.system('clear')
	print 'You can\'t handle me.'
