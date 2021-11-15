import pandas as pd

# Nu hoef je alleen ene constante aan te roepen om je tijd te krijgen
# Dan ben je minder kwetsbaar voor fouten
STOF_KOPERCHLORIDE = "koper(ii)chloride"
STOF_ACETOON = ""
STOF_KOPERCHLORIDE_ACETOON = ""

SI_PULSE = 1
SI_SIGNAL = 2

T1 = "T1"
T2 = "T2"

K_DELAY_INTERVALS = "K_DELAY_INTERVALS"
K_VERHOUDINGEN = "K_VERHOUDINGEN"

# Zo dadelijk willen we snel bestanden oproepen
# Helaas zijn we niet consistent geweest -> dus lijsten aanmaken die je telkens kan oproepen
METADATA = {
    STOF_KOPERCHLORIDE: {
        K_VERHOUDINGEN: ["1_1", "1_2", "1_4", "1_16"],
        K_DELAY_INTERVALS: {
            T1: {
                "1_1": [400, 420, 440, 460, 480, 520],
                "1_2": [400, 450, 500, 550, 600, 650, 700],
                "1_4": [400, 450, 500, 550, 600, 650, 700],
                "1_16": [400, 410, 420, 450] # Deze meting was niet optimaal/realistisch
            },
            T2: {
                "1_1": [400, 450, 500, 550, 600, 650, 700, 750, 800],
                "1_2": [400, 450, 500, 550, 600, 650, 700, 750, 800, 900],
                "1_4": [400, 450, 500, 550, 600, 650, 700, 750, 950],
                "1_16": [400, 450, 500, 550, 600, 650, 700, 900]
            }
        }
    }
}


def df_for_csv(path):
    df = pd.read_csv(path, skiprows=20)
    df = df.iloc[:, [3, 4]]
    df.columns = ["x", "y"]
    return df


def get_verhoudingen(stof):
    return METADATA[stof][K_VERHOUDINGEN]


def get_delays(stof, verhouding, T):
    return METADATA[stof][K_DELAY_INTERVALS][T][verhouding]


def get_df(stof, verhouding, T, delay, signal_index, v=False):
    filepath = filepath_for_measurement_params(stof, verhouding, T, delay, signal_index)
    if v:
        print(filepath)
    return df_for_csv(filepath)


def get_df_of_all_delays(stof, verhouding, T, signal_index, v=False):
    delays = get_delays(stof, verhouding, T)
    if v:
        print(delays)
    return [get_df(stof, verhouding, T, delay, signal_index, v) for delay in delays]


def filepath_for_measurement_params(stof, verhouding, T, delay, signal_index):
    """
    remember dat koper(ii)chloride veelal wordt aangegeven als cucl
    :param stof: stof is een van de STOF_ constantes. Bijvoorbeeld STOF_KOPERCHLORIDE
    :param verhouding: verhouding is 1 of 'parameter'
    :param T: T is T1 of T2
    :param delay: delay is waar je begon - meestal 400
    :param signal_index: signal index is welke channel je hebt
    :return:
    """
    return f"../data/cucl/verhouding {verhouding} {stof}/{T}/delay{delay}u00{signal_index}.csv"

