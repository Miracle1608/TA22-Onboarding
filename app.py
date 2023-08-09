import numpy as np
import pyodbc
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import urllib
from calculate import calculate_carbon_emissions
from sqlalchemy import func
#import pymssql
from flask import Flask, render_template, request,jsonify
from flask_sqlalchemy import SQLAlchemy
import urllib
from calculate import calculate_carbon_emissions
import pandas as pd

app = Flask(__name__)

# params = urllib.parse.quote_plus("DRIVER={ODBC Driver 18 for SQL Server};"
#                                  "SERVER=week3proj.database.windows.net;"
#                                  "DATABASE=ta22;"
#                                  "UID=kcha0109;"
#                                  "PWD=Monash@2024;")

params = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=week3proj.database.windows.net;DATABASE=ta22;UID=kcha0109;PWD=Monash@2024;'


app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
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


class ElecEmissionsData(db.Model):
    __tablename__ = 'ElecEmissionsData'

    year = db.Column(db.Integer, primary_key=True)
    postcode = db.Column(db.Integer, db.ForeignKey('SuburbData.postcode'), primary_key=True)
    suburb = db.Column(db.String(255))
    emission_source = db.Column(db.String(255))
    total_electricity_kwh = db.Column(db.Float)
    average_intensity_kwh_per_customer_per_annum = db.Column(db.Float)
    average_intensity_kwh_per_customer_per_day = db.Column(db.Float)
    scope_2_kg_co2e = db.Column(db.Float)
    scope_3_kg_co2e = db.Column(db.Float)
    total_emissions_kg_co2e = db.Column(db.Float)
    average_emissions_per_customer_kg_co2e = db.Column(db.Float)
    average_emissions_energy_per_customer_kg_co2e_per_day = db.Column(db.Float)
    rest_of_municipality_total_electricity_kwh = db.Column(db.Float)
    rest_of_municipality_emissions_kg_co2e = db.Column(db.Float)
    total_cost = db.Column(db.Float)
    average_intensity_household_per_day = db.Column(db.Float)
    average_intensity_household_per_month = db.Column(db.Float)
    average_intensity_household_per_annum = db.Column(db.Float)


class GasEmissionsData(db.Model):
    __tablename__ = 'GasEmissionsData'

    year = db.Column(db.Integer, primary_key=True)
    postcode = db.Column(db.Integer, db.ForeignKey('SuburbData.postcode'), primary_key=True)
    suburb = db.Column(db.String(255))
    emission_source = db.Column(db.String(255))
    total_gas_gj = db.Column(db.Float)
    average_intensity_gj_per_customer_per_annum = db.Column(db.Float)
    average_intensity_mj_per_customer_per_day = db.Column(db.Float)
    scope_1_kg_co2e = db.Column(db.Float)
    scope_3_kg_co2e = db.Column(db.Float)
    total_emissions_kg_co2e = db.Column(db.Float)
    average_emissions_per_customer_kg_co2e = db.Column(db.Float)
    average_emissions_energy_per_customer_kg_co2e_per_day = db.Column(db.Float)
    rest_of_municipality_total_gas_gj = db.Column(db.Float)
    rest_of_municipality_emissions_kg_co2e = db.Column(db.Float)
    total_cost = db.Column(db.Float)
    average_intensity_household_per_day = db.Column(db.Float)
    average_intensity_household_per_month = db.Column(db.Float)
    average_intensity_household_per_annum = db.Column(db.Float)


# server = 'week3proj.database.windows.net'
# database = 'ta22'
# username = 'kcha0109'
# password = 'Monash@2024'

@app.route('/', methods=['GET', 'POST'])
def home():
    # [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]
    conn = db.engine.connect()
    # conn = pymssql.connect(server=server, user=username, password=password, database=database)
    ElecEmissionsData = pd.read_sql('SELECT * FROM ElecEmissionsData', conn)
    GasEmissionsData = pd.read_sql('SELECT * FROM GasEmissionsData', conn)

    conn.close()

    suburbs = ElecEmissionsData['suburb'].unique().tolist()
    highest_elec1 = ElecEmissionsData.loc[ElecEmissionsData['total_emissions_kg_co2e'].idxmax()]
    lowest_elec1 = ElecEmissionsData.loc[ElecEmissionsData['total_emissions_kg_co2e'].idxmin()]

    highest_gas1 = GasEmissionsData.loc[GasEmissionsData['total_emissions_kg_co2e'].idxmax()]
    lowest_gas1 = GasEmissionsData.loc[GasEmissionsData['total_emissions_kg_co2e'].idxmin()]

    table_data = None

    if request.method == 'POST':
        selected_suburb = request.form.get('suburb')
        filtered_data_elec = ElecEmissionsData[ElecEmissionsData['suburb'] == selected_suburb]
        filtered_data_gas = GasEmissionsData[GasEmissionsData['suburb'] == selected_suburb]
        table_data = {
            'Suburb': selected_suburb,
            'Average Carbon Emission Electricity': np.round(filtered_data_elec['total_emissions_kg_co2e'].mean()),
            'Average Carbon Emission Per Customer Electricity': np.round(filtered_data_elec['average_emissions_per_customer_kg_co2e'].mean()),
            'Average Carbon Emission Gas': np.round(filtered_data_gas['total_emissions_kg_co2e'].mean()),
            'Average Carbon Emission Per Customer Gas': np.round(filtered_data_gas['average_emissions_per_customer_kg_co2e'].mean()),
        }

    return render_template('home.html', suburbs=suburbs, table_data=table_data,
                           highest_elec1=highest_elec1, lowest_elec1=lowest_elec1,
                           highest_gas1=highest_gas1, lowest_gas1=lowest_gas1)

@app.route('/emissions', methods=['POST'])
def emissions(postcode):
    try:
        suburb_data = SuburbData.query.filter_by(postcode=postcode).first()

        avg_gas_emission_per_customer = db.session.query(
            func.avg(GasEmissionsData.average_emissions_per_customer_kg_co2e)).filter(
            GasEmissionsData.postcode == postcode).scalar()
        avg_elec_emission_per_customer = db.session.query(
            func.avg(ElecEmissionsData.average_emissions_per_customer_kg_co2e)).filter(
            ElecEmissionsData.postcode == postcode).scalar()

        return render_template('emissions.html', suburb=suburb_data,
                               avg_gas_emission_per_customer=avg_gas_emission_per_customer,
                               avg_elec_emission_per_customer=avg_elec_emission_per_customer)
    except Exception as e:
        return str(e)

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
    app.run(host="0.0.0.0", port = int("80"), debug =True)
