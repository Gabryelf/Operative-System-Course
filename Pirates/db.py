import mysql.connector


def connect():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='pirates'
    )


def load_or_create_player(name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, total_score FROM players WHERE name=%s", (name,))
    row = cur.fetchone()
    if row is None:
        cur.execute("INSERT INTO players (name, total_score) VALUES (%s, 0)", (name,))
        conn.commit()
        pid, score = cur.lastrowid, 0
    else:
        pid, score = row
    cur.close()
    conn.close()
    return pid, score


def save_result(player_id, score, attempts_used):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO games (player_id, score, attempts_used) VALUES (%s, %s, %s)",
                (player_id, score, attempts_used))
    cur.execute("UPDATE players SET total_score = total_score + %s WHERE id = %s",
                (score, player_id))
    conn.commit()
    cur.execute("SELECT total_score FROM players WHERE id = %s", (player_id,))
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return total
