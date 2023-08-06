
import pymssql
from flask import Flask, render_template, request,jsonify
from flask_sqlalchemy import SQLAlchemy
import urllib
from calculate import calculate_carbon_emissions
import pandas as pd



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # ElecEmissionsData = pd.read_csv("C:/Users/15969/Desktop/工作/2023-08-05/PythonProjects/ElecEmissionsData.csv")
    # GasEmissionsData = pd.read_csv("C:/Users/15969/Desktop/工作/2023-08-05/PythonProjects/GasEmissionsData.csv")
    ElecEmissionsData = pd.read_csv("D:\PythonProjects\ElecEmissionsData.csv")
    GasEmissionsData = pd.read_csv("D:\PythonProjects\GasEmissionsData.csv")

    suburbs = ElecEmissionsData['suburb'].unique().tolist()

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

    return render_template('home.html', suburbs=suburbs, table_data=table_data)

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
