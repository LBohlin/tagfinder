from tkinter import *

from PIL import ImageTk, Image

import mapping
root = Tk()
root.title("Using Pack")
root.geometry("1000x600")  # set starting size of window
root.config(bg="skyblue")

searchFrame = Frame(root, width=0, height=10, bg="#6FAFE7")
searchFrame.grid(row=0, column=0)
pictureFrame = Frame(root, width=200, height=400, bg='grey')
pictureFrame.grid(row=1, column=0, padx=10, pady=5)
#scale = Scale(master=root, orient=VERTICAL, from_=1, to=len(imageList)/8, resolution=1, showvalue=False, command=toFrame)
#scale.grid(row=1, column=1)
def searchFunction():
    x = searchEntry.get()
    print(x)


searchFrame.grid(row=0,column=0)

#Label(searchFrame, bg="#6FAFE7").pack(side='left', padx=5)

searchEntry = Entry(searchFrame, bd=3)
searchEntry.grid(row=0, column=0)

searchbutton = Button(root, text="search", command=searchFunction)
searchbutton.grid(row=0, column=1)

def toFrame(i):
    print("next")

m = mapping.Mapping("/home/user/Documents/Projekte/Image/test")
m.printdata()

imageList = ["pic/pic.jpg","pic/pic2.gif","pic/pic.gif","pic/pic.gif","pic/pic.gif","pic/pic.gif","pic/pic.gif","pic/pic.gif","pic/pic.gif", "pic/pic.gif","pic/pic2.gif","pic/pic.gif","pic/pic.gif","pic/pic.gif","pic/pic.gif","pic/pic.gif","pic/pic.gif"]

r = 0
c = 0
pictures = []
for img in imageList:
    if c > 3:
        c = 0
        r = r + 1
    temp = Image.open(img)
    temp=temp.resize((150, 100))
    image = ImageTk.PhotoImage(temp)
    
    #original_image = image.subsample(5,5)  # resize image using subsample
    pictures.append(image)
    Label(pictureFrame, image=image).grid(row=r, column=c, padx=1, pady=1)
    c = c + 1


root.mainloop()
