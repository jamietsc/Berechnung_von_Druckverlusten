import tkinter.ttk
from tkinter import *
from tkinter import messagebox
import math
from scipy.optimize import fsolve
import numpy as np


"""
Begonnen wird mit dem lesen der eingegeben Werte.
Danach werden diese Werte auf richtigkeit (kommafehler, buchstaben, etc.) überprüft.
Mit diesen Werten wird nun die Reynoldszahl berechnet.
MIthilfe der Reynoldszahl wird der richtige Fall für die Rohrreibungszahl gesucht. 
Wenn der richtige Fall gefunden wurde wird die Rohrreibungszahl berechnet.
Mit dieser wird dann der Druckverlust berechnet.
Als letztes werden nun die Rohrreibungszahl und der Druckverlust im Label ausgegeben.
"""


def berechnen():
    max_vstrom_testfall2 = 0
    """
    test zum verkürzen des codes
    entrys = ["rohrdurchmesser_entry", "rohrlänge_entry", "dichte_entry", "zähigkeit_entry", "volumenstrom_entry"
              , "rauhigkeitswert_entry"]

    variablen = ["rohrdurchmesser", "rohrlänge", "dichte", "zähigkeit", "volumenstrom", "rauhigkeit"]

    for i in range(len(entrys)):
        try:
            variablen[i] = float(entrys[i].get())
        except:
            messagebox.showinfo("Achtung", "Es wurde kein Werte bzgl. " + variablen[i] + " gefunden")
    """

    try:
        rohrdurchmesser = float(rohrdurchmesser_entry.get())
        if (rohrdurchmesser_einheiten.get() != "m"):
            rohrdurchmesser = in_meter_umrechnen(rohrdurchmesser, rohrdurchmesser_einheiten.get())
    except:
        messagebox.showinfo("Achtung", "Es konnte kein Wert für den Rohrdurchmesser gefunden werden")
        return 0

    try:
        rohrlänge = float(rohrlänge_entry.get())
        if (rohrlänge_einheiten.get() != "m"):
            rohrlänge = in_meter_umrechnen(rohrlänge, rohrlänge_einheiten.get())
    except:
        messagebox.showinfo("Achtung", "Es konnte kein Wert für die Rohrlänge gefunden werden")
        return 0

    try:
        dichte = float(dichte_entry.get())
        if (dichte_einheiten.get() != "kg/m³"):
            dichte = dichte_in_Einheit_umrechnen(dichte, dichte_einheiten.get())
    except:
        messagebox.showinfo("Achtung", "Es konnte leider kein Wert für die Dichte gefunden werden")
        return 0

    try:
        zähigkeit = float(zähigkeit_entry.get())
    except:
        messagebox.showinfo("Achtung", "Es konnte kein Wert für die Zähigkeit gefunden werden")
        return 0

    try:
        volumenstrom = float(volumenstrom_entry.get())
        if (volumenstrom_einheiten.get() != "m³/sec"):
            volumenstrom = volumenstrom_in_einheit_umrechnen(volumenstrom, volumenstrom_einheiten.get())
    except:
        messagebox.showinfo("Achtung", "Es konnte kein Wert für den Volumenstrom gefunden werden")
        return 0

    strömungsgeschwindigkeit = strömungsgeschwindigkeit_berechnen(volumenstrom, rohrdurchmesser)
    reynoldszahl = reynoldszahl_berechnen(strömungsgeschwindigkeit, rohrdurchmesser, zähigkeit)
    print(str(reynoldszahl) + "RE")
    print(str(strömungsgeschwindigkeit) + "Strömungsgeschwindigkeit")

    if (reynoldszahl <= 2320):
        rohrreibungszahl = rohrreibungs_zahl_laminare_strömung(reynoldszahl)
    else:
        try:
            rauhigkeitswert = float(rauhigkeitswert_entry.get())
            if (rauhigkeitswert_einheiten.get() != "m"):
                rauhigkeitswert = in_meter_umrechnen(rauhigkeitswert, rauhigkeitswert_einheiten.get())
        except:
            messagebox.showinfo("Achtung", "Bitte geben Sie noch ein Wert für die Rauhigkeit ein")
        if (reynoldszahl * (rauhigkeitswert / rohrdurchmesser) < 65):
            if (2320 < reynoldszahl < pow(10, 5)):
                rohrreibungszahl = 0.3164 * pow(reynoldszahl, -0.25)
            elif (pow(10, 5) < reynoldszahl < 5 * (pow(10, 6))):
                rohrreibungszahl = 0.0032 + 0.221 * pow(reynoldszahl, -0.237)

            elif (5 * (pow(10, 6)) < reynoldszahl):
                rohrreibungszahl = rohrreibungszahl_glatte_rohre()
        elif (65 < reynoldszahl * (rauhigkeitswert / rohrdurchmesser) < 1300):
            rohrreibungszahl = rohrreibungszahl_übergangsgebiet(reynoldszahl, rohrdurchmesser, rauhigkeitswert)
            max_vstrom_testfall2 = maximaler_volumenstrom(rohrreibungszahl, rohrlänge, rohrdurchmesser, dichte)
        else:
            rohrreibungszahl_für_raue_rohre(rohrdurchmesser, rauhigkeitswert)


    druckverlust = berechnung_druckverlust(rohrreibungszahl, rohrlänge, rohrdurchmesser, dichte,
                                           strömungsgeschwindigkeit)
    druckverlust = pascal_in_bar(druckverlust)



    if(max_vstrom_testfall2 == 0):
        ergebnis_label.config(
            text="Die Rohrreibungszahl beträgt: " + str(rohrreibungszahl) + ".\nDer Druckverlust beträgt: " + str(
                druckverlust) + " bar.")
    else:
        ergebnis_label.config(
            text="Die Rohrreibungszahl beträgt: " + str(rohrreibungszahl) + ".\nDer Druckverlust beträgt: " + str(
                druckverlust) + f" bar. \nDer Volumenenstrom darf maximal um ${max_vstrom_testfall2}% erhöht werden,\ndamit ein Druckverlust von mehr als einem Bar nicht überschritten wird.")

