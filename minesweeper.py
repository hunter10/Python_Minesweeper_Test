from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from random import randint
from random import *

N=20 #게임판의 갯수를 20*20의 크기로 만든다.
bomb=40 #지뢰 갯수를 40개로 만든다.

cnt = 0
map = [[0 for col in range(N+2)] for row in range(N+2)] # 맵을 만들자.
buttonchk = [[0 for col in range(N)] for row in range(N)] # 버튼이 눌렸는지 여부 
Button_X = [[0 for col in range(N)] for row in range(N)] # 깃발 플래그
visit = [[0 for col in range(N)] for row in range(N)] # 자동 열기 검출용 방문 여부
dir = [[0,1],[0,-1],[1,0],[-1,0]]
flag = bomb

root = Tk()
root.geometry("800x800")

# 왼쪽 버튼 클릭시 0의 위치이면 근처의 0의 위치를 모두 찾아서 셋팅하자.
def DFS(indx, indy):
    if(indx < 0 or indx >= N):
        return 0
    if(indy < 0 or indy >= N):
        return 0

    print("DFS 처리중")
    if Button_X[indy][indx] == 1:
       return 0

    if visit[indy][indx] == 0: # 한번도 방문 안한 위치라면
        visit[indy][indx] = 1

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
        if(Button_X[self.tmpy][self.tmpx] == 0): # 깃발이 없으면
            if(map[self.tmpy][self.tmpx] == -1): # 폭탄이라면
                #Button_map[self.tmpy][self.tmpx].Show(self.tmpx,self.tmpy)
                Game_over() # 전체 맵 보여주기 포함
            elif(map[self.tmpy][self.tmpx] == 0): # 빈 공간이라면
                Button_map[self.tmpy][self.tmpx].Show(self.tmpx,self.tmpy)
                buttonchk[self.tmpy][self.tmpx] = 1 # 이 버튼은 눌렸음.
                clear() # visit 데이터 초기화
                DFS(self.tempx, self.tempy) # 빈공간 처리 실행
            else:
                Button_map[self.tmpy][self.tmpx].Show(self.tmpx,self.tmpy)
                buttonchk[self.tmpy][self.tmpx] = 1 # 이 버튼은 눌렸음.

            print(f"Left {self.tmpx:10d}, {self.tmpy:10d}, {map[self.tmpx][self.tmpy]}")
        
    def Right(self, event):
        print("Right")

Button_map = [[Button_(0, 0) for col in range(N)] for row in range(N)]


def clear():
    for i in range(N):
        for j in range(N):
            visit[i][j] = 0

#게임을 성공했을때 메시지를 띄우자
def Game_clear():
    messagebox.showinfo("Success!", "Congratulation!")

# 게임실패시 메시지를 띄우자.
def Game_over():
    for i in range(N):
        for j in range(N):
            Button_map[i][j].Show(j,i)
    messagebox.showinfo("Game over...", "You Have Failed This Game... Try agian!")

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

'''
# 지뢰 갯수만큼 랜덤위치에 지뢰를 -1로 셋팅하자.
while(cnt < bomb):
    tmpx = randint(0,N-1)
    tmpy = randint(0,N-1)
    if(map[tmpy][tmpx] == -1):
        pass
    else:
        map[tmpy][tmpx] = -1
        cnt += 1
'''

#지뢰 테스트 세팅
map[1][1] = -1
map[2][2] = -1

# 지뢰 갯수를 세어서 맵에 세팅하자
# 지뢰 주변에 번호 세팅
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

root.mainloop()

