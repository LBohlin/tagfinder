import subprocess, sys
from pathlib import Path
dummypic = "/home/user/Documents/Projekte/Image/error.jpeg"
class pic:
    path = Path
    def __init__(self, path):
        if path.exists():
            self.path = path
        else:
            self.path = Path(dummypic)
        self.ppath = path.parent

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
                    print(lines)
                    for l in lines:
                        exists = False
                        for item in self.data:
                            if item.k == l:
                                print("true")
                                exist = True
                                item.pics.append(pic(picpath))
                                break
                        if not exists:
                            nobj = obj(l)                        
                            nobj.pics.append(pic(picpath))                        
                            self.data.append(nobj)

    def printdata(self):
        print("printdata")
        for o in self.data:            
            print(o.k)
            for p in o.pics:
                print(p.path)

            
                    


    

#m = Mapping("/home/user/Documents/Projekte/Image/test")
#m.printdata()
