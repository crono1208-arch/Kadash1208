import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from autos import crear_ventana_auto
from refacciones import crear_ventana_refa
from Logic import crear_ventana_cotizacion
import sqlite3
import aceite_1
import afinacion_1
import frenos_1
import susp_1
import otro_1
import sqlite3
import Variable
import os

ruta = os.path.join(os.getenv("LOCALAPPDATA"), "CotizadorTaller")

db_path = os.path.join(ruta, "taller.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Configuración de la ventana principal
Variable.app_root = tk.Tk()
Variable.app_root.title("Cotizador Taller Midas")
Variable.app_root.iconbitmap('images.ico')
Variable.app_root.geometry("400x780")
bold_font1 = Font(family="Gotham Book",size=10, weight="bold")
style = ttk.Style()
style.configure("Bold.TButton", font=bold_font1)
#Declaracion de variables globales
Variable.check_cafs = tk.BooleanVar(value=False)
Variable.check_cafm = tk.BooleanVar(value=False)
Variable.check_afmen = tk.BooleanVar(value=False)
Variable.check_afmay = tk.BooleanVar(value=False)
Variable.check_fred = tk.BooleanVar(value=False)
Variable.check_fret = tk.BooleanVar(value=False)
Variable.check_ajuf = tk.BooleanVar(value=False)
Variable.check_recd = tk.BooleanVar(value=False)
Variable.check_amdel = tk.BooleanVar(value=False)
Variable.check_basam = tk.BooleanVar(value=False)
Variable.check_amtra = tk.BooleanVar(value=False)
Variable.check_tores = tk.BooleanVar(value=False)
Variable.check_horq = tk.BooleanVar(value=False)
Variable.check_junhom = tk.BooleanVar(value=False)
Variable.check_revg = tk.BooleanVar(value=False)
Variable.check_revcv = tk.BooleanVar(value=False)
Variable.check_filcab = tk.BooleanVar(value=False)
Variable.check_reemba = tk.BooleanVar(value=False)
Variable.marca_var = tk.StringVar()
Variable.modelo_var = tk.StringVar()
Variable.anio_var = tk.StringVar()
Variable.cil_var = tk.StringVar()
Variable.aire_var = tk.StringVar()
Variable.bujia_var = tk.StringVar()
Variable.balde_var = tk.StringVar()
Variable.baltra_var = tk.StringVar()
Variable.filcab_var = tk.StringVar() 
Variable.bat_var = tk.StringVar()
Variable.fil_var = tk.StringVar()
Variable.amdel_var = tk.StringVar()
Variable.amdelcant_var = tk.IntVar()
Variable.bases_var = tk.StringVar()
Variable.basescant_var = tk.IntVar()
Variable.amtra_var = tk.StringVar()
Variable.amtracant_var = tk.IntVar()
Variable.tor_var = tk.StringVar()
Variable.torcant_var = tk.IntVar()
Variable.horq_var = tk.StringVar()
Variable.horqcant_var = tk.IntVar()
Variable.junth_var = tk.StringVar()
Variable.junthcant_var = tk.IntVar()
Variable.reccant_var = tk.IntVar()
Variable.ace_sint = tk.StringVar()
Variable.ace_min = tk.StringVar()

#Encabezado
mylabel = ttk.Label(Variable.app_root, text='Taller Midas Ruiz Cortines', font=('Gotham Bold', 18, 'bold'))
mylabel.grid(row=0, column=0, padx=10, pady=10, sticky=E)
mymenu = ttk.Label(Variable.app_root, text='Ingresa datos del Vehiculo:', font=('Gotham Book', 14))
mymenu.grid(row=1, column=0, padx=10, pady=10, sticky=W)
def abrir_ventana1():
    crear_ventana_auto(Variable.app_root)
    #nueva ventana para ver y editar el catalogo de autos
def abrir_ventana2():
    crear_ventana_refa(Variable.app_root)
    #nueva ventana para ver y editar el catalogo de refacciones
def abrir_ventana3():
    crear_ventana_cotizacion(Variable.app_root)
    #nueva ventana para ver y mostrar la cotizacion
    #Dropdown para seleccionar la marca 
def cargar_marcas():
    cursor.execute("SELECT DISTINCT marca FROM autos ORDER BY marca ASC")
    marcas = [row[0] for row in cursor.fetchall()]
    marca_combo['values'] = marcas
    modelo_combo.set("")
    anio_combo.set("")
    cil_combo.set('')
        
    #Dropdown para seleccionar modelo dependiente de la marca seleccionada
def actualizar_modelos(event):
    marca = Variable.marca_var.get()

    cursor.execute(
         "SELECT DISTINCT modelo FROM autos WHERE marca=? ORDER BY modelo ASC",
        (marca,)
        )

    modelos = [row[0] for row in cursor.fetchall()]
    modelo_combo['values'] = modelos
    modelo_combo.set("")
    anio_combo.set("")
    cil_combo.set('')
    #Dropdown para seleccionar año dependiente del modelo seleccionado    
def actualizar_anios(event):

    marca = Variable.marca_var.get()
    modelo = Variable.modelo_var.get()

    cursor.execute(
        "SELECT DISTINCT año FROM autos WHERE marca=? AND modelo=? ORDER BY año",
        (marca, modelo)
    )

    anios = [row[0] for row in cursor.fetchall()]
    anio_combo['values'] = anios
    anio_combo.set("")
    cil_combo.set('')
    #Dropdown para seleccionar cantidad de cilindros dependiente del año seleccionado    
def actualizar_cil(event):

    marca = Variable.marca_var.get()
    modelo = Variable.modelo_var.get()
    anio = Variable.anio_var.get()

    cursor.execute(
        "SELECT DISTINCT cilindros FROM autos WHERE marca=? AND modelo=? AND año=? ORDER BY cilindros",
        (marca, modelo, anio)
    )

    cil = [row[0] for row in cursor.fetchall()]
    cil_combo['values'] = cil
    cil_combo.set("")
    
def update_combobox():
    new_values = cargar_marcas()
    marca_combo.set("")
    marca_combo.configure(values=new_values)
            
            
marca = ttk.Label(Variable.app_root, text='Marca del Vehículo:', font=('Gotham Book', 10))
marca.grid(row=2, column=0, padx=0, pady=10, sticky=W)
marca_combo = ttk.Combobox(Variable.app_root, textvariable=Variable.marca_var, state="readonly", postcommand=update_combobox)
marca_combo.grid(row=2, column=0, padx=0, pady=10, sticky=E)
modelo = ttk.Label(Variable.app_root, text='Modelo del Vehículo:', font=('Gotham Book', 10))
modelo.grid(row=3, column=0, padx=0, pady=10, sticky=W)
modelo_combo = ttk.Combobox(Variable.app_root, textvariable=Variable.modelo_var, state="readonly")
modelo_combo.grid(row=3, column=0, padx=0, pady=10, sticky=E)
anio = ttk.Label(Variable.app_root, text='Año del Vehículo:', font=('Gotham Book', 10))
anio.grid(row=4, column=0, padx=0, pady=10, sticky=W)
anio_combo = ttk.Combobox(Variable.app_root, textvariable=Variable.anio_var, state="readonly")
anio_combo.grid(row=4, column=0, padx=0, pady=10, sticky=E)
cil = ttk.Label(Variable.app_root, text='Cantidad de Cilindros:', font=('Gotham Book', 10))
cil.grid(row=5, column=0, padx=0, pady=10, sticky=W)
cil_combo = ttk.Combobox(Variable.app_root, textvariable=Variable.cil_var, state="readonly")
cil_combo.grid(row=5, column=0, padx=0, pady=10, sticky=E)
myopcion = ttk.Label(Variable.app_root, text='Selecciona la cotizacion solicitada:', font=('Gotham Book', 12))
myopcion.grid(row=6, column=0, padx=10, pady=10, sticky=W)
marca_combo.bind("<<ComboboxSelected>>", actualizar_modelos)
modelo_combo.bind("<<ComboboxSelected>>", actualizar_anios)
anio_combo.bind("<<ComboboxSelected>>", actualizar_cil)
cargar_marcas()
update_combobox()

# Crear el Notebook (contenedor de pestañas)
notebook = ttk.Notebook(Variable.app_root)
notebook.grid(row=7, column=0)

# Crear los marcos (frames) para cada pestaña
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
frame3 = ttk.Frame(notebook)
frame4 = ttk.Frame(notebook)
frame5 = ttk.Frame(notebook)

# Añadir los marcos al notebook
notebook.add(frame1, text="Cambio de Aceite")
notebook.add(frame2, text="Afinaciones")
notebook.add(frame3, text="Frenos")
notebook.add(frame4, text="Suspension")
notebook.add(frame5, text="Otros")

# Añadir contenido a la Pestaña 1
aceite_1.aceite(frame1)

# Añadir contenido a la Pestaña 2
afinacion_1.afina(frame2)

# Añadir contenido a la Pestaña 3
frenos_1.frenos(frame3)

# Añadir contenido a la Pestaña 4
susp_1.susp(frame4)

# Añadir contenido a la Pestaña 5
otro_1.otro(frame5)

mybutton6 = ttk.Button(Variable.app_root, text="Generar cotización", command=abrir_ventana3, style="Bold.TButton")
mybutton6.grid(row=8, column=0, padx=10, pady=10, sticky=W)
mybutton7 = ttk.Button(Variable.app_root, text='Catalogo Autos',command=lambda: [abrir_ventana1(),update_combobox()], style="Bold.TButton")
mybutton7.grid(row=9, column=0, padx=10, pady=10, sticky=W)
mybutton8 = ttk.Button(Variable.app_root, text='Catalogo Refacciones', command=lambda: [abrir_ventana2(),update_combobox()], style="Bold.TButton")
mybutton8.grid(row=9, column=0, padx=10, pady=10, sticky=E)
mybutton9 = ttk.Button(Variable.app_root, text='SALIR', command=Variable.app_root.destroy, style="Bold.TButton")
mybutton9.grid(row=10, column=0, padx=10, pady=10, sticky=E)

Variable.app_root.mainloop() 