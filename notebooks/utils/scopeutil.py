import numpy as np
import pandas as pd

# Nu hoef je alleen ene constante aan te roepen om je tijd te krijgen
# Dan ben je minder kwetsbaar voor fouten
from matplotlib import pyplot as plt

STOF_KOPERCHLORIDE_A = "koper(ii)chloride_a H20"
STOF_KOPERCHLORIDE_B = "koper(ii)chloride_b H20"
STOF_ACETOON = "aceton H20"
STOF_KOPERCHLORIDE_ACETOON = "aceton koper(ii)chloride_a"

SI_PULSE = 1
SI_SIGNAL = 2

T1 = "T1"
T2 = "T2"

K_DELAY_INTERVALS = "K_DELAY_INTERVALS"
K_VERHOUDINGEN = "K_VERHOUDINGEN"
K_CONCENTRATION = "K_CONCENTRATION"

# Zo dadelijk willen we snel bestanden oproepen
# Helaas zijn we niet consistent geweest -> dus lijsten aanmaken die je telkens kan oproepen
METADATA = {
    STOF_KOPERCHLORIDE_A: {
        K_VERHOUDINGEN: ["1_0"],
        K_DELAY_INTERVALS: {
            T1: {
                "1_0": range(400, 850, 50),
            },
            T2: {
                "1_0": [880],
            },
        },
       K_CONCENTRATION: 1.0
    },
    STOF_KOPERCHLORIDE_B: {
        K_VERHOUDINGEN: ["1_0", "1_1"],
        K_DELAY_INTERVALS: {
            T1: {
                "1_0": range(430, 590, 20),
                "1_1": range(420, 670, 50),
            },
            T2: {
                "1_0": [950, 1000],
                "1_1": [920, 970],
            },
        },
        K_CONCENTRATION: 1.0 # TODO this is wrong!
    },
    STOF_ACETOON: {
        K_VERHOUDINGEN: ["1_0"],
        K_DELAY_INTERVALS: {
            T1: {
                "1_0": range(370, 640, 30),
            },
            T2: {
                "1_0": range(770, 2770, 200),
            },
        },
        K_CONCENTRATION: 1.0 # TODO what is it?
    },
    STOF_KOPERCHLORIDE_ACETOON: {
        K_VERHOUDINGEN: ["1_1"],
        K_DELAY_INTERVALS: {
            T1: {
                "1_1": range(400, 3150, 250),
            },
            T2: {
                "1_1": range(800, 1350, 50),
            },
        },
        K_CONCENTRATION: 1.0 # TODO what is it?
    },
}


def df_for_csv(path):
    """
    Leest een csv bestand op en zet het om in een dataframe.

    :param path: het pad van de csv bestand om te lezen
    :return: een dataframe
    """
    df = pd.read_csv(path, skiprows=20)
    df = df.iloc[:, [3, 4]]
    df.columns = ["x", "y"]
    return df


def get_verhoudingen(stof):
    """
    Haalt de mogelijke verhoudingen op voor de specifieke stof.

    :param stof: een van STOF_KOPERCHLORIDE, STOF_ACETOON of STOF_KOPERCHLORIDE_ACETOON
    :return: een lijst van verhoudingen
    """
    return METADATA[stof][K_VERHOUDINGEN]


def get_delays(stof, verhouding, T):
    """
    Haalt de mogelijke delays op voor de specifieke stof, verhouding, T meting.

    :param stof: een van STOF_KOPERCHLORIDE, STOF_ACETOON of STOF_KOPERCHLORIDE_ACETOON
    :param verhouding: bijvoorbeeld "1_4", zie functie get_delays()
    :param T: een van T1 of T2
    :return: een lijst van delays
    """
    return METADATA[stof][K_DELAY_INTERVALS][T][verhouding]


