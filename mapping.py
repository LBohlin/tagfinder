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
        # possible names of subfolders
        self.SUBFOLDERS = ["files", "images"]

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
                        # $ is treated as a character to allow special properties
                        if l[0] == '$':
                            # date syntax "!d:DD.MM.YYYY
                            if l[1] == 'd':
                                dateComp = l.split(':')[1].split('.')
                                date=datetime.date(int(dateComp[2]),int(dateComp[1]),int(dateComp[0]))
                                if not p in self.sparam:
                                    self.sparam[picpath] = SecParam()
                                self.sparam[picpath].date = date

                            # no continue, the date is supposed to work as a search parameter
                            # else if other command chars
                            
                        
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
        notSearchedKeys = []        
        results = []
        for k in searchKeys:
            if k[0] == '!':
                notSearchedKeys.append(k[1:])
        if (len(searchKeys) == len(notSearchedKeys)):
            searchKeys.append('*')
        searchKeys=list(filter(None, searchKeys))
        # create a set of !searched keywords to exclude
        notSearchedSet = set()
        for nsk in notSearchedKeys:
            for k in self.data.keys():
                if nsk in k:
                    for p in self.data[k]:
                        notSearchedSet.add(p)
        for sk in searchKeys:
            # if !sk don't waste time
            if sk[0] == '!':
                continue
            resultSet = set()
            foundKeywords = []
            for k in self.data.keys():            
                if sk == '*' or sk in k:
                    for p in self.data[k]:
                        resultSet.add(p)
                    foundKeywords.append(k)
            if len(foundKeywords) > 0:
                # number of pictures NOT of keywords!!
                for k in foundKeywords:                    
                    metalist.append(resultSet-notSearchedSet)
                    imageSet = set.intersection(*metalist)
            results = list()
            for i in imageSet:
                results.append(i)
            results.sort(reverse=True,key=lambda x: datetime.date(1,1,1) if x not in self.sparam else self.sparam[x].date)
        return results
                
    def printdata(self):
        print("printdata")
        for k in self.data.keys():
            print(k)
            print(self.data[k])
