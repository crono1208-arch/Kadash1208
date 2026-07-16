import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
import Variable
import sqlite3

db_path = Variable.obtener_ruta_db()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def movimientos(frame1):
    style = ttk.Style()
    style.configure(
    "Custom.TCheckbutton",
    font=("Gotham Book", 8)

)

    frame1.grid_columnconfigure(0, weight=0)
    frame1.grid_columnconfigure(1, weight=0)
    frame1.grid_columnconfigure(2, weight=0)
            
    def mostrar_movimiento():
        # Ocultar todo primero para que no se estorben
        widgets = [
            mylabel4, amount_entry,
            mylabel5, dropdown1,
            mylabel6, dropdown2,
            mylabel7, dropdown3,
            mylabel8, dropdown4,
            mylabel9, description_entry,
            mybutton, mybutton1, mybutton2
        ]

        for widget in   widgets:
            widget.grid_remove()

        # Limpiar campos
        amount_entry.delete(0, tk.END)
        dropdown1.set("")
        dropdown2.set("")
        dropdown3.set("")
        dropdown4.set("")
        description_entry.delete(0, tk.END)

        movimiento = Variable.movimientos.get()

        if movimiento == "Ingreso":
            mylabel4.grid(row=3, column=0, padx=5, pady=4, sticky=W)
            amount_entry.grid(row=3, column=1, padx=5, pady=4, sticky=W)

            mylabel6.grid(row=6, column=0, padx=5, pady=4, sticky=W)
            dropdown2.grid(row=6, column=1, padx=5, pady=4, sticky=W)

            mylabel9.grid(row=8, column=0, padx=5, pady=4, sticky=W)
            description_entry.grid(row=8, column=1, padx=5, pady=4, sticky=W)

            mybutton.grid(row=9, column=0, padx=5, pady=4, sticky=W, columnspan=2)

        elif movimiento == "Gasto":
            mylabel4.grid(row=3, column=0, padx=5, pady=4, sticky=W)
            amount_entry.grid(row=3, column=1, padx=5, pady=4, sticky=W)

            mylabel5.grid(row=4, column=0, padx=5, pady=4, sticky=W)
            dropdown1.grid(row=4, column=1, padx=5, pady=4, sticky=W)

            mylabel7.grid(row=5, column=0, padx=5, pady=4, sticky=W)
            dropdown3.grid(row=5, column=1, padx=5, pady=4, sticky=W)

            mylabel8.grid(row=6, column=0, padx=5, pady=4, sticky=W)
            dropdown4.grid(row=6, column=1, padx=5, pady=4, sticky=W)

            mylabel9.grid(row=7, column=0, padx=5, pady=4, sticky=W)
            description_entry.grid(row=7, column=1, padx=5, pady=4, sticky=W)

            mybutton1.grid(row=8, column=0, padx=5, pady=4, sticky=W, columnspan=2)

        elif movimiento == "Transferencia":
            mylabel4.grid(row=3, column=0, padx=5, pady=4, sticky=W)
            amount_entry.grid(row=3, column=1, padx=5, pady=4, sticky=W)

            mylabel5.grid(row=4, column=0, padx=5, pady=4, sticky=W)
            dropdown1.grid(row=4, column=1, padx=5, pady=4, sticky=W)

            mylabel6.grid(row=5, column=0, padx=5, pady=4, sticky=W)
            dropdown2.grid(row=5, column=1, padx=5, pady=4, sticky=W)

            mylabel9.grid(row=7, column=0, padx=5, pady=4, sticky=W)
            description_entry.grid(row=7, column=1, padx=5, pady=4, sticky=W)

            mybutton2.grid(row=8, column=0, padx=5, pady=4, sticky=W, columnspan=2)

    cuentas_dict = {}
    categorias_dict = {}
    comercios_dict = {}
    
    def cargar_cuentas():
        nonlocal cuentas_dict
        cursor.execute("""SELECT idcuentas,nombrecuenta,termcuenta FROM cuentas""")
        cuentas_dict = {}     
        valores = []
        for idcuentas, nombrecuenta, termcuenta in cursor.fetchall():
            texto = f"{nombrecuenta} - {termcuenta}"
            valores.append(texto)
            cuentas_dict[texto] = idcuentas
        dropdown1['values'] = valores
        dropdown2['values'] = valores
        
        
    def cargar_categorias():
        nonlocal categorias_dict
        cursor.execute("""
            SELECT idcategoria, nombre FROM categorias""")
        categorias_dict = {}
        valores = []
        for idcat, nombre in cursor.fetchall():
            valores.append(nombre)
            categorias_dict[nombre] = idcat
        dropdown3['values'] = valores
        
    def cargar_comercios():
        nonlocal comercios_dict
        cursor.execute("""SELECT idcomercio, nombre FROM comercios""")
        comercios_dict = {}
        valores = []
        for idcomercio, nombre in cursor.fetchall():
            valores.append(nombre)
            comercios_dict[nombre] = idcomercio
        dropdown4['values'] = valores
        
    def obtener_saldo(id_cuenta):
        cursor.execute("""
            SELECT saldoactual
            FROM cuentas
            WHERE idcuentas = ?
        """, (id_cuenta,))

        resultado = cursor.fetchone()

        if resultado:
            return float(resultado[0])

        return 0
    
    def limpiar_formulario():

        amount_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)

        dropdown1.set("")
        dropdown2.set("")
        dropdown3.set("")
        dropdown4.set("")
       
    def guardar_ingreso():
        monto = float(amount_entry.get())       
        cursor.execute("""
            INSERT INTO movimientos (fecha, tipodemovimientoid, monto, cuentadestinoid,
            descripcion, fecharegistro, activo)
            VALUES (?,1,?,?,?,CURRENT_TIMESTAMP,1)
        """ ,
        (
            date_entry.get_date().isoformat(),
            monto,
            cuentas_dict[dropdown2.get()],
            description_entry.get()
        ))

        actualizar_saldo(
            cuentas_dict[dropdown2.get()],
            monto
        )
        try:
            conn.commit()
            limpiar_formulario()
            messagebox.showinfo(
                "Éxito",
                "Movimiento guardado correctamente."
            )

        except Exception as e:
            conn.rollback()

            messagebox.showerror(
                "Error",
                f"No fue posible guardar el movimiento.\n\n{e}"
            )
        
    def guardar_gasto():
        monto = float(amount_entry.get())
        id_cuenta = cuentas_dict[dropdown1.get()]

        saldo = obtener_saldo(id_cuenta)

        if monto > saldo:
            messagebox.showwarning(
                "Saldo insuficiente",
                "No hay saldo suficiente para realizar este gasto."
            )
            return
        cursor.execute("""INSERT INTO movimientos (fecha,tipodemovimientoid,monto,cuentaorigenid,categoriaid,comercioid,descripcion,fecharegistro,activo)
                       VALUES (?,2,?,?,?,?,?,CURRENT_TIMESTAMP,1)""",
        (date_entry.get_date().isoformat(),
         monto,
         cuentas_dict[dropdown1.get()],
         categorias_dict[dropdown3.get()],
         comercios_dict[dropdown4.get()],
         description_entry.get(),   
        ))
        actualizar_saldo(
            cuentas_dict[dropdown1.get()],
            -monto
        )   
        try:
            conn.commit()
            limpiar_formulario()
            messagebox.showinfo(
                "Éxito",
                "Movimiento guardado correctamente."
            )

        except Exception as e:
            conn.rollback()

            messagebox.showerror(
                "Error",
                f"No fue posible guardar el movimiento.\n\n{e}"
            ) 
        
    def guardar_transferencia():
        monto = float(amount_entry.get())
        id_cuenta = cuentas_dict[dropdown1.get()]

        saldo = obtener_saldo(id_cuenta)

        if monto > saldo:
            messagebox.showwarning(
                "Saldo insuficiente",
                "No hay saldo suficiente para realizar este gasto."
            )
            return
        cursor.execute("""INSERT INTO movimientos (fecha,tipodemovimientoid,monto,cuentaorigenid,cuentadestinoid,descripcion,fecharegistro,activo)
                       VALUES (?,3,?,?,?,?,CURRENT_TIMESTAMP,1)""",
        (date_entry.get_date().isoformat(),
         monto,
         cuentas_dict[dropdown1.get()],
         cuentas_dict[dropdown2.get()],
         description_entry.get(),   
        ))
        actualizar_saldo(
            cuentas_dict[dropdown1.get()],
            -monto
        )

        actualizar_saldo(
            cuentas_dict[dropdown2.get()],
            monto
        )
        try:
            conn.commit()
            limpiar_formulario()
            messagebox.showinfo(
                "Éxito",
                "Movimiento guardado correctamente."
            )

        except Exception as e:
            conn.rollback()

            messagebox.showerror(
                "Error",
                f"No fue posible guardar el movimiento.\n\n{e}"
            )
        
    def actualizar_saldo(id_cuenta, monto):
        cursor.execute("""
            UPDATE cuentas
            SET saldoactual = saldoactual + ?
            WHERE idcuentas = ?
        """, (monto, id_cuenta))
        
    # Encabezado
    mylabel = ttk.Label(frame1, text='Movimientos', font=('Gotham Bold', 12, 'bold'), width=20)
    mylabel.grid(row=0, column=0, padx=5, pady=4, sticky=W, columnspan=4)
    mylabel2 = ttk.Label(frame1, text='Fecha:', font=('Gotham Book', 8), width=15)
    mylabel2.grid(row=1, column=0, padx=5, pady=4, sticky=W)
    date_entry = DateEntry(frame1, width=12, background='darkblue', foreground='white', borderwidth=2)
    date_entry.grid(row=1, column=1, padx=5, pady=4, sticky=W, columnspan=1)
    mylabel3 = ttk.Label(frame1, text='Tipo:', font=('Gotham Book', 8), width=15)
    mylabel3.grid(row=2, column=0, padx=5, pady=4, sticky=W)
    chk1 = ttk.Radiobutton(frame1, text='Ingreso', variable=Variable.movimientos, value="Ingreso", command=lambda: [mostrar_movimiento(),cargar_cuentas()])
    chk1.grid(row=2, column=0, padx=5, pady=4, sticky=E, columnspan=1)
    chk2 = ttk.Radiobutton(frame1, text='Gasto', variable=Variable.movimientos, value="Gasto", command=lambda: [mostrar_movimiento(),cargar_cuentas(),cargar_categorias(),cargar_comercios()])
    chk2.grid(row=2, column=1, padx=5, pady=4, sticky=W, columnspan=1)
    chk3 = ttk.Radiobutton(frame1, text='Transferencia', variable=Variable.movimientos, value="Transferencia", command=lambda: [mostrar_movimiento(), cargar_cuentas()])
    chk3.grid(row=2, column=2, padx=5, pady=4, sticky=W, columnspan=1)
    mylabel4 = ttk.Label(frame1, text='Monto:', font=('Gotham Book', 8), width=12)
    amount_entry = ttk.Entry(frame1, font=('Gotham Book', 8), width=14)
    mylabel5 = ttk.Label(frame1, text='Cuenta origen:', font=('Gotham Book', 8), width=12)
    dropdown1 = ttk.Combobox(frame1, state="readonly", font=('Gotham Book', 8), width=12)
    mylabel6 = ttk.Label(frame1, text='Cuenta destino:', font=('Gotham Book', 8), width=12)
    dropdown2 = ttk.Combobox(frame1, state="readonly", font=('Gotham Book', 8), width=12)
    mylabel7 = ttk.Label(frame1, text='Categoria:', font=('Gotham Book', 8), width=12)
    dropdown3 = ttk.Combobox(frame1, state="readonly", font=('Gotham Book', 8), width=12)
    mylabel8 = ttk.Label(frame1, text='Comercio:', font=('Gotham Book', 8), width=12)
    dropdown4 = ttk.Combobox(frame1, state="readonly", font=('Gotham Book', 8), width=12)
    mylabel9 = ttk.Label(frame1, text='Descripcion:', font=('Gotham Book', 8), width=12)
    description_entry = ttk.Entry(frame1, font=('Gotham Book', 8), width=14)
    mybutton = ttk.Button(frame1, text='Guardar', style="Bold.TButton", command=guardar_ingreso)
    mybutton1 = ttk.Button(frame1, text='Guardar', style="Bold.TButton", command=guardar_gasto)
    mybutton2= ttk.Button(frame1, text='Guardar', style="Bold.TButton", command=guardar_transferencia)
