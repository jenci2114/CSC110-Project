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


if __name__ == '__main__':
    alberta_temp = read_csv_temp('temperature/alberta.csv')