"""
In dieser Funktion wird der wert auf die normale EInheit umgerechnet
@:param wert den wert der eingegeben Variabel
@:param aktuelle_einheit ist die aktuelle Einheit welche ausgewählt wurde
@:returns wert in der normalen Einheiten
"""


def in_meter_umrechnen(wert, aktuelle_einheit):
    if (aktuelle_einheit == "mm"):
        return wert / 1000
    elif (aktuelle_einheit == "cm"):
        return wert / 100
    elif (aktuelle_einheit == "dm"):
       return wert / 10
    elif (aktuelle_einheit == "km"):
        return wert * 1000

"""
In dieser Funktion wird die dichte in die normale Einheit umgerechnet 
@:param dichte die dichte der eingegeben Variabel
@:param aktuelle_einheit ist die aktuelle Einheit welche ausgewählt wurde
@:returns den wert der dichte in der normalen Einheit
"""


def dichte_in_Einheit_umrechnen(dichte, aktuelle_einheit):
    if(aktuelle_einheit == "g/cm³"):
        return dichte * 1000
    elif (aktuelle_einheit == "g/ml"):
        return dichte * 1000
    elif(aktuelle_einheit == "kg/l"):
        return dichte * 1000


"""
In dieser Funktion wird der Volumenstrom in die normale Einheit umgerechnet 
@:param volumenstrom den wert des aktuell eingegeben Volumenstroms
@:param aktuelle_einheit ist die aktuelle Einheit welche ausgewählt wurde
@:returns volumenstrom in der normalen Einheit
"""


def volumenstrom_in_einheit_umrechnen(volumenstrom, aktuelle_einheit):
    if(aktuelle_einheit == "m³/h"):
        return ((volumenstrom / 60) / 60)


"""
In dieser Funktion wird die Strömungsgeschwindkeit berechnet.
@:param volumenstrom der volumenstrom welche eingegeben wurde
@:param der rohrdurchmesser welcher eingeben wurde
@:returns strömungsgeschwindigkeit
"""


def strömungsgeschwindigkeit_berechnen(volumenstrom, rohrdurchmesser):
    strömungsgeschwindigkeit = volumenstrom / (math.pi * pow((rohrdurchmesser / 2), 2))
    return strömungsgeschwindigkeit


"""
Berechnet die Reynoldszahl.
@:param strömungsgeschwindigkeit ist die ausgerechnete Strömungsgeschwindigkeit
@:param rohrdurchmesser ist der eingegebene Rohrdurchmesser
@:param zähigkeit ist die eingegeben Viskosität
@:returns reynoldszahl
"""


def reynoldszahl_berechnen(strömungsgeschwindigkeit, rohrdurchmesser, zähigkeit):
    reynoldszahl = (strömungsgeschwindigkeit * rohrdurchmesser) / zähigkeit
    return reynoldszahl


"""
In dieser Funktion wird die Rohrreibungszahl für laminare Strömungen berechnet. 
@:param reynoldszahl
@:returns rohrreibungszahl
"""


def rohrreibungs_zahl_laminare_strömung(reynoldszahl):
    rohrreibungszahl = 64 / reynoldszahl
    return rohrreibungszahl


