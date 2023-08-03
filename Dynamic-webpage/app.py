from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for, redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class Student(db.Model):
	__tablename__ = 'student'
	student_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
	roll_number = db.Column(db.String, unique = True, nullable = False)
	first_name = db.Column(db.String, nullable = False)
	last_name = db.Column(db.String)

class Course(db.Model):
	__tablename__ = 'course'
	course_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
	course_code = db.Column(db.String, unique = True, nullable = False)
	course_name = db.Column(db.String, nullable = False)
	course_description = db.Column(db.String)
	
class Enrollments(db.Model):
	__tablename__ = 'enrollments'
	enrollment_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
	estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), primary_key= True, nullable = False)
	ecourse_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), primary_key= True, nullable = False)
	
@app.route("/", methods = ["GET", "POST"])
def index():
	studentlist = Student.query.all()
	return render_template("index.html", students = studentlist)

@app.route("/student/create", methods = ["GET", "POST"])
def add_student():
	if(request.method=="GET"):
		return render_template("add_student.html", flag = False)
	elif(request.method=="POST"):
		roll_no = request.form["roll"]
		fname = request.form["f_name"]
		lname = request.form["l_name"]
		list = request.form.getlist("courses")
		temp = Student.query.filter_by(roll_number = roll_no).all()
		if(temp==[]):
			obj = Student()
			obj.roll_number = roll_no
			obj.first_name = fname
			obj.last_name = lname
			db.session.add(obj)
			db.session.commit()
			temp = Student.query.filter_by(roll_number = roll_no).all()[0]
			for j in list:
				obj2 = Enrollments()
				if j=="course_1":
					obj2.estudent_id = temp.student_id
					obj2.ecourse_id = 1
				elif j=="course_2":
					obj2.estudent_id = temp.student_id
					obj2.ecourse_id = 2
				elif j=="course_3":
					obj2.estudent_id = temp.student_id
					obj2.ecourse_id = 3
				elif j=="course_4":
					obj2.estudent_id = temp.student_id
					obj2.ecourse_id = 4
				db.session.add(obj2)
				db.session.commit()
			return redirect(url_for('index'))
		else:
			return render_template("add_student.html", flag = True)
			
@app.route("/student/<s_id>/update", methods = ["GET", "POST"])
def update_student(s_id):
	if(request.method=="GET"):
		return render_template("update_student.html", id = s_id, obj = Student.query.filter_by(student_id = s_id).all()[0])
	elif(request.method=="POST"):
		fname = request.form.get("f_name")
		lname = request.form.get("l_name")
		list = request.form.getlist("courses")
		obj = Student.query.filter_by(student_id = s_id).all()[0]
		obj.first_name = fname
		obj.last_name = lname
		obj.verified = True
		db.session.commit()
		obj2 = Enrollments.query.filter_by(estudent_id = s_id).all()
		for j in obj2:
			db.session.delete(j)
			db.session.commit()
		for j in list:
			obj2 = Enrollments()
			if j=="course_1":
				obj2.estudent_id = s_id
				obj2.ecourse_id = 1
			elif j=="course_2":
				obj2.estudent_id = s_id
				obj2.ecourse_id = 2
			elif j=="course_3":
				obj2.estudent_id = s_id
				obj2.ecourse_id = 3
			elif j=="course_4":
				obj2.estudent_id = s_id
				obj2.ecourse_id = 4
			db.session.add(obj2)
			db.session.commit()
		return redirect(url_for('index'))
		
@app.route("/student/<s_id>/delete", methods = ["GET", "POST"])
def delete_student(s_id):
	if(request.method=="GET"):
		obj1 = Student.query.filter_by(student_id = s_id).all()
		ls = Enrollments.query.filter_by(estudent_id = s_id).all()
		db.session.delete(obj1[0])
		db.session.commit()
		for i in ls:
			db.session.delete(i)
			db.session.commit()
	return redirect(url_for('index'))
	
@app.route("/student/<s_id>", methods = ["GET"])
def show_details(s_id):
	list = []
	temp = Enrollments.query.filter_by(estudent_id = s_id).all()
	for i in temp:
		list.append(Course.query.filter_by(course_id = i.ecourse_id).all()[0])
	return render_template("details.html", obj = Student.query.filter_by(student_id = s_id).all()[0], obj2 = list)

if __name__ == '__main__':
	app.run()