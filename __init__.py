from flask import Flask, render_template, flash, url_for, redirect
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, DateField, HiddenField
from wtforms.validators import InputRequired
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MY SUPER SAVE KEY'

dbconfig = {'host': 'kark.uit.no',
            'user': 'stud_v22_hartlmar',
            'password': 'NyFqKw5rZBFLrAH',
            'database': 'stud_v22_hartlmar', }

connection = mysql.connector.connect(**dbconfig)

with connection.cursor(dictionary=True) as cursor:
    cursor.execute('SELECT * FROM kategori')
    categories = cursor.fetchall()


class RegisterForm(FlaskForm):
    kategori = SelectField("Category", choices=[('1', 'Cars and Motorcycles'), ('2', 'Furniture'), ('3', 'Electronics'), ('4', 'Properties for Rent'), ('5', 'Help Wanted')],
                           validate_choice=True)

    tittel = StringField("Title", validators=[InputRequired()],
                         render_kw={'autofocus': True, 'placeholder': 'Your title'})
    ingress = StringField("Ingress", validators=[InputRequired()],
                          render_kw={'autofocus': True, 'placeholder': 'Your ingress'})
    oppslagtekst = TextAreaField("Oppslagtekst", validators=[InputRequired()],
                                 render_kw={'autofocus': True, 'placeholder': 'Your text'})
    bruker = StringField("Username", validators=[InputRequired()],
                       render_kw={'autofocus': True, 'placeholder': 'Your username'})
    today = date.today()

    dato = DateField('Post date:', format='%Y-%m-%d', default=today, validators=[InputRequired()])

    submit = SubmitField('Submit')

class EditForm(FlaskForm):
    kategori = SelectField("Category", choices=[('1', 'Cars and Motorcycles'), ('2', 'Furniture'), ('3', 'Electronics'),
                                                ('4', 'Properties for Rent'), ('5', 'Help Wanted')],
                           validate_choice=True)
    submit = SubmitField('Submit')


@app.route("/")
def index():
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM oppslag ORDER BY dato DESC")
        result = cursor.fetchall()
        return render_template('oppslagtavla.html', result=result, categories=categories)


@app.route('/category<int:id>')
def category(id):
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute('SELECT * FROM oppslag WHERE kategori = %s ORDER BY dato DESC', [id])
        res = cursor.fetchall()
        return render_template('oppslagtavla.html', result=res, categories=categories)


@app.route('/message<int:id>')
def message(id):
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute('UPDATE oppslag SET treff = treff + 1 WHERE id = %s', [id])
        connection.commit()
        cursor.execute('SELECT * FROM oppslag WHERE id = %s', [id])
        single = cursor.fetchall()
        return render_template('oppslagtavla.html', result=single, categories=categories)


@app.route("/addpost", methods=['GET', 'POST'])
def addpost():
    form = RegisterForm()
    if form.validate_on_submit():
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(
                "INSERT INTO `oppslag`(kategori, tittel, ingress, oppslagtekst, bruker, dato, treff) VALUES (%s, %s, %s, %s, %s, %s, %s)", [form.kategori.data, form.tittel.data, form.ingress.data, form.oppslagtekst.data, form.bruker.data, form.dato.data, 0])
            connection.commit()
        flash('Post created', 'success')
        return redirect(url_for('index'))
    else:
        return render_template('addpost.html', form=form)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    edit_form = EditForm()
    if edit_form.validate_on_submit():
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute('UPDATE oppslag SET kategori = %s WHERE id = %s', [edit_form.kategori.data, id])
            connection.commit()
            return redirect(url_for('index'))
    else:
        return render_template('edit.html', edit_form=edit_form)

@app.route('/delete<int:id>')
def delete(id):
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute('DELETE FROM `oppslag` WHERE id = %s', [id])
        connection.commit()
        return redirect(url_for('index'))



if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        connection.close()