"""
Funktion zum Berechnen des Druckverlustes
@:param rohrreibungszahl die eingegeben rohrreibungszahl
@:param rohrlänge die eingegeben rohrlänge
@:param rohrdurchmesser ist der eingegeben Rohrdurchmesser
@:param dichte ist die eingegeben dichte
@:param strömungsgeschwindigkeit ist die berechnete strömungsgeschwindigkeit
@:returns druckverlust
"""


def berechnung_druckverlust(rohrreibungszahl, rohrlänge, rohrdurchmesser, dichte, strömungsgeschwindigkeit):
    druckverlust = rohrreibungszahl * (rohrlänge / rohrdurchmesser) * (dichte / 2) * pow(strömungsgeschwindigkeit, 2)
    return druckverlust


"""
In dieser Funktion ist die Gleichung zum berechnen der Rohrreibungszahl für glatte Rohre.
@:param lamda_ der anfangswert für lamda
@:param Re die berechnete Reynoldszahl
@:returns ergebnis der umgestellten Gleichung
"""


def gleichung_für_glatte_rohre(lamda_, Re):
    return 1 / np.sqrt(lamda_) - 2 * np.log10(Re * np.sqrt(lamda_)) + 0.8


"""
In dieser Funktion wird die Rohrreibungszahl für glatte Rohre mithilfe der Gleichung berechnet
@:param Re die berechnete Reynoldszahl
@:returns rohrreibungszahl 
"""


def rohrreibungszahl_glatte_rohre(Re):
    anfangswert = 0.02
    rohrreibungszahl = fsolve(gleichung_für_glatte_rohre(), anfangswert, args=(Re))
    return rohrreibungszahl


"""
Diese Funktion ist die Gleichung zur annäherung der Rohrreibungszahl für das Übergangsgebiet
@:param lamda_ annäherungswert für lamda
@:param Re die berechnete Reynoldszaghl
@:param rohrdurchmesser der eingegeben Rohrdurchmesser
@:param rauhigkeitswert der eingegeben wurde
@:returns annährungswert für die rohrreibungszahl 
"""


def gleichung_für_übergangsgebiet(lamda_, Re, rohrdurchmesser, rauhigkeitswert):
    lamda_ = lamda_[0]
    return 1 / np.sqrt(lamda_) + 2 * math.log10(
        (2.51 / (Re * np.sqrt(lamda_)) + (rauhigkeitswert / rohrdurchmesser) * 0.269))


"""
In dieser Funktion wird ein annäherungswert für die Rohrreibungszahl für das Übergangsgebiet berechnet.
@:param Re ist die berechnete Reynoldszahl
@:param rohrdurchmesser ist der eingegebene rohrdurchmesser
@:param ist der eingegeben rauhigkeitswert
@:returns eine annäherung für die Rohrreibungszahl
"""


def rohrreibungszahl_übergangsgebiet(Re, rohrdurchmesser, rauhigkeitswert):
    anfangswert = 0.01
    rohrreibungszahl = fsolve(gleichung_für_übergangsgebiet, anfangswert, args=(Re, rohrdurchmesser, rauhigkeitswert))
    return rohrreibungszahl[0]


"""
In dieser Funktion wird die Rohrreibungszahl für raue Rohre berechnet.
@:param rohrdurchmesser ist der eingegeben Rohrdurchmesser
@:param ist der eingegeben rauhigkeitswert
@:returns rohrreibungszahl
"""


def rohrreibungszahl_für_raue_rohre(rohrdurchmesser, rauhigkeitswert):
    rohrreibungszahl = 1 / pow((2 * math.log10(3.71 * (rohrdurchmesser / rauhigkeitswert))), 2)
    return rohrreibungszahl


"""
In dieser Funktion wird der berechnete Druckverlust von pascal in bar umgerechnet. 
@:param wert ist der berechente Druckverlust
@:returns wert_in_bar 
"""


def pascal_in_bar(wert):
    wert_in_bar = wert / 100000
    return wert_in_bar


"""
In dieser Funktion wird berechnet um wie viel Prozent der Volumenstrom maximal steigen kann, damit ein druckverlust von einem Bar nicht überschritten wird.
@:param rohrreibungszahl ist die berechnete Rohrreibungszahl
@:param L ist die eingegebene Rohrlänge
@:param d ist der eingegebene Rohrdurchmesser
@:returns max_voluemsntrom 
"""
def maximaler_volumenstrom(rohrreibungszahl, L, d, dichte):
    max_volumenstrom = ((1 * math.pi * math.pow(d, 3)) / (rohrreibungszahl * 2 * L * dichte)) * 100
    return max_volumenstrom


window = Tk()
window.title("Berechnung von Stoffströmen in geschlossenen Rohrleitungen")
window.geometry("500x500")
window.maxsize(500, 500)
window.minsize(500, 500)

