from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog

global linewidth
linewidth = 1
root = Tk()

h = ttk.Scrollbar(root, orient=HORIZONTAL)
v = ttk.Scrollbar(root, orient=VERTICAL)
canvas = Canvas(root, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v.set, xscrollcommand=h.set)
h['command'] = canvas.xview
v['command'] = canvas.yview

canvas.grid(column=0, row=0, sticky=(N, W, E, S))
h.grid(column=0, row=1, sticky=(W, E))
v.grid(column=1, row=0, sticky=(N, S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

lastx, lasty = 0, 0


def xy(event):
    global lastx, lasty
    lastx, lasty = canvas.canvasx(event.x), canvas.canvasy(event.y)


def setColor(newcolor):
    global color
    color = newcolor
    canvas.dtag('all', 'paletteSelected')
    canvas.itemconfigure('palette', outline='white')
    canvas.addtag('paletteSelected', 'withtag', 'palette%s' % color)
    canvas.itemconfigure('paletteSelected', outline='#999999')

horizental = Scale(master=canvas, from_=1, to=150, orient = HORIZONTAL)
canvas.create_window(130, 0, anchor = 'nw', window = horizental)

def addLine(event):
    global lastx, lasty
    x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)
    canvas.create_line((lastx, lasty, x, y), fill='blue', width=horizental.get(), tags='currentline')
    lastx, lasty = x, y




canvas.bind("<Button-1>", xy)
canvas.bind("<B1-Motion>", addLine)


id = canvas.create_rectangle((10, 10, 30, 30), fill="red", tags=('palette', 'palettered'))
canvas.tag_bind(id, "<Button-1>", lambda x: setColor("red"))
id = canvas.create_rectangle((10, 35, 30, 55), fill="blue", tags=('palette', 'paletteblue'))
canvas.tag_bind(id, "<Button-1>", lambda x: setColor("blue"))
id = canvas.create_rectangle((10, 60, 30, 80), fill="black", tags=('palette', 'paletteblack', 'paletteSelected'))
canvas.tag_bind(id, "<Button-1>", lambda x: setColor("black"))
id = canvas.create_rectangle((10, 85, 30, 105), fill="green", tags=('palette', 'palettebgreen'))
canvas.tag_bind(id, "<Button-1>", lambda x: setColor("green"))

setColor('black')
canvas.itemconfigure('palette', width=5)

def open():
    global myimg
    global id_im
    canvas.filename = filedialog.askopenfilename(title = 'Select A File',
                                                 filetypes=(("jpg files", "*.jpg"),("all files", "*.*")) )
    myimg = ImageTk.PhotoImage(Image.open(canvas.filename))
    id_im = canvas.create_image(40, 45, image = myimg, anchor = 'nw')


b = ttk.Button(canvas, text='Import', command = open)
canvas.create_window(40, 0, anchor='nw', window=b)

def dsave():
    canvas.find_withtag(id_im)
    print(canvas.find_withtag(id_im))



s = ttk.Button(canvas, text='sv', command = dsave)
canvas.create_window(250, 0, anchor='nw', window=s)

root.mainloop()