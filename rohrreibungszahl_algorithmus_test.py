import math
import numpy as np
from scipy.optimize import fsolve

def gleichung_für_übergangsgebiet(lamda_, Re, rohrdurchmesser, rauhigkeitswert):
    return 1/np.sqrt(lamda_) + 2 * math.log10((2.51/(Re*np.sqrt(lamda_)) + (rauhigkeitswert/rohrdurchmesser) * 0.269))

def rohrreibungszahl_übergangsgebiet(Re, rohrdurchmesser, rauhigkeitswert):
    anfangswert = 0.01
    rohrreibungszahl = fsolve(gleichung_für_übergangsgebiet, anfangswert, args=(Re, rohrdurchmesser, rauhigkeitswert))
    return rohrreibungszahl[0]

def strömungsgeschwindigkeit_berechnen(volumenstrom, rohrdurchmesser):
    strömungsgeschwindigkeit = volumenstrom / (math.pi * pow((rohrdurchmesser / 2), 2))
    return strömungsgeschwindigkeit

def reynoldszahl_berechnen(strömungsgeschwindigkeit, rohrdurchmesser, viskositätDerFlüssigkeit):
    reynoldszahl = (strömungsgeschwindigkeit * rohrdurchmesser) / viskositätDerFlüssigkeit
    return reynoldszahl

def berechnung_druckverlust(rohrreibungszahl, rohrlänge, durchmesser, flüssigkeitsdichte, strömungsgeschwindigkeit):
    druckverlust = rohrreibungszahl * (rohrlänge/rohrdurchmesser) * (flüssigkeitsdichte/2) * pow(strömungsgeschwindigkeit, 2)
    return druckverlust

def pascal_in_bar(wert):
    wert_in_bar = wert / 100000
    return wert_in_bar

# Gegebene Werte
rohrdurchmesser = 0.5  # Meter
rauhigkeitswert = 0.0001  # Meter
rohrlänge = 2000  # Meter (wird in diesem Beispiel nicht verwendet)
dichte = 1000  # kg/m³ (wird in diesem Beispiel nicht verwendet)
zähigkeit = 0.00000113  # m²/s
volumenstrom = 0.333333  # m³/s

# Berechnungen
strömungsgeschwindigkeit = strömungsgeschwindigkeit_berechnen(volumenstrom, rohrdurchmesser)
reynoldszahl = reynoldszahl_berechnen(strömungsgeschwindigkeit, rohrdurchmesser, zähigkeit)

# Rohrreibungszahl berechnen
rohrreibungszahl = rohrreibungszahl_übergangsgebiet(reynoldszahl, rohrdurchmesser, rauhigkeitswert)
druckverlust = berechnung_druckverlust(rohrreibungszahl, rohrlänge, rohrdurchmesser, dichte, strömungsgeschwindigkeit)
druckverlust = pascal_in_bar(druckverlust)
print(f"Reynoldszahl: {reynoldszahl}")
print(f"Rohrreibungszahl: {rohrreibungszahl}")
print(f"Druckverlust: {druckverlust} bar")
