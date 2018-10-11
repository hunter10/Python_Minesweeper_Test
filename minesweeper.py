from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from random import randint
from random import *

N=20 #게임판의 갯수를 20*20의 크기로 만든다.
bomb=40 #지뢰 갯수를 40개로 만든다.

cnt = 0
map = [[0 for col in range(N+2)] for row in range(N+2)]
buttonchk = [[0 for col in range(N)] for row in range(N)]
Button_X = [[0 for col in range(N)] for row in range(N)]
dir = [[0,1],[0,-1],[1,0],[-1,0]]
flag = bomb

root = Tk()
root.geometry("800x800")
visit = [[0 for col in range(N)] for row in range(N)]

'''
canvas_height = 400
canvas_width = 600
canvas_colour = "black"
canvas = Canvas(bg=canvas_colour, 
                height=canvas_height, 
                width=canvas_width, 
                highlightthickness=0)
canvas.pack()
'''

#topframe = Frame(root)
#topframe.pack()

class Button_:
    global map
    def __init__(self, x, y):
        self.tmpx = x
        self.tmpy = y
        self.Num_Button = ttk.Button(root, width=4)
        self.Num_Button.grid(row=y, column=x, ipady=5)
        self.Num_Button.bind('<Button-1>', self.Left)
        self.Num_Button.bind('<Button-3>', self.Right)

    def Show(self, x1, y1):
        self.Num_Button.configure(text = str(map[y1][x1]))

    def Left(self, event):
        print(f"Left {self.tmpx:10d}, {self.tmpy:10d}, {map[self.tmpx][self.tmpy]}")
        
    def Right(self, event):
        print("Right")

Button_map = [[Button_(0, 0) for col in range(N)] for row in range(N)]

'''
def clear():
    for i in range(N):
        for j in range(N):
            visit[i][j] = 0

#게임을 성공했을때 메시지를 띄우자
def Game_clear():
    messagebox.showinfo("Success!", "Congratulation!")

#Game_clear()
'''

# 사방의 지뢰의 갯수를 세어서 리턴하자
def count(x,y):
    cnt_ = 0
    if(map[x + 1][y] == -1):
        cnt_ += 1
    if(map[x - 1][y] == -1):
        cnt_ += 1
    if(map[x][y + 1] == -1):
        cnt_ += 1
    if(map[x][y - 1] == -1):
        cnt_ += 1
    if(map[x + 1][y + 1] == -1):
        cnt_ += 1
    if(map[x + 1][y - 1] == -1):
        cnt_ += 1
    if(map[x - 1][y + 1] == -1):
        cnt_ += 1
    if(map[x - 1][y - 1] == -1):
        cnt_ += 1
    return cnt_


# 맵을 0으로 초기화 하자
for i in range(N):
    for j in range(N):
        map[i][j] = 0

# 지뢰 갯수만큼 랜덤위치에 지뢰를 -1로 셋팅하자.
while(cnt < bomb):
    tmpx = randint(0,N-1)
    tmpy = randint(0,N-1)
    if(map[tmpy][tmpx] == -1):
        pass
    else:
        map[tmpy][tmpx] = -1
        cnt += 1

# 지뢰 갯수를 세어서 맵에 세팅하자
for i in range(N):
    for j in range(N):
        if(map[i][j]==0):
            map[i][j] = count(i, j)

# 버튼을 20*20으로 만들어서 세팅하자
for i in range(N):
    for j in range(N):
        Button_map[i][j] = Button_(j,i)

def All_Show():
    for i in range(N):
        for j in range(N):
            Button_map[i][j].Show(j,i)

#Button(topframe, text="All", command=All_Show, width=50).pack(side=LEFT)

root.mainloop()

#if __name__ == '__main__':
#    main()
