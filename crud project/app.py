from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os




app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir,"data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    passenger_Name = db.Column(db.String(100))
    card_number = db.Column(db.String(100))
    phone = db.Column(db.String(100))


    def __init__(self, passenger_Name, card_number, phone):

        self. passenger_Name = passenger_Name
        self.card_number = card_number
        self.phone = phone





#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("crud_index.html", passengers = all_data)



#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        passenger_Name = request.form['passenger_Name']
        card_number = request.form['card_number']
        phone = request.form['phone']


        my_data = Data(passenger_Name, card_number, phone)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.passenger_Name = request.form['passenger_Name']
        my_data.card_number = request.form['card_number']
        my_data.phone = request.form['phone']

        db.session.commit()

        return redirect(url_for('Index'))




#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('Index'))






if __name__ == "__main__":
    app.run(port= 5002,debug=True)