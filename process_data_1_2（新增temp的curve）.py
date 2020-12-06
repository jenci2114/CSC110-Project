"""CSC110 Project - Fall 2020
"""
import csv
import numpy
import statistics

from dataclasses import dataclass
from scipy.optimize import curve_fit
from typing import *


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
    """Return the temperature data stored in the csv file with the given filename.

    Preconditions:
        - filename refers to a valid csv file in the 'temperature' folder
    """
    with open(filename, encoding='gbk', errors='ignore') as file:
        reader = csv.reader(file)
        next(reader)  # skips the headers line
        data = [process_row_temp(row) for row in reader]

    # Change this line if we want another month(s)
    return [item for item in data if item.temp != -9999.9 and item.month == 7]


def process_row_temp(row: List[str]) -> Temperature:
    """Convert a row of temperature data to Temperature object

    Preconditions:
        - row has the correct format for the temperature data set
    """
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

    temp_mapping = {t.year: [] for t in data}
    province = data[0].prov

    for t in data:
        temp_mapping[t.year].append(t.temp)

    for year in temp_mapping:
        temp_mapping[year] = statistics.median(temp_mapping[year])

    return temp_mapping


def read_csv_emission(filename: str) -> Dict[int, int]:
    """Return the greenhouse gas emission data stored in the csv file with the given filename.

    Preconditions:
        - filename refers to a valid csv file in the 'other_data' folder
    """
    with open(filename, encoding='gbk', errors='ignore') as file:
        reader = csv.reader(file)
        mapping_so_far = {}
        for row in reader:
            if row[0].isnumeric():
                mapping_so_far[int(row[0])] = int(row[1])

    return mapping_so_far


def model_emission(data: Dict[int, int]) -> Tuple[float, float, float]:
    """Return the a- and b- value of y = a(ln(x - b)) + c, the best-fit curve
    of emission data.

    Return (a, b, c)
    """
    x = [k for k in data]
    y = [data[k] for k in data]

    def func(x, a, b, c) -> Any:
        return a * numpy.log(x - b) + c

    a, b, c = curve_fit(func, xdata=x, ydata=y)[0]

    return (a, b, c)


