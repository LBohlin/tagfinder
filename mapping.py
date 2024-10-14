import subprocess, sys
from pathlib import Path

class obj:
    k = str
    pics = []
    def __init__(self, k):
        self.k = k
        self.pics = []
    

class Mapping:    
    def __init__(self, path):
        self.data = []
        locations = subprocess.run(["find", path, "-name", "stats.txt"], capture_output=True).stdout.decode("utf-8")
        
        for e in locations.split('\n'):
            if len(e) > 0:                
                p = Path(e)
                picpath = p.parent.joinpath("pic")
                if p.exists():
                    f = open(p, "r")
                    lines = f.readlines()
                    for l in lines:
                        exists = False
                        for item in self.data:
                            if item.k == l:
                                exists = True
                                item.pics.append(picpath)
                                break
                        if not exists:
                            nobj = obj(l)                        
                            nobj.pics.append(picpath)
                            self.data.append(nobj)

    def printdata(self):
        print("printdata")
        for o in self.data:            
            print(o.k)
            for p in o.pics:
                print(p)

            
                    


    

#m = Mapping("/home/user/Documents/Projekte/Image/test")
#m.printdata()
