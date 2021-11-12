import pandas as pd


def xy_for_scope_csv(path):
    df = pd.read_csv(path, skiprows=20)
    df = df.iloc[:, [3, 4]]
    df.columns = ['x', 'y']
    return df


def path_for_measurement_params(delay, signal_index):
    return f"../data/T2/delay{delay}u00{signal_index}.csv"
