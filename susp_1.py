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

def susp(frame4):
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
        if Variable.check_amdel.get() == True:
            amdel.grid(row=2, column=0, padx=0, pady=10, sticky=W)
            amdel_combo.grid(row=2, column=1, padx=0, pady=10, sticky=W)
            amdelcant_combo.grid(row=2, column=1, padx=0, pady=10, sticky=E)
            amdel_combo.set("")
            amdelcant_combo.set("")
        else:
            amdel.grid_forget()
            amdel_combo.grid_forget()
            amdelcant_combo.grid_forget()
            
    def mostrar_dropdown1():
        if Variable.check_basam.get() == True:
            bases.grid(row=3, column=0, padx=0, pady=10, sticky=W)
            bases_combo.grid(row=3, column=1, padx=0, pady=10, sticky=W)
            basescant_combo.grid(row=3, column=1, padx=0, pady=10, sticky=E)
            bases_combo.set("")
            basescant_combo.set("")

        else:
            bases.grid_forget()
            bases_combo.grid_forget()
            basescant_combo.grid_forget()
            
    def mostrar_dropdown2():
        if Variable.check_amtra.get() == True:
            amtra.grid(row=6, column=0, padx=0, pady=10, sticky=W)
            amtra_combo.grid(row=6, column=1, padx=0, pady=10, sticky=W)
            amtracant_combo.grid(row=6, column=1, padx=0, pady=10, sticky=E)
            amtra_combo.set("")
            amtracant_combo.set("")
        else:
            amtra.grid_forget()
            amtra_combo.grid_forget()
            amtracant_combo.grid_forget()
            
    def mostrar_dropdown3():
        if Variable.check_tores.get() == True:
            tores.grid(row=7, column=0, padx=0, pady=10, sticky=W)
            tores_combo.grid(row=7, column=1, padx=0, pady=10, sticky=W)
            torescant_combo.grid(row=7, column=1, padx=0, pady=10, sticky=E)
            tores_combo.set("")
            torescant_combo.set("")
        else:
            tores.grid_forget()
            tores_combo.grid_forget()
            torescant_combo.grid_forget()

    def mostrar_dropdown4():
        if Variable.check_horq.get() == True:
            horq.grid(row=9, column=0, padx=0, pady=10, sticky=W)
            horq_combo.grid(row=9, column=1, padx=0, pady=10, sticky=W)
            horqcant_combo.grid(row=9, column=1, padx=0, pady=10, sticky=E)
            horq_combo.set("")
            horqcant_combo.set("")
        else:
            horq.grid_forget()
            horq_combo.grid_forget()
            horqcant_combo.grid_forget()
            
    def mostrar_dropdown5():
        if Variable.check_junhom.get() == True:
            junt.grid(row=10, column=0, padx=0, pady=10, sticky=W)
            junt_combo.grid(row=10, column=1, padx=0, pady=10, sticky=W)
            juntcant_combo.grid(row=10, column=1, padx=0, pady=10, sticky=E)
            junt_combo.set("")
            juntcant_combo.set("")
        else:
            junt.grid_forget()
            junt_combo.grid_forget()
            juntcant_combo.grid_forget()
    
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
        amdel_combo["values"] = cargar_refaccion("Amortiguador Delantero")
        amdel_combo.set("")
        amdelcant_combo.set("")

    def update_combobox1():
        bases_combo["values"] = cargar_refaccion("Bases de amortiguador")
        bases_combo.set("")
        basescant_combo.set("") 
        
    def update_combobox2():
        amtra_combo["values"] = cargar_refaccion("Amortiguador Trasero")
        amtra_combo.set("")
        amtracant_combo.set("")
        
    def update_combobox3():
        tores_combo["values"] = cargar_refaccion("Tornillo Estabilizador")
        tores_combo.set("")
        torescant_combo.set("")

    def update_combobox4():
        horq_combo["values"] = cargar_refaccion("Horquilla")
        horq_combo.set("")
        horqcant_combo.set("")

    def update_combobox5():
        junt_combo["values"] = cargar_refaccion("Junta Homocinetica")
        junt_combo.set("")
        juntcant_combo.set("")

    #Seleccion del tipo de servicio de suspension
    chk = ttk.Checkbutton(frame4, text="Amortiguadores Delanteros",variable=Variable.check_amdel, style="Custom.TCheckbutton",command=mostrar_dropdown)
    chk.grid(row=1, column=0, sticky=W)
    chk1 = ttk.Checkbutton(frame4, text="Bases de Amortiguador", variable=Variable.check_basam, style="Custom.TCheckbutton", command=mostrar_dropdown1)
    chk1.grid(row=1, column=1, sticky=W)
    chk2 = ttk.Checkbutton(frame4, text="Amortiguadores Traseros", variable=Variable.check_amtra, style="Custom.TCheckbutton", command=mostrar_dropdown2)
    chk2.grid(row=4, column=0, sticky=W)
    chk3 = ttk.Checkbutton(frame4, text="Tornillos Estabilizadores", variable=Variable.check_tores, style="Custom.TCheckbutton", command=mostrar_dropdown3)
    chk3.grid(row=4, column=1, sticky=W)
    chk4 = ttk.Checkbutton(frame4, text="Horquillas", variable=Variable.check_horq, style="Custom.TCheckbutton", command=mostrar_dropdown4)
    chk4.grid(row=8, column=0, sticky=W)
    chk5 = ttk.Checkbutton(frame4, text="Juntas Homocineticas", variable=Variable.check_junhom, style="Custom.TCheckbutton", command=mostrar_dropdown5)
    chk5.grid(row=8, column=1, sticky=W)
    amdel = ttk.Label(frame4, text='Amortiguador Delantero:', font=('Gotham Book', 10))
    amdel_combo = ttk.Combobox(frame4, textvariable=Variable.amdel_var, state="readonly", postcommand=update_combobox, width=10)
    amdelcant_combo = ttk.Combobox(frame4, textvariable=Variable.amdelcant_var, values=["1","2"], state="readonly", width="2")
    bases = ttk.Label(frame4, text='Base de Amortiguador:', font=('Gotham Book', 10))
    bases_combo = ttk.Combobox(frame4, textvariable=Variable.bases_var, state="readonly", postcommand=update_combobox1, width=10)
    basescant_combo = ttk.Combobox(frame4, textvariable=Variable.basescant_var, values=["1","2","3","4"], state="readonly", width="2")
    amtra = ttk.Label(frame4, text='Amortiguador Trasero:', font=('Gotham Book', 10))
    amtra_combo = ttk.Combobox(frame4, textvariable=Variable.amtra_var, state="readonly", postcommand=update_combobox2, width=10)
    amtracant_combo = ttk.Combobox(frame4, textvariable=Variable.amtracant_var, values=["1","2"], state="readonly", width="2")
    tores = ttk.Label(frame4, text='Tornillo Estabilizador:', font=('Gotham Book', 10))
    tores_combo = ttk.Combobox(frame4, textvariable=Variable.tor_var, state="readonly", postcommand=update_combobox3, width=10)
    torescant_combo = ttk.Combobox(frame4, textvariable=Variable.torcant_var, values=["1","2"], state="readonly", width="2")
    horq = ttk.Label(frame4, text='Horquilla:', font=('Gotham Book', 10))
    horq_combo = ttk.Combobox(frame4, textvariable=Variable.horq_var, state="readonly", postcommand=update_combobox4, width=10)
    horqcant_combo = ttk.Combobox(frame4, textvariable=Variable.horqcant_var, values=["1","2"], state="readonly", width="2")
    junt = ttk.Label(frame4, text='Junta Homocinetica:', font=('Gotham Book', 10))
    junt_combo = ttk.Combobox(frame4, textvariable=Variable.junth_var, state="readonly", postcommand=update_combobox5, width=10)
    juntcant_combo = ttk.Combobox(frame4, textvariable=Variable.junthcant_var, values=["1","2"], state="readonly", width="2")

    cargar_refaccion
    update_combobox()
    update_combobox1()
    update_combobox2()
    update_combobox3()
    update_combobox4() 
    update_combobox5() 