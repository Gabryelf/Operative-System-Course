import tkinter as tk

root = tk.Tk()

root.geometry('500x500')
root.iconbitmap('../assets/icon.ico')
root.title('КАЛЬКУЛЯТОР ТОП')

def insert_value():
    pass

def init():
    frame_top = tk.Frame(root, width=500, height=100, background='grey')
    frame_bottom_left = tk.Frame(root, width=350, height=100, background='grey')
    frame_bottom_right = tk.Frame(root, width=150, height=100, background='grey')
    return [frame_top.pack(side="top"), frame_bottom_left, frame_bottom_right.pack(side="right")]

def gui():
    frame_bottom_left= init()
    frame_bottom_left[1].pack(side="left", padx=15, pady=15)
    col = 0
    row = 0
    for button in range(10):
        button = tk.Button(frame_bottom_left[1], text=button, width=10, height=5, command=insert_value)
        button.grid(column=col, row=row)
        col += 1
        if col == 3:
            col = 0
            row += 1

gui()
