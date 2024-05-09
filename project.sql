CREATE TABLE Credentials (
    username VARCHAR(100) PRIMARY KEY,
    password VARCHAR(100)
);

-- Hostel table in 3NF
CREATE TABLE Hostel (
    hostel_number VARCHAR(20) PRIMARY KEY,
    supervisor_name VARCHAR(100),
    supervisor_contact VARCHAR(20),
    room_number INT UNIQUE, 
    hostel_capacity INT
);

-- Department table in 3NF
CREATE TABLE Department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) UNIQUE,
    dean_id INT,
    contact_email VARCHAR(100)
);

-- Program table in 3NF
CREATE TABLE Program (
    program_id SERIAL PRIMARY KEY,
    program_name VARCHAR(100) UNIQUE,
    program_department_id INT,
    FOREIGN KEY (program_department_id) REFERENCES Department(department_id)
);

-- Teachers table in 3NF
CREATE TABLE Teachers (
    teacher_id SERIAL PRIMARY KEY,
    teacher_name VARCHAR(100),
    teacher_email VARCHAR(100),
    teacher_specialization VARCHAR(100),
    teacher_hire_date DATE,
    teacher_degree VARCHAR(100),
    teacher_date_of_birth DATE,
    teacher_cnic VARCHAR(15),
    teacher_address VARCHAR(255),
    teacher_position VARCHAR(100),
    teacher_salary DECIMAL(10,2),
    teacher_attendance DECIMAL(5,2),
    teacher_qualifications TEXT,
    teacher_experience_years INT,
    teacher_professional_development TEXT,
    teacher_research_interests TEXT,
    teacher_publication_record TEXT,
    teacher_peer_evaluations TEXT,
    teacher_department_id INT,
    FOREIGN KEY (teacher_department_id) REFERENCES Department(department_id)
);

-- Course table in 3NF
CREATE TABLE Course (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100),
    teacher_id INT,
    course_description TEXT,
    students_enrolled INT,
    FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)
);

-- Students table in 3NF
CREATE TABLE Students (
    registration_number VARCHAR(20) PRIMARY KEY,
    student_name VARCHAR(100),
    student_email VARCHAR(100),
    student_date_of_birth DATE,
    student_cgpa DECIMAL(4,2),
    student_sgpa DECIMAL(4,2),
    student_degree VARCHAR(100),
    student_parent_name VARCHAR(100),
    student_parent_cnic VARCHAR(15),
    student_parent_occupation VARCHAR(100),
    student_enrollment_year INT,
    student_address VARCHAR(255),
    student_graduation DATE,
    student_department_id INT,
    student_program_id INT,
    student_room_number INT,
    student_attendance DECIMAL(5,2),
    student_scholarship VARCHAR(100),
    student_fee_status VARCHAR(50),
    student_emergency_contact_phone VARCHAR(20),
    student_blood_type VARCHAR(5),
    student_previous_institution VARCHAR(100),
    student_year_of_completion INT,
    student_status VARCHAR(20),
    FOREIGN KEY (student_department_id) REFERENCES Department(department_id),
    FOREIGN KEY (student_program_id) REFERENCES Program(program_id),
    FOREIGN KEY (student_room_number) REFERENCES Hostel(room_number)
);

-- Mess table in 3NF
CREATE TABLE Mess (
    hostel_number VARCHAR(20),
    room_number INT,
    registration_number VARCHAR(20),
    mess_hall VARCHAR(100),
    mess_bill DECIMAL(10,2),
    number_of_days INT,
    PRIMARY KEY (hostel_number, room_number, registration_number),
    FOREIGN KEY (hostel_number) REFERENCES Hostel(hostel_number),
    FOREIGN KEY (room_number) REFERENCES Hostel(room_number),
    FOREIGN KEY (registration_number) REFERENCES Students(registration_number)
);

CREATE TABLE Admin (
    admin_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    supervisor_name VARCHAR(100),
    supervisor_contact VARCHAR(20),
    room_number INT,
    hostel_capacity INT,
    department_id INT,
    department_name VARCHAR(100),
    contact_email VARCHAR(100),
    program_id INT,
    program_name VARCHAR(100),
    teacher_id INT,
    teacher_name VARCHAR(100),
    teacher_email VARCHAR(100),
    teacher_specialization VARCHAR(100),
    teacher_hire_date DATE, 
    teacher_degree VARCHAR(100),
    teacher_date_of_birth DATE,
    teacher_cnic VARCHAR(15), 
    teacher_address VARCHAR(255),
    teacher_position VARCHAR(100),
    teacher_salary DECIMAL(10,2),
    teacher_attendance DECIMAL(5,2),
    teacher_qualifications TEXT,
    teacher_experience_years INT,
    teacher_professional_development TEXT,
    teacher_research_interests TEXT,
    teacher_publication_record TEXT,
    teacher_peer_evaluations TEXT,
    course_id INT,
    course_name VARCHAR(100),
    course_description TEXT,
    students_enrolled INT,
    registration_number VARCHAR(20),
    student_name VARCHAR(100),
    student_email VARCHAR(100),
    student_date_of_birth DATE,
    student_cgpa DECIMAL(4,2),
    student_sgpa DECIMAL(4,2),
    student_degree VARCHAR(100),
    student_parent_name VARCHAR(100),
    student_parent_cnic VARCHAR(15),
    student_parent_occupation VARCHAR(100),
    student_enrollment_year INT,
    student_address VARCHAR(255),
    student_graduation DATE,
    student_department_id INT,
    student_program_id INT,
    student_room_number INT,
    student_attendance DECIMAL(5,2),
    student_scholarship VARCHAR(100),
    student_fee_status VARCHAR(50),
    student_emergency_contact_phone VARCHAR(20),
    student_blood_type VARCHAR(5),
    student_previous_institution VARCHAR(100),
    student_year_of_completion INT,
    student_status VARCHAR(20),
    mess_hall VARCHAR(100),
    mess_bill DECIMAL(10,2),
    number_of_days INT,
    FOREIGN KEY (room_number) REFERENCES Hostel(room_number),
    FOREIGN KEY (department_id) REFERENCES Department(department_id),
    FOREIGN KEY (program_id) REFERENCES Program(program_id),
    FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id),
    FOREIGN KEY (registration_number) REFERENCES Students(registration_number)
);