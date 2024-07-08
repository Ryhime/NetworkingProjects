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
    total+=server.dnsLookup("whitehouse.gov")[1]

    if (total==12): return True
    return False

def smallCacheSize():
    server = DNSServer(maxCacheSize=200)
    total = server.dnsLookup("bing.com")[1]
    total+=server.dnsLookup("google.com")[1]
    total+=server.dnsLookup("youtube.com")[1]
    total+=server.dnsLookup("whitehouse.gov")[1]
    if (list(server.cache.keys())==["whitehouse.gov"]): return True
    return False

if (__name__=="__main__"):
    print(goingToOneSiteOver())
    # NOTE: Notic the amount of time this takes for only 4 compared to the last one which is 501 requests with caching
    print(goingToAllDifferent())
    print(smallCacheSize())