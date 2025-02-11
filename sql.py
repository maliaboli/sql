import sqlite3

# Create a connection to the database
connection = sqlite3.connect('student.db')
cursor = connection.cursor()

# Create STUDENT table
cursor.execute("""
CREATE TABLE IF NOT EXISTS STUDENT(
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
""")

# Check if data already exists in STUDENT table
cursor.execute("SELECT COUNT(*) FROM STUDENT")
record_count = cursor.fetchone()[0]

# Insert only if table is empty
if record_count == 0:
    cursor.executemany("""
    INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES (?, ?, ?, ?)
    """, [
        ('Aboli', 'Data Science', 'A', 90),
        ('Tushar', 'Data Science', 'B', 100),
        ('Omkar', 'DEVOPS', 'A', 86),
        ('Chaitanya', 'DEVOPS', 'A', 50),
        ('Abhi', 'DEVOPS', 'B', 60)
    ])

# Create TEACHER table
cursor.execute("""
CREATE TABLE IF NOT EXISTS TEACHER(
    NAME VARCHAR(25),
    SUBJECT VARCHAR(25),
    EXPERIENCE INT
);
""")

# Check if data already exists in TEACHER table
cursor.execute("SELECT COUNT(*) FROM TEACHER")
record_count = cursor.fetchone()[0]

# Insert only if table is empty
if record_count == 0:
    cursor.executemany("""
    INSERT INTO TEACHER (NAME, SUBJECT, EXPERIENCE) VALUES (?, ?, ?)
    """, [
        ('Dr. Smith', 'Data Science', 10),
        ('Ms. Patel', 'DEVOPS', 7),
        ('Mr. John', 'Mathematics', 15)
    ])

# Create COURSES table
cursor.execute("""
CREATE TABLE IF NOT EXISTS COURSES(
    COURSE_NAME VARCHAR(50),
    DURATION VARCHAR(25),
    FEES INT
);
""")

# Check if data already exists in COURSES table
cursor.execute("SELECT COUNT(*) FROM COURSES")
record_count = cursor.fetchone()[0]

# Insert only if table is empty
if record_count == 0:
    cursor.executemany("""
    INSERT INTO COURSES (COURSE_NAME, DURATION, FEES) VALUES (?, ?, ?)
    """, [
        ('Data Science', '6 months', 50000),
        ('DEVOPS', '4 months', 40000),
        ('Mathematics', '3 months', 30000)
    ])

# Commit and close connection
connection.commit()
connection.close()
