import numpy as np
import matplotlib.pyplot as plt 
def modulateBASK(bitStream: str, symbolDuration = 1, fc = 1/2):
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

def modulatePBSK(bitStream: str, symbolDuration = 1, fc = 1/2):
    s = .001
    totalDuration = symbolDuration * len(bitStream)
    x = np.arange(1, totalDuration, step=s)
    y = []
    lastInterval = 0
    for i in range(len(bitStream)):
        interval = symbolDuration*int(1/s)*(i+1)
        y.extend(np.sin(2*np.pi*fc*x[lastInterval:interval]+(np.pi if bitStream[i]=='1' else 0)))
        lastInterval = interval


    plt.plot(x, y)
    plt.show()


modulatePBSK('0000001111100011')