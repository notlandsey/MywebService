from flask import Flask, render_template, request, redirect
import psycopg2
app = Flask(__name__)
conn = psycopg2.connect(database="service",
                        user="postgres",
                        password="12345",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            if not username or not password:
                return 'Заполните все поля.'
            try:
                cursor.execute("SELECT full_name FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
                records = list(cursor.fetchall())
                return render_template('account.html', full_name=records[0][0])
            except:
                return 'Введен неверный пароль, или вы не зарегистрированы'
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if len(name) == 0:
            return 'Введено некорректное имя'
        elif len(login) == 0:
            return 'Введен некорректный логин'
        elif len(password) == 0:
            return 'Введите пароль'
        elif [s for s in name if s in '1234567890-+)(*-_!@#$%^&']:
            return "Имя не может содержать цифры"
        elif not name or not login or not password:
            return 'Заполните все поля ввода'
        elif login:
            cursor.execute('SELECT * FROM service.users')
            rows = cursor.fetchall()
            for row in rows:
                if login == row[2]:
                    return 'Такой пользователь уже существует'
        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()

        return redirect('/login/')

    return render_template('registration.html')