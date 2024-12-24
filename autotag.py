import subprocess, sys, os, datetime
from pathlib import Path

TAG="$AUTOTAG$"
PICFORMATS=[".gif", ".jpg", ".png"]

configpath = Path("./config.txt")
if  (not configpath.exists()):
    print("Wrong working directory.")
    exit(1)
f = open(configpath, "r")
config = f.readline()
path = config.replace('\n','')
f.close()
          
fileTypes = ["*.gif", "*.jpg", "*.png", "*.stl"]
paths = set()
for ft in fileTypes:
    l = subprocess.run(["find", path, "-name", ft], capture_output=True).stdout.decode("utf-8")
    objects = list(filter(None,l.split('\n')))
    for o in objects:
        paths.add(Path(o).parent)

print(paths)
        
for p in paths:
    infoPath = p.joinpath("info.txt")
    linkPath =p.joinpath("pic")
    if (os.path.exists(infoPath)):
        info = open(infoPath, "r")
        if info.readline()[:9] == TAG:
            print("Automatisch generierte Tags in " + str(p) + " werden gelöscht.")
            os.remove(infoPath)            
            if os.path.exists(linkPath):
                os.unlink(linkPath)
        else:
            # don't generate a tag if info.txt without autotag keyword exists
            continue
    files = [x for x in p.glob('*')]
    infoFile = open(infoPath,'a')
    infoFile.write(TAG+'\n')
    oldestModDate = datetime.date(1,1,1)
    newestModDate = datetime.date(3000,1,1)
    symlinkDate = datetime.date(1,1,1)
    symlinkTarget = None
    print("Gefundene Files: ")
    print(files)
    for f in files:
        name = f.name
        infoFile.write(str(name)+'\n')
        date=datetime.date.fromtimestamp(os.path.getmtime(f))
        if (date<newestModDate):
            newestModDate = date
        if (date>oldestModDate):
            oldestModDate = date
        for pf in PICFORMATS:
            if pf in name:
                if date > symlinkDate:
                    symlinkTarget=f
                    break
    print("Neustes gefundenes Bild: "+str(symlinkTarget))
    if symlinkTarget:        
        linkPath.symlink_to(symlinkTarget.resolve())
    timetag = "!d:" + str(oldestModDate.day) + '.' + str(oldestModDate.month) + '.' + str(oldestModDate.year)
    infoFile.write(timetag)
    infoFile.close()
             
    
        

