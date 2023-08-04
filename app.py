from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import urllib
from calculate import calculate_carbon_emissions

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kcha0109:Monash@2024@week3proj.database.windows.net:1433/ta22'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class SuburbData(db.Model):
    __tablename__ = 'SuburbData'

    postcode = db.Column(db.Integer, primary_key=True)
    suburb = db.Column(db.String(128))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return f'<Suburb {self.suburb}>'




@app.route('/')
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get the form data submitted by the user
    electricity_usage = float(request.form['electricity'])
    gas_usage = float(request.form['gas'])

    # Calculate carbon emissions using the Calculator.py function
    total_emissions = calculate_carbon_emissions(electricity_usage, gas_usage)

    # Pass the calculated result to the template
    return render_template("result.html", total_emissions=total_emissions)


if __name__ == '__main__':
    app.run()
