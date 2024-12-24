from tkinter import *
from PIL import ImageTk, Image
from pathlib import Path

import mapping

root = Tk()
root.title("tagfinder")
root.geometry("1200x600")  # set starting size of window
root.config(bg="skyblue")

searchFrame = Frame(root, width=0, height=10, bg="#6FAFE7")
searchFrame.pack(side='top')

canvas = Canvas(root, height=800, width=600, background="lightblue")

canvas.pack(expand=True, fill=BOTH)

vbar = Scrollbar(canvas, orient = VERTICAL)
vbar.pack(side = RIGHT, fill = Y)
vbar.config(command = canvas.yview)
canvas.config(yscrollcommand=vbar.set)


#infoFrame = Frame(canvas, width = 50, height = 100, bg='grey')
#infoFrame.pack(side='right')
configpath = Path("./config.txt")

if  (not configpath.exists()) or (not Path("./error.jpeg").exists()):
    print("Wrong working directory, config or error.jpeg missing.")
    exit(1)
    
f = open(configpath, "r")
config = f.readline()
config = config.replace('\n','')
f.close()

m = mapping.Mapping(config)
pictures = []
labels = []
def on_mousewheel(event):    
    if event.num == 4:
        direction = -1
    else:
        direction = 1
    canvas.yview_scroll(direction, "units")
root.bind("<Button-4>", on_mousewheel)
root.bind("<Button-5>", on_mousewheel)

def searchFunction():
    global canvas, root
    searchKeys = searchEntry.get().lower().split(' ')
    if len(list(filter(None,searchKeys))) < 1:
        return
    
    global labels
    for l in labels:        
        l.destroy()
    global pictures
    pictures = []
    labels = []

    results = m.search(searchKeys)    
    x = 0
    y = 0
    height = 150
    dist = 70
    maxwidth = 800
    for img in results:        
        if x > maxwidth:
            y = y + height + dist
            x = 0
            
        ppath = Path(img).parent        
        if not img.exists():            
            img = Path("./error.jpeg")
        temp = Image.open(img)
        relative = temp.width/temp.height
        
        temp = temp.resize((int(relative*height), height))
        image = ImageTk.PhotoImage(temp)                
        pictures.append(image)        
        label = Label(canvas, text=str(ppath).replace(m.basePath,"")[1:], image=image, compound='top')        
        label.pack()
        canvas.create_window(x,y,window=label, anchor=NW)
        wdth=label.winfo_reqwidth()
        labels.append(label)
        x = x + wdth
    root.update()
    canvas.configure(scrollregion = (canvas.bbox('all')))

searchEntry = Entry(searchFrame, bd=3)
searchEntry.pack()

searchButton = Button(searchFrame, text="search", command=searchFunction)
searchButton.pack()
root.bind('<Return>', lambda enter: searchButton.invoke())
searchEntry.focus_set()
#m.printdata()



root.mainloop()
