from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    phone = db.Column(db.String(15))

    
class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100))
    company_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    eligibility = db.Column(db.String(200))
    deadline = db.Column(db.String(50))
    status = db.Column(db.String(20))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    drive_id = db.Column(db.Integer)
    application_date = db.Column(db.String(50))
    status = db.Column(db.String(20))

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    hr_contact = db.Column(db.String(100))
    email = db.Column(db.String(100))
    website = db.Column(db.String(100))
    password = db.Column(db.String(100))
    approval_status = db.Column(db.String(20))