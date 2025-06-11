import pandas as pd

def calculate_sub_index(C, breakpoints):
    for bp in breakpoints:
        if bp['low'] <= C <= bp['high']:
            return ((bp['index_high'] - bp['index_low']) / (bp['high'] - bp['low'])) * (C - bp['low']) + bp['index_low']
    return None
def get_pollutant_breakpoints(pollutant):
    breakpoints = {
        'PM2.5': [
            {'low': 0, 'high': 30, 'index_low': 0, 'index_high': 50},
            {'low': 31, 'high': 60, 'index_low': 51, 'index_high': 100},
            {'low': 61, 'high': 90, 'index_low': 101, 'index_high': 200},
            {'low': 91, 'high': 120, 'index_low': 201, 'index_high': 300},
            {'low': 121, 'high': 250, 'index_low': 301, 'index_high': 400},
            {'low': 251, 'high': 500, 'index_low': 401, 'index_high': 500},
        ],
        'PM10': [
            {'low': 0, 'high': 50, 'index_low': 0, 'index_high': 50},
            {'low': 51, 'high': 100, 'index_low': 51, 'index_high': 100},
            {'low': 101, 'high': 250, 'index_low': 101, 'index_high': 200},
            {'low': 251, 'high': 350, 'index_low': 201, 'index_high': 300},
            {'low': 351, 'high': 430, 'index_low': 301, 'index_high': 400},
            {'low': 431, 'high': 600, 'index_low': 401, 'index_high': 500},
        ],
        'NO2': [
            {'low': 0, 'high': 40, 'index_low': 0, 'index_high': 50},
            {'low': 41, 'high': 80, 'index_low': 51, 'index_high': 100},
            {'low': 81, 'high': 180, 'index_low': 101, 'index_high': 200},
            {'low': 181, 'high': 280, 'index_low': 201, 'index_high': 300},
            {'low': 281, 'high': 400, 'index_low': 301, 'index_high': 400},
            {'low': 401, 'high': 1000, 'index_low': 401, 'index_high': 500},
        ],
        'SO2': [
            {'low': 0, 'high': 40, 'index_low': 0, 'index_high': 50},
            {'low': 41, 'high': 80, 'index_low': 51, 'index_high': 100},
            {'low': 81, 'high': 380, 'index_low': 101, 'index_high': 200},
            {'low': 381, 'high': 800, 'index_low': 201, 'index_high': 300},
            {'low': 801, 'high': 1600, 'index_low': 301, 'index_high': 400},
            {'low': 1601, 'high': 2000, 'index_low': 401, 'index_high': 500},
        ],
        'CO': [
            {'low': 0, 'high': 1.0, 'index_low': 0, 'index_high': 50},
            {'low': 1.1, 'high': 2.0, 'index_low': 51, 'index_high': 100},
            {'low': 2.1, 'high': 10.0, 'index_low': 101, 'index_high': 200},
            {'low': 10.1, 'high': 17.0, 'index_low': 201, 'index_high': 300},
            {'low': 17.1, 'high': 34.0, 'index_low': 301, 'index_high': 400},
            {'low': 34.1, 'high': 50.0, 'index_low': 401, 'index_high': 500},
        ],
        'O3': [
            {'low': 0, 'high': 50, 'index_low': 0, 'index_high': 50},
            {'low': 51, 'high': 100, 'index_low': 51, 'index_high': 100},
            {'low': 101, 'high': 168, 'index_low': 101, 'index_high': 200},
            {'low': 169, 'high': 208, 'index_low': 201, 'index_high': 300},
            {'low': 209, 'high': 748, 'index_low': 301, 'index_high': 400},
            {'low': 749, 'high': 1000, 'index_low': 401, 'index_high': 500},
        ],
    }
    return breakpoints.get(pollutant, [])

def calculate_overall_aqi(row):
    pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
    sub_indices = []
    for pollutant in pollutants:
        if pollutant in row and pd.notna(row[pollutant]):
            bp = get_pollutant_breakpoints(pollutant)
            index = calculate_sub_index(row[pollutant], bp)
            if index is not None:
                sub_indices.append(index)
    return max(sub_indices) if sub_indices else None