
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shnr@1165",
    database="dbms",
    port=3306
)
cursor = db.cursor(dictionary=True)


departments_credentials = {
    'it': ('it@gmail.com', 'it'),
    'hr': ('hr@gmail.com', 'hr'),
    'finance': ('finance@gmail.com', 'finance'),
    'marketing': ('marketing@gmail.com', 'marketing'),
    'accounts': ('accounts@gmail.com', 'accounts'),
    'admin': ('admin@gmail.com', 'admin'),
}

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    departments = list(departments_credentials.keys())
    

    if request.method == 'POST':
        department = request.form['department']
        email = request.form['email']
        password = request.form['password']

        correct_email, correct_password = departments_credentials.get(department, ('', ''))

        if email == correct_email and password == correct_password:
            session['department'] = department

            # Get department ID from Department table
            cursor.execute("SELECT Department_ID FROM Department WHERE Department_Name = %s", (department,))
            dept = cursor.fetchone()
            if dept:
                session['department_id'] = dept['Department_ID']
                return redirect(url_for('dashboard'))
            else:
                return "Department not found in DB."

        return render_template('login.html', error='Invalid credentials', departments=departments)

    return render_template('login.html', departments=departments)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'department_id' not in session:
        return redirect(url_for('login'))

    dept_id = session['department_id']
    department = session['department']

    if department == 'admin':
        
        cursor.execute("""
    SELECT p.Project_ID, p.Project_Name, p.Status, p.Proof, d.Department_Name 
    FROM Project p
    JOIN Department d ON p.Department_ID = d.Department_ID
    WHERE p.Assigned = TRUE
""")
        projects = cursor.fetchall()


        cursor.execute("""
    SELECT Project_ID, Project_Name FROM Project WHERE Assigned = FALSE
""")
        future_projects = cursor.fetchall()


        cursor.execute("SELECT Department_ID, Department_Name FROM Department WHERE Department_Name != 'admin'")
        departments = cursor.fetchall()

        return render_template('admin_dashboard.html', 
            projects=projects, 
            future_projects=future_projects,
            departments=departments,
            department=department
)

    else:
        cursor.execute("SELECT * FROM Project WHERE Department_ID = %s", (dept_id,))
        projects = cursor.fetchall()
        return render_template('dashboard.html', projects=projects, department=department)


@app.route('/update_project/<int:project_id>', methods=['POST'])
def update_project(project_id):
    new_status = request.form['status']
    image = request.files['proof']
    image_path = ''
    ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png')

    if image and image.filename.lower().endswith(ALLOWED_EXTENSIONS):
        filename = image.filename
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        image_db_path = f'uploads/{filename}'
    else:
        image_db_path = ''

    cursor.execute("UPDATE Project SET Status = %s, Proof = %s WHERE Project_ID = %s", (new_status, image_db_path, project_id))
    db.commit()

    return redirect(url_for('dashboard'))

@app.route('/register_project', methods=['GET', 'POST'])
def register_project():
    cursor.execute("SELECT Department_ID, Department_Name FROM Department")
    departments = cursor.fetchall()

    if request.method == 'POST':
        project_name = request.form['project_name']
        department_id = request.form['department_id']

       
        cursor.execute(
            "INSERT INTO Project (Project_Name, Department_ID, Status, Proof) VALUES (%s, %s, %s, %s)",
            (project_name, department_id, 'Not Started', '')
        )
        db.commit()

        return redirect(url_for('home'))  

    return render_template('register_project.html', departments=departments)

@app.route('/assign_project/<int:project_id>', methods=['POST'])
def assign_project(project_id):
    dept_id = request.form.get('department_id')

    cursor.execute("""
        UPDATE Project SET Department_ID = %s, Assigned = TRUE, Status = 'Not Started' 
        WHERE Project_ID = %s
    """, (dept_id, project_id))
    db.commit()

    return redirect(url_for('dashboard'))

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'department' not in session:
        return redirect(url_for('login')) 

    sender = session['department']  

    if request.method == 'POST':
        receiver = request.form['receiver']
        message = request.form['message']

        if receiver != sender:  
            cursor.execute("""
                INSERT INTO Chat (Sender_Department, Receiver_Department, Message)
                VALUES (%s, %s, %s)
            """, (sender, receiver, message))
            db.commit()
        return redirect(url_for('chat'))

    
    cursor.execute("""
        SELECT * FROM Chat
        WHERE Sender_Department = %s OR Receiver_Department = %s
        ORDER BY Timestamp ASC
    """, (sender, sender))
    chat_history = cursor.fetchall()

    
    cursor.execute("SELECT Department_Name FROM Department WHERE Department_Name != %s", (sender,))
    departments = cursor.fetchall()

    return render_template("chat.html", sender=sender, departments=departments, chat_history=chat_history)



if __name__ == '__main__':
    app.run(debug=True)
