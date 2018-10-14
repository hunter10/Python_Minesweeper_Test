import enum
import time
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image
# python3에서는 pillow로 대체 되었다. pillow 설치하고 이렇게 사용해도 된다.

np.random.seed(1)
PhotoImage = ImageTk.PhotoImage # 사진을 object로 받을 것이라는 의미
CellPerPixel = 50  # 셀 당 픽셀 (한 셀의 크기)
CellCenter = 25 # CellPerPixel / 2 # 셀 중앙 위치(픽셀)
MapWidth = 14  # 그리드 월드 가로셀 갯수 14열
MapHeight = 9  # 그리드 월드 세로셀 갯수 9행 
mine = 2 # 전체 지뢰갯수
flag = mine # 전체 깃발갯수, 나중에 깃발 갯수와 지뢰위치가 같으면 승리

# 논리적 맵 좌표
# 2차원 리스트에 접근할때 조심 - 헷갈리기 쉬움.
# map[row][col] 으로 접근해야 함. 좌표는 (x, y)
map = [[0 for col in range(MapWidth+2)] for row in range(MapHeight+2)] # 맵을 만들자. count 유틸함수 때문에 +2
flag_map = [[0 for col in range(MapWidth)] for row in range(MapHeight)] # 깃발 여부만 체크하는 맵
visit = [[0 for col in range(MapWidth)] for row in range(MapHeight)] # 자동 열기 검출용 방문 여부 빈공간 클릭시 초기화하고 전체 영역 검사
dir = [[0,1],[0,-1],[1,0],[-1,0]]

