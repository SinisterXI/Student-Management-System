from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0328@localhost/DBMS Project'
db = SQLAlchemy(app)

# User model
class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

# Hostel model 
class Hostel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50), nullable=False)
    hostel = db.Column(db.String(50), nullable=False)
    room_number = db.Column(db.String(10), nullable=False)

# Mess Hall model
class MessHall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50), nullable=False)
    mess_hall = db.Column(db.String(50), nullable=False)

# Create tables function
def create_tables():
    with app.app_context():
        db.create_all()

# User routes
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({'error': 'Username, password, and role are required'}), 400

    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Hostel routes
@app.route('/api/hostels', methods=['POST'])
def allot_hostel():
    data = request.json
    student_name = data.get('student_name')
    hostel = data.get('hostel')
    room_number = data.get('room_number')

    if not student_name or not hostel or not room_number:
        return jsonify({'error': 'Student name, hostel, and room number are required'}), 400

    new_hostel = Hostel(student_name=student_name, hostel=hostel, room_number=room_number)
    db.session.add(new_hostel)
    db.session.commit()
    return jsonify({'message': 'Hostel allotted successfully'}), 201

# Mess Hall routes
@app.route('/api/mess-halls', methods=['POST'])
def allot_mess_hall():
    data = request.json
    student_name = data.get('student_name')
    mess_hall = data.get('mess_hall')

    if not student_name or not mess_hall:
        return jsonify({'error': 'Student name and mess hall are required'}), 400

    new_mess_hall = MessHall(student_name=student_name, mess_hall=mess_hall)
    db.session.add(new_mess_hall)
    db.session.commit()
    return jsonify({'message': 'Mess hall allotted successfully'}), 201

# Root route
@app.route('/')
def index():
    return 'Welcome to the DBMS Project API'

if __name__ == '__main__':
    create_tables()  # Call the function to create tables
    app.run(debug=True)
