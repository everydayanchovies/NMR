# Hierbij enkele functies waarmee het mogelijk is om de data aan te fitten
import numpy as np
import math
from lmfit import models
from numpy import log as ln

# lambda functie waaraan je kan fitten
# Dit is de gelineariseerde versie van de gegeven formule in de handleiding
f = lambda t, M0, T1: M0 * (1 - 2 * np.exp(-t / T1))

model_T1 = models.Model(f)

# t = delays
# magnetisatie_z = gemiddelde piek
# evenwichtsmagnetisatie = pi/2 puls
# (want dan kijk je naar hoe groot je vector is als je geen extra veld hebt)
