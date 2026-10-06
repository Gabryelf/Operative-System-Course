""" Простой калькулятор на Tkinter. Реализован для знакомства с библиотекой"""
import tkinter as tk

root = tk.Tk()
root.title("Калькулятор")
root.geometry("260x260")

# ---------- состояние ----------
first_number = None
operation = None
new_number = True

# ---------- дисплеи ----------
text_input = tk.Label(root, text="0", anchor="e", font=("Arial", 14), bg="white")
text_input.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=(5, 0))

text_result = tk.Label(root, text="0", anchor="e", font=("Arial", 20, "bold"), bg="white")
text_result.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=5, pady=(0, 5))

frame_numbers = tk.Frame(root, bg="grey", width=250, height=250)
frame_numbers.grid(row=2, column=0, padx=10)

frame_operators = tk.Frame(root, bg="grey", width=100, height=180)
frame_operators .grid(row=2, column=3, padx=4)


def create_gui():
    count = 1
    b = tk.Button(frame_numbers, text=0, width=5, height=2)
    b.grid(row=0, column=1)
    for row in range(3):
        for button in range(3):
            b = tk.Button(frame_numbers, text=button+count, width=5, height=2)
            b.grid(row=row+1, column=button)
        count += 3


# ---------- запуск ----------
create_gui()
root.mainloop()
