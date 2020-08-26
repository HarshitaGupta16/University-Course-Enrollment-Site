from application import app, db, api
from flask import render_template, request, json, Response, redirect, flash, url_for, session, jsonify
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm
from flask_restplus import Resource
#Resource class handles all the API requests
from application.course_list import course_list

courseData = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, 
    {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, 
    {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, 
    {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"},
    {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]

###################################################
#if we do /api with no parameters then fetch everything with get method, if we pass some id then return specific data
@api.route('/api', '/api/')
class GetAndPost(Resource):

    #GET ALL
    def get(self):
        return jsonify(User.objects.all())

    #POST
    def post(self):
        data = api.payload                         #payload is the part of Flask RESTplus API, it saves data here and tranfer it to local variable

        user = User(user_id=data['user_id'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
        user.set_password(data['password'])             #We will save the hashed password in database
        user.save()
        return jsonify(User.objects(user_id=data['user_id']))  #we send that same data to postman
#the class name here doesn't really matters, we can call it whatever we want because it is managed by the Resource object by rest plus, passed in function
#it automatically detects your request type

@api.route('/api/<idx>')
class GetUpdateDelete(Resource):

    #GET ONE
    def get(self, idx):
        return jsonify(User.objects(user_id=idx))

    #PUT
    def put(self, idx):
        data = api.payload

        User.objects(user_id=idx).update(**data)            #This **data is for packing unpacking and passing in the data, that is the payload(json data)
        #The system is smart enough to compare the incoming data to existing data and compares which one has changed.
        #if incoming data has changed certain field it just update that, the rest it leaves untouched.
        return jsonify(User.objects(user_id=idx))

    #DELETE
    def delete(self, idx):
        data = api.payload

        User.objects(user_id=idx).delete()
        return jsonify("User is deleted!")

###################################################

@app.route("/")
@app.route("/index")
def index():
    #index=True meansit should highlight the page name at the top in blue like Home, Classes, Register and Login 
    return render_template('index.html', index=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form  = LoginForm()
    if form.validate_on_submit():
        email = form.email.data                              #we can also use request.form.get
        password = form.password.data

        user = User.objects(email=email).first()
        #if user and password == user.password:
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are succuessfully logged in!", "success")
            session['user_id']  = user.user_id
            session['username'] = user.first_name 
            return redirect('/index')
        #if request.form.get("email") == "test@uta.com":
            
        else:
            flash("Sorry, Something went wrong.","danger")
    return render_template("login.html", title="Login", form=form, login=True)

@app.route('/logout')
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/courses/')
@app.route('/courses/<term>')
#def courses(term="Spring 2020"):
def courses(term = None):
    #using API we will dump this couurseData back to the browser or to the user using the Response class
    #courseData = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, .....]
    #this whole courseData is shifted up in global space

    #print(courseData[1]["title"])
    if term == None:
        term = "Spring 2020"
    #classes = Course.objects.all()
    classes = Course.objects.order_by("+courseID")     #if u want to sort it be courseID, + means ascening order and - means decending order

    return render_template('courses.html', courseData=classes, courses=True, term=term)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user_id         = User.objects.count()
        user_id         += 1                      #increase user_id after till where it exixts

        email           = form.email.data
        password        = form.password.data
        first_name      = form.first_name.data
        last_name       = form.last_name.data
        #since in forms.py the RegisterForm will already validate the email for us so we are good to go and save it in database

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)             #We will save the hashed password in database
        user.save()
        flash("You are successfully registered!", "success")
        return redirect(url_for('index'))
    return render_template('register.html', title="Register", form=form, register=True)

#Request and Response objects are all JSON API format

@app.route('/enrollment', methods=['GET', 'POST'])
def enrollment():
    if not session.get('username'):
        flash("You are not logged in. Please login to enroll in any course!", "danger")
        return redirect(url_for('login'))              #if not signed in then redirect to login page.

    courseID        = request.form.get('courseID')
    #we use request.args.get() so that if the id with that token is not passed then will get message saying None and site won't crash
    #if we use request.args[] as array then if it does not get id with token, then site will crash. so if its a gurantee that we get id and token then use it.
    #title = request.form['title']      now we are also using POST so we write request.form, but title has to be provided
    courseTitle     = request.form.get('title')
    user_id         = session.get('user_id')

    if courseID:              #to check if user is coming from course page that is taken new course
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"Oops! You are already registered in this course { courseTitle }!", "danger")
            return redirect(url_for('courses'))
        else:
            Enrollment(user_id=user_id,courseID=courseID).save()
            flash(f"You are enrolled in {courseTitle}!", "success")

    courses = course_list()

    #term = request.form.get('term')
    return render_template('enrollment.html', enrollment=True, title="Enrollment", classes=classes)


#@app.route('/api')
#@app.route('/api/<idx>')
#def api(idx=None):
#    if idx == None:
#        jdata = courseData
#    else:
#        jdata = courseData[int(idx)]

#    return Response(json.dumps(jdata), mimetype="application/json")


@app.route("/user")
def user():
    #User(user_id=1, first_name="Harshita", last_name="Gupta", email="harshita@uta.com", password="abc1234").save()
    #User(user_id=2, first_name="Shiva", last_name="Bhagwaan", email="shiva@uta.com", password="password123").save()
    users = User.objects.all()
    return render_template("user.html", users=users)


#the mongo engine is a document object mapper(DOM) primarily used for mongo db with python