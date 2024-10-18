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

    def printdata(self):
        print("printdata")
        for k in self.data.keys():
            print(k)
            print(self.data[k])
