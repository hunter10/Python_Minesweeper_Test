import time
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image

tk_inst = tk.Tk()

np.random.seed(1)
PhotoImage = ImageTk.PhotoImage # 사진을 object로 받을 것이라는 의미
UNIT = 100  # 픽셀 수 = 한 칸의 크기
HEIGHT = 5  # 그리드 월드 가로
WIDTH = 5  # 그리드 월드 세로

tk_inst.mainloop()