# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models.user import User
from models.group import StudentGroup
import os


app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "..", "static"),
)
app.secret_key = "12345"

engine = create_engine(
    "mysql+pymysql://root:admin@localhost/academy",
    echo=True,
)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")

    user_name = request.form.get('user_name', '').strip()
    user_password = request.form.get('user_pass', '').strip()

    if not user_name or not user_password:
        return render_template('index.html', error='Введите имя и пароль')

    with Session(engine) as session:
        user = session.scalars(
            select(User).where(User.user_name == user_name)
        ).first()

    if user is None:
        return register()
    if user.user_password != user_password:
        return render_template('index.html', error='Пароль не подходит!')
    return redirect(url_for('groups_list'))


@app.route("/login", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', error='Пользователя с таким именем нет — зарегистрируйтесь')

    reg_name = request.form.get('reg_name', '').strip()
    reg_password = request.form.get('reg_pass', '').strip()

    if not reg_name or not reg_password:
        return render_template('register.html', error='Имя и пароль обязательны')

    with Session(engine) as session:
        existing = session.scalars(
            select(User).where(User.user_name == reg_name)
        ).first()
        if existing:
            return render_template('register.html', error='Такое имя уже занято')

        session.add(User(user_name=reg_name, user_password=reg_password))
        session.commit()

    flash("Пользователь создан", "success")
    return redirect(url_for("groups_list"))


@app.route("/groups")
def groups_list():
    with Session(engine) as session:
        groups = session.scalars(select(StudentGroup).order_by(StudentGroup.id)).all()
    return render_template("groups_list.html", groups=groups)


@app.route("/groups/create", methods=["GET", "POST"])
def groups_create():
    pass


@app.route("/groups/<int:group_id>/edit", methods=["GET", "POST"])
def groups_edit(group_id):
    pass


@app.route("/groups/<int:group_id>/delete", methods=["POST"])
def groups_delete(group_id):
    with Session(engine) as session:
        group = session.get(StudentGroup, group_id)
        if group is None:
            flash("Группа не найдена", "error")
        else:
            session.delete(group)
            session.commit()
            flash("Группа удалена", "success")
    return redirect(url_for("groups_list"))


if __name__ == '__main__':
    app.run(debug=True)