def get_df(stof, verhouding, T, delay, signal_index, v=False):
    """
    Haalt de dataframe op volgens de parameters die jij meegeeft.

    Bijvoorbeeld:

    df_CuCl_1_16_T2_300us_signal = get_df(STOF_KOPERCHLORIDE, "1_16", T2, 300, SI_SIGNAL)
    df_CuCl_1_16_T2_300us_signal.plot()

    :param stof: een van STOF_KOPERCHLORIDE, STOF_ACETOON of STOF_KOPERCHLORIDE_ACETOON
    :param verhouding: bijvoorbeeld "1_4", zie functie get_delays()
    :param T: een van T1 of T2
    :param delay: een delay waarde, haal ze op met de functie get_delays()
    :param signal_index: een van SI_SIGNAL of SI_PULSE
    :param v: verbose. Stel v=True als je extra prints() wilt krijgen om makkelijk fouten te kunnen opsporen.
    :return: een dataframe
    """
    filepath = filepath_for_measurement_params(stof, verhouding, T, delay, signal_index)
    if v:
        print(filepath)
    return df_for_csv(filepath)


def get_df_of_all_delays(stof, verhouding, T, signal_index, v=False):
    """
    Haalt de dataframes op van alle delays.

    Kun je gebruiken om bijvoorbeeld de hele reeks metingen in een klap op te halen:

    meetreeks_CuCl_1_4_T1_signal = get_df_of_all_delays(STOF_KOPERCHLORIDE, "1_4", T1, SI_SIGNAL)
    for (delay, df) in meetreeks_CuCl_1_4_T1_signal:
        df.plot(title=f"Plot van meting op t={delay}us")

    :param stof: een van STOF_KOPERCHLORIDE, STOF_ACETOON of STOF_KOPERCHLORIDE_ACETOON
    :param verhouding: bijvoorbeeld "1_4", zie functie get_delays()
    :param T: een van T1 of T2
    :param signal_index: een van SI_SIGNAL of SI_PULSE
    :param v: verbose. Stel v=True als je extra prints() wilt krijgen om makkelijk fouten te kunnen opsporen.
    :return: een lijst van (delay, dataframe) tuples
    """
    delays = get_delays(stof, verhouding, T)
    if v:
        print(delays)
    return [
        (delay, get_df(stof, verhouding, T, delay, signal_index, v)) for delay in delays
    ]


def filepath_for_measurement_params(stof, verhouding, T, delay, signal_index):
    """
    Geeft je filepath (op je hardeschijf) waar de csv hoort te staan.
    Remember dat koper(ii)chloride veelal wordt aangegeven als cucl

    :param stof: stof is een van de STOF_ constantes. Bijvoorbeeld STOF_KOPERCHLORIDE
    :param verhouding: verhouding is 1 of 'parameter'
    :param T: T is T1 of T2
    :param delay: delay is waar je begon - meestal 400
    :param signal_index: signal index is welke channel je hebt
    :return: pad waar csv hoort te staan
    """
    return f"../data/{verhouding} {stof}/{T}/delay{delay}u00{signal_index}.csv"


def My_for_T1_df(df, v=False):
    x = list(df['x'])
    y = list(df['y'])

    i_x_y_pairs = [(i, x[i], y[i]) for i in range(0, len(df))]

    max_y = np.max(y)
    i_values_at_near_max_y = [i for (i, x, y) in i_x_y_pairs if y > 0.8 * max_y]

    i_of_end_of_last_peak = i_values_at_near_max_y[len(i_values_at_near_max_y) - 1]

    READ_LEFT_OFFSET_START = round(0.03 * len(i_x_y_pairs)) + i_of_end_of_last_peak
    READ_LEFT_OFFSET_END = READ_LEFT_OFFSET_START + round(0.01 * len(i_x_y_pairs))

    if v:
        plt.plot([x for (i, x, y) in i_x_y_pairs], [y for (i, x, y) in i_x_y_pairs])
        plt.vlines([i_x_y_pairs[READ_LEFT_OFFSET_START][1],
                    i_x_y_pairs[READ_LEFT_OFFSET_END][1]],
                   ymin=0,
                   ymax=max_y,
                   colors="k")
        plt.show()

    sample = i_x_y_pairs[READ_LEFT_OFFSET_START:READ_LEFT_OFFSET_END]

    return np.average([y for (i, x, y) in sample])


