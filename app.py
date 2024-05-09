from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import session
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

app.secret_key = '1PoepThNcgk6MiS1EM3wygyokLzjTNkY'
# Database setup
DB_NAME = 'project'
DB_USER = 'postgres'
DB_PASSWORD = '0328'
DB_HOST = 'localhost'
DB_PORT = '5432'

# Create a connection function to avoid repeating code
def create_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    print("Received:", email, password, role)  # Debugging output

    conn = create_connection()
    cur = conn.cursor()

    # Use SQL injection safe query
    query = sql.SQL("SELECT * FROM Credentials WHERE email=%s AND password=%s AND role=%s")
    cur.execute(query, (email, password, role))

    Credentials = cur.fetchone()
    conn.close()

    print("Credentials from DB:", Credentials)  # Debugging output

    if Credentials:
        # Store the email in the session
        session['email'] = email  # Add this line to store email in session

        if role == 'student':
            return redirect(url_for('student'))
        elif role == 'teacher':
            return redirect(url_for('teacher'))
        elif role == 'admin':
            return redirect(url_for('admin'))
    else:
        return "Invalid credentials"
    
from flask import jsonify


def get_student_info(email):
    try:
        # Establish a new connection to the database
        connection = psycopg2.connect(
            dbname="project",
            user="postgres",
            password="0328",
            host="localhost",
            port="5432"
        )

        cursor = connection.cursor()

        # Execute the SQL query to fetch student details based on email
        cursor.execute("SELECT * FROM Students WHERE email = %s", (email,))
        
        # Fetch the first row, if exists
        row = cursor.fetchone()
        
        if row:
            # Convert the fetched data into a dictionary for easy access
            student_info = {
                "student_id": row[0],
                "student_name": row[1],
                "email": row[2],
                "student_department_id": row[3]
            }
            return student_info
        else:
            # If no row exists, it means the email doesn't match any credentials
            return {'message': 'Email not found in credentials'}

    except Error as e:
        # Handle any exceptions
        return {'error': str(e)}, 500

    finally:
        # Ensure cursor and connection are closed
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


import psycopg2
from psycopg2 import Error

import psycopg2
from psycopg2 import Error

def get_teacher_details(teacher_id):
    try:
        # Establish connection to the database
        connection = psycopg2.connect(
            user="postgres",
            password="0328",
            host="localhost",
            port="5432",
            database="project"
        )

        cursor = connection.cursor()

        # Query to fetch details of the teacher with the given teacher_id
        cursor.execute("SELECT * FROM Teachers WHERE teacher_id = %s", (3,))
        teacher_details = cursor.fetchone()

        if teacher_details:
            # Convert the fetched data into a dictionary for easy access
            teacher_info = {
                "teacher_id": teacher_details[0],
                "teacher_name": teacher_details[1],
                "email": teacher_details[2],
                "teacher_position": teacher_details[3],
                "teacher_salary": teacher_details[4],
                "teacher_department_id": teacher_details[5]
            }
            return teacher_info
        else:
            return {"error": "Teacher not found"}

    except Error as e:
        print("Error fetching teacher details:", e)
        return {"error": str(e)}

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")



@app.route('/student')
def student():
    # Retrieve the email from the session
    email = session.get('email')
    
    if email:
        # Fetch student information based on the provided email
        student_info = get_student_info(email)
        
        # Render the student.html template with the retrieved student information
        return render_template('student.html', students=[student_info])
    else:
        # Handle the case where the email is not found in the session
        return "Email not found in session"

@app.route('/teacher')
def teacher():
    teacher_id = 1  # Example teacher ID, replace with actual teacher ID
    teacher_details = get_teacher_details(teacher_id)
    print("Teacher Details in Flask Route:", teacher_details)  # Add this line to check data
    return render_template('teacher.html', teacher_details=teacher_details)

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)