from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from random import randint
from random import *

N = 20    #게임판의 갯수를 20*20 의 크기로 만든다.
bomb = 40 # 지뢰 갯수를 40개로 만든다.

cnt = 0
map = [[0 for col in range(N+2)] for row in range(N+2)]    # 맵을 만들자.
buttonchk = [[0 for col in range(N)] for row in range(N)]
Button_X = [[0 for col in range(N)] for row in range(N)]
dir = [[0,1],[0,-1],[1,0],[-1,0]]
flag = bomb

root = Tk()
root.geometry("800x800")
visit = [[0 for col in range(N)] for row in range(N)]

def clear():
    for i in range(N):
        for j in range(N):
            visit[i][j] = 0

# 게임을 성공했을때 메시지를 띄우자
def Game_clear():
    messagebox.showinfo("Success!","Congratulations! You have Successed This Game!")

# 왼쪽 버튼 클릭시 0의 위치이면 근처의 0의 위치를 모두 찾아서 셋팅하자.
def DFS(indx,indy):
    if(indx < 0 or indx >= N):
        return 0
    if(indy < 0 or indy >= N):
        return 0

    #print(indx,indy)
    if Button_X[indy][indx] == 1:
        return 0
    if visit[indy][indx] == 0:
        visit[indy][indx] = 1
        if map[indy][indx] == 0:
            Button_map[indy][indx].Show(indx,indy)
            buttonchk[indy][indx] = 1
        elif map[indy][indx] > 0:
            Button_map[indy][indx].Show(indx, indy)
            buttonchk[indy][indx] = 1
            return 0
        for i in range(4):
            DFS(indx+dir[i][0],indy+dir[i][1])

    else:
        return 0

"""
def right(a,b):
    global flag
    cnt = 0
    print("right_clicked")
    if(not Button_X[b][a] == 1 and buttonchk[b][a] == 0):
        if(flag > 0):
            print(flag)
            Button_map[b][a].Num_Button["bg"] = "red"  #버튼의 색상을 변경하려고 했는데 변경이 안되고 bg 에러가 발생
            Button_X[b][a] = 1
            flag -= 1
        if(flag == 0):
            for i in range(N):
                for j in range(N):
                    if(buttonchk[i][j] == 1 and not map[i][j] == -1):
                        cnt += 1

            if cnt == 360:
                Game_clear()
    elif(Button_X[b][a] == 1):
        Button_map[b][a].Num_Button["bg"] = "white"
        Button_X[b][a] = 0
        flag += 1
def right(event):
    global flag
    cnt = 0
    a=10
    b=10
    print("right_clicked")
    print(type(Button_map[b][a].Num_Button))
    Button_map[b][a].Num_Button.configure(Button_map[b][a].Num_Button,bg="white")
    if(not Button_X[b][a] == 1 and buttonchk[b][a] == 0):
        if(flag > 0):
            print(flag)
            Button_map[b][a].Num_Button["bg"] = "red"
            Button_X[b][a] = 1
            flag -= 1
        if(flag == 0):
            for i in range(N):
                for j in range(N):
                    if(buttonchk[i][j] == 1 and not map[i][j] == -1):
                        cnt += 1

            if cnt == 360:
                Game_clear()
    elif(Button_X[b][a] == 1):
        Button_map[b][a].Num_Button["bg"] = "white"
        Button_X[b][a] = 0
        flag += 1
"""

# 버튼 클래스를 만들자.
class Button_:
    global map
    def __init__(self,x,y):
        self.tmpx = x
        self.tmpy = y
        self.Num_Button = ttk.Button(root,width = 4)
        self.Num_Button.grid(row=y, column=x,ipady = 5)
        self.Num_Button.bind('<Button-1>', self.Left)
        self.Num_Button.bind('<Button-3>', self.right)

    def Show(self,x1,y1):
        self.Num_Button.configure(text = str(map[y1][x1]))

    def Left(self,event):
        if(Button_X[self.tmpy][self.tmpx] == 0):
            if(map[self.tmpy][self.tmpx] == -1):
                Button_map[self.tmpy][self.tmpx].Show(self.tmpx,self.tmpy)
                Game_over()
            elif(map[self.tmpy][self.tmpx] == 0):
                Button_map[self.tmpy][self.tmpx].Show(self.tmpx,self.tmpy)
                buttonchk[self.tmpy][self.tmpx] = 1
                clear()
                DFS(self.tmpx,self.tmpy)
            else:
                Button_map[self.tmpy][self.tmpx].Show(self.tmpx,self.tmpy)
                buttonchk[self.tmpy][self.tmpx] = 1
            #obj = Button_map[tmpy][tmpx]
            #print("clicked")
        if (flag == 0):
            cnt = 0
            for i in range(N):
                for j in range(N):
                    if (buttonchk[i][j] == 1 and not map[i][j] == -1):
                        cnt += 1
            if cnt == N*N-bomb:
                Game_clear()

    def right(self, event):
        global flag
        cnt = 0
        #print("right_clicked")

        if (not Button_X[self.tmpy][self.tmpx] == 1 and buttonchk[self.tmpy][self.tmpx] == 0):
            if (flag > 0):
                #print(flag)
                Button_map[self.tmpy][self.tmpx].Num_Button.configure(text = "X")
                Button_X[self.tmpy][self.tmpx] = 1
                flag -= 1

        elif (Button_X[self.tmpy][self.tmpx] == 1 and buttonchk[self.tmpy][self.tmpx] == 0):
            #print("came")
            Button_map[self.tmpy][self.tmpx].Num_Button.configure(text = " ")
            Button_X[self.tmpy][self.tmpx] = 0
            flag += 1
        if (flag == 0):
            for i in range(N):
                for j in range(N):
                    if (buttonchk[i][j] == 1 and not map[i][j] == -1):
                        cnt += 1
            if cnt == N*N-bomb:
                Game_clear()


Button_map = [[Button_(0,0) for col in range(N)] for row in range(N)]

# 게임실패시 메시지를 띄우자.
def Game_over():
    for i in range(N):
        for j in range(N):
            Button_map[i][j].Show(j,i)
    messagebox.showinfo("Game over...", "You Have Failed This Game... Try agian!")
    #frame = ttk.Frame(root,width = 50,height = 50,text = "Game over! Try again!")
    #frame.pack()

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

# 지뢰 갯수를 세어서 맵에 셋팅하자.
for i in range(N):
    for j in range(N):
        if(map[i][j] == 0):
            map[i][j] = count(i,j)

# 버튼을 20*20으로 만들어서 셋팅하자.
for i in range(N):
    for j in range(N):
        Button_map[i][j] = Button_(j,i)

root.mainloop()