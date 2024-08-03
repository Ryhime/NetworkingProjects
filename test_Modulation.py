import pytest
from Modulation import *

bits = "10000000000000000000111111111111111101010100101010101001010101010101001010101010101010101"
def test_BASKModulatioWithDemodulationDefaultParams():
    modded = modulateBASK(bits)
    demoded = demodulateBASK(modded)
    assert demoded == bits

def test_BASKModulationDemodulationTooLowFc():
    modded = modulateBASK(bits, fc=1/2)
    try:
        demodulateBASK(modded)
        assert False
    except:
        assert True

def test_BASKModulationDemodulationTooHighFc():
    modded = modulateBASK(bits, fc = 500)
    try:
        demodulateBASK(modded)
        assert False
    except:
        assert True

def test_BASKModulationDemodulationHighFc():
    modded = modulateBASK(bits, fc=100)
    demodded = demodulateBASK(modded)
    assert demodded == bits

def test_BASKModulationDemodulationHighSymbolDuration():
    modded = modulateBASK(bits, symbolDuration=500)
    demoded = demodulateBASK(modded, 500)
    assert demoded == bits

def test_BASKModulationDemodulationHighSymbolDuraitonAndFc():
    modded = modulateBASK(bits, symbolDuration=500, fc=100)
    demoded = demodulateBASK(modded, 500)
    assert demoded == bits