class ActionType(enum.Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    BREAK = 4
    FLAG = 5

class Env(tk.Tk): #tkinter module 상속받기
    
    # 생성자
    def __init__(self):
        super(Env, self).__init__() #tkinter module의 생성자 실행
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('MI_TF_Project 9*14 size_map')
        self.geometry('{0}x{1}'.format(MapWidth * CellPerPixel, MapHeight * CellPerPixel)) # setting window_size
        self.shapes = self.load_images()
        self.canvas = self._build_canvas()
        self.texts = []

        self.IsBombTouch = False
        self.currAct = ActionType.RIGHT # 주인공 초기 방향
        self.currCellPos = [0, 0]   # 주인공 초기 위치

    # canvas 그리는 method
    def _build_canvas(self):
        canvas = tk.Canvas(self, bg='white', height = MapHeight * CellPerPixel, width = MapWidth * CellPerPixel)
        canvas.pack()

        # 가로 방향으로 움직이면서 세로 선 한 칸씩 그리기 : 0, 800, 100
        # 시점=(x0, y0), 종점=(x1, y1)
        # line 그릴 때 for loop에서 0을 반드시 추가...
        for c in range(0, MapWidth * CellPerPixel, CellPerPixel):  
            x0, y0, x1, y1 = c, 0, c, MapHeight * CellPerPixel
            canvas.create_line(x0, y0, x1, y1)

        # 세로 방향으로 움직이면서 가로 선 한 칸씩 선 그리기 : 0, 1300, 100
        for r in range(0, MapHeight * CellPerPixel, CellPerPixel):
            x0, y0, x1, y1 = 0, r, MapWidth * CellPerPixel, r           
            canvas.create_line(x0, y0, x1, y1)
        
        # 캔버스에 이미지 추가, 이미지가 나타날 좌표와 대상 정하기.
        # self.shapes가 하나의 list로 image file을 원소로 하는 tuple
        x = CellCenter
        y = CellCenter
        self.player = canvas.create_image(x, y, image=self.shapes[0]) # player
       
        '''
        # 처음부터 지뢰 위치를 표시할지
        for row in range(MapHeight):
            for col in range(MapWidth):
                if(map[row][col] == -1):
                    tempPixel = self.CellToPixel([row, col])
                    self.bomb = canvas.create_image(tempPixel[0], tempPixel[1], image=self.shapes[1]) # mine
        '''
        
        x = (MapWidth * CellPerPixel) - CellCenter
        y = (MapHeight * CellPerPixel) - CellCenter
        self.goal = canvas.create_image(x, y, image=self.shapes[2]) # goal

        return canvas

    # canvas에 넣을 img file object로 불러오는 method
    def load_images(self):
        player = PhotoImage(Image.open("img/agent.png").resize((35, 35)))
        bomb = PhotoImage(Image.open("img/mine.png").resize((35, 35)))
        goal = PhotoImage(Image.open("img/finish.png").resize((35, 35)))
        return player, bomb, goal

    # 픽셀에서의 위치 -> state 좌표로 변환 method
    def coords_to_state(self, coords):
        x = int((coords[0] - 50) / 100)
        y = int((coords[1] - 50) / 100)
        return [x, y]

    # 움직이는 놈인 rectangle을 시작점에 놓기
    def reset(self):
        self.update()
        time.sleep(0.5)
        x, y = self.canvas.coords(self.rectangle) # 픽셀 단위 좌표 return
        self.canvas.move(self.rectangle, CellPerPixel / 2 - x, CellPerPixel / 2 - y) # object를 설정한 픽셀 좌표로 움직이게 
        self.render()
        return self.coords_to_state(self.canvas.coords(self.rectangle))

    # agent의 action 결정은 sarsa_agent.py에서 하고 여기에선 결정 난 action을 좌표평면에 표시해주는 역할을 한다.
    def step(self, action):
        state = self.canvas.coords(self.rectangle)
        base_action = np.array([0, 0])
        self.render()

        # state를 index화 하였지만 실제로 작동될 때는 pixel 값을 기준으로 한 좌표로 계산 된다.
        if action == 0:  # 상
            if state[1] > CellPerPixel: # map의 경계선 확인
                base_action[1] -= CellPerPixel
        elif action == 1:  # 하
            if state[1] < (MapHeight - 1) * CellPerPixel:
                base_action[1] += CellPerPixel
        elif action == 2:  # 좌
            if state[0] > CellPerPixel:
                base_action[0] -= CellPerPixel
        elif action == 3:  # 우
            if state[0] < (MapWidth - 1) * CellPerPixel:
                base_action[0] += CellPerPixel

        # 에이전트 이동 : canvas.move가 agent를 이동하게 해주는 핵심적인 method이다.
        # 따로 저장하지 않아도 object에 변화된 값이 적용된다.
        self.canvas.move(self.rectangle, base_action[0], base_action[1])
        
        # 에이전트(빨간 네모)를 가장 상위로 배치 : 마치 한글에서 맨 앞으로 배치와 같다.
        self.canvas.tag_raise(self.rectangle)

        # 픽셀 값 좌표로 return.
        next_state = self.canvas.coords(self.rectangle)

        # 보상 함수
        if next_state == self.canvas.coords(self.circle):
            reward = 1000
            done = True ; sucess=0
        elif next_state in [self.canvas.coords(self.triangle1), self.canvas.coords(self.triangle2), self.canvas.coords(self.triangle3)]: # fail case 설정
            reward = -100
            done = True ; sucess=1
        else:
            reward = 0
            done = False ; sucess=2

        next_state = self.coords_to_state(next_state)

        # 결국 가장 핵심적인 내용은 모든 요소들을(map, agent, obstacle) 좌표화 하는 것이다.
        return next_state, reward, done, sucess

    def render(self):
        time.sleep(0.03)
        self.update()

    # 0이 아닌것이 나올때까지 찾는 함수
    def DFS(self, row, col):
        if(col < 0 or col >= MapWidth):
            return 0
        if(row < 0 or row >= MapHeight):
            return 0
        if flag_map[row][col] == 1:
           return 0
        
        if visit[row][col] == 0: # 한번도 방문 안한 위치라면
            visit[row][col] = 1 # 방문변수 체크후

            if(not map[row][col] == -1): # 맵 데이터가 폭탄이 아니라면
                data = map[row][col] # 맵 데이터 보여주기
                pixelcoords = self.CellToPixel([row, col])
                self.canvas.create_text(pixelcoords[0], pixelcoords[1]+5, font="Times 12 italic bold", text=str(data))
                #buttonchk[indy][indx] = 1 # 버튼이 눌렸다고 체크
        
            if(map[row][col] > 0): # 맵 데이터가 빈칸이 아니라면 DSF종료
                return 0

            for i in range(4): # 맵데이터가 비어있다면 
                #dir = [[0,1],[0,-1],[1,0],[-1,0]]
                self.DFS(row+dir[i][0], col+dir[i][1]) # 현재 위치 기준 사방 각 블록 체크
        else:
            return 0


    # 픽셀값을 셀 인덱스 값으로 변환해서 돌려줌.
    # 주의할것은 좌표는 [x, y], 셀 인덱스는 [row, col]
    def PixelToCell(self, p_coords):
        cellX = int(p_coords[1] / CellPerPixel)
        cellY = int(p_coords[0] / CellPerPixel)
        return [cellX, cellY]

    # 셀 픽셀값으로 변환해서 돌려줌. 이때 계산 편의성 때문에 셀 중앙값으로 변환
    # 주의할것은 좌표는 [x, y], 셀 인덱스는 [row, col]
    def CellToPixel(self, c_coords): 
        pixelX = int(c_coords[1] * CellPerPixel) + CellCenter
        pixelY = int(c_coords[0] * CellPerPixel) + CellCenter
        return [pixelX, pixelY]

    # 셀 인덱스값을 받아서 폭탄인지 체크
    # 주의할것은 좌표는 [x, y], 셀 인덱스는 [row, col]
    def CheckBomb(self, c_coords):
        row = int(c_coords[0])
        col = int(c_coords[1])
        if(map[row][col] == -1):
            return True
        else:
            return False
    
    # 현재 세팅되어 있는 액션 방향의 다음 셀의 좌표을 얻어옴
    # 주의할것은 좌표는 [x, y], 셀 인덱스는 [row, col]
    def GetNextCell(self):
        if(self.currAct == ActionType.UP):
            tempCellPos = [self.currCellPos[0]-1, self.currCellPos[1]]
        elif(self.currAct == ActionType.DOWN):
            tempCellPos = [self.currCellPos[0]+1, self.currCellPos[1]]
        elif(self.currAct == ActionType.LEFT):
            tempCellPos = [self.currCellPos[0], self.currCellPos[1]-1]
        elif(self.currAct == ActionType.RIGHT):
            tempCellPos = [self.currCellPos[0], self.currCellPos[1]+1]

        return tempCellPos

    # 맵 가장자리 바깥체크 (입력한 좌표가 바깥으로 나갔다면 True)
    def CheckMapOutBound(self, c_coords):
        if(c_coords[0] < 0 or c_coords[0] > MapWidth or
           c_coords[1] < 0 or c_coords[1] > MapHeight):
           print("CheckMapOutBound... True")
           return True
        else:
            print("CheckMapOutBound... False")
            return False
    
    # Action값이 Break, Flag 라면 현재바라보는 방향의 다음 셀을 좌표로 받음
    def GetActionResult(self, act):
        print("GetActionResult : ", act)
        
        # 이 부분은 처리 애매함... 
        # 가장자리라면 에이전트에 값을 주지 말아야할지등 처리방법 정해야 함.
        #if(act == ActionType.BREAK or act == ActionType.FLAG): # 맵의 가장자리 체크
        #    IsMapOut = self.CheckMapOutBound(self.GetNextCell())
        #    if(IsMapOut == True):
        #        return
        
        if(act == ActionType.BREAK):
            self.IsBombTouch = self.CheckBomb(self.GetNextCell()) # 폭탄 체크
            if(self.IsBombTouch == True): # 폭탄 건드리면 게임오버
                return
            else:
                # 맵 열기 
                return
        
        elif(act == ActionType.FLAG):
            # 맵에 깃발 꽂기
            self.Act_Flag(self.GetNextCell())
            return

        else: # 방향값을 받으면 다음 셀의 픽셀값을 리턴
            tempCellCoord = self.GetNextCell()
            tempPixel = self.CellToPixel(tempCellCoord)

        #print("Action 액션값에 따라 숫자리스트, 다음셀의 좌표, 깃발표시등을 리턴")
        print("Action number list, next cell coords, flag")

    def LClick(self, event):
        x = event.x
        y = event.y
        #print("LClick [", x, y, "] ---> ", "Cell ", self.PixelToCell([x, y]))
        self.Act_Break(self.PixelToCell([x, y]))

    def RClick(self, event):
        x = event.x
        y = event.y
        #print("RClick [", x, y, "] ---> ", "Cell ", self.PixelToCell([x, y]))
        self.Act_Flag(self.PixelToCell([x, y]))
        
    # 블록 깨기
    def Act_Break(self, c_coords):
        print("Act_Break...", c_coords)

        row = c_coords[0]
        col = c_coords[1]
        pixelcoords = self.CellToPixel([row, col])

        if(flag_map[row][col] == 0): # 깃발이 없으면
            if(map[row][col] == -1): # 폭탄이라면
                self.Game_Over()
            elif(map[row][col] == 0): # 빈공간이라면
                data = map[row][col]
                self.canvas.create_text(pixelcoords[0], pixelcoords[1]+5, font="Times 12 italic bold", text=str(data))
                self.clear() # visit 데이터 초기화 
                self.DFS(row, col) # 빈공간 처리 실행
            else:
                data = map[row][col]
                self.canvas.create_text(pixelcoords[0], pixelcoords[1]+5, font="Times 12 italic bold", text=str(data))
                
    def clear(self):
        for row in range(MapHeight):
                for col in range(MapWidth):
                    visit[row][col] = 0

    # 깃발 꽂기
    def Act_Flag(self, c_coords):
        #print("Act_Flag...", c_coords)
        global flag
        cnt = 0
        
        row = c_coords[0]
        col = c_coords[1]
        pixelcoords = self.CellToPixel([row, col])

        if(not flag_map[row][col] == 1):
            self.canvas.create_text(pixelcoords[0], pixelcoords[1], font="Times 15", text="X", tags="flag{0}{1}".format(row, col))
            flag_map[row][col] = 1
            flag -= 1
        else:
            self.canvas.delete("flag{0}{1}".format(row, col))
            flag_map[row][col] = 1
            flag += 1

        if(flag == 0):
            for row in range(MapHeight):
                for col in range(MapWidth):
                    if(not map[row][col] == -1):
                        cnt += 1
            
            if cnt == MapWidth * MapHeight - mine:
                self.Game_Clear()

    def Game_Clear():
        print("Win!")
    
    def Game_Over():
        print("lose....")

    #def GetRewardState(act):
    #    if(act == ActionType.BREAK)
    #        if(폭탄인지 체크)
    #    print("액션값에 따라 reward, done, success 값을 세팅해서 리턴")

    def MapAllView(self, event):
        Cellidx = 0
        for row in range(MapHeight):
            for col in range(MapWidth):
                
                # 셀인덱스
                tempPixelPos = self.CellToPixel([row, col])
                self.canvas.create_text(tempPixelPos[0], tempPixelPos[1]-10, font="Times 8", text=str(Cellidx), tags="Cellidx")
                
                # 맵데이터
                data = map[row][col]
                self.canvas.create_text(tempPixelPos[0], tempPixelPos[1]+5, font="Times 12 italic bold", text=str(data), tags="MapData")
                Cellidx+=1
        
    def MapAllHide(self, event):
        self.canvas.delete("Cellidx", "MapData")
        #print("MapAllHide")
    
    # 왼쪽 버튼 클릭시 0의 위치이면 근처의 0의 위치를 모두 찾아서 셋팅하자.


# 유틸 함수
# 사방의 지뢰의 갯수를 세어서 리턴하자
def count(row, col):
    cnt_ = 0
    if(map[row + 1][col] == -1):
        cnt_ += 1
    if(map[row - 1][col] == -1):
        cnt_ += 1
    if(map[row][col + 1] == -1):
        cnt_ += 1
    if(map[row][col - 1] == -1):
        cnt_ += 1

    if(map[row + 1][col + 1] == -1):
        cnt_ += 1
    if(map[row + 1][col - 1] == -1):
        cnt_ += 1
    if(map[row - 1][col + 1] == -1):
        cnt_ += 1
    if(map[row - 1][col - 1] == -1):
        cnt_ += 1
    return cnt_

# 맵을 0으로 초기화 하자
for row in range(MapHeight):
    for col in range(MapWidth):
        map[row][col] = 0

# 폭탄 세팅
map[1][1] = -1
map[2][2] = -1

# 지뢰 갯수를 세어서 맵에 세팅하자
# 지뢰 주변에 번호 세팅
for row in range(MapHeight):
    for col in range(MapWidth):
        if(map[row][col] == 0):
            map[row][col] = count(row, col)


# --------------------------------- 이하 테스트 코드

env = Env()
# 맵 전체 보여주기
# "A"키 누르기
env.bind('a', env.MapAllView)
env.bind('h', env.MapAllHide)

# 변환 테스트
#print("PixelToCell : ", env.PixelToCell([51, 25]))
#print("CellToPixel : ", env.CellToPixel([1, 0]))
#print("CellToPixel : ", env.CellToPixel([0, 2]))

# 빈공간 클릭 테스트

# 깃발 테스트

# 액션 함수 테스트
#env.GetActionResult(ActionType.UP)
#env.GetActionResult(ActionType.LEFT)
#env.GetActionResult(ActionType.RIGHT)
#env.GetActionResult(ActionType.BREAK)
#env.GetActionResult(ActionType.FLAG)

# 클릭 테스트
env.bind('<Button-1>', env.LClick) # 추후 일반 액션에 대응
env.bind('<Button-3>', env.RClick) # 추후 깃발꽂기 액션에 대응

env.mainloop()
