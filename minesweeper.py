from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from random import randint
from random import *

N=20 #게임판의 갯수를 20*20의 크기로 만든다.
bomb=2 #지뢰 갯수를 40개로 만든다.

cnt = 0
map = [[0 for col in range(N+2)] for row in range(N+2)] # 맵을 만들자.
buttonchk = [[0 for col in range(N)] for row in range(N)] # 버튼이 눌렸는지 여부 
Button_X = [[0 for col in range(N)] for row in range(N)] # 깃발 플래그
visit = [[0 for col in range(N)] for row in range(N)] # 자동 열기 검출용 방문 여부 빈공간 클릭시 초기화하고 전체 영역 검사

# visit 와 buttonchk 을 같은 성격의 데이터로 보고 처리하면 되지 않을까?

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

    #print("DFS 처리중")
    if Button_X[indy][indx] == 1:
       return 0

    if visit[indy][indx] == 0: # 한번도 방문 안한 위치라면
        visit[indy][indx] = 1 # 방문변수 체크후

        if(not map[indy][indx] == -1): # 맵 데이터가 폭탄이 아니라면
            Button_map[indy][indx].Show(indx,indy) # 버튼에 맵 데이터 보여주기
            #buttonchk[indy][indx] = 1 # 버튼이 눌렸다고 체크
        
        if(map[indy][indx] > 0): # 맵 데이터가 빈칸이 아니라면 DSF종료
            return 0

        '''
        if map[indy][indx] == 0: # 맵 데이터가 비어있는 거라면
            #Button_map[indy][indx].Show(indx,indy) # 버튼에 맵 데이터 보여주기
            #buttonchk[indy][indx] = 1 # 버튼이 눌렸다고 체크
        elif map[indy][indx] > 0: # 맵 데이터가 폭탄 말고 뭔가 있다면
            #Button_map[indy][indx].Show(indx,indy) # 버튼에 맵 데이터 보여주기  
            #buttonchk[indy][indx] = 1 # 버튼이 눌렸다고 체크
            return 0
        '''

        for i in range(4): # 맵데이터가 비어있다면 
            DFS(indx+dir[i][0], indy+dir[i][1]) # 현재 위치 기준 사방 각 블록 체크
    else:
        return 0



class Button_:
    global map
    def __init__(self, x, y):
        self.tmpx = x
        self.tmpy = y
        self.Num_Button = ttk.Button(root, width=3)
        self.Num_Button.grid(row=y, column=x, ipady=4)
        self.Num_Button.bind('<Button-1>', self.Left)
        self.Num_Button.bind('<Button-3>', self.Right) # 맥은 Button-2, PC Button-3

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
                clear() # visit 데이터 초기화 ... buttonchk 데이터 초기화? ... 바로 윗줄의 buttonchk 데이터가 클리어되는 상황?...
                DFS(self.tmpx, self.tmpy) # 빈공간 처리 실행
                
            else:
                Button_map[self.tmpy][self.tmpx].Show(self.tmpx,self.tmpy)
                buttonchk[self.tmpy][self.tmpx] = 1 # 이 버튼은 눌렸음.
        
        if(flag == 0):
            cnt = 0
            for i in range(N):
                for j in range(N):
                    if(buttonchk[i][j]==1 and not map[i][j] == -1): # 버튼은 눌렸지만 폭탄이 아닌거
                        cnt += 1

            print("cnt ", cnt)
            if cnt == N * N - bomb: #모든 칸에서 폭탄을 뺀 칸과 클릭한 칸 숫자가 같으면 승리!!
                Game_clear()
            
            #print(f"Left {self.tmpx:10d}, {self.tmpy:10d}, {map[self.tmpx][self.tmpy]}")
        
    def Right(self, event): # 깃발 찍기
        global flag
        cnt = 0
        print("Right")

        if(not Button_X[self.tmpx][self.tmpy] == 1 and buttonchk[self.tmpx][self.tmpy] == 0): #깃발찍기
            if(flag > 0):   
                Button_map[self.tmpx][self.tmpy].Num_Button.configure(text = "X")
                Button_X[self.tmpx][self.tmpy] = 1
                flag -= 1
        elif(Button_X[self.tmpx][self.tmpy] == 1 and buttonchk[self.tmpy][self.tmpx] == 0): #깃발빼기
            Button_map[self.tmpy][self.tmpx].Num_Button.configure(text = " ")
            Button_X[self.tmpy][self.tmpx] = 0
            flag += 1
        
        if(flag==0):
            for i in range(N):
                for j in range(N):
                    if(buttonchk[i][j] == 1 and not map[i][j] == -1):
                        cnt += 1

            if cnt == N * N - bomb:
                Game_clear()

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

