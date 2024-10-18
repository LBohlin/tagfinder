import subprocess, sys
from pathlib import Path

class Mapping:    
    def __init__(self, path):
        self.data = dict()
        self.basePath=path
        locations = subprocess.run(["find", path, "-name", "info.txt"], capture_output=True).stdout.decode("utf-8")
        objects = list(filter(None,locations.split('\n')))
        self.numberOfObjects = len(objects)
        for e in objects:
            if len(e) > 0:                
                p = Path(e)
                picpath = p.parent.joinpath("pic")
                if p.exists():
                    f = open(p, "r")
                    lines = f.readlines()
                    for l in lines:
                        if l[0] == '#':
                            continue
                        if l in self.data:
                            s = self.data.get(l)
                            s.add(picpath)
                            self.data[l] = s
                        else:
                            s = set()
                            s.add(picpath)                            
                            self.data[l.lower()] = s

    def search(self, searchKeys):
        metalist = []
        metadesc = []
        imageSet = {}
        searchKeys=list(filter(None, searchKeys))
        for sk in searchKeys:        
            sublist = set()
            foundKeywords = []
            for k in self.data.keys():            
                if sk == '*' or sk in k:
                    for p in self.data[k]:
                        sublist.add(p)
                    foundKeywords.append(k)
            if len(foundKeywords) > 0:
                # number of pictures NOT of keywords!!
                desc = sk + ": "+ str(len(sublist)) + ' ('
                for k in foundKeywords:
                    desc = desc + k[:-1] + ', '        
                    desc = desc[:-2] + ')'
                    if not sk == '*':
                        metadesc.append(desc)
                    metalist.append(sublist)
                    imageSet = set.intersection(*metalist)
        return [imageSet, metadesc]
                
    def printdata(self):
        print("printdata")
        for k in self.data.keys():
            print(k)
            print(self.data[k])
