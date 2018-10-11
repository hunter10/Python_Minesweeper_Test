from tkinter import *
import random
import time

tk = Tk()
canvas = Canvas(tk, width=500, height=500)
canvas.pack()
canvas.create_polygon(250, 400, 275, 450, 225, 450)
for y in range(0, 70):
    canvas.move(1, 0, -5)
    tk.update()
    time.sleep(0.05)

tk.mainloop()
