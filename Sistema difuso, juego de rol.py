import tkinter as tk
from tkinter import ttk, messagebox  
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


dif_poder = ctrl.Antecedent(np.arange(-5, 5.1, 0.1), 'dif_poder')
recursos = ctrl.Antecedent(np.arange(0, 101, 1), 'recursos')
salud = ctrl.Antecedent(np.arange(0, 101, 1), 'salud')
ventaja_enemigo = ctrl.Antecedent(np.arange(0, 101, 1), 'ventaja_enemigo')

dificultad = ctrl.Consequent(np.arange(0, 101, 1), 'dificultad')

dif_poder['muy_baja'] = fuzz.trimf(dif_poder.universe, [-5, -5, -2.5])
dif_poder['baja']     = fuzz.trimf(dif_poder.universe, [-4, -2.5, -1])
dif_poder['igual']    = fuzz.trimf(dif_poder.universe, [-1.5, 0, 1.5])
dif_poder['alta']     = fuzz.trimf(dif_poder.universe, [1, 2.5, 4])
dif_poder['muy_alta'] = fuzz.trimf(dif_poder.universe, [2.5, 5, 5])

recursos['bajos']   = fuzz.trimf(recursos.universe, [0, 0, 40])
recursos['medios']  = fuzz.trimf(recursos.universe, [20, 50, 80])
recursos['altos']   = fuzz.trimf(recursos.universe, [60, 100, 100])

salud['mala']    = fuzz.trimf(salud.universe, [0, 0, 40])
salud['media']   = fuzz.trimf(salud.universe, [20, 50, 80])
salud['buena']   = fuzz.trimf(salud.universe, [60, 100, 100])

ventaja_enemigo['baja']  = fuzz.trimf(ventaja_enemigo.universe, [0, 0, 40])
ventaja_enemigo['media'] = fuzz.trimf(ventaja_enemigo.universe, [20, 50, 80])
ventaja_enemigo['alta']  = fuzz.trimf(ventaja_enemigo.universe, [60, 100, 100])

dificultad['trivial'] = fuzz.trapmf(dificultad.universe, [0, 0, 10, 20])
dificultad['facil']   = fuzz.trimf(dificultad.universe, [10, 25, 40])
dificultad['media']   = fuzz.trimf(dificultad.universe, [35, 50, 65])
dificultad['dificil'] = fuzz.trimf(dificultad.universe, [60, 75, 85])
dificultad['mortal']  = fuzz.trapmf(dificultad.universe, [80, 90, 100, 100])


reglas = []
reglas.append(ctrl.Rule(dif_poder['muy_alta'] & salud['buena'] & recursos['altos'] & ventaja_enemigo['baja'],
                        dificultad['trivial']))
reglas.append(ctrl.Rule(dif_poder['alta'] & (salud['buena'] | recursos['altos']) & ventaja_enemigo['baja'],
                        dificultad['facil']))
reglas.append(ctrl.Rule(dif_poder['igual'] & (salud['buena'] | recursos['altos']) & ventaja_enemigo['baja'],
                        dificultad['media']))
reglas.append(ctrl.Rule((dif_poder['baja'] | dif_poder['muy_baja']) & (salud['media'] | recursos['medios']) &
                        (ventaja_enemigo['media'] | ventaja_enemigo['alta']),
                        dificultad['dificil']))
reglas.append(ctrl.Rule((dif_poder['muy_baja'] | dif_poder['baja']) & (salud['mala'] | recursos['bajos']) &
                        ventaja_enemigo['alta'], dificultad['mortal']))


sistema_ctrl = ctrl.ControlSystem(reglas)
sistema = ctrl.ControlSystemSimulation(sistema_ctrl)


def interpretar_dificultad(valor):
    if valor <= 20:
        return "Trivial"
    elif valor <= 34:
        return "Fácil"
    elif valor <= 65:
        return "Media"
    elif valor <= 85:
        return "Difícil"
    else:
        return "Mortal"
    

def recomendacion(dif_val, rec_val, sal_val, vent_val):
    sistema.input['dif_poder'] = dif_val
    sistema.input['recursos'] = rec_val
    sistema.input['salud'] = sal_val
    sistema.input['ventaja_enemigo'] = vent_val
    sistema.compute()
    return sistema.output['dificultad']

def calcular():
    try:
        dif_val = float(entry_dif_poder.get())
        rec_val = float(entry_recursos.get())
        sal_val = float(entry_salud.get())
        vent_val = float(entry_ventaja.get())

        valor = recomendacion(dif_val, rec_val, sal_val, vent_val)
        etiqueta = interpretar_dificultad(valor)

        resultado_label.config(text=f"Dificultad: {etiqueta} ({valor:.2f})")
    except Exception as e:
        resultado_label.config(text=f"Error: {str(e)}")

root = tk.Tk()
root.title("Sistema Difuso - Dificultad del Juego de Rol")
root.geometry("700x400")

tk.Label(root, text="diferencia de poder entre el cr de la criatura y el del equipo (APL - CR, debe ser de -5 a 5):").pack()
entry_dif_poder = tk.Entry(root)
entry_dif_poder.pack()

tk.Label(root, text="del 0 al 100 como están los recursos del grupo (objetos, pociones, espacios de conjuros, etc):").pack()
entry_recursos = tk.Entry(root)
entry_recursos.pack()

tk.Label(root, text="porcentaje del estado de la salud del equipo (0 es en las últimas y 100 es sin daños):").pack()
entry_salud = tk.Entry(root)
entry_salud.pack()

tk.Label(root, text="del 0 al 100 cuanta ventaja tiene el enemigo sobre el grupo (terreno, tienen rehenes, cosas a su favor):").pack()
entry_ventaja = tk.Entry(root)
entry_ventaja.pack()

tk.Button(root, text="Calcular Dificultad", command=calcular).pack(pady=10)
resultado_label = tk.Label(root, text="Dificultad: ")
resultado_label.pack()

root.mainloop()