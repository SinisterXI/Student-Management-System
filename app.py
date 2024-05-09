from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

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
        if role == 'student':
            return redirect(url_for('student'))
        elif role == 'teacher':
            return redirect(url_for('teacher'))
        elif role == 'admin':
            return redirect(url_for('admin'))
    else:
        return "Invalid credentials"

@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
