from flask import Flask,request,jsonify,make_response   
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
import jwt
import datetime


app = Flask(__name__)
bcrypt = Bcrypt(app)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'thisissecret'

class User(db.Model):
    username = db.Column(db.String(100),primary_key=True)
    password = db.Column(db.String(80))

@app.route('/login/<username>',methods=['GET'])
def login(username):
    auth = request.authorization
    if username !=  auth.username:
        return make_response('Could not Verify',401,{'WWW-Authenticate':'Basic realm="Login Required!'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not Verify',401,{'WWW-Authenticate':'Basic realm="Login Required!'})

    if(bcrypt.check_password_hash(user.password, auth.password)==True):
        token = jwt.encode({'username':user.username,'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('UTF-8')})

    return make_response('Could not Verify',401,{'WWW-Authenticate':'Basic realm="Login Required!'})

    
@app.route('/signup',methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = bcrypt.generate_password_hash(data['password'])
    new_user = User(username = data['username'], password = hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'new user created'})
    

if __name__ == '__main__':
    app.run(debug=True)