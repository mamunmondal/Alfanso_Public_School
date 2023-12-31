from alfanso.models import Student, Principle
from alfanso import login_manager, app, db
from flask import render_template , request, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required

  


@login_manager.user_loader
def load_user(user_id):
        # Check if the user_id is valid and convert it to an integer
    try:
        user_id = int(user_id)
    except ValueError:
        return None

    # Try loading the user from the Student table
    student = Student.query.get(user_id)
    if student:
        return student

    # If the user is not in the Student table, try loading from the Principle table
    principle = Principle.query.get(user_id)
    if principle:
        return principle

    # If the user is not found in either table, return None
    return None




@app.route('/')
def home():
    active_user = current_user
    return render_template('home.html', active_user = active_user)



@app.route('/register')
def registration():
    return render_template('register.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and len(request.form) == 1:
        login_as = ''
        login_as = request.form['loginTypeInput']
        return render_template('login.html',login_as=login_as)

    if request.method == 'POST' and len(request.form) > 1:
            login_as = request.form['login_as']
            # will authenticate the principle
            if login_as == 'principle':
                email = request.form['email']
                password = request.form['password']
                principle = Principle.query.filter_by(email=email).first()
                if principle and principle.password == password:
                    login_user(principle)
                    return redirect(url_for('home'))

    return render_template('login.html',)
    
    



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
    active_user = current_user
    if active_user.is_authenticated:
        return render_template('profile.html', active_user = active_user)
    return redirect(url_for('login'))



@app.route('/student_list')
def student_list():
    students = Student.query.all()
    return render_template('student_list.html', students = students)