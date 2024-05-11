from flask import Flask, render_template, request, redirect, url_for, session, make_response
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

# Function to establish database connection
def create_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Global variable to hold the database connection
db_connection = create_connection()

# Function to add cache-control headers to all responses
def no_cache(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    cur = db_connection.cursor()
    query = sql.SQL("SELECT * FROM Credentials WHERE email=%s AND password=%s AND role=%s")
    cur.execute(query, (email, password, role))

    credentials = cur.fetchone()

    if credentials:
        session['email'] = email
        if role == 'student':
            return redirect(url_for('student'))
        elif role == 'teacher':
            return redirect(url_for('teacher'))
        elif role == 'admin':
            return redirect(url_for('admin'))
    else:
        return "Invalid credentials"

# Function to fetch student information from the database
def get_student_info(email):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM Students WHERE email = %s", (email,))
        row = cursor.fetchone()

        if row:
            student_info = {
                "student_name": row[1],
                "email": row[2],
                "student_date_of_birth": row[3],
                "student_cgpa": row[4],
                "student_enrollment_year": row[5],
                "student_father_name": row[6],
                "student_cnic": row[7],
                "student_address": row[8],
                "student_program": row[9],
                "student_scholarship": row[11],
                "student_status": row[13]
            }
            return student_info
        else:
            return {'message': 'Email not found in credentials'}

    except psycopg2.Error as e:
        return {'error': str(e)}, 500

# Function to fetch teacher information from the database
def get_teacher_details(email):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM Teachers WHERE email = %s", (email,))
        teacher_details = cursor.fetchone()

        if teacher_details:
            teacher_info = {
                "teacher_name": teacher_details[1],
                "email": teacher_details[2],
                "teacher_position": teacher_details[3]
            }
            return teacher_info
        else:
            return {"error": "Teacher not found"}

    except psycopg2.Error as e:
        print("Error fetching teacher details:", e)
        return {"error": str(e)}

# Function to get student's program
def get_student_program(email):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT student_program_name FROM Students WHERE email = %s", (email,))
        program = cursor.fetchone()

        if program:
            return program[0]
        else:
            return None

    except psycopg2.Error as e:
        print("Error fetching student program:", e)
        return None

# Function to get courses by program
def get_courses_by_program(program):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT course_name, teacher_name FROM Course WHERE program_name = %s", (program,))
        courses = cursor.fetchall()

        return courses

    except psycopg2.Error as e:
        print("Error fetching courses by program:", e)
        return []

# Function to register student courses
def register_student_courses(email, selected_courses):
    try:
        cursor = db_connection.cursor()

        for course in selected_courses:
            cursor.execute("SELECT registration_number FROM Students WHERE email = %s", (email,))
            registration_number = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO registrations (course_name, teacher_name, registration_number) VALUES (%s, %s, %s)",
                (course['course_name'], course['teacher_name'], registration_number)
            )

        db_connection.commit()
        print("Courses registered successfully")

    except psycopg2.Error as e:
        db_connection.rollback()
        print("Error registering courses:", e)

# Function to get course details by name
def get_course_by_name(course_name):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM Course WHERE course_name = %s", (course_name,))
        course = cursor.fetchone()

        if course:
            course_info = {
                "course_name": course[0],
                "teacher_name": course[1],
            }
            return course_info
        else:
            return None

    except psycopg2.Error as e:
        print("Error fetching course details by name:", e)
        return None

@app.route('/registration-confirmation')
def registration_confirmation():
    return render_template('registration_confirmation.html')

@app.route('/register-courses', methods=['GET', 'POST'])
def register_courses():
    email = session.get('email')
    
    if not email:
        return "Email not found in session"

    cursor = db_connection.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT student_program_name FROM Students WHERE email = %s", (email,))
        student_program = cursor.fetchone()

        if student_program:
            program_name = student_program[0]

            cursor.execute("SELECT course_name, teacher_name FROM Course WHERE program_name = %s", (program_name,))
            courses = cursor.fetchall()
            courses_dict = [{'course_name': row[0], 'teacher_name': row[1]} for row in courses]

            response = make_response(render_template('student.html', courses=courses_dict))
            return no_cache(response)
        else:
            return "Student program not found"

    elif request.method == 'POST':
        selected_course_names = request.form.getlist('course')
        cursor.execute("SELECT registration_number FROM Students WHERE email = %s", (email,))
        registration_number = cursor.fetchone()[0]

        for course_name in selected_course_names:
            cursor.execute(
                "SELECT COUNT(*) FROM registrations WHERE registration_number = %s AND course_name = %s",
                (registration_number, course_name)
            )
            exists = cursor.fetchone()[0]

            if exists == 0:
                cursor.execute(
                    "INSERT INTO registrations (registration_number, course_name, teacher_name) "
                    "VALUES (%s, %s, (SELECT teacher_name FROM Course WHERE course_name = %s))",
                    (registration_number, course_name, course_name)
                )
            else:
                print(f"Course '{course_name}' is already registered by this student.")

        db_connection.commit()
        return redirect(url_for('student'))

