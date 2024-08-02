import numpy as np
import matplotlib.pyplot as plt
s = .001
def modulateBASK(bitStream: str, symbolDuration = 1, fc = 1/2):
    print(len(bitStream))
    totalDuration = symbolDuration * len(bitStream)
    x = np.arange(0, totalDuration, step=s)
    y = []
    lastInterval = 0
    for i in range(len(bitStream)):
        interval = symbolDuration*int(1/s)*(i+1)
        y.extend(np.sin(2*np.pi*fc*x[lastInterval:interval])/(2 if bitStream[i]=='0' else 1))
        lastInterval = interval
    return y


def demodulateBASK(wave: list, symbolDuration = 1) -> str:
    numberBits = len(wave)//(symbolDuration*int(1/s))
    bitsFound = "";
    lastInterval = 0
    for i in range(numberBits):
        interval = symbolDuration*int(1/s)*(i+1)
        maximumValue = max(wave[lastInterval:interval])
        if (abs(maximumValue)<=10**(-3)): raise Exception("Frequency Not High Enough to Demodulate")
        bitsFound+="1" if abs(maximumValue-1)<=abs(maximumValue-.5) else "0"
        lastInterval = interval
    return bitsFound

def modulatePBSK(bitStream: str, symbolDuration = 1, fc = 1/2):
    totalDuration = symbolDuration * len(bitStream)
    x = np.arange(1, totalDuration, step=s)
    y = []
    lastInterval = 0
    for i in range(len(bitStream)):
        interval = symbolDuration*int(1/s)*(i+1)
        y.extend(np.sin(2*np.pi*fc*x[lastInterval:interval]+(np.pi if bitStream[i]=='1' else 0)))
        lastInterval = interval
    return y


bits = "1001010101010101111010110"
modulated = modulateBASK(bits, fc=5)
demoded = demodulateBASK(modulated)

print(demoded==bits)

plt.plot(np.arange(len(modulated)),modulated)
plt.show()
