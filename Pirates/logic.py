import random

SIZE = 10
ATTEMPTS = 15

# имя ориентира -> цвет фона кнопки
LANDMARK_COLORS = {
    'дерево':  '#a8e6a3',   # зелёный
    'скала':   '#c9c9c9',   # серый
    'пещера':  '#8b6b4a',   # коричневый
    'река':    '#8ecbff',   # голубой
    'озеро':   '#4a90e2',   # синий
    'холм':    '#e6d29c',   # песочный
    'болото':  '#7fae6a',   # болотно-зелёный
}

DECOYS_COUNT = 5   # сколько отвлекающих ориентиров добавить


def create_game():
    """Возвращает: field (dict клетка -> ориентир), treasure, names (3 имени для подсказки)."""
    all_cells = [(r, c) for r in range(SIZE) for c in range(SIZE)]
    random.shuffle(all_cells)

    # три «нужных» ориентира — они попадут в подсказку
    names = random.sample(list(LANDMARK_COLORS.keys()), 3)
    landmark_cells = []
    for name in names:
        cell = all_cells.pop()
        landmark_cells.append((cell, name))

    field = {}
    for cell, name in landmark_cells:
        field[cell] = name

    # отвлекающие ориентиры — имена не из подсказки
    decoys = [n for n in LANDMARK_COLORS if n not in names]
    for _ in range(DECOYS_COUNT):
        cell = all_cells.pop()
        # чтобы отвлекающий не совпал с уже занятой клеткой — pop гарантирует
        field[cell] = random.choice(decoys)

    # клетка-клад: не дальше 2 от КАЖДОГО из трёх нужных ориентиров
    candidates = []
    for r in range(SIZE):
        for c in range(SIZE):
            if (r, c) in field:
                continue
            ok = True
            for (lr, lc), _ in landmark_cells:
                if abs(r - lr) + abs(c - lc) > 2:
                    ok = False
                    break
            if ok:
                candidates.append((r, c))

    if not candidates:
        return create_game()

    treasure = random.choice(candidates)
    return field, treasure, names
