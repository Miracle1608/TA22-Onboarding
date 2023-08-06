
import pymssql
from flask import Flask, render_template, request,jsonify
from flask_sqlalchemy import SQLAlchemy
import urllib
from calculate import calculate_carbon_emissions
import pandas as pd

server = 'week3proj.database.windows.net'
database = 'ta22'
username = 'kcha0109'
password = 'Monash@2024'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    conn = pymssql.connect(server=server, user=username, password=password, database=database)
    ElecEmissionsData = pd.read_sql('SELECT * FROM ElecEmissionsData', conn)
    GasEmissionsData = pd.read_sql('SELECT * FROM GasEmissionsData', conn)

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
            'Average Carbon Emission Electricity': filtered_data_elec['total_emissions_kg_co2e'].mean(),
            'Average Carbon Emission Per Customer Electricity': filtered_data_elec[
                'average_emissions_per_customer_kg_co2e'].mean(),
            'Average Carbon Emission Gas': filtered_data_gas['total_emissions_kg_co2e'].mean(),
            'Average Carbon Emission Per Customer Gas': filtered_data_gas[
                'average_emissions_per_customer_kg_co2e'].mean(),
        }

    return render_template('home.html', suburbs=suburbs, table_data=table_data,
                           highest_elec1=highest_elec1, lowest_elec1=lowest_elec1,
                           highest_gas1=highest_gas1, lowest_gas1=lowest_gas1)

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
    app.run(debug=True)
