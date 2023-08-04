

def calculate_carbon_emissions(electricity_usage, gas_usage):
    # Constants for carbon emissions factor (CO2 emissions per unit)
    electricity_emission_factor = 0.5  # Assume 0.5 kg CO2 per kWh
    gas_emission_factor = 1.9  # Assume 1.9 kg CO2 per m³

    # Calculate carbon emissions for electricity and gas usage
    electricity_emissions = electricity_usage * electricity_emission_factor
    gas_emissions = gas_usage * gas_emission_factor

    total_emissions = electricity_emissions + gas_emissions

    return total_emissions

if __name__ == '__main__':
    # Sample usage for testing
    electricity_usage = float(input("Enter electricity usage (kWh): "))
    gas_usage = float(input("Enter gas usage (m³): "))

    total_emissions = calculate_carbon_emissions(electricity_usage, gas_usage)
    print(f"Total carbon emissions: {total_emissions:.2f} kg CO2")
