from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost/kollege'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def index():
    groups = db.session.execute(db.text("SELECT * FROM student_groups")).fetchall()
    return str(groups)


if __name__ == '__main__':
    app.run(debug=True)
