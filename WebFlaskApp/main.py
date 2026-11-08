from flask import Flask, render_template, request
import mysql.connector
import redis
import json

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': 'admin',
    'host': 'localhost',
    'database': 'default_db',
    'auth_plugin': 'mysql_native_password'
}

cache = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)


@app.route('/', methods=['GET', 'POST'])
def index():
    employee = None
    error = None

    if request.method == 'POST':
        search_term = request.form.get('search_term', '').strip()
        if search_term:
            cache_key = f"employee_search:{search_term.lower()}"
            cached_data = cache.get(cache_key)
            if cached_data:
                employee = json.loads(cached_data)
                print(f"DEBUG: Данные для '{search_term}' взяты из Redis")
            else:
                print(f"DEBUG: Данные для '{search_term}' взяты из MySQL")
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

                if employee:
                    # Преобразуем дату в строку, чтобы JSON мог ее сериализовать
                    employee_for_json = employee.copy()
                    if employee_for_json.get('hire_date'):
                        employee_for_json['hire_date'] = str(employee_for_json['hire_date'])

                    cache.setex(cache_key, 300, json.dumps(employee_for_json))

                if not employee:
                    error = "Сотрудник не найден"

    return render_template('index.html', employee=employee, error=error)


if __name__ == '__main__':
    app.run(debug=True)
