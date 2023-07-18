from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///register1.db'
db = SQLAlchemy(app)
app.app_context().push()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mobile_number = db.Column(db.String(20), unique=True)
    otp = db.Column(db.String(4))

    def __init__(self, mobile_number):
        self.mobile_number = mobile_number
        self.generate_otp()

    def generate_otp(self):
        self.otp = str(random.randint(1000, 9999))

@app.route('/register/<mobile_number>', methods=['GET'])
def register_user(mobile_number):
    user = User.query.filter_by(mobile_number=mobile_number).first()

    if user:
        user.generate_otp()
    else:
        user = User(mobile_number=mobile_number)
        db.session.add(user)

    db.session.commit()

    return jsonify({'otp': user.otp})

if __name__ == '__main__': 
    app.run(debug=True)
