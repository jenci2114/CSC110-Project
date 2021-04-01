"""CSC110 Fall 2020 Project

Description
===============================

This Python module is responsible for running the simulation game
that utilizes modules 'process_data.py' and 'game.py'. Run
this file to start the simulation game.

Copyright Information
===============================

This file is Copyright (c) 2020 Caules Ge, Jenci Wei, Zheng Luan
"""
from game import *

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

CANADA_MEDIAN = {}
for i in range(1991, 2020):
    CANADA_MEDIAN[i] = (ALBERTA_MEDIAN[i] + BRITISH_COLUMBIA_MEDIAN[i] +
                        MANITOBA_MEDIAN[i] + NEW_BRUNSWICK_MEDIAN[i] +
                        NEWFOUNDLAND_MEDIAN[i] + NORTHWEST_MEDIAN[i] +
                        NOVA_SCOTIA_MEDIAN[i] + NUNAVUT_MEDIAN[i] +
                        ONTARIO_MEDIAN[i] + PRINCE_EDWARD_MEDIAN[i] +
                        QUEBEC_MEDIAN[i] + SASKATCHEWAN_MEDIAN[i] +
                        YUKON_MEDIAN[i]) / 13

# Processed greenhouse gas emission data
EMISSION_DATA = read_csv_emission('other_data/emission.csv')
EMISSION_CURVE = model_emission(EMISSION_DATA)

# Processed deforestation data
DEFORESTATION_DATA = read_csv_deforestation('other_data/deforestation.csv')
DEFORESTATION_HYDRO = read_csv_deforestation_hydro('other_data/deforestation.csv')
DEFORESTATION_REST = {k: DEFORESTATION_DATA[k] - DEFORESTATION_HYDRO[k]
                      for k in DEFORESTATION_DATA}
DEFORESTATION_REST_CURVE = model_deforestation(DEFORESTATION_REST)

# Processed correlation data
TEMP_CHANGE = {k: CANADA_MEDIAN[k + 1] - CANADA_MEDIAN[k] for k in CANADA_MEDIAN
               if k in range(1991, 2018)}
FINAL_DATA = (
    [TEMP_CHANGE[k] for k in TEMP_CHANGE if k in range(1991, 2018)],
    [EMISSION_DATA[k] for k in EMISSION_DATA if k in range(1991, 2018)],
    [DEFORESTATION_DATA[k] for k in DEFORESTATION_DATA if k in range(1991, 2018)]
)
FINAL_CORRELATION = model_correlation(FINAL_DATA)

# Run the simulation game
if __name__ == '__main__':
    game = TemperatureGame(EMISSION_CURVE, DEFORESTATION_REST_CURVE, FINAL_CORRELATION, 14)
    game.run()
