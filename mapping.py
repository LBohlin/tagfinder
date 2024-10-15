import subprocess, sys
from pathlib import Path

class Mapping:    
    def __init__(self, path):
        self.data = dict()
        locations = subprocess.run(["find", path, "-name", "stats.txt"], capture_output=True).stdout.decode("utf-8")
        
        for e in locations.split('\n'):
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
                            self.data[l] = s

    def printdata(self):
        print("printdata")
        for k in self.data.keys():
            print(k)
            print(self.data[k])

            
#m = Mapping("/home/user/Documents/Projekte/Image/test")
#m.printdata()
