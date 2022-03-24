import mysql as mysql
from flask import Flask, render_template, request, url_for, flash, redirect
import mysql.connector


app = Flask(__name__)

# from mysql.connector import connect, Error
#
# try:
#     with connect(
#         host="localhost",
#         user=input("Enter username: "),
#         password=getpass("Enter password: "),
#           database='stud_v22_hartlmar'
#     ) as connection:
#         create_db_query = "CREATE DATABASE online_movie_rating"
#         with connection.cursor() as cursor:
#             cursor.execute(create_db_query)
# except Error as e:
#     print(e)

dbconfig = {'host': 'kark.uit.no',
            'user': 'stud_v22_hartlmar',
            'password': 'NyFqKw5rZBFLrAH',
            'database': 'stud_v22_hartlmar', }

connection = mysql.connector.connect(**dbconfig)



# i = 0
# while i < 20:
#     kat = 2
#     tit = fake.company()
#     ing = fake.paragraph(nb_sentences=1)
#     opp = fake.paragraph(nb_sentences=5)
#     bru = fake.name()
#     dat = fake.date()
#
#     i += 1
#     cursor = connection.cursor()
#     cursor.execute(
#         'INSERT INTO stud_v22_hartlmar.oppslag (kategori, tittel, ingress, oppslagtekst, bruker, dato, treff) VALUES (%s, %s, %s, %s, %s, %s, %s)',
#         [kat, tit, ing, opp, bru, dat, 0])
#     connection.commit()
#     cursor.close()


# class BoardPost(db.Model):
#     __tablename__ = 'oppslag'
#     id = db.Column(db.Integer, primary_key=True)
#     kategori = db.Column(db.Integer)
#     tittel = db.Column(db.String(50))
#     ingress = db.Column(db.Text())
#     oppslagtekst = db.Column(db.Text())
#     bruker = db.Column(db.String(50))
#     dato = db.Column(db.Date())
#     treff = db.Column(db.Integer)
#
#     def __init__(self, kategori, tittel, ingress, oppslagstekst, bruker, dato, treff):
#         self.kategori = kategori
#         self.tittel = tittel
#         self.ingress = ingress
#         self.oppslagtekst = oppslagstekst
#         self.bruker = bruker
#         self.dato = dato
#         self.treff = treff


@app.route("/")
def index():
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute('SELECT * FROM kategori')
        categories = cursor.fetchall()
        cursor.execute("SELECT id, tittel, ingress FROM oppslag ORDER BY dato DESC")
        result = cursor.fetchall()
        return render_template('oppslagtavla.html', result=result, categories=categories)


@app.route('/category/<int:id>')
def category(id):
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute('SELECT * FROM kategori')
        categories = cursor.fetchall()
        cursor.execute('SELECT id, tittel, ingress FROM oppslag WHERE kategori = %s ORDER BY dato DESC', [id])
        res = cursor.fetchall()
        return render_template('oppslagtavla.html', result=res, categories=categories)


@app.route('/message/<int:id>')
def message(id):
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute('SELECT * FROM kategori')
        categories = cursor.fetchall()
        cursor.execute('SELECT * FROM oppslag WHERE id = %s', [id])
        single = cursor.fetchall()
        return render_template('oppslagtavla.html', result=single, categories=categories)

# @app.route("/submit", methods=["POST"])
# def submit():
#     if request.method == "POST":
#         kategori = request.form.get("kategori")
#         tittel = request.form.get("tittel")
#         ingress = request.form.get("ingress")
#         oppslagtekst = request.form.get("oppslagstekst")
#         bruker = request.form.get("bruker")
#         dato = request.form.get("dato")
#         treff = 0
#         if kategori == "" or tittel == "" or ingress == "" or oppslagtekst == "" or bruker == "" or dato == "":
#             return render_template(
#                 'index2.html', message="Please fill the required fields"
#             )
#
#         data = BoardPost(kategori, tittel, ingress, oppslagtekst, bruker, dato, treff)
#         db.session.add(data)
#         db.session.commit()
#         return render_template('success.html')


if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        connection.close()
