from alfanso.models import User, Student, Principle, Post
from alfanso import login_manager, app, db
from flask import render_template , request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required

  


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)




@app.route('/')
def home():
    active_user = current_user
    return render_template('base/home.html', active_user = active_user)




@app.route('/create_account', methods=['GET','POST'])
def create_account():
    if request.method == 'POST':
        userType = request.form['userType']

        if userType == 'student':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            registration_no = request.form['registration_no']

            student = Student(username=username, email=email, password=password, registration_no=registration_no)

            valid_student = Student.query.filter_by(registration_no=student.registration_no).first()

            if valid_student:
                db.session.add(student)
                db.session.commit()
                flash('You Can Login Now , Click as_student')
                return redirect(url_for('auth/login'))
            else:
                flash('Entered Registraion No Does Not Exist! , Try As Others')
            
                        
    return render_template('auth/create_account.html')


@app.route('/register_new_student',methods=['GET','POST'])
def register_new_student():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        class_name = request.form['class']
        registration_no = request.form['registration_no']
        rull = request.form['rull']
        password = request.form['password']
      

        new_student = Student(name=name, rull=rull, password=password, class_name=class_name, registration_no=registration_no,username=username)

        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('student_list'))

    return render_template('user/register_new_student.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and len(request.form) == 1:
        login_as = ''
        login_as = request.form['loginTypeInput']
        return render_template('auth/login.html',login_as=login_as)

    if request.method == 'POST' and len(request.form) > 1:
            # here login_as variable decide who is trying to login 
            login_as = request.form['login_as'] 

            # will authenticate the principle
            if login_as == 'principle':
                email = request.form['email']
                password = request.form['password']
                principle = Principle.query.filter_by(email=email).first()
                if principle and principle.password == password:
                    print(principle.name)
                    login_user(principle)
                    return redirect(url_for('home'))
            
            # will authenticate the student
            if login_as == 'student':
                registration_no = request.form['registration_no']
                password = request.form['password']
                student = Student.query.filter_by(registration_no=registration_no).first()
                if student and student.password == password:
                    login_user(student)
                    flash('YOU ARE LOGGED IN')
                    return redirect(url_for('home'))
                else:
                    flash('Please provide the correct information')

    return render_template('auth/login.html',)
    
    

@app.route('/logout')
def logout():
    logout_user()   
    return redirect(url_for('home'))






@app.route('/delete_user/<string:registration>',  methods=['GET','POST'])
def delete_user(registration):
    student = Student.query.filter_by(registration_no=registration).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            return redirect(url_for('student_list'))
    
    return render_template('user/delete_user.html', student = student)



@app.route('/post',  methods=['GET','POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if current_user.__tablename__ == 'student':
            post = Post(title=title, content=content, student_id=current_user.id)
        if current_user.__tablename__ == 'principle':
            post = Post(title=title, content=content, principle_id=current_user.id)

        if post:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('allPost'))
    return render_template('blog/post.html')


@app.route('/allPost')
def allPost():
    posts = Post.query.all()
    return render_template('blog/allPost.html',posts=posts)

@app.route('/yourPost')
def yourPost():
    return render_template('blog/yourPost.html')


@app.route('/profile')
def profile():
    active_user = current_user
    return render_template('user/profile.html', active_user=active_user)


@app.route('/student_list')
def student_list():
    students = Student.query.all()
    return render_template('user/student_list.html', students = students)