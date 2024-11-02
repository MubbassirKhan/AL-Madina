from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
import mysql.connector
import bcrypt

import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.secret_key = 'mkj'  # Set a secret key for session management

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Khan@123'
app.config['MYSQL_DB'] = 'ALMADINA_DB'

db_config = {
    'host': 'localhost',      # Replace with your database host
    'user': 'root',      # Replace with your database username
    'password': 'Khan@123',  # Replace with your database password
    'database': 'ALMADINA_DB'     # Replace with your database name
}

import mysql.connector

def init_db():
    # Establish connection
    conn = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD']
    )
    cur = conn.cursor()

    # Create the database if it doesn't exist
    cur.execute("CREATE DATABASE IF NOT EXISTS ALMADINA_DB")
    conn.database = 'ALMADINA_DB'
    
    # Create the users table
    # Create the users table
# Create the users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create the courses table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            crs_id INT NOT NULL AUTO_INCREMENT,
            c_name VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            fees DECIMAL(10, 2),
            duration VARCHAR(50),
            PRIMARY KEY (crs_id)
        )
    ''')

    # Create the students table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            student_id_number VARCHAR(100) NOT NULL,
            address TEXT NOT NULL,
            aadhar_copy VARCHAR(255) NOT NULL,
            fees_paid DECIMAL(10, 2) NOT NULL,
            balance DECIMAL(10, 2) NOT NULL,
            course_duration VARCHAR(100) NOT NULL,
            crs_id INT NOT NULL,
            FOREIGN KEY (crs_id) REFERENCES courses(crs_id) ON DELETE CASCADE
        )
    ''')

   

    # Create the attendance table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT NOT NULL,
            course_id INT NOT NULL,
            date DATE,
            status ENUM('present', 'absent'),
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(crs_id) ON DELETE CASCADE
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            admin_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100)
        )
    ''')
    # Check if the admin already exists
    cur.execute("SELECT * FROM admin WHERE username = 'ADMIN'")
    existing_admin = cur.fetchone()

     # Create the admin table

    # Check if the admin user already exists
    cur.execute("SELECT * FROM admin WHERE username = %s", ('ADMIN',))
    existing_admin = cur.fetchone()

    if existing_admin is None:
        # Define the password to use for initialization
        password = 'ADMIN'  # This is the initial password
        hashed_password = generate_password_hash(password)  # Hash the initial password

        # Insert the admin user into the database
        cur.execute('''
            INSERT INTO admin (username, password, email)
            VALUES (%s, %s, %s)
        ''', ('ADMIN', hashed_password, 'admin@example.com'))

    conn.commit()
    cur.close()
    conn.close()

def get_db_connection():
    """Create a new database connection."""
    connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return connection

# Home route
@app.route('/')
def home():
    return render_template('user/index.html')


# arabic_courses route
@app.route('/arabic_courses.html')
def arabic_courses():
    return render_template('user/arabic_courses.html')

# About Us route
@app.route('/about.html')
def about():
    return render_template('user/about.html')

# Contact route
@app.route('/contact.html')
def contact():
    return render_template('user/contact.html')

# Fashion Design route
@app.route('/fashion.html')
def fashion():
    return render_template('user/fashion.html')

@app.route('/nikha.html')
def nikha():
    return render_template('user/nikha.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form['action']  # Determine whether it's a login or signup action

        # Login process
        if request.form['action'] == 'login':
            email = request.form['email']
            password = request.form['password']

            # Database connection and login logic
            conn = mysql.connector.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PASSWORD'],
                database=app.config['MYSQL_DB']
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
    # Assuming user details are stored in the database
                session['logged_in'] = True
                session['username'] = user[1]  # Assuming the second column is username
                session['email'] = email
                session['member_since'] = user[3]  # Assuming the third column is member_since

                return '''
                    <script>
                        alert("Login successful!");
                        window.location.href = "/";
                    </script>
                '''
            else:
                return '''
                    <script>
                        alert("Invalid credentials. Please try again.");
                        window.location.href = "/login";
                    </script>
                '''
    
        # Signup process
        elif request.form['action'] == 'signup':
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                return '''
                    <script>
                        alert("Passwords do not match!");
                        window.location.href = "/login";
                    </script>
                '''

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Establish connection
            conn = mysql.connector.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PASSWORD'],
                database=app.config['MYSQL_DB']
            )
            cur = conn.cursor()

            try:
                cur.execute("INSERT INTO users(email, password) VALUES(%s, %s)", (email, hashed_password))
                conn.commit()
                return '''
                    <script>
                        alert("Registration successful! You can now log in.");
                        window.location.href = "/login";
                    </script>
                '''
            except mysql.connector.Error as e:
                conn.rollback()  # Rollback in case of error
                return '''
                    <script>
                        alert("Registration failed! Email may already be in use.");
                        window.location.href = "/login";
                    </script>
                '''
            finally:
                cur.close()
                conn.close()

    return render_template('user/login.html')  # Render the login form for GET requests

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear all session data
    return '''
        <script>
            alert("Logged out successfully!");
            window.location.href = "/";
        </script>
    '''

@app.route('/digital.html')
def digital():
    return render_template('user/digital.html')

@app.route('/content_creator.html')
def content_creator():
    return render_template('user/content_creator.html')

@app.route('/graphic_design.html')
def graphic_design():
    return render_template('user/graphic_design.html')

@app.route('/spoken_arabic.html')
def spoken_arabic():
    return render_template('user/spoken_arabic.html')

@app.route('/qurantajweed.html')
def qurantajweed():
    return render_template('user/qurantajweed.html')

@app.route('/hifz_quran.html')
def hifz_quran():
    return render_template('user/hifz_quran.html')

@app.route('/tafseer.html')
def tafseer():
    return render_template('user/tafseer.html')

@app.route('/quran_kids.html')
def quran_kids():
    return render_template('user/quran_kids.html')

@app.route('/quran_advance.html')
def quran_advance():
    return render_template('user/quran_advance.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('user/dashboard.html')


# Admin login route
from werkzeug.security import check_password_hash  # Import this function

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            # Execute the query to select the admin
            cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
            admin = cursor.fetchone()  # Fetch the first matching record
            
            # Check if an admin record is found
            if admin and check_password_hash(admin['password'], password):  # Validate the password
                return redirect(url_for('admin_home'))
            else:
                return '''
                    <script>
                        alert("Invalid credentials. Please try again.");
                        window.location.href = "/admin_login";
                    </script>
                '''
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return '''
                <script>
                    alert("An error occurred while logging in. Please try again.");
                    window.location.href = "/admin_login";
                </script>
            '''
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    return render_template('admin/admin_login.html')


@app.route('/logout_admin')  # Updated route
def logout_admin():
    # Clear the session if needed
    session.clear()  # Uncomment this if you are using sessions

    # Redirect to the login page after logging out
    return redirect(url_for('admin_login'))

@app.route('/admin_home')
def admin_home():
    return render_template('admin/admin_home.html')  

from collections import namedtuple

@app.route('/admin_courses', methods=['GET', 'POST'])
def admin_courses():
    connection = get_db_connection()
    Course = namedtuple('Course', ['crs_id', 'c_name', 'description'])
    courses = []

    if connection:
        cursor = connection.cursor()
        cursor.execute('SELECT crs_id, c_name, description FROM courses')
        rows = cursor.fetchall()
        courses = [Course(*row) for row in rows]  # Convert tuples to named tuples
        cursor.close()
        connection.close()

    return render_template('admin/admin_courses.html', courses=courses)


@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    connection = get_db_connection()
    
    if request.method == 'POST':
        # Extract student data from the form
        name = request.form['name']
        address = request.form['address']
        aadhar_copy = request.form['aadhar_copy']  # If you have a file upload for Aadhar
        fees_paid = request.form['fees_paid']
        balance = request.form['balance']
        course_duration = request.form['course_duration']
        crs_id = request.form['crs_id']

        if connection:
            cursor = connection.cursor()
            # Update the student record in the database
            cursor.execute('''
                UPDATE students 
                SET name = %s, address = %s, aadhar_copy = %s, fees_paid = %s, balance = %s, course_duration = %s, crs_id = %s 
                WHERE student_id = %s
            ''', (name, address, aadhar_copy, fees_paid, balance, course_duration, crs_id, student_id))
            connection.commit()
            cursor.close()
            connection.close()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('view_course', course_id=crs_id))  # Redirect back to the course view page

    # Fetch current student data to pre-fill the form
    student = None
    if connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM students WHERE student_id = %s', (student_id,))
        student = cursor.fetchone()
        cursor.close()
        connection.close()

    return render_template('edit_student.html', student=student)  # Render the edit_student.html template

@app.route('/remove_course/<int:course_id>', methods=['POST'])
def remove_course(course_id):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM courses WHERE crs_id = %s', (course_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return '''
                <script>
                alert("Course Removed Successfully");
                window.location.href = "/admin_courses";  // Redirect without course_id if it's a list
                </script>
            '''

@app.route('/add_student/<int:course_id>', methods=['POST'])
def add_student(course_id):
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id_number']  # Updated key
        address = request.form['address']
        aadhar_copy = request.files['aadhar_copy']
        fees_paid = request.form['fees_paid']
        balance = request.form['balance']
        duration = request.form['course_duration']  # Updated key

        # Ensure the uploads directory exists
        uploads_dir = 'uploads'
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        # Save the Aadhar photocopy in the uploads directory
        aadhar_copy_path = os.path.join(uploads_dir, secure_filename(aadhar_copy.filename))
        aadhar_copy.save(aadhar_copy_path)

        # Initialize the connection and cursor
        connection = None
        cursor = None

        # Insert data into the students table
        
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO students (name, student_id_number, address, aadhar_copy, fees_paid, balance, course_duration, crs_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (name, student_id, address, aadhar_copy_path, fees_paid, balance, duration, course_id))
        connection.commit()  # Commit the changes
        return '''
                <script>
                    alert("Data Stored");
                    window.location.href = "/admin_courses";
                </script>
            '''        

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    connection = get_db_connection()
    if request.method == 'POST':
        c_name = request.form['c_name']
        description = request.form['description']
        duration = request.form['duration']
        fees = request.form['fees']

        if connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO courses (c_name, description, duration, fees) VALUES (%s, %s, %s, %s)', 
                           (c_name, description, duration, fees))
            connection.commit()
            cursor.close()
            connection.close()
            return '''
            <script>
                alert("Course Added Successfully");
                window.location.href = "/admin_courses";  // Redirect without course_id if it's a list
            </script>
            '''

    return render_template('admin/admin_courses.html')

@app.route('/student_data/<int:course_id>', methods=['GET', 'POST'])
def student_data(course_id):
    connection = get_db_connection()
    
    if request.method == 'POST':
        name = request.form['name']
        student_id_number = request.form['student_id_number']
        address = request.form['address']
        
        # Handle file upload for Aadhar copy
        aadhar_copy = request.files['aadhar_copy']
        aadhar_copy_path = f"uploads/{aadhar_copy.filename}"  # Store in uploads folder
        aadhar_copy.save(aadhar_copy_path)
        
        fees_paid = request.form['fees_paid']
        balance = request.form['balance']
        course_duration = request.form['course_duration']
        
        if connection:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO students (name, student_id_number, address, aadhar_copy, fees_paid, balance, course_duration, crs_id) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                           (name, student_id_number, address, aadhar_copy_path, fees_paid, balance, course_duration, course_id))
            connection.commit()
            cursor.close()
            connection.close()
            flash('Student added successfully!', 'success')
            return redirect(url_for('admin_courses'))

    # Get course details for display
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT c_name FROM courses WHERE crs_id = %s', (course_id,))
    course_name = cursor.fetchone()[0]
    cursor.close()
    connection.close()

    return render_template('admin/student_data.html', course_id=course_id, course_name=course_name)

@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    connection = None
    cursor = None

    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # SQL query to delete the student
        delete_query = "DELETE FROM students WHERE student_id = %s"
        cursor.execute(delete_query, (student_id,))

        # Commit the changes
        connection.commit()

        return '''
            <script>
                alert("Student Deleted Successfully");
               window.history.back();  // Ensure this matches your defined route
            </script>
        '''
    except mysql.connector.Error as err:
        return f'''
            <script>
                alert("Database error: {str(err)}");
                window.history.back();
            </script>
        '''
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/view_course/<int:course_id>', methods=['GET'])
def view_course(course_id):
    connection = get_db_connection()
    course = None
    students = []  # Initialize an empty list for students

    if connection:
        cursor = connection.cursor()
        
        # Fetch course details
        cursor.execute('SELECT * FROM courses WHERE crs_id = %s', (course_id,))
        course = cursor.fetchone()

        # Fetch students enrolled in this course
        cursor.execute(''' 
            SELECT 
                name, 
                student_id, 
                address, 
                aadhar_copy, 
                fees_paid, 
                balance, 
                course_duration, 
                crs_id 
            FROM 
                students 
            WHERE 
                crs_id = %s
        ''', (course_id,))

        student_rows = cursor.fetchall()

        # Construct a list of dictionaries to store student details
        students = [{
            'name': row[0],               # Student's name
            'student_id': row[1],        # Student's ID
            'address': row[2],           # Student's address
            'aadhar_copy': row[3],       # Path to the Aadhar photocopy
            'fees_paid': row[4],         # Fees paid by the student
            'balance': row[5],           # Remaining balance
            'course_duration': row[6],   # Duration of the course
            'crs_id': row[7]             # Course ID
        } for row in student_rows]

        cursor.close()
        connection.close()

    return render_template('admin/view_course.html', course=course, students=students)

@app.route('/admin_users')
def admin_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)  # Use dictionary for easier access
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()  # Fetch all users
    cursor.close()
    connection.close()
    
    return render_template('admin/admin_users.html', users=users)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    connection.commit()
    cursor.close()
    connection.close()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin_users'))

@app.route('/edit_user', methods=['POST'])
def edit_user():
    user_id = request.form['user_id']
    email = request.form['email']
    # Retrieve more fields as needed

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('UPDATE users SET email = %s WHERE id = %s', (email, user_id))
    connection.commit()
    cursor.close()
    connection.close()
    flash('User updated successfully!', 'success')
    return redirect(url_for('admin_users'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']  # This may be empty if the user doesn't want to change it

    # Hash the password if it's provided
    hashed_password = generate_password_hash(password) if password else None

    connection = get_db_connection()
    cursor = connection.cursor()

    # Update admin details in the database
    if hashed_password:
        cursor.execute("UPDATE admin SET username = %s, email = %s, password = %s WHERE admin_id = %s",
                       (username, email, hashed_password, 1))  # Assuming admin_id is 1 for example
    else:
        cursor.execute("UPDATE admin SET username = %s, email = %s WHERE admin_id = %s",
                       (username, email, 1))

    connection.commit()
    cursor.close()
    connection.close()

    flash('Profile updated successfully!', 'success')
    return redirect(url_for('settings'))

# Your settings route
@app.route('/settings')
def settings():
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch admin data (assuming admin_id is known; here it’s hardcoded as 1 for example)
    cursor.execute("SELECT * FROM admin WHERE admin_id = %s", (1,))
    admin = cursor.fetchone()  # Fetch the admin record

    # Close the database connection
    cursor.close()
    connection.close()

    # If admin data is None, handle the error appropriately
    if admin is None:
        flash('Admin not found.', 'danger')
        return redirect(url_for('some_other_route'))  # Redirect to another page if needed

    return render_template('admin/settings.html', admin=admin)  # Pass admin data to the template


@app.route('/attendance_report', methods=['GET'])
def attendance_report():
    # Get the course ID from the URL query parameter
    course_id = request.args.get('course_id')

    # Initialize variables
    attendance_data = []
    course_name = ""

    # Only proceed if course_id is provided
    if course_id:
        # Database connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Khan@123',
            database='ALMADINA_DB'
        )
        cursor = connection.cursor(dictionary=True)

        try:
            # Fetch course name for display
            course_query = "SELECT c_name FROM courses WHERE crs_id = %s"
            cursor.execute(course_query, (course_id,))
            course_result = cursor.fetchone()
            
            if course_result:
                course_name = course_result['c_name']
            
            # Fetch attendance records for the specified course
            attendance_query = """
                SELECT 
                    students.student_id AS student_id,
                    students.name AS student_name,
                    COUNT(attendance.status) AS total_classes,
                    SUM(CASE WHEN attendance.status = 'Present' THEN 1 ELSE 0 END) AS attended_classes
                FROM 
                    attendance
                JOIN 
                    students ON attendance.student_id = students.student_id
                WHERE 
                    attendance.course_id = %s
                GROUP BY 
                    students.student_id, students.name
            """

            cursor.execute(attendance_query, (course_id,))
            attendance_data = cursor.fetchall()

            # Calculate attendance percentage for each student
            for student in attendance_data:
                if student['total_classes'] > 0:
                    student['attendance_percentage'] = (student['attended_classes'] / student['total_classes']) * 100
                else:
                    student['attendance_percentage'] = 0  # No classes held or recorded

        except mysql.connector.Error as err:
            print("Error: {}".format(err))
        finally:
            # Close the database connection
            cursor.close()
            connection.close()

    # Render the template with course name and attendance data
    return render_template('admin/attendance_report.html', course_name=course_name, attendance=attendance_data, course_id=course_id)

@app.route('/attendance', methods=['GET'])
def attendance():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT crs_id, c_name FROM courses")
    courses = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('admin/attendance.html', courses=courses)

@app.route('/mark_attendance/<int:course_id>', methods=['GET', 'POST'])
def mark_attendance(course_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch course name
    cursor.execute("SELECT c_name FROM courses WHERE crs_id = %s", (course_id,))
    course = cursor.fetchone()
    course_name = course['c_name'] if course else "Unknown Course"

    # Fetch students for the specified course
    cursor.execute("SELECT * FROM students WHERE crs_id = %s", (course_id,))
    students = cursor.fetchall()

    if request.method == 'POST':
        date = request.form.get('date')
        attendance_records = []

        # Process the attendance data
        attendance_data = request.form.getlist('attendance')
        for record in attendance_data:
            student_id, status = record.split(":")
            print(f"Recording attendance: Student ID: {student_id}, Course ID: {course_id}, Date: {date}, Status: {status}")  # Debugging statement
            attendance_records.append((student_id, course_id, date, status))  # Collect records
            
            # Insert attendance record
            cursor.execute(
                "INSERT INTO attendance (student_id, course_id, date, status) VALUES (%s, %s, %s, %s)",
                (student_id, course_id, date, status)
            )

        connection.commit()
        print(f"Attendance records inserted: {attendance_records}")  # Debugging statement

    cursor.close()
    connection.close()

    return render_template('admin/mark_attendance.html', course_id=course_id, course_name=course_name, students=students)

@app.route('/view_attendance/<int:course_id>', methods=['GET', 'POST'])
def view_attendance(course_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch course name
    cursor.execute("SELECT c_name FROM courses WHERE crs_id = %s", (course_id,))
    course = cursor.fetchone()
    course_name = course['c_name'] if course else "Unknown Course"

    attendance_data = []

    if request.method == 'POST':
        selected_date = request.form.get('date')  # Get the selected date from the form
        
        # Query to fetch attendance records for the selected course and date
        cursor.execute("""
            SELECT students.student_id, students.name, attendance.status
            FROM attendance
            JOIN students ON attendance.student_id = students.student_id
            WHERE attendance.course_id = %s AND attendance.date = %s
        """, (course_id, selected_date))
        
        attendance_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('admin/view_attendance.html', course_name=course_name, attendance_data=attendance_data, course_id=course_id)

if __name__ == '__main__':
    init_db()  # Call to initialize the database and tables
    app.run(debug=True, port=3000) 
