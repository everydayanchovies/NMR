# Hierbij enkele functies waarmee het mogelijk is om de data aan te fitten
import numpy as np
import math
from lmfit import models
from numpy import log as ln

# lambda functie waaraan je kan fitten
# Dit is de gelineariseerde versie van de gegeven formule in de handleiding
f = lambda t, evenwichtsmagnetisatie, magnetisatie_z: t / (
    -1 * ln(1 - ((magnetisatie_z / evenwichtsmagnetisatie)))
)

model_eerstetijd = models.Model(f)

test = lambda t, M0, T1: M0 * (1 - 2 * np.exp(-1 * (t / T1)))

model_test = models.Model(test)

# t = delays
# magnetisatie_z = gemiddelde piek
# evenwichtsmagnetisatie = pi/2 puls
# (want dan kijk je naar hoe groot je vector is als je geen extra veld hebt)
