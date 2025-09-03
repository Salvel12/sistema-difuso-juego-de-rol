import tkinter as tk
from tkinter import ttk, messagebox  
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def recomendación(dif_poder_val, recursos_val, salud_val, ventaja_enemigo_val):

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

    try:
        sistema.input['dif_poder'] = float(dif_poder_val)
        sistema.input['recursos'] = float(recursos_val)
        sistema.input['salud'] = float(salud_val)
        sistema.input['ventaja_enemigo'] = float(ventaja_enemigo_val)
        
        sistema.compute()

        print("Variables de salida disponibles:", sistema.output)  # 👀 depuración

        if 'dificultad' in sistema.output:
            score = float(sistema.output['dificultad'])
            return f"Dificultad recomendada: {score:.2f}"
        else:
            return "No se pudo calcular la dificultad (revisa reglas o rangos)."
    
    except Exception as e:
        return f"Error en la recomendación: {e}"


def calcular():
    try:
        dif_poder = float(entry_poder.get())
        recursos = float(entry_recursos.get())
        salud = float(entry_salud.get())
        ventaja_enemigo = float(entry_ventaja.get())

        resultado = recomendación(dif_poder, recursos, salud, ventaja_enemigo)
        label_resultado.config(text=f"Dificultad: {resultado}")
    except:
        label_resultado.config(text="ingrese un número válido")
        return


ventana = tk.Tk()
ventana.title("Sistema difuso - dnd")
ventana.geometry("700x400")


label1 = tk.Label(ventana, text="diferencia de poder entre el cr de la criatura y el del equipo (APL - CR, debe ser de -5 a 5):")
label1.pack(pady=5)
entry_poder = tk.Entry(ventana)
entry_poder.pack(pady=5)

label1 = tk.Label(ventana, text="porcentaje del estado de la salud del equipo (0 es en las últimas y 100 es sin daños):")
label1.pack(pady=5)
entry_salud = tk.Entry(ventana)
entry_salud.pack(pady=5)

label1 = tk.Label(ventana, text="del 0 al 100 como están los recursos del grupo (objetos, pociones, espacios de conjuros, etc):")
label1.pack(pady=5)
entry_recursos = tk.Entry(ventana)
entry_recursos.pack(pady=5)

label1 = tk.Label(ventana, text="del 0 al 100 cuanta ventaja tiene el enemigo sobre el grupo (terreno, tienen rehenes, cosas a su favor):")
label1.pack(pady=5)
entry_ventaja = tk.Entry(ventana)
entry_ventaja.pack(pady=5)


btn = tk.Button(ventana, text="Recomendar", command=calcular)
btn.pack(pady=10)

label_resultado = tk.Label(ventana, text="", wraplength=350, justify="center")
label_resultado.pack(pady=20)

ventana.mainloop()

