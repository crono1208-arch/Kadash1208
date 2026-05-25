import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.font import Font
import sqlite3
import os

ruta = os.path.join(os.getenv("LOCALAPPDATA"), "CotizadorTaller")

db_path = os.path.join(ruta, "taller.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def crear_ventana_auto(parent):
    # Usamos Toplevel para crear una ventana dependiente de la principal
    new_window = tk.Toplevel(parent)
    new_window.title("Catalogo de Autos")
    new_window.geometry("520x480")
    new_window.iconbitmap('images.ico')
    bold_font1 = Font(family="Gotham Book", size=10, weight="bold")
    style = ttk.Style()
    style.configure("Bold.TButton", font=bold_font1)
    mylabel = ttk.Label(new_window, text='Catalogo de Autos', font=('Gotham Book', 14, 'bold'))
    mylabel.pack(pady=5, anchor=CENTER)
    # Configurar colores de la tabla
    style.configure("Treeview", 
	    background="#FFFFFF",
	    foreground="black",
	    rowheight=25,
	    fieldbackground="#D3D3D3"
	    )
    # Cambiar color seleccionado
    style.map('Treeview', 
	background=[('selected', 'grey')])

    # Crear el marco del Treeview
    tree_frame = Frame(new_window)
    tree_frame.pack(pady=0)

    # Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Crear el Treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    # Pack to the screen
    my_tree.pack()

    #Configurar el scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Definir Columnas
    my_tree['columns'] = ("id_auto","marca", "modelo", "año", "motor", "cilindros")

    # Formato de Columnas
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("id_auto", width=0, stretch=NO)
    my_tree.column("marca", anchor=W, width=90)
    my_tree.column("modelo", anchor=W, width=90)
    my_tree.column("año", anchor=W, width=50)
    my_tree.column("motor", anchor=W, width=60)
    my_tree.column("cilindros", anchor=W, width=60)

    # Crear Encabezados 
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("id_auto", text="", anchor=W)
    my_tree.heading("marca", text="Marca", anchor=W)
    my_tree.heading("modelo", text="Modelo", anchor=W)
    my_tree.heading("año", text="Año", anchor=W)
    my_tree.heading("motor", text="Motor", anchor=W)
    my_tree.heading("cilindros", text="Cilindros", anchor=W)
    
    def load_data():
          
        # 1. Fetch all records from the table
        cursor.execute("SELECT * FROM autos ORDER BY marca ASC, modelo ASC, Año")
        rows = cursor.fetchall()
    
        # 2. Clear current treeview data (optional)
        for item in my_tree.get_children():
            my_tree.delete(item)
        
        # 3. Insert database rows into the treeview
        for row in rows:
            my_tree.insert("", tk.END, values=row)
                
    load_data()
    #crear etiquetas para cargar los datos
    data_frame = ttk.Frame(new_window)
    data_frame.pack(pady=10)

    marca_entry = ttk.Entry(data_frame, width=20)
    marca_entry.grid(row=0, column=1)

    modelo_entry = ttk.Entry(data_frame, width=20)
    modelo_entry.grid(row=0, column=3)

    anio_entry = ttk.Entry(data_frame, width=20)
    anio_entry.grid(row=1, column=1)

    motor_entry = ttk.Entry(data_frame, width=20)
    motor_entry.grid(row=1, column=3)

    cilindros_entry = ttk.Entry(data_frame, width=20)
    cilindros_entry.grid(row=2, column=1)

    ttk.Label(data_frame, text="Marca").grid(row=0, column=0)
    ttk.Label(data_frame, text="Modelo").grid(row=0, column=2)
    ttk.Label(data_frame, text="Año").grid(row=1, column=0)
    ttk.Label(data_frame, text="Motor").grid(row=1, column=2)
    ttk.Label(data_frame, text="Cilindros").grid(row=2, column=0)
    
    #carga los datos del auto seleccionado 
    def select_record():

        marca_entry.delete(0, END)
        modelo_entry.delete(0, END)
        anio_entry.delete(0, END)
        motor_entry.delete(0, END)
        cilindros_entry.delete(0, END)

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        marca_entry.insert(0, values[1])
        modelo_entry.insert(0, values[2])
        anio_entry.insert(0, values[3])
        motor_entry.insert(0, values[4])
        cilindros_entry.insert(0, values[5])
    
    my_tree.bind("<ButtonRelease-1>", lambda e: select_record())
    
    #Limpia los campos para nuevos datos
    def clear_entries():

        marca_entry.delete(0, END)
        modelo_entry.delete(0, END)
        anio_entry.delete(0, END)
        motor_entry.delete(0, END)
        cilindros_entry.delete(0, END)
        
        conn.commit()
        
        load_data()
        
    #Agrega nuevo registro a la base de datos    
    def add_record():

        cursor.execute("""
        INSERT INTO autos (marca, modelo, año, motor, cilindros)
        VALUES (?, ?, ?, ?, ?)
        """,(
        marca_entry.get(),
        modelo_entry.get(),
        anio_entry.get(),
        motor_entry.get(),
        cilindros_entry.get()
    ))   
        conn.commit()
        load_data()
        clear_entries()
    
    #Actualiza cambios realizados a los datos
    def update_record():

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        cursor.execute("""
        UPDATE autos
        SET marca=?, modelo=?, año=?, motor=?, cilindros=?
            WHERE id_auto=?
    """,(
            marca_entry.get(),
            modelo_entry.get(),
            anio_entry.get(),
            motor_entry.get(),
            cilindros_entry.get(),
            values[0]
    ))

        conn.commit()
        load_data()
        clear_entries()
    
    def delete_record():

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        cursor.execute("DELETE FROM autos WHERE id_auto=?", (values[0],))    
  
        conn.commit()
        load_data()
        clear_entries()
    #Frame para los botones de control
    button_frame = Frame(new_window)
    button_frame.pack(pady=10)
    #Botones de control
    add_btn = ttk.Button(button_frame, text="Agregar", command=add_record, style="Bold.TButton")
    add_btn.grid(row=0, column=0, padx=5)
    update_btn = ttk.Button(button_frame, text="Modificar", command=update_record, style="Bold.TButton")
    update_btn.grid(row=0, column=1, padx=5)
    delete_btn = ttk.Button(button_frame, text="Eliminar", command=delete_record, style="Bold.TButton")
    delete_btn.grid(row=0, column=2, padx=5)
    clear_btn = ttk.Button(button_frame, text="Limpiar", command=clear_entries, style="Bold.TButton")
    clear_btn.grid(row=0, column=3, padx=5)    
    button_close = ttk.Button(new_window, text="Cerrar", command=new_window.destroy, style="Bold.TButton")
    button_close.pack(pady=0, side=RIGHT)