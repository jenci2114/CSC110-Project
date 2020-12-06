"""CSC110 Project - Fall 2020
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
