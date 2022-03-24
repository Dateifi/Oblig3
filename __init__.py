from flask import Flask, render_template, url_for
import mysql.connector


app = Flask(__name__)

dbconfig = {'host': 'kark.uit.no',
            'user': 'stud_v22_hartlmar',
            'password': 'NyFqKw5rZBFLrAH',
            'database': 'stud_v22_hartlmar', }

connection = mysql.connector.connect(**dbconfig)

with connection.cursor(dictionary=True) as cursor:
    cursor.execute('SELECT * FROM kategori')
    categories = cursor.fetchall()


@app.route("/")
def index():
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM oppslag ORDER BY dato DESC")
        result = cursor.fetchall()
        return render_template('index.html', result=result, categories=categories)


@app.route('/category<int:id>')
def category(id):
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute('SELECT * FROM oppslag WHERE kategori = %s ORDER BY dato DESC', [id])
        res = cursor.fetchall()
        return render_template('index.html', result=res, categories=categories)


@app.route('/message<int:id>')
def message(id):
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute('UPDATE oppslag SET treff = treff + 1 WHERE id = %s', [id])
        connection.commit()
        cursor.execute('SELECT * FROM oppslag WHERE id = %s', [id])
        single = cursor.fetchall()
        return render_template('index.html', result=single, categories=categories)


if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        connection.close()

