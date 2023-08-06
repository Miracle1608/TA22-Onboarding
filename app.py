from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import urllib
from calculate import calculate_carbon_emissions
from sqlalchemy import func

app = Flask(__name__)

params = urllib.parse.quote_plus("DRIVER={ODBC Driver 18 for SQL Server};"
                                 "SERVER=week3proj.database.windows.net;"
                                 "DATABASE=ta22;"
                                 "UID=kcha0109;"
                                 "PWD=Monash@2024;")

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




@app.route('/')
def home():
    suburbs = SuburbData.query.all()  # Query the database for all suburbs
    return render_template("home.html", suburbs=suburbs)  # Pass the suburbs to the template

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
    app.run()
