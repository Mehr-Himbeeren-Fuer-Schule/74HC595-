#rot -> vorne 1
#schwarz -> vorne 3
#lila -> vorne 6
#grün -> hinten 6
#weiß -> hinten 7

import RPi.GPIO as GPIO
import time

SIn = 11
MemoryPush = 12
ShiftPush = 13

Length = 8

StatusList = [False]*Length

#test only length = 8
look1 = [True]*8
look2 = [False]*8
look3 = [True,False,True,False,True,False,True,False]
look4 = [False,True,False,True,False,True,False,True]
allLook = [look1, look2, look3, look4]
allLook2 = [look3, look4]
timeBetween = 0.1



def loop(): #main loop
        while True:
                #print('run')
                for aList in allLook: #geht durch liste
                        #print(aList)
                        shiftIn(aList)
                        time.sleep(0.001)
                        shiftMemory()
                        time.sleep(timeBetween)


def shiftIn(OutList): #bringt alles in den register
        #print(OutList)
        for index in OutList:
                if index:
                        GPIO.output(SIn, GPIO.LOW)
                        #print('Low')
                else:
                        GPIO.output(SIn, GPIO.HIGH)
                        #print('High')
                GPIO.output(ShiftPush, GPIO.HIGH)
                #print('shift-h')
                time.sleep(0.001)
                GPIO.output(ShiftPush, GPIO.LOW)
                #print('shift-l')

def shiftMemory(): #gibt paralel aus
        GPIO.output(MemoryPush, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(MemoryPush,GPIO.LOW)

        
def print_msg():
	print('Program is running...')
	print('Please press Ctrl+C to end the program...')

def setup():
	GPIO.setmode(GPIO.BOARD)    # Number GPIOs by its physical location
	GPIO.setup(SIn, GPIO.OUT)
	GPIO.setup(MemoryPush, GPIO.OUT)
	GPIO.setup(ShiftPush, GPIO.OUT)
	GPIO.output(SIn, GPIO.LOW)
	GPIO.output(MemoryPush, GPIO.LOW)
	GPIO.output(ShiftPush, GPIO.LOW)

def destroy():   # When program ending, the function is executed.
        print('Interrupt')
        shiftIn([False]*Length)
        time.sleep(0.001)
        shiftMemory()
        GPIO.output(SIn, GPIO.LOW)
        GPIO.output(MemoryPush, GPIO.LOW)
        GPIO.output(ShiftPush, GPIO.LOW)
        GPIO.cleanup()
        print('Interrupted')

if __name__ == '__main__': # Program starting from here 
	print_msg()
	setup() 
	try:
		loop()  
	except KeyboardInterrupt:  
		destroy()  
