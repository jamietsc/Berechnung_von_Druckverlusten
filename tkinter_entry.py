import tkinter.ttk
from tkinter import messagebox
from tkinter import *


def berechnen():
    rohrdurchmesser = rohrdurchmesser_einheiten.get()
    messagebox.showinfo("Berechnen", rohrdurchmesser)

window = Tk()
window.title("Berechnung von Stoffströmen in geschlossenen Rohrleitungen")
window.geometry("500x500")

rohrdurchmesser_label = tkinter.Label(window, text= "Rohrdurchmesser: ", relief= RIDGE, width=20)
rohrdurchmesser_label.place(x = 20, y = 20 + 1 * 30)
rohrdurchmesser_entry = tkinter.Entry(relief= RIDGE, width=15, textvariable=rohrdurchmesser_label)
rohrdurchmesser_entry.place(x = 200, y = 20 + 1 * 30)
rohrdurchmesser_einheiten = tkinter.ttk.Combobox(
    window, state= "readonly", values= ["mm", "cm", "dm", "m", "km"]
)
rohrdurchmesser_einheiten.place(x = 300, y = 20 + 1 * 30)

ende = tkinter.Button(window, text="Ende", command=window.destroy)
ende.place(x = 100, y = 20 + 7 * 30)

berechnen = tkinter.Button(window, text = "Berechnen", command = berechnen)
berechnen.place(x = 20, y = 20 + 7 * 30)



window.mainloop()