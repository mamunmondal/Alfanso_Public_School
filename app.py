from flask import Flask, render_template , request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)
app.app_context().push()
login_manager = LoginManager(app)

    
class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    registration_no = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))




@app.route('/')
def home():
    usr = current_user
    return render_template('home.html', usr = usr)

@app.route('/register')
def registration():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        registration_no = request.form['registration_no']
        password = request.form['password']

        student = Student.query.filter_by(registration_no=registration_no).first()

        if student and student.password == password:
            login_user(student)
            return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()   
    return redirect(url_for('home'))


@app.route('/update_profile', methods=['GET','POST'])
def update_profile():
    usr = current_user
    if request.method == 'POST':
        usr.name = request.form['name']
        usr.class_name = request.form['class']
        usr.email = request.form['email']
        usr.password = request.form['password']
        usr.registration_no = request.form['registration_no']
       
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('update_profile.html', usr = usr)



@app.route('/confirm', methods=['POST'])
def confirm():     
    if request.method == 'POST':
        name = request.form['name']
        class_name = request.form['class']
        registration_no = request.form['registration_no']
        email = request.form['email']
        password = request.form['password']

        new_student = Student(name=name, email=email, class_name=class_name, password=password, registration_no=registration_no)

        db.session.add(new_student)
        db.session.commit()
        
    return render_template('confirm.html', new_student=new_student, password=password)



@app.route('/profile')
def profile():
    student = current_user
    if student.is_authenticated:
        return render_template('profile.html', student = student)
    return redirect(url_for('login'))



@app.route('/student_list')
def student_list():
    students = Student.query.all()
    return render_template('student_list.html', students = students)

if __name__ == '__main__':
    app.run(debug=True)