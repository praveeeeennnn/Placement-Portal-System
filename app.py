from flask import Flask, render_template, request, redirect
from models import db, Student, Drive, Application, Company
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SECRET_KEY"] = "secret123"

db.init_app(app)

# Welcome Page (First Page)
@app.route("/")
def welcome():
    return render_template("welcome.html")

# Second Page (About / Main Page)
@app.route("/home")
def home():
    return render_template("home.html")


#@app.route("/")
##def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]

        new_student = Student(
            name=name,
            email=email,
            password=password,
            phone=phone
        )

        db.session.add(new_student)
        db.session.commit()

        return redirect("/")

    return render_template("student_register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        student = Student.query.filter_by(email=email, password=password).first()

        if student:
            return redirect("/dashboard")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    drives = Drive.query.filter_by(status="Approved").all()

    return render_template("student_dashboard.html", drives=drives)

@app.route("/add_drive")
def add_drive():

    drive = Drive(
        job_title="Software Developer",
        company_name="Infosys",
        description="Software development role",
        eligibility="B.Tech CSE",
        deadline="30 June",
        status="Approved"
    )

    db.session.add(drive)
    db.session.commit()

    return "Drive Added Successfully"

@app.route("/apply/<int:drive_id>")
def apply(drive_id):

    student_id = 1  

    existing = Application.query.filter_by(
        student_id=student_id,
        drive_id=drive_id
    ).first()

    if existing:
        return "You already applied for this drive."

    application = Application(
        student_id=student_id,
        drive_id=drive_id,
        application_date="Today",
        status="Applied"
    )

    db.session.add(application)
    db.session.commit()

    return "Application Submitted Successfully"

@app.route("/company_register", methods=["GET", "POST"])
def company_register():

    if request.method == "POST":

        name = request.form["name"]
        hr_contact = request.form["hr_contact"]
        email = request.form["email"]
        website = request.form["website"]
        password = request.form["password"]

        company = Company(
            name=name,
            hr_contact=hr_contact,
            email=email,
            website=website,
            password=password,
            approval_status="Pending"
        )

        db.session.add(company)
        db.session.commit()

        return "Company Registered. Waiting for Admin Approval."

    return render_template("company_register.html")

@app.route("/company_login", methods=["GET","POST"])
def company_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        company = Company.query.filter_by(email=email, password=password).first()

        if company:

            if company.approval_status == "Approved":
                return redirect("/company_dashboard")
            else:
                return "Company not approved by admin yet."

        else:
            return "Invalid Login"

    return render_template("company_login.html")

@app.route("/company_dashboard")
def company_dashboard():

    drives = Drive.query.all()

    return render_template("company_dashboard.html", drives=drives)

@app.route("/create_drive", methods=["GET","POST"])
def create_drive():

    if request.method == "POST":

        job_title = request.form["job_title"]
        company_name = request.form["company_name"]
        description = request.form["description"]
        eligibility = request.form["eligibility"]
        deadline = request.form["deadline"]

        drive = Drive(
            job_title=job_title,
            company_name=company_name,
            description=description,
            eligibility=eligibility,
            deadline=deadline,
            status="Pending"
        )

        db.session.add(drive)
        db.session.commit()

        return redirect("/company_dashboard")

    return render_template("create_drive.html")

@app.route("/approve_drive/<int:id>")
def approve_drive(id):

    drive = Drive.query.get(id)

    drive.status = "Approved"

    db.session.commit()

    return redirect("/admin_dashboard")

@app.route("/reject_drive/<int:id>")
def reject_drive(id):

    drive = Drive.query.get(id)

    drive.status = "Rejected"

    db.session.commit()

    return redirect("/admin_dashboard")

@app.route("/view_applications/<int:drive_id>")
def view_applications(drive_id):

    applications = Application.query.filter_by(drive_id=drive_id).all()

    return render_template("view_applications.html", applications=applications)

@app.route("/admin_login", methods=["GET","POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            return redirect("/admin_dashboard")

        else:
            return "Invalid Admin Login"

    return render_template("admin_login.html")

@app.route("/admin_dashboard")
def admin_dashboard():

    students = Student.query.all()
    companies = Company.query.all()
    drives = Drive.query.all()
    applications = Application.query.all()

    return render_template(
        "admin_dashboard.html",
        students=students,
        companies=companies,
        drives=drives,
        applications=applications
    )

@app.route("/approve_company/<int:id>")
def approve_company(id):

    company = Company.query.get(id)

    company.approval_status = "Approved"

    db.session.commit()

    return redirect("/admin_dashboard")

@app.route("/reject_company/<int:id>")
def reject_company(id):

    company = Company.query.get(id)

    company.approval_status = "Rejected"

    db.session.commit()

    return redirect("/admin_dashboard")

@app.route("/my_applications")
def my_applications():

    student_id = 1   

    applications = Application.query.filter_by(student_id=student_id).all()

    return render_template("my_applications.html", applications=applications)




if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)