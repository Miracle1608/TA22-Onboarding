from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy
import urllib
from calculate import calculate_carbon_emissions



app = Flask(__name__)

params = urllib.parse.quote_plus("""
Driver={ODBC Driver 18 for SQL Server};
Server=tcp:week3proj.database.windows.net,1433;
Database=ta22;
Uid=kcha0109;
Pwd=Monash@2024;
Encrypt=yes;
TrustServerCertificate=no;
Connection Timeout=30;
""")

# Setup SQL Alchemy with the connection string
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: Suppress warning

# Create an instance of SQL Alchemy
#db = SQLAlchemy(app)


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
