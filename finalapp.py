import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_db_connection():
    try:
        conn = sqlite3.connect('users_vouchers.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500


def initialize_database():
    conn = get_db_connection()
    if isinstance(conn, tuple):  # Check if there was an error while connecting to DB
        return conn

    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_info (
                        user_id INTEGER PRIMARY KEY,
                        name TEXT,
                        email TEXT,
                        age INTEGER
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_spending (
                        user_id INTEGER,
                        money_spent REAL,
                        year INTEGER,
                        FOREIGN KEY(user_id) REFERENCES user_info(user_id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS high_spenders (
                        user_id INTEGER PRIMARY KEY,
                        total_spending REAL
                    )''')
    conn.commit()
    conn.close()


initialize_database()


# API Endpoints

@app.route('/total_spent/<int:user_id>', methods=['GET'])
def total_spent(user_id):
    conn = get_db_connection()
    if isinstance(conn, tuple):  # Check if there was an error while connecting to DB
        return conn

    cursor = conn.cursor()
    cursor.execute("SELECT SUM(money_spent) AS total_spending FROM user_spending WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row["total_spending"] is None:
        return jsonify({"message": "User has spent 0.00"}), 404
    return jsonify({"user_id": user_id, "total_spending": row["total_spending"]})


@app.route('/average_spending_by_age', methods=['GET'])
def average_spending_by_age():
    age_ranges = [(18, 24), (25, 30), (31, 36), (37, 47), (48, None)]
    results = {}

    conn = get_db_connection()
    if isinstance(conn, tuple):  # Check if there was an error while connecting to DB
        return conn

    cursor = conn.cursor()
    for start, end in age_ranges:
        if end:
            cursor.execute("""
                SELECT AVG(money_spent) AS avg_spending
                FROM user_spending
                JOIN user_info ON user_spending.user_id = user_info.user_id
                WHERE user_info.age BETWEEN ? AND ?
            """, (start, end))
        else:
            cursor.execute("""
                SELECT AVG(money_spent) AS avg_spending
                FROM user_spending
                JOIN user_info ON user_spending.user_id = user_info.user_id
                WHERE user_info.age >= ?
            """, (start,))

        avg_spent = cursor.fetchone()["avg_spending"]
        range_label = f"{start}-{end}" if end else f">{start}"
        results[range_label] = avg_spent or 0

    conn.close()
    return jsonify(results)


@app.route('/write_high_spenders/<int:user_id>/<float:total_spending>', methods=['POST', 'GET'])
def write_high_spenders(user_id, total_spending):
    spending_threshold = 1000

    # Validate input
    if user_id is None or total_spending is None:
        return jsonify({"message": "Invalid data format"}), 400

    if total_spending > spending_threshold:
        try:
            conn = get_db_connection()
            if isinstance(conn, tuple):  # Check if there was an error while connecting to DB
                return conn
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO high_spenders (user_id, total_spending)
                VALUES (?, ?)
            """, (user_id, total_spending))
            conn.commit()
            conn.close()
            return jsonify({"message": "User data successfully inserted"}), 201
        except sqlite3.IntegrityError:
            return jsonify({"message": "User already exists in high spenders"}), 409
    else:
        return jsonify({"message": "User spending does not meet threshold"}), 400


if __name__ == '__main__':
    app.run(debug=True)
