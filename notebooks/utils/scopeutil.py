import pandas as pd


def df_for_csv(path):
    df = pd.read_csv(path, skiprows=20)
    df = df.iloc[:, [3, 4]]
    df.columns = ["x", "y"]
    return df


def filepath_for_measurement_params(verhouding, tijd, delay, signal_index):
    return f"../data/cucl/verhouding 1_{verhouding} koper(ii)chloride/T{tijd}/delay{delay}u00{signal_index}.csv"

    # remember dat koper(ii)chloride veelal wordt aangegeven als cucl
    # verhouding is 1 of 'parameter'
    # tijd is T1 of T2
    # delay is waar je begon - meestal 400
    # signal index is welke channel je hebt
