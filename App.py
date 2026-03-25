from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "flash message"


# 🔹 Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# 🔹 Table create (first time)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT
)
''')
conn.commit()
conn.close()


# 🔹 Home route
@app.route('/')
def Index():
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    count = len(data)
    return render_template('index.html', students=data, count=count)


# 🔹 Insert
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO students (name, email, phone) VALUES (?, ?, ?)",
            (name, email, phone)
        )
        conn.commit()
        conn.close()

        flash("Data inserted successfully!")
        return redirect('/')


# 🔹 Update
@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        conn = get_db_connection()
        conn.execute(
            "UPDATE students SET name=?, email=?, phone=? WHERE id=?",
            (name, email, phone, id_data)
        )
        conn.commit()
        conn.close()

        flash("Data updated successfully!")
        return redirect('/')


# 🔹 Delete
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    flash("Data Deleted Successfully!")
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)