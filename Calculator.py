from tkinter import *
from tkinter import ttk

operation = '' #연산자 저장 변수
temp_number = 0 #이전값 저장 변수
#결과 출력 상태인지 상태저장
answer_trigger = False

def button_pressed(value):
    global temp_number
    global answer_trigger
    
    if value=='AC':
        number_entry.delete(0, 'end')
        operation = ''
        answer_trigger = False
        print("AC pressed")
    else:
        if answer_trigger:
            number_entry.delete(0, "end")
            answer_trigger = False
        number_entry.insert("end", value)
        print(value, "pressed")

def math_button_pressed(value):
    global operation
    global temp_number
    global answer_trigger
    if not number_entry.get() == '': #기존에 입력한 숫자가 있을때만 연산버튼 인식
        operation = value
        temp_number = int(number_entry.get())
        number_entry.delete(0, 'end')
        print(temp_number, operation)

def equal_button_pressed():
    global operation
    global temp_number
    global answer_trigger
    if not (operation == '' and number_entry.get() == ''):
        number = int(number_entry.get())
        if operation == '/':
            solution = temp_number/number
        elif operation == '*':
            solution = temp_number*number
        elif operation == '+':
            solution = temp_number+number
        else:
            solution = temp_number-number

        #계산후, 숫자표시칸을 비우고, 계산결과를 표시.
        number_entry.delete(0, 'end')
        number_entry.insert(0, solution)
        print(temp_number, operation, number, "=", solution)
        operation = ''
        temp_number = 0
        answer_trigger = True

root = Tk()
root.title("Calculator")
root.geometry("350x200")

entry_value = StringVar(root, value='')

#인터페이스(버튼, 창) 추가할 부분.
number_entry = ttk.Entry(root, textvariable=entry_value, width=20)
number_entry.grid(row=0, columnspan=3)

button7 = ttk.Button(root, text="7", command = lambda:button_pressed('7'))
button7.grid(row=1, column=0)
button8 = ttk.Button(root, text="8", command = lambda:button_pressed('8'))
button8.grid(row=1, column=1)
button9 = ttk.Button(root, text="9", command = lambda:button_pressed('9'))
button9.grid(row=1, column=2)


button_div = ttk.Button(root, text="/", command = lambda:math_button_pressed('/'))
button_div.grid(row=1, column=3)

button4 = ttk.Button(root, text="4", command = lambda:button_pressed('4'))
button4.grid(row=2, column=0)
button5 = ttk.Button(root, text="5", command = lambda:button_pressed('5'))
button5.grid(row=2, column=1)
button6 = ttk.Button(root, text="6", command = lambda:button_pressed('6'))
button6.grid(row=2, column=2)

button_mult = ttk.Button(root, text="*", command = lambda:math_button_pressed('*'))
button_mult.grid(row=2, column=3)


button1 = ttk.Button(root, text="1", command = lambda:button_pressed('1'))
button1.grid(row=3, column=0)
button2 = ttk.Button(root, text="2", command = lambda:button_pressed('2'))
button2.grid(row=3, column=1)
button3 = ttk.Button(root, text="3", command = lambda:button_pressed('3'))
button3.grid(row=3, column=2)

button_add = ttk.Button(root, text="+", command = lambda:math_button_pressed('+'))
button_add.grid(row=3, column=3)


#숫자 버튼.
button_ac = ttk.Button(root, text="AC", command=lambda:button_pressed('AC'))
button_ac.grid(row=4, column=0)

button0 = ttk.Button(root, text="0", command=lambda:button_pressed('0'))
button0.grid(row=4, column=1)

button_equal = ttk.Button(root, text="=", command=lambda:equal_button_pressed())
button_equal.grid(row=4, column=2)

button_sub = ttk.Button(root, text="-", command=lambda:math_button_pressed('-'))
button_sub.grid(row=4, column=3)

root.mainloop()