def read_csv_deforestation(filename: str) -> Dict[int, int]:
    """Return the deforestation data stored in the csv file with the given filename.

    Preconditions:
        - filename refers to a valid csv file in the 'other_data' folder
    """
    with open(filename, encoding='gbk', errors='ignore') as file:
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

    Preconditions:
        - filename refers to a valid csv file in the 'other_data' folder
    """
    with open(filename, encoding='gbk', errors='ignore') as file:
        reader = csv.reader(file)
        mapping_so_far = {}
        for row in reader:
            if row[0].isnumeric():
                num = row[5].replace(',', '')
                mapping_so_far[int(row[0])] = int(num)

    return mapping_so_far


def model_deforestation(data: Dict[int, int]) -> Tuple[float, float, float]:
    """Return the a- and b- value of y = a/(x-b) + c, the best-fit curve
    of emission data.

    Return (a, b, c)
    """
    x = [k for k in data]
    y = [data[k] for k in data]

    def func(x, a, b, c) -> Any:
        return a / (x - b) + c

    a, b, c = curve_fit(func, xdata=x, ydata=y)[0]

    return (a, b, c)


def model_temp(data: Dict[int, float]) -> Tuple[float, float, float]:
    """Return the a- and b- value of y = a(ln(x - b)) + c, the best-fit curve
    of emission data.

    Return (a, b, c)
    """
    x = [k for k in data]
    y = [data[k] for k in data]

    def func(x, a, b, c) -> Any:
        return a * numpy.log(x - b) + c

    a, b, c = curve_fit(func, xdata=x, ydata=y)[0]

    return (a, b, c)


# Processed temperature data for each province
ALBERTA_TEMP = read_csv_temp('temperature/alberta.csv')
BRITISH_COLUMBIA_TEMP = read_csv_temp('temperature/british_columbia.csv')
MANITOBA_TEMP = read_csv_temp('temperature/manitoba.csv')
NEW_BRUNSWICK_TEMP = read_csv_temp('temperature/new_brunswick.csv')
NEWFOUNDLAND_TEMP = read_csv_temp('temperature/newfoundland.csv')
NORTHWEST_TEMP = read_csv_temp('temperature/northwest.csv')
NOVA_SCOTIA_TEMP = read_csv_temp('temperature/nova_scotia.csv')
NUNAVUT_TEMP = read_csv_temp('temperature/nunavut.csv')
ONTARIO_TEMP = read_csv_temp('temperature/ontario.csv')
PRINCE_EDWARD_TEMP = read_csv_temp('temperature/prince_edward.csv')
QUEBEC_TEMP = read_csv_temp('temperature/quebec.csv')
SASKATCHEWAN_TEMP = read_csv_temp('temperature/saskatchewan.csv')
YUKON_TEMP = read_csv_temp('temperature/yukon.csv')

ALBERTA_MEDIAN = get_yearly_median_temp(ALBERTA_TEMP)
BRITISH_COLUMBIA_MEDIAN = get_yearly_median_temp(BRITISH_COLUMBIA_TEMP)
MANITOBA_MEDIAN = get_yearly_median_temp(MANITOBA_TEMP)
NEW_BRUNSWICK_MEDIAN = get_yearly_median_temp(NEW_BRUNSWICK_TEMP)
NEWFOUNDLAND_MEDIAN = get_yearly_median_temp(NEWFOUNDLAND_TEMP)
NORTHWEST_MEDIAN = get_yearly_median_temp(NORTHWEST_TEMP)
NOVA_SCOTIA_MEDIAN = get_yearly_median_temp(NOVA_SCOTIA_TEMP)
NUNAVUT_MEDIAN = get_yearly_median_temp(NUNAVUT_TEMP)
ONTARIO_MEDIAN = get_yearly_median_temp(ONTARIO_TEMP)
PRINCE_EDWARD_MEDIAN = get_yearly_median_temp(PRINCE_EDWARD_TEMP)
QUEBEC_MEDIAN = get_yearly_median_temp(QUEBEC_TEMP)
SASKATCHEWAN_MEDIAN = get_yearly_median_temp(SASKATCHEWAN_TEMP)
YUKON_MEDIAN = get_yearly_median_temp(YUKON_TEMP)


def get_canada_median() -> Dict[int, float]:
    """
    This a helper function to get the canada median temperature.
    This not the traditional meaning of median data.
    This is calculated from the average of the province median data.
    """
    canada_median_so_far = {}
    for i in range(1991, 2020):
        canada_median_so_far[i] = (ALBERTA_MEDIAN[i] + BRITISH_COLUMBIA_MEDIAN[i] +
                                   MANITOBA_MEDIAN[i] + NEW_BRUNSWICK_MEDIAN[i] +
                                   NEWFOUNDLAND_MEDIAN[i] + NORTHWEST_MEDIAN[i] +
                                   NOVA_SCOTIA_MEDIAN[i] + NUNAVUT_MEDIAN[i] +
                                   ONTARIO_MEDIAN[i] + PRINCE_EDWARD_MEDIAN[i] +
                                   QUEBEC_MEDIAN[i] + SASKATCHEWAN_MEDIAN[i] +
                                   YUKON_MEDIAN[i]) / 13
    return canada_median_so_far


CANADA_MEDIAN = get_canada_median()

CANADA_CURVE = model_temp(CANADA_MEDIAN)
# Processed greenhouse gas emission data
EMISSION_DATA = read_csv_emission('other_data/emission.csv')
EMISSION_CURVE = model_emission(EMISSION_DATA)

# Processed deforestation data
DEFORESTATION_DATA = read_csv_deforestation('other_data/deforestation.csv')
DEFORESTATION_HYDRO = read_csv_deforestation_hydro('other_data/deforestation.csv')
DEFORESTATION_REST = {k: DEFORESTATION_DATA[k] - DEFORESTATION_HYDRO[k]
                      for k in DEFORESTATION_DATA}
DEFORESTATION_REST_CURVE = model_deforestation(DEFORESTATION_REST)


