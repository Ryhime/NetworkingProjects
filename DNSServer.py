import subprocess

class DNSCacheEntry:
    def __init__(self,ips:tuple,ttl:int)->None:
        self.ips = ips
        self.ttl = ttl

    def __str__(self) -> str:
        return "IPs: "+", ".join(self.ips)+'\n'+"TTL: "+str(self.ttl)        

class DNSServer:
    # ttl in seconds
    # CacheSize in bytes
    def __init__(self,ttl:int=3600,maxCacheSize:int=1000) -> None:
        self.cache = {}
        self.cacheSize = 0

        self.ttl = ttl
        self.maxCacheSize = maxCacheSize

    def removeFromCache(self)->None:
        # To reduce number of lookups on map
        mnEntry = None
        mnEntryKey = None
        for key in self.cache.keys():
            currEntry = self.cache[key]
            if (mnEntry==None or currEntry.ttl<=mnEntry.ttl):
                mnEntry = currEntry
                mnEntryKey = key

        self.cacheSize-=len(key)+sum(list(map(lambda x: len(x),mnEntry.ips)))
        del self.cache[mnEntryKey]




    def addToCache(self,domainName:str,ips:tuple)->None:
        sizeToAdd = len(domainName)+sum(list(map(lambda x: len(x),ips)))
        # Kick out
        if (self.cacheSize+sizeToAdd>self.maxCacheSize): self.removeFromCache()

        self.cache[domainName] = DNSCacheEntry(ips,self.ttl)
        self.cacheSize+=sizeToAdd





    def getIpFromNsLookup(self,nslookupOutput:str)->str:
        spl = nslookupOutput.split('\n')
        filtered = list(filter(lambda x: "internet address" in x,spl))[0].rstrip()
        return filtered.split("= ")[1]

    def getNameServerFromNsLookup(self,nslookupOutput:str)->str:
        spl = nslookupOutput.split('\n')
        filtered = list(filter(lambda x: "nameserver" in x,spl))[0].rstrip()
        return filtered.split("= ")[1]

    def getIpFromNameServerLookup(self,nameServerOutput:str)->str:
        spl = nameServerOutput.split('\n')[2::]
        filtered = list(filter(lambda x: "Address:" in x,spl))
        splits = list(map(lambda x: x.rstrip().split(": ")[1],filtered))
        return splits

    # Returns ip and how many servers needed to be reached out to get the ip address
    # Loop through domain name to reach out to each server
    def dnsLookup(self,domainName:str) -> tuple[str,int]:
        # Check cache first
        if (domainName in self.cache): 
            self.cache[domainName].ttl = self.ttl
            return (self.cache[domainName].ips,0)

        domainSplits = list(reversed(domainName.split('.')))
        #https://stackoverflow.com/questions/12297500/python-module-for-nslookup
        addrCovered = domainSplits[0]
        ip = self.getIpFromNsLookup(subprocess.Popen(["nslookup","-type=ns",addrCovered],stdout=subprocess.PIPE).communicate()[0].decode())
        for i in range(1,len(domainSplits)-1):
            addrCovered = domainSplits[i]+'.'+addrCovered
            proc = subprocess.Popen(["nslookup","-norecurse","-type=ns",addrCovered,ip],stdout=subprocess.PIPE).communicate()[0].decode()
            ip = self.getIpFromNsLookup(proc)

        # Get the final name server
        addrCovered = domainSplits[-1]+'.'+addrCovered
        proc = subprocess.Popen(["nslookup","-type=ns",addrCovered,ip],stdout=subprocess.PIPE).communicate()[0].decode()
        nameServer = self.getNameServerFromNsLookup(proc)

        # Name server -> ip address
        proc = subprocess.Popen(["nslookup",addrCovered,nameServer],stdout=subprocess.PIPE).communicate()[0].decode()
        ips = self.getIpFromNameServerLookup(proc)

        self.addToCache(domainName,ips)
        
        return (ips, len(domainSplits)+1)
    

if (__name__=="__main__"):
    dns = DNSServer()
    print(dns.dnsLookup("whitehouse.gov"))