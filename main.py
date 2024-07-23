import math
import numpy as np
from scipy.optimize import fsolve

def strömungsgeschwindigkeit_berechnen(volumenstrom, rohrdurchmesser):
    strömungsgeschwindigkeit = volumenstrom / (math.pi * pow((rohrdurchmesser / 2), 2))
    return strömungsgeschwindigkeit
def reynoldszahl_berechnen(strömungsgeschwindigkeit, rohrdurchmesser, viskositätDerFlüssigkeit):
    reynoldszahl = (strömungsgeschwindigkeit * rohrdurchmesser) / viskositätDerFlüssigkeit
    return reynoldszahl

def rohrreibungs_zahl_laminare_strömung(reynoldszahl):
    rohrreibungszahl = 64/reynoldszahl
    return rohrreibungszahl


def berechnung_druckverlust(rohrreibungszahl, rohrlänge, durchmesser, flüssigkeitsdichte, strömungsgeschwindigkeit):
    druckverlust = rohrreibungszahl * (rohrlänge/rohrdurchmesser) * (flüssigkeitsdichte/2) * pow(strömungsgeschwindigkeit, 2)
    return druckverlust

def gleichung_für_glatte_rohre(lamda_, Re):
    return 1 / np.sqrt(lamda_) - 2 * np.log10(Re * np.sqrt(lamda_)) + 0.8
def rohrreibungszahl_glatte_rohre(Re):
    anfangswert = 0.02
    rohrreibungszahl = fsolve(gleichung_für_glatte_rohre(), anfangswert, args=(Re))
    return rohrreibungszahl

def gleichung_für_übergangsgebiet(lamda_, Re, rohrdurchmessser, rauhigkeitswert):
    return 1/np.sqrt(lamda_) + 2 * log10(2,51/(Re*np.sqrt(lamda_)) + rauhigkeitswert/rohrdurchmesser * 0.269)

def rohrreibungszahl_übergangsgebiet(Re, rohrdurchmesser, rauhigkeitswert):
    anfangswert = 0.01
    rohrreibungszahl = fsolve(gleichung_für_übergangsgebiet, anfangswert, args=(Re, rohrdurchmesser, rauhigkeitswert) )
    return rohrreibungszahl[0]

def rohrreibungszahl_für_raue_rohre(rohrdurchmesser, rauhigkeitswert):
    rohrreibungszahl = 1/pow((2* log10(3.71*(rohrdurchmesser/rauhigkeitswert))),2)
    return rohrreibungszahl

def pascal_in_bar(wert):
    wert_in_bar = wert / 100000
    return wert_in_bar



end = False

while end == False:

    print("Was möchten Sie machen?")
    print("0 - Programm beenden")
    print("1 - Berechnung von Stoffströmen in geschlossenen Rohrleitungen")
    selection = input()

    match selection:
        case "0":
            break
        case "1":
            rohrdurchmesser = float(input("Bitte geben Sie die den Rohrdurchmesser (in m) ein: "))
            rohrlänge = float(input("Bitte geben Sie die Rohrlänge(in m) ein: "))
            flüssigkeitsdichte = float(input("Bitte geben Sie die Dichte der Flüssigkeit (in kg/m^3) ein: "))
            viskositätDerFlüssigkeit = float(input("Bitte geben Sie die Viskosität(in m^2/s) ein: "))
            volumenstrom = float(input("Bitte geben Sie den Volumenstrom ein (in m^3/s: "))

            strömungsgeschwindigkeit = strömungsgeschwindigkeit_berechnen(volumenstrom, rohrdurchmesser)
            print (strömungsgeschwindigkeit)
            reynoldszahl = reynoldszahl_berechnen(strömungsgeschwindigkeit, rohrdurchmesser, viskositätDerFlüssigkeit)
            print(reynoldszahl)
            if(reynoldszahl <= 2320):
                rohrreibungszahl = rohrreibungs_zahl_laminare_strömung(reynoldszahl)
            else:
                rauhigkeitswert = float(input("Bitte geben Sie den Rauhigkeitswert(in m) ein: "))
                if(reynoldszahl * (rauhigkeitswert/rohrdurchmesser) < 65):
                    if(2320 < reynoldszahl < pow(10, 5)):
                        rohrreibungszahl = 0.3164 * pow(reynoldszahl, -0.25)
                    elif(pow(10,5 ) < reynoldszahl < 5*(pow(10, 6))):
                        rohrreibungszahl = 0.0032 + 0,221 * pow(reynoldszahl, -0.237)
                    elif(5*(pow(10, 6)) < reynoldszahl):
                        rohrreibungszahl = rohrreibungszahl_glatte_rohre()
                elif(65 < reynoldszahl * (rauhigkeitswert/rohrdurchmesser) < 1300):
                    rohrreibungszahl_übergangsgebiet(reynoldszahl, rohrdurchmesser, rauhigkeitswert)
                else:
                    rohrreibungszahl_für_raue_rohre(rohrdurchmesser, rauhigkeitswert)

            druckverlust = berechnung_druckverlust(rohrreibungszahl, rohrlänge, rohrdurchmesser, flüssigkeitsdichte,
                                                   strömungsgeschwindigkeit)
            druckverlust = pascal_in_bar(druckverlust)
            print("Die Rohrreibungszahl beträgt: " + str(rohrreibungszahl))
            print("Der Druckverlust beträgt " + str(druckverlust) + " bar")




