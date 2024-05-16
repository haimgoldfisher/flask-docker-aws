from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:haim@localhost/users'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enter_info', methods=['POST'])
def enter_info():
    name = request.form.get('name')
    email = request.form.get('email')

    if name and email:
        # Check if user already exists
        user = User.query.filter_by(name=name, email=email).first()
        if user:
            return redirect('/welcome')
        else:
            # Save new user to the database
            new_user = User(name=name, email=email)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/welcome')
    else:
        return render_template('index.html', message="Please enter both name and email.")

@app.route('/welcome')
def welcome():
    user = User.query.order_by(User.id.desc()).first()
    if user:
        return render_template('welcome.html', name=user.name)
    else:
        return redirect('/')

@app.route('/db')
def show_db():
    users = User.query.all()
    return render_template('db.html', users=users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
