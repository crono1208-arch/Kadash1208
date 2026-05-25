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


def aceite(frame1):
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
        if Variable.check_cafs.get():
            chk1.state(['disabled']) 
        else:
            chk1.state(['!disabled'])
            
    def toggle_checkbox1():
        if Variable.check_cafm.get():
            chk.state(['disabled']) 
        else:
            chk.state(['!disabled'])
            
    def mostrar_dropdown():
        if Variable.check_cafs.get() == True:
            fil.grid(row=2, column=0, padx=0, pady=10, sticky=W)
            fil_combo.grid(row=2, column=1, padx=0, pady=10, sticky=E)
            fil_combo.set("")
            Variable.ace_sint = "MOBIL5W30"
        else:
            fil.grid_forget()
            fil_combo.grid_forget()
            
    def mostrar_dropdown1():
        if Variable.check_cafm.get() == True:
            fil.grid(row=2, column=0, padx=0, pady=10, sticky=W)
            fil_combo.grid(row=2, column=1, padx=0, pady=10, sticky=E)
            fil_combo.set("")
            Variable.ace_min = "VAL20W50"
        else:
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
        fil_combo["values"] = cargar_refaccion("Filtro de Aceite")
        fil_combo.set("")
         
    #Seleccion del tipo de servicio Adicional
    chk = ttk.Checkbutton(frame1, text="Aceite Sintetico",variable=Variable.check_cafs, style="Custom.TCheckbutton",command= lambda: [toggle_checkbox(),mostrar_dropdown()])
    chk.grid(row=1, column=0, sticky=W)
    chk1 = ttk.Checkbutton(frame1, text="Aceite Mineral", variable=Variable.check_cafm, style="Custom.TCheckbutton" ,command= lambda: [toggle_checkbox1(),mostrar_dropdown1()])
    chk1.grid(row=1, column=1, sticky=W)
    fil = ttk.Label(frame1, text='Filtro de Aceite:', font=('Gotham Book', 10))
    fil_combo = ttk.Combobox(frame1, textvariable=Variable.fil_var, state="readonly", postcommand=update_combobox, width=10)
   
    cargar_refaccion
    update_combobox()