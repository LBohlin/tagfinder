import subprocess, sys
import datetime
from pathlib import Path

# define possible parameters and their type.
class SecParam:
    date: datetime.date

class Mapping:    
    def __init__(self, path):
        #map keywords to paths:
        self.data = dict()
        #map paths to secondary parameters:
        self.sparam = dict()

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
                        l = l.lower()
                        # evaluate command characters
                        if l[0] == '#':
                            continue
                        # ! is treated as a character to allow special properties
                        if l[0] == '!':
                            # date syntax "!d:DD.MM.YYYY
                            if l[1] == 'd':
                                dateComp = l.split(':')[1].split('.')
                                date=datetime.date(int(dateComp[2]),int(dateComp[1]),int(dateComp[0]))
                                if not p in self.sparam:
                                    self.sparam[picpath] = SecParam()
                                self.sparam[picpath].date = date

                            # else if other command chars
                            continue
                        
                        if l in self.data:
                            s = self.data.get(l)
                        else:
                            s = set()
                        s.add(picpath)                            
                        self.data[l] = s
                # evaluate lines containing a command:
                

    def search(self, searchKeys):
        metalist = []
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
                    metalist.append(sublist)
                    imageSet = set.intersection(*metalist)
            # generalisation for more search parameters should be added here
            sortlist = list()
            for i in imageSet:
                if i in self.sparam:
                    entry = [i,self.sparam[i].date]
                else:
                    entry = [i,datetime.date(3000,1,1)]
                sortlist.append(entry)
                print(entry)
            sortlist.sort(key=lambda x: x[1])
            results = list()
            # remove the secondary parameters needed for sorting
            for e in sortlist:
                results.append(e[0])                
        return results
                
    def printdata(self):
        print("printdata")
        for k in self.data.keys():
            print(k)
            print(self.data[k])
