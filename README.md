# rpi_modulate

What is it?
-----------

This is a small script to modulate 433mhz signals. Simple as it can be- haven't found this before.

Hardware to use
---------------

I use a Realtek RTL2832 based DVB dongle to receive all those 433mhz signals and for sending with this script i use the very cheap MX-FS-03V!

Hardware setup
--------------

Connect pin VCC of the MX-FS-03V with 5V (Pin 2 on Raspberry) and GND with GROUND-Pin (Pin 6) on Raspberry. Then connect the DATA-Pin e.g. to Pin 15, thats
Pin 22 in the GPIO-World.

Use the command "gpio readall" for an overview:

 +-----+-----+---------+------+---+---Pi 3---+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
 |   2 |   8 |   SDA.1 |   IN | 1 |  3 || 4  |   |      | 5v      |     |     |
 |   3 |   9 |   SCL.1 |   IN | 1 |  5 || 6  |   |      | 0v      |     |     |
 |   4 |   7 | GPIO. 7 |   IN | 1 |  7 || 8  | 1 | ALT0 | TxD     | 15  | 14  |
 |     |     |      0v |      |   |  9 || 10 | 1 | ALT0 | RxD     | 16  | 15  |
 |  17 |   0 | GPIO. 0 |   IN | 0 | 11 || 12 | 0 | IN   | GPIO. 1 | 1   | 18  |
 |  27 |   2 | GPIO. 2 |   IN | 0 | 13 || 14 |   |      | 0v      |     |     |
 |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
 |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
 |  10 |  12 |    MOSI |   IN | 0 | 19 || 20 |   |      | 0v      |     |     |
 |   9 |  13 |    MISO |   IN | 0 | 21 || 22 | 0 | IN   | GPIO. 6 | 6   | 25  |
 |  11 |  14 |    SCLK |   IN | 0 | 23 || 24 | 1 | IN   | CE0     | 10  | 8   |
 |     |     |      0v |      |   | 25 || 26 | 1 | IN   | CE1     | 11  | 7   |
 |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |
 |   5 |  21 | GPIO.21 |   IN | 1 | 29 || 30 |   |      | 0v      |     |     |
 |   6 |  22 | GPIO.22 |   IN | 1 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |
 |  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      | 0v      |     |     |
 |  19 |  24 | GPIO.24 |   IN | 0 | 35 || 36 | 0 | IN   | GPIO.27 | 27  | 16  |
 |  26 |  25 | GPIO.25 |   IN | 0 | 37 || 38 | 0 | IN   | GPIO.28 | 28  | 20  |
 |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+---Pi 3---+---+------+---------+-----+-----+

Software setup
--------------

I use this nice piece of software to receive 433mhz signals and to decode them:
https://github.com/merbanan/rtl_433

Use the switch "-a" when running the software and the signals will be printed out with modulation- you will need this information to use my script!

Example
-------

Lets try to act as a Chuango Alarmsystem ;)

This is what we get with RTL 433 when a door sensor transmits a signal:

2019-01-06 19:12:13|Chuango Security Technology
{"time" : "2019-01-06 19:12:13", "model" : "Chuango Security Technology", "id" : 906652, "cmd" : "Normal Zone", "cmd_id" : 7} > *** signal_start = -1712433787, signal_end = -1712281227, signal_len = 152560, pulses_found = 572
Iteration 1. t: 206    min: 30 (485)    max: 382 (87)    delta 884
Iteration 2. t: 206    min: 30 (485)    max: 382 (87)    delta 0
Pulse coding: Short pulse length 30 - Long pulse length 382

Short distance: 132, long distance: 392, packet distance: 4467

p_limit: 206
bitbuffer:: Number of rows: 6
[00] { 1} 00                                                                                                                   : 0
[01] {25} dd 59 c7 00                                                                                                          : 11011101 01011001 11000111 0
[02] {25} dd 59 c7 00                                                                                                          : 11011101 01011001 11000111 0
[03] {25} dd 59 c7 00                                                                                                          : 11011101 01011001 11000111 0
[04] {25} dd 59 c7 00                                                                                                          : 11011101 01011001 11000111 0
[05] {25} dd 59 c7 00                                                                                                          : 11011101 01011001 11000111 0

-------------------------------------------------------------------------------------------------------------------------------

And this it what my script needs:

./rpi_modulate.py
BCM BINARY_CODE_TO_SEND PROTOCOL SHORT DISTANCE LONG DISTANCE PACKET DISTANCE [NUM_ATTEMPTS] [SHORT PULSE] [LONG_PULSE]
22  e.g. 00000001       (0 or 1) 142            403           4067            default: 5

Informations:
-------------
- You will get the right port on your pi with command 'gpio readall'
- Binary Code can include spaces or other chars
- Protocol is 0 for binary and 1 for inverted binary

# In our example BCM is -> 22 (Pin 15 on Raspberry)
# The binary code above is "11011101 01011001 11000111 0"
# The protocol is "1" for inverted signals
# Short distance is 132
# Long distance is 392
# Packet distance is 4467
# We use the default of 5 attempts for sending the signals

You have to play a bit with short, long and packet distance until you have the right settings, check them with rtl 433.

Have fun!














