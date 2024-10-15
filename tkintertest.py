from tkinter import *
from PIL import ImageTk, Image
from pathlib import Path

import mapping

root = Tk()
root.title("Using Pack")
root.geometry("1000x600")  # set starting size of window
root.config(bg="skyblue")

searchFrame = Frame(root, width=0, height=10, bg="#6FAFE7")
#searchFrame.grid(row=0, column=0)
searchFrame.pack()
pictureFrame = Frame(root, width=200, height=400, bg='grey')
pictureFrame.pack()#.grid(row=1, column=0, padx=10, pady=5)
#scale = Scale(master=root, orient=VERTICAL, from_=1, to=len(imageList)/8, resolution=1, showvalue=False, command=toFrame)
#scale.grid(row=1, column=1)
m = mapping.Mapping("/home/user/Documents/Projekte/Image/test")
pictures = []
labels = []
def searchFunction():
    searchKeys = searchEntry.get().split(' ')
    #x = searchEntry.get()
    global labels
    for l in labels:        
        l.destroy()
    global pictures
    pictures = []
    labels = []
    metalist = []
    for sk in searchKeys:
        sublist = set()
        for k in m.data.keys():                
            if sk in k:
                for p in m.data[k]:
                    sublist.add(p)
        metalist.append(sublist)
    imageSet = set.intersection(*metalist)
    print(imageSet)
    r = 0
    c = 0
    for img in imageSet:        
        if c > 3:
            c = 0
            r = r + 1
        ppath = Path(img).parent        
        if not img.exists():            
            img = Path("/home/user/Documents/Projekte/Image/error.jpeg")
        temp = Image.open(img)
        relative = temp.width/temp.height
        height = 150
        temp = temp.resize((int(relative*height), height))
        image = ImageTk.PhotoImage(temp)                
        pictures.append(image)                       
        label = Label(pictureFrame, text=ppath, image=image, compound='top')
        label.pack()
        #label.grid(row=r, column=c, padx=1, pady=1)
        labels.append(label)
        c = c + 1
    pictureFrame.update()

searchEntry = Entry(searchFrame, bd=3)
searchEntry.pack()#grid(row=0, column=0)

searchbutton = Button(searchFrame, text="search", command=searchFunction)
searchbutton.pack()#grid(row=0, column=1)


m.printdata()



root.mainloop()
