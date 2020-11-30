"""CSC110 Project - Fall 2020
"""

import math
import csv
import plotly.graph_objects as go
from dataclasses import dataclass
from typing import *


@dataclass
class Temperature:
    """A custom data type that represents a temperature point

    Instance Attributes:
        - prov: the province in which the temperature is recorded
        - year: the year in which the temperature is recorded
        - temp: temperature in degrees Celsius

    Representation Invariants:
        - self.prov in {'AB', 'BC', 'MB', 'NB', 'NL', 'NT', 'NS', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT'}
        - self.year in range(1990, 2020)
    """
    prov: str
    year: int
    temp: float


def read_csv_temp(filename: str) -> List[Temperature]:
    """Return the temperature data stored in the csv file with the given filename.

    Preconditions:
        - filename refers to a valid csv file in the 'temperature' folder
    """
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)  # skips the headers line
        data = [process_row_temp(row) for row in reader]

    return [item for item in data if item.temp != -9999.9]


def process_row_temp(row: List[str]) -> Temperature:
    """Convert a row of temperature data to Temperature object

    Preconditions:
        - row has the correct format for the temperature data set
    """
    if row[10] == '':
        row[10] = '-9999.9'

    return Temperature(
        row[8],  # province
        int(row[9]),  # year
        float(row[10])  # temperature
    )


def visualize_temp_data(temp_data: List[Temperature]) -> None:
    """Visualize the results of temperature of a province.
    Use a plotly *scatterplot* to visualize the data.
    """
    x_coords, y_coords = [], []
    for element in temp_data:
        x_coords.append(element.year)
        y_coords.append(element.temp)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='markers'))
    fig.update_layout(title=temp_data[0].prov, xaxis_title='Year', yaxis_title='Temperature')
    fig.show()


def read_csv_emission(filename: str) -> Dict[int, int]:
    """Return the greenhouse gas emission data stored in the csv file with the given filename.

    Preconditions:
        - filename refers to a valid csv file in the 'other_data' folder
    """
    with open(filename) as file:
        reader = csv.reader(file)
        mapping_so_far = {}
        for row in reader:
            if row[0].isnumeric():
                mapping_so_far[int(row[0])] = int(row[1])

    return mapping_so_far


def visualize_emission_data(data: Dict[int, int]) -> None:
    """Visualize the emission data
    Use a plotly *scatterplot* to visualize the data.
    """
    x_coords, y_coords = [], []
    for element in data:
        x_coords.append(element)
        y_coords.append(data[element])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_coords, y=y_coords))
    fig.update_layout(title='Emission Data', xaxis_title='Year', yaxis_title='Emission (Megatonnes of CO2 Equivalent)')
    fig.show()


def read_csv_deforestation(filename: str) -> Dict[int, int]:
    """Return the deforestation data stored in the csv file with the given filename.

    Preconditions:
        - filename refers to a valid csv file in the 'other_data' folder
    """
    with open(filename) as file:
        reader = csv.reader(file)
        mapping_so_far = {}
        for row in reader:
            if row[0].isnumeric():
                num = row[6].replace(',', '')
                mapping_so_far[int(row[0])] = int(num)

    return mapping_so_far


def visualize_deforestation_data(data: Dict[int, int]) -> None:
    """Visualize the deforestation data
    Use a plotly *scatterplot* to visualize the data.
    """
    x_coords, y_coords = [], []
    for element in data:
        x_coords.append(element)
        y_coords.append(data[element])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_coords, y=y_coords))
    fig.update_layout(title='Deforestation Data', xaxis_title='Year', yaxis_title='Deforstation (Hectares)')
    fig.show()


if __name__ == '__main__':
    # Processed temperature data for each province
    alberta_temp = read_csv_temp('temperature/alberta.csv')
    british_columbia_temp = read_csv_temp('temperature/british_columbia.csv')
    manitoba_temp = read_csv_temp('temperature/manitoba.csv')
    new_brunswick_temp = read_csv_temp('temperature/new_brunswick.csv')
    newfoundland_temp = read_csv_temp('temperature/newfoundland.csv')
    northwest_temp = read_csv_temp('temperature/northwest.csv')
    nova_scotia_temp = read_csv_temp('temperature/nova_scotia.csv')
    nunavut_temp = read_csv_temp('temperature/nunavut.csv')
    ontario_temp = read_csv_temp('temperature/ontario.csv')
    prince_edward_temp = read_csv_temp('temperature/prince_edward.csv')
    quebec_temp = read_csv_temp('temperature/quebec.csv')
    saskatchewan_temp = read_csv_temp('temperature/saskatchewan.csv')
    yukon_temp = read_csv_temp('temperature/yukon.csv')

    # Processed greenhouse gas emission data
    emission_data = read_csv_emission('other_data/emission.csv')

    # Processed deforestation data
    deforestation_data = read_csv_deforestation('other_data/deforestation.csv')
