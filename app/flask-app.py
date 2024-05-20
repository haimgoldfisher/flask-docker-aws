from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import boto3
from botocore.exceptions import NoCredentialsError

# init boto3 client for S3
s3_client = boto3.client('s3')

app = Flask(__name__)

# SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bucket_name = 'haimon-bucket'
img_path = 'haim_img.jpeg'

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
        user = User.query.filter_by(name=name, email=email).first()
        if user: # exist user case
            return redirect('/welcome')
        else: # new user case
            new_user = User(name=name, email=email)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/welcome')
    else: # the user did not enter name & email
        return render_template('index.html', message="Please enter both name and email.")


def get_img_url(buck_name, object_key):
    try:
        s3_client.head_object(Bucket=buck_name, Key=object_key) # checks if the obj exist (if permitted)
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': buck_name, 'Key': object_key},
            ExpiresIn=3600
        )  # create a pre-signed URL to extract the public URL of the obj
        return url
    except NoCredentialsError as e:
        print("No AWS credentials found:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None


@app.route('/welcome')
def welcome():
    user = User.query.order_by(User.id.desc()).first()
    img_url = get_img_url(bucket_name, img_path) # public URL of the obj (if permitted & exist)
    if img_url is not None:
        return render_template('welcome.html', name=user.name, has_access=True, img_url=img_url)
    else:
        return render_template('welcome.html', name=user.name, has_access=False)


@app.route('/db')
def show_db():
    users = User.query.all()
    return render_template('db.html', users=users)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=8000)
