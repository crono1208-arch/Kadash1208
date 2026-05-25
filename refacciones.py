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

def crear_ventana_refa(parent):
    # Usamos Toplevel para crear una ventana dependiente de la principal
    new_window = tk.Toplevel(parent)
    new_window.title("Catalogo de Refacciones")
    new_window.geometry("520x480")
    new_window.iconbitmap('images.ico')
    bold_font1 = Font(family="Gotham Book", size=10, weight="bold")
    style = ttk.Style()
    style.configure("Bold.TButton", font=bold_font1)
    mylabel = ttk.Label(new_window, text='Catalogo de Refacciones', font=('Gotham Book', 14, 'bold'))
    mylabel.pack(pady=5, anchor=CENTER)
    # Configurar colores de la tabla
    style.configure("Treeview", 
	    background="#FFFFFF",
	    foreground="black",
	    rowheight=25,
	    fieldbackground="#D3D3D3"
	    )
    # Cambiar color de seleccion
    style.map('Treeview', 
	    background=[('selected', 'grey')])

    # Crear marco del treeview
    tree_frame = Frame(new_window)
    tree_frame.pack(pady=0)

    # Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Crear Treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    # Pack to the screen
    my_tree.pack()

    #Configurar el scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Definir Columnas
    my_tree['columns'] = ("id_refaccion","numero_parte", "descripcion", "marca", "precio")

    # Formato de Columnas
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("id_refaccion", width=0, stretch=NO)
    my_tree.column("numero_parte", anchor=W, width=80)
    my_tree.column("descripcion", anchor=W, width=120)
    my_tree.column("marca", anchor=W, width=80)
    my_tree.column("precio", anchor=W, width=60)

    # Crear Encabezados 
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("id_refaccion", text="", anchor=W)
    my_tree.heading("numero_parte", text="Numero Parte", anchor=W)
    my_tree.heading("descripcion", text="Descripcion", anchor=CENTER)
    my_tree.heading("marca", text="Marca", anchor=W)
    my_tree.heading("precio", text="precio", anchor=W)
    
    def load_data():
          
        # 1. Fetch all records from the table
        cursor.execute("SELECT * FROM refacciones ORDER BY descripcion ASC")
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

    numero_parte_entry = ttk.Entry(data_frame, width=20)
    numero_parte_entry.grid(row=0, column=1)

    descripcion_entry = ttk.Entry(data_frame, width=20)
    descripcion_entry.grid(row=0, column=3)

    marca_entry = ttk.Entry(data_frame, width=20)
    marca_entry.grid(row=1, column=1)

    precio_entry = ttk.Entry(data_frame, width=20)
    precio_entry.grid(row=1, column=3)

    ttk.Label(data_frame, text="Numero de Parte").grid(row=0, column=0)
    ttk.Label(data_frame, text="Descripción").grid(row=0, column=2)
    ttk.Label(data_frame, text="Marca").grid(row=1, column=0)
    ttk.Label(data_frame, text="Precio").grid(row=1, column=2)
    
    #carga los datos de la refacción seleccionada 
    def select_record():

        numero_parte_entry.delete(0, END)
        descripcion_entry.delete(0, END)
        marca_entry.delete(0, END)
        precio_entry.delete(0, END)
        
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        numero_parte_entry.insert(0, values[1])
        descripcion_entry.insert(0, values[2])
        marca_entry.insert(0, values[3])
        precio_entry.insert(0, values[4])
        
    my_tree.bind("<ButtonRelease-1>", lambda e: select_record())

    #Limpia los campos para nuevos datos
    def clear_entries():

        numero_parte_entry.delete(0, END)
        descripcion_entry.delete(0, END)
        marca_entry.delete(0, END)
        precio_entry.delete(0, END)
        
    #Agrega nuevo registro a la base de datos    
    def add_record():

        cursor.execute("""
        INSERT INTO refacciones (numero_parte, descripcion, marca, precio)
        VALUES (?, ?, ?, ?)
        """,(
        numero_parte_entry.get(),
        descripcion_entry.get(),
        marca_entry.get(),
        precio_entry.get(),
    ))
        conn.commit()
        load_data()
        clear_entries()        
    
    #Actualiza cambios realizados a los datos
    def update_record():

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        cursor.execute("""
        UPDATE refacciones
        SET numero_parte=?, descripcion=?, marca=?, precio=?
            WHERE id_refaccion=?
    """,(
            numero_parte_entry.get(),
            descripcion_entry.get(),
            marca_entry.get(),
            precio_entry.get(),
            values[0]
    ))
        conn.commit()
        load_data()
        clear_entries()

    def delete_record():

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        cursor.execute("DELETE FROM refacciones WHERE id_refaccion=?", (values[0],))    
  
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