import tkinter as tk
from tkinter import messagebox
from logic import create_game, SIZE, ATTEMPTS, LANDMARK_COLORS
from db import load_or_create_player, save_result

player_id = None
player_name = ''
field = {}
treasure = None
attempts_left = 0
buttons = {}

DEFAULT_BG = 'SystemButtonFace'


def start():
    global player_id, player_name, field, treasure, attempts_left

    name = entry.get().strip()
    if not name:
        messagebox.showwarning('Внимание', 'Введите имя')
        return

    player_id, total = load_or_create_player(name)
    player_name = name

    field, treasure, names = create_game()
    attempts_left = ATTEMPTS

    label_player.config(text=f'Игрок: {name}  (всего очков: {total})')
    label_attempts.config(text=f'Попытки: {attempts_left}')
    label_hint.config(text='Клад рядом с: ' + ', '.join(names))
    label_result.config(text='')

    for b in buttons.values():
        b.config(text='?', state='normal', bg=DEFAULT_BG)


def click(row, col):
    global attempts_left

    if attempts_left <= 0 or player_id is None:
        return

    btn = buttons[(row, col)]
    if btn['state'] == 'disabled':
        return

    # попали в клад
    if (row, col) == treasure:
        used = ATTEMPTS - attempts_left + 1
        score = (ATTEMPTS - used + 1) * 5
        total = save_result(player_id, score, used)
        btn.config(text='К', bg='gold', state='disabled')
        label_player.config(text=f'Игрок: {player_name}  (всего очков: {total})')
        label_result.config(text=f'Победа! Очки за партию: {score}')
        disable_all()
        messagebox.showinfo('Победа!', f'{player_name}, клад найден!\n'
                                        f'Очки за партию: {score}\n'
                                        f'Всего очков: {total}')
        return

    # обычная клетка — показываем ориентир или пустоту
    content = field.get((row, col))
    if content is None:
        btn.config(text='·', state='disabled', bg='lightgray')
    else:
        btn.config(text=content, state='disabled',
                   bg=LANDMARK_COLORS.get(content, 'lightgray'))

    attempts_left -= 1
    label_attempts.config(text=f'Попытки: {attempts_left}')

    if attempts_left == 0:
        save_result(player_id, 0, ATTEMPTS)
        buttons[treasure].config(text='К', bg='gold', state='disabled')
        disable_all()
        messagebox.showinfo('Игра окончена',
                            f'{player_name}, попытки закончились.\n'
                            f'Клад был в клетке {treasure}')


def disable_all():
    for b in buttons.values():
        b.config(state='disabled')


# --- окно ---
root = tk.Tk()
root.title('Поиск клада')
root.geometry('720x600')

top = tk.Frame(root)
top.pack(pady=6)
tk.Label(top, text='Имя:').pack(side='left')
entry = tk.Entry(top, width=15)
entry.pack(side='left', padx=5)
tk.Button(top, text='Начать', command=start).pack(side='left')

label_player = tk.Label(root, text='Игрок: —')
label_player.pack()

label_attempts = tk.Label(root, text=f'Попытки: {ATTEMPTS}')
label_attempts.pack()

label_hint = tk.Label(root, text='Клад рядом с: —', font=('Arial', 11, 'bold'))
label_hint.pack(pady=4)

label_result = tk.Label(root, text='', fg='blue')
label_result.pack(pady=2)

board = tk.Frame(root)
board.pack(pady=8)
for r in range(SIZE):
    for c in range(SIZE):
        b = tk.Button(board, text='?', width=5, height=2,
                      command=lambda r=r, c=c: click(r, c))
        b.grid(row=r, column=c, padx=1, pady=1)
        buttons[(r, c)] = b

root.mainloop()
