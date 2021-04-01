"""CSC110 Fall 2020 Project

Description
===============================

This Python module contains functions needed to process the raw data
retrieved from various datasets. Additionally, processed data are
stored at the bottom of this module in the form that can be accessed by
other modules.

Copyright Information
===============================

This file is Copyright (c) 2020 Caules Ge, Jenci Wei, Zheng Luan
"""
import csv
import statistics

from dataclasses import dataclass
from typing import List, Dict, Tuple, Any

import numpy
from scipy.optimize import curve_fit


@dataclass
class Temperature:
    """A custom data type that represents a temperature point

    Instance Attributes:
        - prov: the province in which the temperature is recorded
        - year: the year in which the temperature is recorded
        - month: the month in which the temperature is recorded
        - temp: temperature in degrees Celsius

    Representation Invariants:
        - self.prov in {'AB', 'BC', 'MB', 'NB', 'NL', 'NT', 'NS', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT'}
        - self.year in range(1990, 2020)
        - self.month in range(1, 13)
    """
    prov: str
    year: int
    month: int
    temp: float


def read_csv_temp(filename: str) -> List[Temperature]:
    """Return the temperature data stored in the csv file with the given filename."""

    with open(filename, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # skips the headers line
        data = [process_row_temp(row) for row in reader]

    # Change this line if we want another month(s)
    return [item for item in data if item.temp != -9999.9 and item.month in {8, 9}]


def process_row_temp(row: List[str]) -> Temperature:
    """Convert a row of temperature data to Temperature object"""

    if row[10] == '':
        row[10] = '-9999.9'

    year, month = row[9].split('-')

    return Temperature(
        row[8],  # province
        int(year),  # year
        int(month),  # month
        float(row[10])  # temperature
    )


def get_yearly_median_temp(data: List[Temperature]) -> Dict[int, float]:
    """Returns a list of temperature containing the median for each year."""

    temp_mapping = {temp_class.year: [] for temp_class in data}

    for t in data:
        temp_mapping[t.year].append(t.temp)

    for year in temp_mapping:
        temp_mapping[year] = statistics.median(temp_mapping[year])

    return temp_mapping


def read_csv_emission(filename: str) -> Dict[int, int]:
    """Return the greenhouse gas emission data stored in the csv file with the given filename."""

    with open(filename, encoding='utf-8') as file:
        reader = csv.reader(file)
        mapping_so_far = {}
        for row in reader:
            if row[0].isnumeric():
                mapping_so_far[int(row[0])] = int(row[1])

    return mapping_so_far


def model_emission(data: Dict[int, int]) -> Tuple[float, float, float]:
    """Return the a-, b-, and c-value of y = a(ln(x - b)) + c, the best-fit curve
    of emission data.

    Return (a, b, c)
    """
    x = list(data.keys())
    y = list(data.values())

    def func(x, a, b, c) -> Any:
        return a * numpy.log(x - b) + c

    a, b, c = curve_fit(func, xdata=x, ydata=y)[0]

    return (a, b, c)


def read_csv_deforestation(filename: str) -> Dict[int, int]:
    """Return the deforestation data stored in the csv file with the given filename."""

    with open(filename, encoding='utf-8') as file:
        reader = csv.reader(file)
        mapping_so_far = {}
        for row in reader:
            if row[0].isnumeric():
                num = row[6].replace(',', '')
                mapping_so_far[int(row[0])] = int(num)

    return mapping_so_far


def read_csv_deforestation_hydro(filename: str) -> Dict[int, int]:
    """Return the deforestation data CAUSED BY HYDROELECTRIC
    stored in the csv file with the given filename.
    """
    with open(filename, encoding='utf-8') as file:
        reader = csv.reader(file)
        mapping_so_far = {}
        for row in reader:
            if row[0].isnumeric():
                num = row[5].replace(',', '')
                mapping_so_far[int(row[0])] = int(num)

    return mapping_so_far


def model_deforestation(data: Dict[int, int]) -> Tuple[float, float, float]:
    """Return the a-, b-, and c-value of y = a/(x-b) + c, the best-fit curve
    of emission data.

    Return (a, b, c)
    """
    x = list(data.keys())
    y = list(data.values())

    def func(x, a, b, c) -> Any:
        return a / (x - b) + c

    a, b, c = curve_fit(func, xdata=x, ydata=y)[0]

    return (a, b, c)


def model_correlation(data: Tuple[List[float], List[int], List[int]]) -> \
        Tuple[float, float, float, float, float]:
    """Return the a-, b-, c-, d-, and e-value of y = a(x1 - b) + c(x2 - d) + e, the prediction of
    temperature based on the given values of emission and deforestation.

    y denotes the temperature, x1 denotes the emission, and x2 denotes the deforestation,
    with their respective units

    Input is in the format of (list of temperature values, list of
    emission values, list of deforestation values).

    Returns the tuple (a, b, c, d, e)
    """
    x = numpy.array([data[1], data[2]])  # Emission, deforestation
    y = numpy.array(data[0])  # Temperature

    def func(x, a, b, c, d, e) -> Any:
        return numpy.abs(a) * (x[0] - b) + numpy.abs(c) * (x[1] - d) + e

    a, b, c, d, e = curve_fit(func, xdata=x, ydata=y)[0]

    return (a, b, c, d, e)


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
