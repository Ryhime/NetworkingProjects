from DNSServer import *
import pytest
def test_GoingToOneSiteOver():
    server = DNSServer()
    total = server.dnsLookup("google.com")[1]
    for i in range(500):
        total+=server.dnsLookup("google.com")[1]

    assert total == 3


def test_GoingToAllDifferent():
    server = DNSServer()
    total = server.dnsLookup("bing.com")[1]
    total+=server.dnsLookup("google.com")[1]
    total+=server.dnsLookup("youtube.com")[1]

    assert total == 9

def test_SmallCacheSize():
    server = DNSServer(maxCacheSize=90)
    total = server.dnsLookup("bing.com")[1]
    total+=server.dnsLookup("google.com")[1]
    total+=server.dnsLookup("youtube.com")[1]
    assert list(server.cache.keys()) == ["youtube.com"]

def test_LargeCacheSize():
    server = DNSServer(maxCacheSize=500)
    total = server.dnsLookup("bing.com")[1]
    total+=server.dnsLookup("google.com")[1]
    total+=server.dnsLookup("youtube.com")[1]
    assert list(server.cache.keys())==["bing.com", "google.com", "youtube.com"]
