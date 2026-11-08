import pymysql
import pymysql.cursors

con = pymysql.connect(
    host='localhost',
    user='root',
    password='admin',
    database='default_db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

with con:
    cur = con.cursor()
    cur.execute("SELECT VERSION()")

    version = cur.fetchone()

    print("Database version: {}".format(version[0]))
