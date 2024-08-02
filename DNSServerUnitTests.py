from DNSServer import *

def goingToOneSiteOver():
    server = DNSServer()
    total = server.dnsLookup("google.com")[1]
    for i in range(500):
        total+=server.dnsLookup("google.com")[1]

    if (total==3): return True
    return False


def goingToAllDifferent():
    server = DNSServer()
    total = server.dnsLookup("bing.com")[1]
    total+=server.dnsLookup("google.com")[1]
    total+=server.dnsLookup("youtube.com")[1]

    if (total==9): return True
    return False

def smallCacheSize():
    server = DNSServer(maxCacheSize=90)
    total = server.dnsLookup("bing.com")[1]
    total+=server.dnsLookup("google.com")[1]
    total+=server.dnsLookup("youtube.com")[1]
    if (list(server.cache.keys())==["youtube.com"]): return True
    return False

def largeCacheSize():
    server = DNSServer(maxCacheSize=500)
    total = server.dnsLookup("bing.com")[1]
    total+=server.dnsLookup("google.com")[1]
    total+=server.dnsLookup("youtube.com")[1]
    if (list(server.cache.keys())==["bing.com", "google.com", "youtube.com"]): return True
    return False

if (__name__=="__main__"):
    print(goingToOneSiteOver())
    # NOTE: Notic the amount of time this takes for only 4 compared to the last one which is 501 requests with caching
    print(goingToAllDifferent())
    print(smallCacheSize())
    print(largeCacheSize())
