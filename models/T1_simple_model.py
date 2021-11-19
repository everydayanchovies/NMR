# Hierbij enkele functies waarmee het mogelijk is om de data aan te fitten
import numpy as np
import math
from lmfit import models

# lambda functie waaraan je kan fitten
# Dit is de gelineariseerde versie van de gegeven formule in de handleiding
f = lambda evenwichtsmagnetisatie, magnetisatie_z, t: t / (
    -1 * np.ln(1 - ((magnetisatie_z / evenwichtsmagnetisatie)))
)

model_T1 = models.model(f)

# t = delays
# magnetisatie_z = gemiddelde piek
# evenwichtsmagnetisatie = pi/2 puls
# (want dan kijk je naar hoe groot je vector is als je geen extra veld hebt)
