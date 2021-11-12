import pandas as pd


def df_for_csv(path):
    df = pd.read_csv(path, skiprows=20)
    df = df.iloc[:, [3, 4]]
    df.columns = ['x', 'y']
    return df


def filepath_for_measurement_params(delay, signal_index):
    return f"../data/T2/delay{delay}u00{signal_index}.csv"
