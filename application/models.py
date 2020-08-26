import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash
#this is to hash(generate 128 character long password) it and this is to unhash it

class User(db.Document):        #db.Document bcz we are using the flask mongo db engine it is gonna allow us to use WTF form directives to create those fields like sting, boolean fields etc.
    user_id    =    db.IntField( unique=True )
    first_name =    db.StringField( max_length=50 )
    last_name  =    db.StringField( max_length=50 )
    email      =    db.StringField( max_length=30, unique=True )
    password   =    db.StringField(  )

    def set_password(self, password):             #setter
        self.password = generate_password_hash(password)

    def get_password(self, password):             #getter
        return check_password_hash(self.password, password)

    #This class map directly, exactly to the database
    #If we don't create that collection in the database, then once we run this application then it will use the class name and use that as collection inside the database 
    #and it will use lowercaase version instead of uppercase

class Course(db.Document):
    courseID   =    db.StringField( max_length=10, unique=True )
    title       =    db.StringField( max_length=100 )
    description =    db.StringField( max_length=255 )
    credits     =    db.IntField()
    term        =    db.StringField(max_length=25)


#The information can be queried from both the tables this is called many-to-many relationship which we will do in enrollment table
#This is the junction table that combine it together
#A student can enroll in many courses and a course can be enrolled by many students
class Enrollment(db.Document):
    user_id     =    db.IntField()                                #we can use db.ObjectIdField() which is a 12 byte field
    courseID   =    db.StringField( max_length=10 ) 

#both of them can form a primary key. A compound key in relational database world
