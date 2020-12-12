"""CSC110 Fall 2020 Project

Description
===============================

This Python module contains functions needed to visualize
data that are already processed by the module 'process_data.py'
using Plotly.

Copyright Information
===============================

This file is Copyright (c) 2020 Caules Ge, Jenci Wei, Zheng Luan
"""
import plotly.graph_objects as go
from process_data import *


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


def visualize_temp_trend(data: Dict[int, float]) -> None:
    """Visualize the trend of temperature data
    Use a plotly *scatterplot* to visualize the data.
    """
    coords = []
    for element in data:
        coords.append((element, data[element]))
    coords.sort()
    x_coords = [coord[0] for coord in coords]
    y_coords = [coord[1] for coord in coords]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_coords, y=y_coords))
    fig.update_layout(title='Temperature Data', xaxis_title='Year', yaxis_title='Temperature')
    fig.show()


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

    domain = numpy.arange(1990, 2020)
    a, b, c = model_emission(data)
    fig.add_trace(go.Scatter(x=domain, y=a * numpy.log(domain - b) + c))

    fig.update_layout(title='Emission Data', xaxis_title='Year', yaxis_title='Emission (Megatonnes of CO2 Equivalent)')
    fig.show()


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

    domain = numpy.arange(1990, 2020)
    a, b, c = model_deforestation(data)
    fig.add_trace(go.Scatter(x=domain, y=a / (domain - b) + c))

    fig.update_layout(title='Deforestation Data', xaxis_title='Year', yaxis_title='Deforstation (Hectares)')
    fig.show()


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
