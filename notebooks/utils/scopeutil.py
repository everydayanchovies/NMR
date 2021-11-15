import pandas as pd

# Nu hoef je alleen ene constante aan te roepen om je tijd te krijgen
# Dan ben je minder kwetsbaar voor fouten
STOF_KOPERCHLORIDE = "koper(ii)chloride"
STOF_ACETOON = "nog om in te vullen (STOF_ACETOON)"
STOF_KOPERCHLORIDE_ACETOON = "nog om in te vullen (STOF_KOPERCHLORIDE_ACETOON)"

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
    },
    STOF_ACETOON: {
        K_VERHOUDINGEN: ["1_1", "1_2"],
        K_DELAY_INTERVALS: {
            T1: {
                "1_1": [],
                "1_2": [],
            },
            T2: {
                "1_1": [],
                "1_2": [],
            }
        }
    },
    STOF_KOPERCHLORIDE_ACETOON: {
        K_VERHOUDINGEN: ["1_1", "1_2"],
        K_DELAY_INTERVALS: {
            T1: {
                "1_1": [],
                "1_2": [],
            },
            T2: {
                "1_1": [],
                "1_2": [],
            }
        }
    }
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
    return [(delay, get_df(stof, verhouding, T, delay, signal_index, v)) for delay in delays]


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
    return f"../data/verhouding {verhouding} {stof}/{T}/delay{delay}u00{signal_index}.csv"

