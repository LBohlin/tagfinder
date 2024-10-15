from tkinter import *
from PIL import ImageTk, Image
from pathlib import Path

import mapping

root = Tk()
root.title("Using Pack")
root.geometry("1200x600")  # set starting size of window
root.config(bg="skyblue")

searchFrame = Frame(root, width=0, height=10, bg="#6FAFE7")
searchFrame.pack(side='top')

canvas = Canvas(root, height=800, width=600, background="lightblue")
                 
canvas.pack(expand=True, fill=BOTH)
#canvas.pack()


vbar = Scrollbar(canvas, orient = VERTICAL)
vbar.pack(side = RIGHT, fill = Y)
vbar.config(command = canvas.yview)
canvas.config(yscrollcommand=vbar.set)


infoFrame = Frame(canvas, width = 50, height = 100, bg='grey')
infoFrame.pack(side='right')

m = mapping.Mapping("/home/user/Documents/Projekte/Image/test")
pictures = []
labels = []

def searchFunction():
    global canvas, root
    searchKeys = searchEntry.get().split(' ')
    if len(list(filter(None,searchKeys))) < 1:
        return
    global labels
    for l in labels:        
        l.destroy()
    global pictures
    pictures = []
    labels = []
    metalist = []
    metadesc = []
    searchKeys=filter(None, searchKeys)
    for sk in searchKeys:
        print(sk)
        sublist = set()
        foundKeywords = []
        for k in m.data.keys():            
            if sk in k:
                for p in m.data[k]:
                    sublist.add(p)
                foundKeywords.append(k)
        # number of pictures NOT of keywords!!        
        desc = sk + ":"+ str(len(sublist)) + '('
        for k in foundKeywords:
            desc = desc + k[:-1] + ', '        
        desc = desc[:-2] + ')'
        metadesc.append(desc)
        metalist.append(sublist)
    imageSet = set.intersection(*metalist)
    
    x = 0
    y = 0
    height = 150
    dist = 70
    maxwidth = 800
    
    for img in imageSet:        
        if x > maxwidth:
            y = y + height + dist
            x = 0
            
        ppath = Path(img).parent        
        if not img.exists():            
            img = Path("/home/user/Documents/Projekte/Image/error.jpeg")
        temp = Image.open(img)
        relative = temp.width/temp.height
        
        temp = temp.resize((int(relative*height), height))
        image = ImageTk.PhotoImage(temp)                
        pictures.append(image)        
        label = Label(canvas, text=str(ppath).replace(m.basePath,"")[1:], image=image, compound='top')
        canvas.create_window(x,y,window=label, anchor=N+W)
        labels.append(label)
        x = x + int(relative*height) +dist
    metadesc.append("Keywörter:" + str(len(m.data.keys())))
    metadesc.append("Anzahl Objekte:" + str(m.numberOfObjects))
    for md in metadesc:    
        label = Label(infoFrame, text=md)
        label.pack()
        labels.append(label)
    root.update()
    print(canvas.bbox('all'))
    canvas.configure(scrollregion = (canvas.bbox('all')))

searchEntry = Entry(searchFrame, bd=3)
searchEntry.pack()#grid(row=0, column=0)

searchbutton = Button(searchFrame, text="search", command=searchFunction)
searchbutton.pack()#grid(row=0, column=1)

#m.printdata()



root.mainloop()
