import tkinter as tk
from tkinter import ttk
from tkinter import *
import Variable
import sqlite3
import os

ruta = os.path.join(os.getenv("LOCALAPPDATA"), "CotizadorTaller")

db_path = os.path.join(ruta, "taller.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def frenos(frame3):
    style = ttk.Style()
    style.configure(
    "Custom.TCheckbutton",
    font=("Gotham Book", 10)
)

    style.map(
    "Custom.TCheckbutton",
    background=[("active", "#e6f2ff")],  # color cuando pasas el mouse
    foreground=[("active", "black")]
)
    def mostrar_dropdown():
        if Variable.check_fred.get() == True:
            balde.grid(row=2, column=0, padx=0, pady=10, sticky=W)
            balde_combo.grid(row=2, column=1, padx=0, pady=10, sticky=E)
            balde_combo.set("")
        else:
            balde.grid_forget()
            balde_combo.grid_forget()
            
    def mostrar_dropdown1():
        if Variable.check_fret.get() == True:
            baltra.grid(row=3, column=0, padx=0, pady=10, sticky=W)
            baltra_combo.grid(row=3, column=1, padx=0, pady=10, sticky=E)
            baltra_combo.set("")

        else:
            baltra.grid_forget()
            baltra_combo.grid_forget()
            
    def mostrar_dropdown2():
        if Variable.check_recd.get() == True:
            reccant_combo.grid(row=6, column=1, padx=0, pady=10, sticky=E)
            reccant_combo.set("")

        else:
            reccant_combo.grid_forget()


    
    def cargar_refaccion(tipo):
        cursor.execute("""
        SELECT DISTINCT r.numero_parte
        FROM refacciones r
        JOIN compatibilidad_ref ar ON r.numero_parte = ar.numero_parte
        JOIN autos a ON ar.id_auto = auto_id
        WHERE a.modelo = ? AND a.año = ? AND r.descripcion LIKE ?
        """, (Variable.modelo_var.get(), Variable.anio_var.get(),  f"%{tipo}%"))
        datos = cursor.fetchall()
        return [fila[0] for fila in datos]
                    
    def update_combobox():
        balde_combo["values"] = cargar_refaccion("Balatas Delanteras")
        balde_combo.set("")

    def update_combobox1():
        baltra_combo["values"] = cargar_refaccion("Balatas Traseras")
        baltra_combo.set("")
    
    def update_combobox2():
        reccant_combo.set("")
        
    #Seleccion del tipo de cotizacion de frenos
    chk = ttk.Checkbutton(frame3, text="Frenos Delanteros",variable=Variable.check_fred, style="Custom.TCheckbutton", command=mostrar_dropdown)
    chk.grid(row=1, column=0, sticky=W)
    chk1 = ttk.Checkbutton(frame3, text="Frenos Traseros", variable=Variable.check_fret, style="Custom.TCheckbutton", command=mostrar_dropdown1)
    chk1.grid(row=1, column=1, sticky=W)
    chk2 = ttk.Checkbutton(frame3, text="Ajuste y limpieza de frenos", variable=Variable.check_ajuf, style="Custom.TCheckbutton")
    chk2.grid(row=5, column=0, sticky=W)
    chk3 = ttk.Checkbutton(frame3, text="Rectificado de Discos", variable=Variable.check_recd, style="Custom.TCheckbutton", command=mostrar_dropdown2)
    chk3.grid(row=5, column=1, sticky=W)
    balde = ttk.Label(frame3, text='Balata delantera:', font=('Gotham Book', 10))
    balde_combo = ttk.Combobox(frame3, textvariable=Variable.balde_var, state="readonly", postcommand=update_combobox, width=10)
    baltra = ttk.Label(frame3, text='Balata Trasera:', font=('Gotham Book', 10))
    baltra_combo = ttk.Combobox(frame3, textvariable=Variable.baltra_var, state="readonly", postcommand=update_combobox1, width=10)
    reccant_combo = ttk.Combobox(frame3, textvariable=Variable.reccant_var, values=["1","2"], state="readonly", width=2, postcommand=update_combobox2)
    
    cargar_refaccion
    update_combobox()
    update_combobox1()
    update_combobox2()