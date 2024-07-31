import numpy as np
import matplotlib.pyplot as plt 
symbolDuration = 5
fc = 1/2.0

def BASK(bitStream: str):
    s = .001
    totalDuration = symbolDuration * len(bitStream)
    x = np.arange(1, totalDuration, step=s)
    y = []
    lastInterval = 0
    for i in range(len(bitStream)):
        interval = symbolDuration*int(1/s)*(i+1)
        y.extend(np.sin(2*np.pi*fc*x[lastInterval:interval])/(2 if bitStream[i]=='0' else 1))
        lastInterval = interval


    plt.plot(x, y)
    plt.show()


BASK('000001111111111111')