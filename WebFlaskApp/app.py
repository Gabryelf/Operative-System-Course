from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': 'admin',
    'host': 'localhost',
    'database': 'default_db'
}


@app.route('/', methods=['GET', 'POST'])
def index():
    employee = None

    if request.method == 'POST':
        search_term = request.form.get('search_term', '').strip()

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = """
                    SELECT full_name, position, email, hire_date 
                    FROM employee_public
                    WHERE full_name LIKE %s OR position LIKE %s
                """

        cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
        employee = cursor.fetchone()

        cursor.close()
        conn.close()

    return render_template('index.html', employee=employee)


if __name__ == '__main__':
    app.run()