def My_for_T2_df(df, v=False):
    x = list(df['x'])
    y = list(df['y'])

    i_x_y_pairs = [(i, x[i], y[i]) for i in range(0, len(df))]

    max_y = np.max(y)
    i_x_y_pairs_at_near_max_y = [(i, x, y) for (i, x, y) in i_x_y_pairs if y > 0.8 * max_y]
    i_values_at_near_max_y = [i for (i, x, y) in i_x_y_pairs_at_near_max_y]

    first_x = i_x_y_pairs_at_near_max_y[0][1]
    last_x = first_x
    i_of_end_of_first_peak = -1
    for (i, x, y) in i_x_y_pairs:
        if i not in i_values_at_near_max_y:
            continue
        if abs(x - last_x) < first_x / 3:
            continue
        i_of_end_of_first_peak = i
        break

    i_of_end_of_last_peak = i_values_at_near_max_y[len(i_values_at_near_max_y) - 1]

    # TODO calculate PI length
    # PI_I_LENGTH = i_at_end_of_first_peak - i_values_at_near_max_y[0]
    PI_I_LENGTH = 40

    if v:
        print(f"PI I length: {PI_I_LENGTH}")

    i_of_end_of_first_peak += round(PI_I_LENGTH / 2)
    i_of_end_of_last_peak -= PI_I_LENGTH

    if v:
        plt.plot([x for (i, x, y) in i_x_y_pairs], [y for (i, x, y) in i_x_y_pairs])
        plt.vlines([i_x_y_pairs[i_of_end_of_first_peak][1],
                    i_x_y_pairs[i_of_end_of_last_peak][1]],
                   ymin=0,
                   ymax=max_y,
                   colors="g")

    DELAY = i_of_end_of_last_peak - i_of_end_of_first_peak
    READ_LEFT_OFFSET_START = i_of_end_of_last_peak + DELAY + PI_I_LENGTH - round(0.005 * len(i_x_y_pairs))
    READ_LEFT_OFFSET_END = READ_LEFT_OFFSET_START + round(0.01 * len(i_x_y_pairs))

    if READ_LEFT_OFFSET_START > len(i_x_y_pairs):
        print("ERROR! DATAPUNT IS ONGELDIG GEMAAKT")
        return -1

    if v:
        plt.plot([x for (i, x, y) in i_x_y_pairs], [y for (i, x, y) in i_x_y_pairs])
        plt.vlines([i_x_y_pairs[READ_LEFT_OFFSET_START][1],
                    i_x_y_pairs[READ_LEFT_OFFSET_END][1]],
                   ymin=0,
                   ymax=max_y,
                   colors="k")
        plt.show()

    sample = i_x_y_pairs[READ_LEFT_OFFSET_START:READ_LEFT_OFFSET_END]

    return np.average([y for (i, x, y) in sample])


def voltage_uncertainty_due_to_noise(v=False):
    df = get_df(STOF_KOPERCHLORIDE_ACETOON, "1_1", T1, 400, SI_SIGNAL)

    x = list(df['x'])
    y = list(df['y'])

    i_x_y_pairs = [(i, x[i], y[i]) for i in range(round(len(df) / 4), len(df))]

    if v:
        plt.plot([x for (i, x, y) in i_x_y_pairs], [y for (i, x, y) in i_x_y_pairs])

    noise = [y for (i, x, y) in i_x_y_pairs]
    return np.sqrt(np.mean(np.square(noise)))


def T_uncertainty_for_stof(stof):
    concentration = METADATA[stof][K_CONCENTRATION] # mol per liter
    concentration *= 1000 # mol per cubic centimeter
    concentration_error = concentration * 0.3 # 30% error
    return 1 / concentration_error # T is inversely proportional to N
