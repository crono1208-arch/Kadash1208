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

def otro(frame5):
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
        if Variable.check_filcab.get() == True:
            filcab.grid(row=3, column=0, padx=0, pady=10, sticky=W)
            filcab_combo.grid(row=3, column=1, padx=0, pady=10, sticky=E)
            filcab_combo.set("")
        else:
            filcab.grid_forget()
            filcab_combo.grid_forget()
            
    def mostrar_dropdown1():
        if Variable.check_reemba.get() == True:
            bat.grid(row=4, column=0, padx=0, pady=10, sticky=W)
            bat_combo.grid(row=4, column=1, padx=0, pady=10, sticky=E)
            bat_combo.set("")
        else:
            bat.grid_forget()
            bat_combo.grid_forget()

    
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
        filcab_combo["values"] = cargar_refaccion("Filtro de Cabina")
        filcab_combo.set("")

    def update_combobox1():
        bat_combo["values"] = cargar_refaccion("Bateria")
        bat_combo.set("")

    #Seleccion del tipo de servicio Adicional
    chk = ttk.Checkbutton(frame5, text="Revision General",variable=Variable.check_revg, style="Custom.TCheckbutton")
    chk.grid(row=1, column=0, sticky=W)
    chk1 = ttk.Checkbutton(frame5, text="Revision Compra/Venta", variable=Variable.check_revcv, style="Custom.TCheckbutton")
    chk1.grid(row=1, column=1, sticky=W)
    chk2 = ttk.Checkbutton(frame5, text="Reemplazo Filtro de Cabina", variable=Variable.check_filcab, style="Custom.TCheckbutton",command=mostrar_dropdown)
    chk2.grid(row=2, column=0, sticky=W)
    chk3 = ttk.Checkbutton(frame5, text="Reemplazo de Bateria", variable=Variable.check_reemba, style="Custom.TCheckbutton", command=mostrar_dropdown1)
    chk3.grid(row=2, column=1, sticky=W)
    filcab = ttk.Label(frame5, text='Filtro de Cabina:', font=('Gotham Book', 10))
    filcab_combo = ttk.Combobox(frame5, textvariable=Variable.filcab_var, state="readonly", postcommand=update_combobox, width=10)
    bat = ttk.Label(frame5, text='Bateria:', font=('Gotham Book', 10))
    bat_combo = ttk.Combobox(frame5, textvariable=Variable.bat_var, state="readonly", postcommand=update_combobox1, width=10)
    
    cargar_refaccion
    update_combobox()
    update_combobox1()