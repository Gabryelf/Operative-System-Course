import tkinter as tk

root = tk.Tk()

root.geometry('500x500')
root.title('КАЛЬКУЛЯТОР ТОП')
root.configure(background='black')

result = ''


def insert_value(value):
    global result
    result = result + f'{value}'
    input_text.config(text=result)


def init():
    frame_top = tk.Frame(root, width=500, height=100, background='grey')
    frame_bottom_left = tk.Frame(root, width=350, height=100)
    frame_bottom_right = tk.Frame(root, width=150, height=100, background='grey')
    return [frame_top, frame_bottom_left, frame_bottom_right]


def gui():
    global input_text

    frames = init()
    frames[0].pack(side="top", padx=25, pady=15)
    frames[1].pack(side="left", padx=25, pady=15)
    frames[2].pack(side="right", padx=25, pady=15)
    col = 0
    row = 0

    input_text = tk.Label(frames[0], width=40, height=3)
    input_text.pack()

    for step in range(10):
        button = tk.Button(frames[1], text=step, width=10, height=5, command=lambda value=step: insert_value(value))
        button.grid(column=col, row=row)
        col += 1
        if col == 3:
            col = 0
            row += 1
    dot = tk.Button(frames[1], text='.', width=10, height=5, command=lambda value='.': insert_value(value))
    dot.grid(column=col, row=row)
    col = 0
    row = 0

    list_operators = ["*", "%", "-", "+", "=", "c"]
    for operator in list_operators:
        operator = tk.Button(frames[2], text=operator, width=15, height=3, command= lambda val=button: insert_value(val))
        operator.pack()


gui()
root.mainloop()
