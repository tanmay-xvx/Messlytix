import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pickle

app = Flask(__name__,
            static_folder='static')

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/studentsfeedback'

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    regno = db.Column(db.String(200))
    attendance = db.Column(db.String(4))

    def __init__(self, name, regno, attendance):
        self.name = name
        self.regno = regno
        self.attendance = attendance

class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    regno = db.Column(db.String(200))

    def __init__(self,regno):
        self.regno = regno




model = pickle.load(open('messmodel.pkl', 'rb'))
attendees = db.session.query(Feedback).filter(Feedback.attendance == 'regno').count()


@app.route('/', methods=["GET", "POST"])
# home
@app.route('/home')
def home():
    return render_template('index.html')

# Choose
@app.route('/choose')
def choose():
    return render_template('choose.html')

# admin
@app.route('/admin')
def admin():
    return render_template('admin.html',new_attendance='The number of attendees are {} \n'.format(attendees))

# analyse
@app.route('/analyse')
def analyse():
    return render_template('analyze.html')

# STUDENT
@app.route('/student')
def student():
    return render_template('student.html')

# submit
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        regno = request.form['regno']
        attendance = request.form['attendance']

        if db.session.query(Feedback).filter(Feedback.regno == regno).count() == 0:
            data = Feedback(name, regno, attendance)
            if db.session.query(Login).filter(Login.regno == regno).count() == 0:
                return render_template('student.html',message='Registraion Number Not Recognised')
            else:
                db.session.add(data)
                db.session.commit()
                return render_template('success.html')
        else:
            return render_template('student.html')


# prediction
@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    # int_features = [int(x) for x in request.form.values()]
    day = request.form.get("weekday")
    print(day)

    def convert_to_int(day):
        if day == 'Monday':
            return 0
        elif day == 'Tuesday':
            return 1
        elif day == 'Wednesday':
            return 2
        elif day == 'Thursday':
            return 3
        elif day == 'Friday':
            return 4
        elif day == 'Saturday':
            return 5
        elif day == 'Sunday':
            return 6

    def weekday():
        if(day1 != [5, 6]):
            return 0
        else:
            return 1

    def menu_rating():
        if day1 == 0:
            return 7
        elif day1 == 1:
            return 8.5
        elif day1 == 2:
            return 9.1
        elif day1 == 3:
            return 8.9
        elif day1 == 4:
            return 8.6
        elif day1 == 5:
            return 7
        elif day1 == 6:
            return 7.9

    def meanwastage():
        mean_wastage = 0
        if(day1 == 0):
            return 153.33333333333
        elif(day1 == 1):
            return 143
        elif(day1 == 2):
            return 107.233
        elif(day1 == 3):
            return 102.233
        elif(day1 == 4):
            return 112.344
        elif(day1 == 5):
            return 349.456
        elif(day1 == 6):
            return 330.233
    # final_features = [int_features]
    Wastage = 0
    day1 = convert_to_int(day)
    weekend = weekday()
    mean_wastage = meanwastage()
    New_Menu_rating = menu_rating()
    prediction = model.predict([[day1, weekend, New_Menu_rating, Wastage]])
    output = round(prediction[0], 3)

    return render_template('admin.html', new_attendance='The number of attendees are {} /n'.format(attendees), prediction_text1='Menu rating for Today is : {} \n'.format(New_Menu_rating), prediction_text2='Average wastage on this day is: {} \n '.format(mean_wastage), prediction_text3='To avoid this wastage this is the predicted amount to be cooked :\n{}'.format(output))


@app.route('/predict_api', methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


if __name__ == "__main__":
    app.run()
