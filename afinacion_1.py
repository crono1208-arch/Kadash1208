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


def afina(frame2):
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
    
    def toggle_checkbox():
        if Variable.check_afmen.get():
            chk1.state(['disabled']) 
            aire_combo.set("")
            bujia_combo.set("")
        else:
            chk1.state(['!disabled'])
            aire_combo.set("")
            bujia_combo.set("")
            
    def toggle_checkbox1():
        if Variable.check_afmay.get():
            chk.state(['disabled'])
            aire_combo.set("")
            bujia_combo.set("")
        else:
            chk.state(['!disabled'])
            aire_combo.set("")
            bujia_combo.set("")
            
    def mostrar_dropdown():
        if Variable.check_afmen.get() == True:
            aire.grid(row=3, column=0, padx=0, pady=10, sticky=W)
            aire_combo.grid(row=3, column=1, padx=0, pady=10, sticky=E)
            fil.grid(row=2, column=0, padx=0, pady=10, sticky=W)
            fil_combo.grid(row=2, column=1, padx=0, pady=10, sticky=E)
            Variable.ace_sint = "MOBIL5W30"
            aire_combo.set("")
            fil_combo.set("")
        else:
            aire.grid_forget()
            aire_combo.grid_forget()
            fil.grid_forget()
            fil_combo.grid_forget()
            
    def mostrar_dropdown1():
        if Variable.check_afmay.get() == True:
            aire.grid(row=3, column=0, padx=0, pady=10, sticky=W)
            aire_combo.grid(row=3, column=1, padx=0, pady=10, sticky=E)
            bujia.grid(row=4, column=0, padx=0, pady=10, sticky=W)
            bujia_combo.grid(row=4, column=1, padx=0, pady=10, sticky=E)
            fil.grid(row=2, column=0, padx=0, pady=10, sticky=W)
            fil_combo.grid(row=2, column=1, padx=0, pady=10, sticky=E)
            Variable.ace_sint = "MOBIL5W30"
            fil_combo.set("")
            aire_combo.set("")
            bujia_combo.set("")
        else:
            aire.grid_forget()
            aire_combo.grid_forget()
            bujia.grid_forget()
            bujia_combo.grid_forget()
            fil.grid_forget()
            fil_combo.grid_forget()
    
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
        aire_combo["values"] = cargar_refaccion("filtro de aire")
        aire_combo.set("")

    def update_combobox1():
        bujia_combo["values"] = cargar_refaccion("bujia")
        bujia_combo.set("")
        
    def update_combobox2():
        fil_combo["values"] = cargar_refaccion("Filtro de Aceite")
        fil_combo.set("")
         
    #Seleccion del tipo de servicio Adicional
    chk = ttk.Checkbutton(frame2, text="Afinación Menor",variable=Variable.check_afmen, style="Custom.TCheckbutton", command= lambda: [toggle_checkbox(),mostrar_dropdown()])
    chk.grid(row=1, column=0, sticky=W)
    chk1 = ttk.Checkbutton(frame2, text="Afinación Mayor", variable=Variable.check_afmay, style="Custom.TCheckbutton", command= lambda: [toggle_checkbox1(),mostrar_dropdown1()])
    chk1.grid(row=1, column=1, sticky=W)
    aire = ttk.Label(frame2, text='Filtro de Aire:', font=('Gotham Book', 10))
    aire_combo = ttk.Combobox(frame2, textvariable=Variable.aire_var, state="readonly", postcommand=update_combobox, width=10)
    bujia = ttk.Label(frame2, text='Bujias:', font=('Gotham Book', 10))
    bujia_combo = ttk.Combobox(frame2, textvariable=Variable.bujia_var, state="readonly", postcommand=update_combobox1, width=10)
    fil = ttk.Label(frame2, text='Filtro de Aceite:', font=('Gotham Book', 10))
    fil_combo = ttk.Combobox(frame2, textvariable=Variable.fil_var, state="readonly", postcommand=update_combobox2, width=10)
    
    cargar_refaccion
    update_combobox()
    update_combobox1()
    update_combobox2()