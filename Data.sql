-- Inserting dummy data into Credentials table
INSERT INTO Credentials (email, password, role) VALUES 
('u2022428@giki.edu.pk', '0328', 'student'),
('u2022506@giki.edu.pk', 'rooshan', 'student'),
('u2022078@giki.edu.pk', 'aizaz', 'student'),
('qasim@giki.edu.pk', 'qasim', 'teacher'),
('admin@giki.edu.pk', 'admin', 'admin');

-- Inserting dummy data into Hostel table
INSERT INTO Hostel (hostel_number, supervisor_name, supervisor_contact, room_number) VALUES 
(9, 'Junaid', 0300123456, 24), (10, 'Ali', 0300123456, 201), (11, 'Ahmed', 0300123456, 301);

-- Inserting dummy data into Department table
INSERT INTO Department (department_name, dean_name) VALUES 
('Faculty of Computer Science', 'Dr. Ali Khan'),
('Faculty of Mechanical Engineering', 'Dr. Ahmed Hassan'),
('Faculty of Civil Engineering', 'Dr. Fatima Ali');

-- Inserting dummy data into Program table
INSERT INTO Program (program_name, program_department_id) VALUES 
('BS in Cyber Security', (SELECT department_id FROM Department WHERE department_name = 'Faculty of Computer Science')),
('BS in Mechanical Engineering', (SELECT department_id FROM Department WHERE department_name = 'Faculty of Mechanical Engineering')),
('BS in Civil Engineering', (SELECT department_id FROM Department WHERE department_name = 'Faculty of Civil Engineering'));


-- Inserting dummy data into Teachers table
INSERT INTO Teachers (teacher_name, email, teacher_position, teacher_salary, teacher_department_id) VALUES 
('Qasim Riaz', 'qasim@giki.edu.pk', 'Lecturer', 350000.00, (SELECT department_id FROM Department WHERE department_name = 'Faculty of Computer Science'));


-- Inserting dummy data into Course table
INSERT INTO Course (course_name, teacher_id, students_enrolled) VALUES 
('Introduction to Programming', (SELECT teacher_id FROM Teachers WHERE email = 'qasim@giki.edu.pk'), 50);

--Inserting dummy data into Students table
INSERT INTO Students (
    registration_number, student_name, email, student_date_of_birth, student_cgpa, student_degree, 
    student_enrollment_year, Father_name, student_cnic, student_address, 
   student_room_number, student_attendance, student_scholarship, student_fee_status, 
    student_blood_type, student_status
) VALUES 
('2022428', 'Shameer Awais', 'u2022428@giki.edu.pk', '2003-09-28', 2.9, 'Bachelor', 
 2022, 'Awais Mehmood', '3650277893491', 'Multan', 24, 90.0, 'Normal Scholarship', 'Paid', 'B+', 'Active'),
('2022506', 'Rooshan Riaz', 'u2022506@giki.edu.pk', '2000-02-01', 3.2, 'Bachelor', 
 2022, 'Riaz', '2345678901234', 'DG Khan', 201, 85.0, 'Normal Scholarship', 'Paid', 'B+', 'Active'),
('2022078', 'Aizaz Khan', 'u2022078@giki.edu.pk', '2000-03-01', 3.8, 'Bachelor', 
 2022, 'Mr Khan', '3456789012345', 'Mardan', 301, 95.0, 'Merit Scholarship', 'Paid', 'A', 'Active');