@app.route('/unregister-course', methods=['POST'])
def unregister_course():
    email = session.get('email')

    if not email:
        return "Email not found in session"

    course_name = request.form['course_name']
    cursor = db_connection.cursor()
    cursor.execute("SELECT registration_number FROM Students WHERE email = %s", (email,))
    registration_number = cursor.fetchone()[0]

    cursor.execute(
        "DELETE FROM registrations WHERE registration_number = %s AND course_name = %s",
        (registration_number, course_name)
    )
    db_connection.commit()

    return redirect(url_for('student'))

# Function to get registered courses
def get_registered_courses(email):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT registration_number FROM Students WHERE email = %s", (email,))
        result = cursor.fetchone()

        if not result:
            return []

        registration_number = result[0]
        cursor.execute("SELECT course_name, teacher_name FROM registrations WHERE registration_number = %s", (registration_number,))
        courses = cursor.fetchall()

        registered_courses = [{'course_name': row[0], 'teacher_name': row[1]} for row in courses]
        return registered_courses

    except psycopg2.Error as e:
        print("Error fetching registered courses:", e)
        return []

@app.route('/view-courses')
def view_courses():
    email = session.get('email')
    
    if email:
        cursor = db_connection.cursor()
        cursor.execute("SELECT registration_number FROM Students WHERE email = %s", (email,))
        registration_number = cursor.fetchone()

        if not registration_number:
            return "Student registration number not found"

        registration_number = registration_number[0]
        cursor.execute(
            "SELECT course_name, teacher_name FROM registrations WHERE registration_number = %s",
            (registration_number,)
        )
        courses = cursor.fetchall()

        registered_courses = [{'course_name': row[0], 'teacher_name': row[1]} for row in courses]

        response = make_response(render_template('student.html', registered_courses=registered_courses))
        return no_cache(response)
    else:
        return "Email not found in session"

@app.route('/view-students')
def view_students():
    email = session.get('email')
    
    if email:
        cursor = db_connection.cursor()
        cursor.execute("SELECT teacher_name, email, teacher_position FROM Teachers WHERE email = %s", (email,))
        teacher_data = cursor.fetchone()

        if teacher_data:
            teacher_details = {
                'teacher_name': teacher_data[0],
                'email': teacher_data[1],
                'teacher_position': teacher_data[2]
            }

            cursor.execute("SELECT course_name FROM Course WHERE teacher_name = %s", (teacher_data[0],))
            courses = [row[0] for row in cursor.fetchall()]

            enrolled_students = {}
            for course_name in courses:
                cursor.execute(
                    "SELECT s.student_name FROM registrations r "
                    "JOIN Students s ON r.registration_number = s.registration_number "
                    "WHERE r.course_name = %s AND r.teacher_name = %s",
                    (course_name, teacher_data[0])
                )
                enrolled_students[course_name] = [row[0] for row in cursor.fetchall()]

            response = make_response(render_template('teacher.html', teacher_details=teacher_details, enrolled_students=enrolled_students))
            return no_cache(response)
        else:
            return "Teacher details not found."
    else:
        return "Email not found in session."

@app.route('/remove-student', methods=['POST'])
def remove_student():
    email = session.get('email')

    if not email:
        return "Email not found in session"

    course_name = request.form['course_name']
    student_name = request.form['student_name']

    cursor = db_connection.cursor()
    cursor.execute("SELECT registration_number FROM Students WHERE student_name = %s", (student_name,))
    registration_number = cursor.fetchone()

    if registration_number:
        registration_number = registration_number[0]
        cursor.execute(
            "DELETE FROM registrations WHERE registration_number = %s AND course_name = %s",
            (registration_number, course_name)
        )
        db_connection.commit()
    else:
        return f"Student '{student_name}' not found."

    return redirect(url_for('view_students'))

@app.route('/student')
def student():
    email = session.get('email')

    if email:
        student_info = get_student_info(email)
        response = make_response(render_template('student.html', students=[student_info]))
        return no_cache(response)
    else:
        return "Email not found in session"

@app.route('/teacher')
def teacher():
    email = session.get('email')

    if email:
        cursor = db_connection.cursor()
        cursor.execute("SELECT teacher_name, email, teacher_position FROM Teachers WHERE email = %s", (email,))
        teacher_data = cursor.fetchone()

        if teacher_data:
            teacher_details = {
                'teacher_name': teacher_data[0],
                'email': teacher_data[1],
                'teacher_position': teacher_data[2]
            }

            cursor.execute(
                "SELECT s.student_name, r.course_name FROM registrations r "
                "JOIN Students s ON r.registration_number = s.registration_number "
                "WHERE r.teacher_name = %s",
                (teacher_data[0],)
            )
            enrolled_students = [{'student_name': row[0], 'course_name': row[1]} for row in cursor.fetchall()]

            response = make_response(render_template('teacher.html', teacher_details=teacher_details, enrolled_students=enrolled_students))
            return no_cache(response)
        else:
            return "Teacher details not found."
    else:
        return "Email not found in session."

@app.route('/admin')
def admin():
    response = make_response(render_template('admin.html'))
    return no_cache(response)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
