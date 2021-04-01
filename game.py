"""CSC110 Fall 2020 Project

Description
===============================

This Python module contains functions needed to create a Pygame interface
that predicts emission, deforestation, and temperature data using
data stored in 'process_data.py'. This Python module also uses Plotly
to generate statistical graphs after one finishes playing the game.

Copyright Information
===============================

This file is Copyright (c) 2020 Caules Ge, Jenci Wei, Zheng Luan
"""
import math
import random

import pygame
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from process_data import *


class TemperatureGame:
    """A simulation of Canada's temperature.

    Instance Attributes:
        - emission: mapping of year to emission (Megatonnes of CO2 equivalent)
        - deforestation: mapping of year to deforestation (Hectares)
        - temperature: mapping of year to temperature (Degrees Celcius)
        - emission_predict: prediction curve of emission
        - deforestation_predict: prediction curve of deforestation
        - correlation: correlation between temperature and (emission and deforestation)

    Representation Invariants:
        - all(k >= 2020 for k in self.emission)
        - all(self.emission[k] >= 0 for k in self.emission)
        - all(k >= 2020 for k in self.deforestation)
        - all(self.deforestation[k] >= 0 for k in self.deforestation)
        - all(k >= 2020 for k in self.temperature)

    Sample usage:
    >>> game = TemperatureGame(EMISSION_CURVE, DEFORESTATION_REST_CURVE, FINAL_CORRELATION, 14)
    >>> game.run()
    """
    emission: Dict[int, float]
    deforestation: Dict[int, float]
    temperature: Dict[int, float]
    emission_predict: Tuple[float, float, float]
    deforestation_predict: Tuple[float, float, float]
    correlation: Tuple[float, float, float, float, float]

    def __init__(self, emission_predict: Tuple[float, float, float],
                 deforestation_predict: Tuple[float, float, float],
                 correlation: Tuple[float, float, float, float, float],
                 start_temp: float) -> None:
        """Initializes the game."""

        # Avoid python_ta from yelling at me for not initializing those
        # three classes before calling a method
        self.emission = {}
        self.deforestation = {}
        self.temperature = {}

        # Actually initialize the game
        self.emission_predict = emission_predict
        self.deforestation_predict = deforestation_predict
        self.correlation = correlation
        self.emission = {2020: self.predict_emission(2020)}
        self.deforestation = {2020: self.predict_deforestation(2020)}
        self.temperature = {2020: start_temp}

    def predict_emission(self, year: int) -> float:
        """Predict the emission value of the following year."""
        a, b, c = self.emission_predict
        return a * math.log(year - b) + c + random.uniform(-30, 30)

    def predict_deforestation(self, year: int) -> float:
        """Predict the deforestation value of the following year."""
        a, b, c = self.deforestation_predict
        return a / (year - b) + c + random.uniform(-3000, 3000)

    def predict_temperature(self, emission: float, deforestation: float,
                            temp_current_year: float) -> float:
        """Predict the temperature value of the following year."""
        a, b, c, d, e = self.correlation
        change = abs(a) * (emission - b) + abs(c) * (deforestation - d) + e
        return temp_current_year + change

    def predict_display(self, screen: pygame.Surface, new_year: int, new_emission: float,
                        new_deforestation: float, new_temperature: float) -> None:
        """Display the prediction of the following year, given all the values
        to be displayed.
        """
        # Define RGB colours
        black = (0, 0, 0)

        # Create font and text
        x_align = 80
        font = pygame.font.SysFont('Comic Sans MS', 32)
        font_title = pygame.font.SysFont('Comic Sans MS', 48)
        title_text = font_title.render('Environmental Data Prediction', True, black)
        title_rect = title_text.get_rect(topleft=(x_align, 60))
        year_text = font.render(f'Year: {new_year}', True, black)
        year_rect = year_text.get_rect(topleft=(x_align, 180))
        emission_text = font.render(f'Emission: {new_emission} Megatonnes of CO2 Equivalent',
                                    True, black)
        emission_rect = emission_text.get_rect(topleft=(x_align, 270))
        deforestation_text = font.render(f'Deforestation: {new_deforestation} Hectares',
                                         True, black)
        deforestation_rect = deforestation_text.get_rect(topleft=(x_align, 360))
        temperature_text = font.render(f'Temperature: {new_temperature} Degrees Celsius',
                                       True, black)
        temperature_rect = temperature_text.get_rect(topleft=(x_align, 450))

        # Display text
        screen.blit(title_text, title_rect)
        screen.blit(year_text, year_rect)
        screen.blit(emission_text, emission_rect)
        screen.blit(deforestation_text, deforestation_rect)
        screen.blit(temperature_text, temperature_rect)

    def run(self) -> None:
        """Run this game."""
        # Initialize pygame
        pygame.init()

        # Define RGB colours
        black = (0, 0, 0)
        red = (255, 0, 0)

        # Create a screen
        size = (1280, 720)
        screen = pygame.display.set_mode(size)
        background = pygame.image.load('images/background.jpg')
        screen.blit(background, (0, 0))

        # Create font and instruction text
        font = pygame.font.SysFont('Comic Sans MS', 24)
        instruction_text = font.render('Press the SPACEBAR to predict the environmental data '
                                       'for the following year.', True, black)
        instruction_rect = instruction_text.get_rect(topleft=(80, 600))
        screen.blit(instruction_text, instruction_rect)

        # Initialize current values
        current_year = 2020
        current_emission = round(self.emission[2020], 3)
        current_deforestation = round(self.deforestation[2020], 3)
        current_temperature = round(self.temperature[2020], 3)
        self.predict_display(screen, current_year, current_emission,
                             current_deforestation, current_temperature)
        pygame.display.flip()

        # Event loop
        while True:
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Exit the event loop
                    pygame.quit()
                    print('Thanks for playing!')
                    graph = input('Do you want a statistical graph for your game? If so, input \'y\': ')
                    if graph == 'y':
                        self.print_graph()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Predict next year's values
                    hydro = random.randint(1, 20) == 1
                    current_year += 1
                    current_emission = self.predict_emission(current_year)
                    current_deforestation = self.predict_deforestation(current_year)
                    if hydro:
                        current_deforestation += random.uniform(20000, 30000)
                    current_temperature = self.predict_temperature(
                        current_emission, current_deforestation, current_temperature
                    )

                    # Store next year's values
                    self.emission[current_year] = current_emission
                    self.deforestation[current_year] = current_deforestation
                    self.temperature[current_year] = current_temperature

                    # Display the values
                    background = pygame.image.load('images/background.jpg')
                    screen.blit(background, (0, 0))
                    screen.blit(instruction_text, instruction_rect)
                    self.predict_display(screen, current_year, round(current_emission, 3),
                                         round(current_deforestation, 3),
                                         round(current_temperature, 3))
                    if hydro:
                        hydro_text = font.render('During the hydroelectric reservoir development this year, '
                                                 'large forest areas are flooded.', True, red)
                        hydro_rect = hydro_text.get_rect(topleft=(80, 540))
                        screen.blit(hydro_text, hydro_rect)
                    pygame.display.flip()

    def print_graph(self) -> None:
        """Print a statistical graph for the game."""
        years = list(self.temperature.keys())

        # Initialize figure with subplots
        fig = make_subplots(rows=3, cols=1, subplot_titles=(
            'Emission Data', 'Deforestation Data', 'Temperature Data'))

        # Add traces
        fig.add_trace(go.Scatter(x=years, y=list(self.emission.values()),
                                 mode='lines+markers', name='Emission Data'),
                      row=1, col=1)
        fig.add_trace(go.Scatter(x=years, y=list(self.deforestation.values()),
                                 mode='lines+markers', name='Deforestation Data'),
                      row=2, col=1)
        fig.add_trace(go.Scatter(x=years, y=list(self.temperature.values()),
                                 mode='lines+markers', name='Temperature Data'),
                      row=3, col=1)

        # Update x-axis properties
        fig.update_xaxes(title_text='Year', row=1, col=1)
        fig.update_xaxes(title_text='Year', row=2, col=1)
        fig.update_xaxes(title_text='Year', row=3, col=1)

        # Update y-axis properties
        fig.update_yaxes(title_text='Emission (Megatonnes of CO2 Equivalent)', row=1, col=1)
        fig.update_yaxes(title_text='Deforestation (Hectares)', row=2, col=1)
        fig.update_yaxes(title_text='Temperature (Degrees Celsius)', row=3, col=1)

        # Show graph
        fig.update_layout(title='Statistical Graph For Your Game')
        fig.show()


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