headline = Label(window, text="Berechnung von Stoffströmen in geschlossenen Rohrleitungen")
headline.place(x=0, y=0, width=500, height=20)

rohrdurchmesser_label = tkinter.Label(window, text="Rohrdurchmesser: ", relief=RIDGE, width=20)
rohrdurchmesser_label.place(x=20, y=20 + 1 * 30)
rohrdurchmesser_entry = tkinter.Entry(relief=RIDGE, width=15, textvariable=rohrdurchmesser_label)
rohrdurchmesser_entry.place(x=200, y=20 + 1 * 30)
rohrdurchmesser_einheiten = tkinter.ttk.Combobox(
    window, state="readonly", values=["mm", "cm", "dm", "m", "km"]
)
rohrdurchmesser_einheiten.place(x=300, y=20 + 1 * 30)

rohrlänge_label = tkinter.Label(window, text="Rohrlänge: ", relief=RIDGE, width=20)
rohrlänge_label.place(x=20, y=20 + 2 * 30)
rohrlänge_entry = tkinter.Entry(relief=RIDGE, width=15, textvariable="rohrlänge")
rohrlänge_entry.place(x=200, y=20 + 2 * 30)
rohrlänge_einheiten = tkinter.ttk.Combobox(
    window, state="readonly", values=["mm", "cm", "dm", "m", "km"]
)
rohrlänge_einheiten.place(x=300, y=20 + 2 * 30)

dichte_label = tkinter.Label(window, text="Dichte der Flüssigkeit: ", relief=RIDGE, width=20)
dichte_label.place(x=20, y=20 + 3 * 30)
dichte_entry = tkinter.Entry(relief=RIDGE, width=15)
dichte_entry.place(x=200, y=20 + 3 * 30)
dichte_einheiten = tkinter.ttk.Combobox(
    window, state="readonly", values=["g/cm³", "g/ml", "kg/l", "kg/m³"]
)
dichte_einheiten.place(x=300, y=20 + 3 * 30)

zähigkeit_label = tkinter.Label(window, text="Kinematische Zähigkeit: ", relief=RIDGE, width=20)
zähigkeit_label.place(x=20, y=20 + 4 * 30)
zähigkeit_entry = tkinter.Entry(relief=RIDGE, width=15)
zähigkeit_entry.place(x=200, y=20 + 4 * 30)
zähigkeit_einheiten = tkinter.ttk.Combobox(
    window, state="readonly", values=["m²/s"]
)
zähigkeit_einheiten.place(x=300, y=20 + 4 * 30)

volumenstrom_label = tkinter.Label(window, text="Volumenstrom: ", relief=RIDGE, width=20)
volumenstrom_label.place(x=20, y=20 + 5 * 30)
volumenstrom_entry = tkinter.Entry(relief=RIDGE, width=15)
volumenstrom_entry.place(x=200, y=20 + 5 * 30)
volumenstrom_einheiten = tkinter.ttk.Combobox(
    window, state="readonly", values=["m³/h", "m³/sec"]
)
volumenstrom_einheiten.place(x=300, y=20 + 5 * 30)

rauhigkeitswert_label = tkinter.Label(window, text="*Rauhigkeitswert: ", relief=RIDGE, width=20)
rauhigkeitswert_label.place(x=20, y=20 + 6 * 30)
rauhigkeitswert_entry = tkinter.Entry(relief=RIDGE, width=15)
rauhigkeitswert_entry.place(x=200, y=20 + 6 * 30)
rauhigkeitswert_einheiten = tkinter.ttk.Combobox(
    window, state="readonly", values=["mm", "cm", "dm", "m", "km"]
)
rauhigkeitswert_einheiten.place(x=300, y=20 + 6 * 30)

ende = tkinter.Button(window, text="Ende", command=window.destroy)
ende.place(x=100, y=20 + 7 * 30)

berechnen = tkinter.Button(window, text="Berechnen", command=berechnen)
berechnen.place(x=20, y=20 + 7 * 30)

ergebnis_label = tkinter.Label(window, relief=RIDGE, width=65, height=12)
ergebnis_label.place(x=20, y=20 + 8 * 30)

rohrdurchmesser_einheiten.set("Bitte auswählen!")
rohrlänge_einheiten.set("Bitte auswählen!")
dichte_einheiten.set("Bitte auswählen!")
zähigkeit_einheiten.set("Bitte auswählen")
volumenstrom_einheiten.set("Bitte auswählen!")
rauhigkeitswert_einheiten.set("Bitte auswählen!")

credits_label = tkinter.Label(window, text="created by CK4®", width=20)
credits_label.place(x=360, y=460)

window.mainloop()
