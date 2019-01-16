#!/usr/bin/python

import time
import sys
import RPi.GPIO as GPIO

#
# Variablen init
#
short_delay = 0
long_delay = 0
extended_delay = 0
short_pulse = 0
long_pulse = 0
protocol = 0
codetosend = ''
newcode=''

# Number of attempts
#
NUM_ATTEMPTS = 5

# Pin to transmit
#
TRANSMIT_PIN = 22

def transmit_code(code):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)

    for t in range(NUM_ATTEMPTS):
	print "SENDING -> " + str(code)
        for i in code:
            if i == '1':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(short_delay)
                #time.sleep(short_pulse)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(long_pulse)
                #time.sleep(long_delay)

            elif i == '0':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(long_delay)
                #time.sleep(long_pulse)
                GPIO.output(TRANSMIT_PIN, 0)
                #time.sleep(short_delay)
		time.sleep(short_pulse)
            else:
                continue
	
	    
	GPIO.output(TRANSMIT_PIN, 0)
	time.sleep(extended_delay)

    GPIO.cleanup()

def transmit_code1(code):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)

    print "SENDING -> " + str(code)
    for i in code:
	if i == '1':
            GPIO.output(TRANSMIT_PIN, 1)
            time.sleep(short_delay)
            #time.sleep(short_pulse)
            GPIO.output(TRANSMIT_PIN, 0)
            time.sleep(long_pulse)
            #time.sleep(long_delay)

        elif i == '0':
            GPIO.output(TRANSMIT_PIN, 1)
            time.sleep(long_delay)
            #time.sleep(long_pulse)
            GPIO.output(TRANSMIT_PIN, 0)
            #time.sleep(short_delay)
	    time.sleep(short_pulse)
        else:
	    continue
    
    GPIO.output(TRANSMIT_PIN, 0)
    time.sleep(extended_delay)

    GPIO.cleanup()

if __name__ == '__main__':
    if len(sys.argv)<7:
	print sys.argv[0]
	print "BCM BINARY_CODE_TO_SEND PROTOCOL SHORT DISTANCE LONG DISTANCE PACKET DISTANCE [NUM_ATTEMPTS] [SHORT PULSE] [LONG_PULSE]"
	print "22  e.g. 00000001       (0 or 1) 142            403           4067            default: 5"
	print ""
	print "Informations:"
	print "-------------"
	print "- You will get the right port on your pi with command 'gpio readall'"
	print "- Binary Code can include spaces or other chars"
	print "- Protocol is 0 for binary and 1 for inverted binary"
	print ""
	sys.exit(0)

    TRANSMIT_PIN = int(sys.argv[1])
    codetosend = str(sys.argv[2])
    protocol = sys.argv[3]

    short_delay = float(sys.argv[4])/1000000*4
    long_delay = float(sys.argv[5])/1000000*4
    extended_delay = float(sys.argv[6])/1000000*4

    if len(sys.argv)>7:
    	NUM_ATTEMPTS = int(sys.argv[7])

    if len(sys.argv)>8:
	short_pulse = float(sys.argv[8])/1000000*4
    else:
	short_pulse = short_delay

    if len(sys.argv)>9:
        long_pulse = float(sys.argv[9])/1000000*4
    else:
	long_pulse = long_delay

    print "BCM PORT: " + str(TRANSMIT_PIN)
    print "PROTOCOL: " + str(protocol)

    for i in codetosend:
	if protocol == '0':
    	    if i == '1':
		newcode += '1'
    	    elif i == '0':
		newcode += '0'
    	    else:
    		continue
	elif protocol == '1':
    	    if i == '1':
		newcode += '0'
    	    elif i == '0':
		newcode += '1'
    	    else:
    		continue
	
    print "BINARY CODE TO SEND: " + str(newcode)
    print "SHORT DELAY: " + str(short_delay) + "ms"
    print "LONG DELAY: " + str(long_delay) + "ms"
    print "PACKET DISTANCE: " + str(extended_delay) + "ms"

    print "NUM ATTEMPTS: " + str(NUM_ATTEMPTS)

    print "SHORT PULSE: " + str(short_pulse) + "ms"
    print "LONG PULSE: " + str(long_pulse) + "ms"

    # send it!
    transmit_code1('1')
    #transmit_code1('11111111 1111')
    transmit_code(newcode)

    sys.exit(0)

