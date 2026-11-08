from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': 'admin',
    'host': 'localhost',
    'database': 'default_db',
    'auth_plugin': 'mysql_native_password'
}


@app.route('/', methods=['GET', 'POST'])
def index():
    employee = None
    error = None

    if request.method == 'POST':
        search_term = request.form.get('search_term', '').strip()
        print(">>> search_term =", repr(search_term))  # что реально пришло

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT full_name, position, email, hire_date
                FROM employee_public
                WHERE full_name LIKE %s OR position LIKE %s
            """
            cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
            employee = cursor.fetchone()
            print(">>> employee =", employee)  # что вернула БД
            cursor.close()
            conn.close()
        except Exception as e:
            import traceback
            traceback.print_exc()
            error = f"Ошибка: {e}"

        if not employee and not error:
            error = "Сотрудник не найден"

    return render_template('index.html', employee=employee, error=error)


if __name__ == '__main__':
    app.run(debug=True)
