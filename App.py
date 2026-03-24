from flask import Flask, render_template, request, redirect, url_for, flash

from flask_mysqldb import MySQL
app = Flask(__name__)
app.secret_key="flash message"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudapplication'

mysql = MySQL(app)


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    count = len(data)
    return render_template('index.html', students=data,count=count)
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()
        flash("Data inserted successfully!")

        return redirect('/')
@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        id_data= request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE students 
            SET name=%s, email=%s, phone=%s 
            WHERE id=%s
        """, (name, email, phone, id_data))
        flash("Data updated successfully!")

        mysql.connection.commit()

        return redirect('/')

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM students WHERE id=%s", (id,))
        flash("Data Deleted Successfully!")
        mysql.connection.commit()


        return redirect('/')


if __name__ == "__main__":
        app.run(debug=True)






