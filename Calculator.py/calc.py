import tkinter as tk

root = tk.Tk()

root.geometry('500x500')
root.title('КАЛЬКУЛЯТОР ТОП')

def insert_value(button):
    number = button.config("text")
    print(number)

def init():
    frame_root = tk.Frame(root, width=500, height=500, background='black')
    frame_root.pack()
    frame_top = tk.Frame(frame_root, width=500, height=100, background='grey')
    frame_bottom_left = tk.Frame(frame_root, width=350, height=100, background='grey')
    frame_bottom_right = tk.Frame(frame_root, width=150, height=100, background='grey')
    return [frame_top, frame_bottom_left, frame_bottom_right]

def gui():
    frames= init()
    frames[0].pack(side="top", padx=25, pady=15)
    frames[1].pack(side="left", padx=25, pady=15)
    frames[2].pack(side="right", padx=25, pady=15)
    col = 0
    row = 0
    for button in range(10):
        b = tk.Button(frames[1], text=button, width=10, height=5, command=insert_value)
        b.grid(column=col, row=row)
        col += 1
        if col == 3:
            col = 0
            row += 1
            
    col = 0
    row = 0

    list_operators = ["*", "%", "-", "+", "=", "c"]
    for operator in list_operators:
        operator = tk.Button(frames[2], text=operator, width=15, height=3, command=insert_value)
        operator.pack()

    input_text = tk.Label(frames[0],width=40, height=3).pack()



    

gui()
root.mainloop()
