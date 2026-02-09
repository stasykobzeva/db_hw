
import psycopg2
from psycopg2.extras import RealDictCursor

DB_NAME = 'my_db'
DB_USER = 'stasykobzeva'
DB_PASSWORD = 'Awedxzs12'
DB_HOST = 5432

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )


def create_employee(name, position, salary):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO employees (name, position, salary) VALUES (%s, %s, %s) RETURNING id;",
                    (name, position, salary)
                )
                new_id = cur.fetchone()[0]
                return new_id
    finally:
        conn.close()


def get_all_employees():
    conn = get_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM employees;")
                return cur.fetchall()
    finally:
        conn.close()


def update_employee(employee_id, fields):
    if not fields:
        return False

    set_clause = ', '.join([f"{key} = %s" for key in fields.keys()])
    values = list(fields.values())
    values.append(employee_id)

    query = f"UPDATE employees SET {set_clause} WHERE id = %s;"

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, values)
                return cur.rowcount > 0
    finally:
        conn.close()

def delete_employee(employee_id):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM employees WHERE id = %s;", (employee_id,))
                return cur.rowcount > 0
    finally:
        conn.close()


if __name__ == '__main__':

    new_employee_id = create_employee('Alice Johnson', 'Developer', 70000)
    print(f'Создан сотрудник с id: {new_employee_id}')


    print('Все сотрудники:', get_all_employees())

    #
    update_employee(new_employee_id, {'position': 'Senior Developer', 'salary': 90000})
    print('Обновленный список сотрудников:', get_all_employees())

    delete_employee(new_employee_id)
    print('После удаления:', get_all_employees())