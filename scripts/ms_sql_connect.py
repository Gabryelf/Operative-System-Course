from mssql_python import connect


def get_connection():
    """Создаёт и возвращает подключение к базе данных."""
    conn_str = "Server=(localdb)\MSSQLLocalDB;"
                "Database=ShopDB;"
                "Trusted_Connection=yes;"
                "Encrypt=yes;TrustServerCertificate=yes"
    return connect(conn_str)


def create_table():
    """Создаёт таблицу Students с 3 колонками, если её ещё нет."""
    query = """
    IF NOT EXISTS (
        SELECT * FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME = 'Students'
    )
    CREATE TABLE Students (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(100) NOT NULL,
        Age INT NOT NULL
    )
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()


def add_student(name, age):
    """Добавляет нового студента и возвращает его ID."""
    query = "INSERT INTO Students (Name, Age) VALUES (?, ?)"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (name, age))
        conn.commit()
        cursor.execute("SELECT @@IDENTITY")
        new_id = cursor.fetchone()[0]
    return new_id


def show_students():
    """Выводит всех студентов."""
    query = "SELECT Id, Name, Age FROM Students ORDER BY Id"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

    print(f"\n📋 Всего студентов: {len(rows)}")
    print(f"{'ID':<5}{'Имя':<20}{'Возраст':<10}")
    print("-" * 35)
    for row in rows:
        print(f"{row[0]:<5}{row[1]:<20}{row[2]:<10}")


def main():
    # 1. Создаём таблицу
    create_table()

    # 2. Добавляем данные
    add_student("Анна", 20)
    add_student("Иван", 22)
    add_student("Мария", 19)

    # 3. Показываем всех
    show_students()


if __name__ == "__main__":
    main()
