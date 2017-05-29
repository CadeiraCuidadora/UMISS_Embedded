import serial
import matplotlib.pyplot as plt

import numpy as np
import time
pd = '/dev/tty.usbmodem1411'
#pd = '/dev/cu.usbmodem0E216FE1'

p = serial.Serial(port=pd, baudrate=230400,
                  bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)
#plt.axis([0, 10, 0, 1])
plt.ion() #Turn on interactive mode on plot from matplotlib

samples = 2048 #Define number of samples to plot
x = np.arange(samples) #set evenly spaced array from captured samples
y = np.zeros(samples) #create a array with the size of x filled with zeros
i = 0
fail_counter = 0
max_freq = 0
min_freq = 1e13


while(1):
    try:
        plt.clf() #clear current graph space
        plt.xlabel("Time(s)")
        plt.xlim(0, samples)
        plt.ylim(-0.5, 5.5)

        start = time.time() #start time counting
        i = 0
        while i < samples:
            value1 = p.read() #read val1  from microcontroller from serial
            value2 = p.read() #read val2 from microcontroller from serail

            try:
                v = ord(value1[0])*256 + ord(value2[0])
                y[i] = float(v)*(5/1023.0)
                x[i] = i
                i = i +1
            except IndexError:
                pass
                fail_counter = fail_counter+1
                #print fail_counter, len(value), ord(value[0])
                #v = ord(value[0])
                #y[i] = float(v)*(5.0/1023.0)
                #x[i] = i
                #i = i +1

        freq = float(samples)/(time.time() - start)
        if freq > max_freq: 
            max_freq = freq
        elif freq < min_freq:
            min_freq = freq

        plt.plot(x, y)
        plt.pause(1.0/60.0)


    except KeyboardInterrupt:
        plt.close()
        break

print "\nFreq max: %.3f kHz" %(max_freq/1000.0)
print "Freq min:%.3f kHz" %(min_freq/1000.0)
print"total fails:", fail_counter
p.close()
