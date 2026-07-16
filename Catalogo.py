import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import Variable
import sqlite3

db_path = Variable.obtener_ruta_db()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def catalogos(frame2):
    style = ttk.Style()
    style.configure(
    "Custom.TCheckbutton",
    font=("Gotham Book", 8)

)

    frame2.grid_columnconfigure(0, weight=0)
    frame2.grid_columnconfigure(1, weight=0)
    frame2.grid_columnconfigure(2, weight=0)

    def cargar_catalogo(filtro=""):
        if Variable.catalogo.get() == "Bancos":
            consulta = """SELECT idbanco, nombre, activo FROM bancos WHERE nombre LIKE ? ORDER BY "Nombre" ASC"""

        elif Variable.catalogo.get() == "Cuentas":
            consulta = """SELECT idcuentas, nombrecuenta, activo FROM cuentas WHERE nombrecuenta LIKE ? ORDER BY nombrecuenta ASC"""

        elif Variable.catalogo.get() == "Categorias":
            consulta = """SELECT idcategoria, nombre, activo FROM categorias WHERE nombre LIKE ? ORDER BY "Nombre" ASC"""

        elif Variable.catalogo.get() == "Comercios":
            consulta = """SELECT idcomercio, nombre, activo FROM comercios WHERE nombre LIKE ? ORDER BY "Nombre" ASC"""
            
        tree.delete(*tree.get_children())

        tree["columns"] = ("Nombre", "Estatus")

        tree.heading("Nombre", text="Nombre")
        tree.heading("Estatus", text="Estatus")

        tree.column("Nombre", width=200)
        tree.column("Estatus", width=100, anchor=CENTER)

        cursor.execute(consulta, (f"%{filtro}%",))

        for i, fila in enumerate(cursor.fetchall()):

            color = "par" if i % 2 == 0 else "impar"
            estatus = "Activo" if fila[2] else "Desactivo"

            tree.insert(
                "",
                "end",
                iid=fila[0],          # idbancos
                values=(fila[1], estatus),
                tags=(color,)
            )
            tree.bind("<Double-1>", lambda event: editar_registro())

    def abrir_ventana_catalogo_simple(tipo, id_registro=None):
        catalogos = {
            "Bancos": ("bancos", "idbanco", "nombre"),
            "Categorias": ("categorias", "idcategoria", "nombre"),
            "Comercios": ("comercios", "idcomercio", "nombre")
        }

        tabla, idcampo, campo_nombre = catalogos[tipo]

        ventana = tk.Toplevel(Variable.app_root)
        ventana.title(f"Catalogo de {tipo}")
        ventana.geometry("250x220")

        ttk.Label(
            ventana,
            text=f"Catalogo de {tipo}",
            font=('Gotham Bold', 12, 'bold')
        ).grid(row=0, column=0, padx=5, pady=4, sticky=W)

        ttk.Separator(ventana, orient='horizontal').grid(
            row=1, column=0, sticky='ew', padx=5, pady=4
        )

        ttk.Label(
            ventana,
            text='Nombre',
            font=('Gotham Bold', 8, 'bold')
        ).grid(row=2, column=0, padx=5, pady=4, sticky=W)

        nombre_entry = ttk.Entry(ventana, font=('Gotham Book', 10))
        nombre_entry.grid(row=3, column=0, padx=5, pady=4, sticky=W)

        if id_registro is not None:
            cursor.execute(
                f"SELECT {campo_nombre} FROM {tabla} WHERE {idcampo} = ?",
                (id_registro,)
            )
            datos = cursor.fetchone()

            if datos:
                nombre_entry.insert(0, datos[0])

        def guardar_catalogo():
            nombre = nombre_entry.get().strip()

            if not nombre:
                messagebox.showwarning("Validacion", "El nombre no puede estar vacio")
                return

            if id_registro is None:
                cursor.execute(
                    f"INSERT INTO {tabla} ({campo_nombre}) VALUES (?)",
                    (nombre,)
                )

            else:
                cursor.execute(
                    f"UPDATE {tabla} SET {campo_nombre} = ? WHERE {idcampo} = ?",
                    (nombre, id_registro)
                )

            conn.commit()
            ventana.destroy()
            cargar_catalogo()

        ttk.Separator(ventana, orient='horizontal').grid(
            row=4, column=0, sticky='ew', padx=5, pady=4)

        ttk.Button(
            ventana,
            text="Guardar",
            command=guardar_catalogo
        ).grid(row=5, column=0, padx=5, pady=4, sticky=W)

        ttk.Button(
            ventana,
            text="Cancelar",
            command=ventana.destroy
        ).grid(row=5, column=0, padx=5, pady=4, sticky=E)
    
    def abrir_ventana_catalogo_cuentas(id_registro=None):
        ventana = tk.Toplevel(Variable.app_root)
        ventana.title("Catalogo de Cuentas")
        ventana.geometry("250x550")

        encabezado = ttk.Label(ventana, text="Catalogo de Cuentas", font=('Gotham Bold', 12, 'bold'))
        encabezado.grid(row=0, column=0, padx=5, pady=4, sticky=W)

        separator = ttk.Separator(ventana, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=3, sticky='ew', padx=5, pady=4)

        nombre_label = ttk.Label(ventana, text='Nombre', font=('Gotham Bold', 8, 'bold'))
        nombre_label.grid(row=2, column=0, padx=5, pady=4, sticky=W)

        nombre_entry = ttk.Entry(ventana, font=('Gotham Book', 10))
        nombre_entry.grid(row=3, column=0, padx=5, pady=4, sticky=W)

        banco_label = ttk.Label(ventana, text='Banco', font=('Gotham Bold', 8, 'bold'))
        banco_label.grid(row=4, column=0, padx=5, pady=4, sticky=W)

        banco_combobox = ttk.Combobox(ventana, font=('Gotham Book', 10))
        banco_combobox.grid(row=5, column=0, padx=5, pady=4, sticky=W)

        cursor.execute("SELECT nombre FROM bancos")
        bancos = cursor.fetchall()
        banco_combobox['values'] = [banco[0] for banco in bancos]

        terminacion_label = ttk.Label(ventana, text='Terminacion', font=('Gotham Bold', 8, 'bold'))
        terminacion_label.grid(row=6, column=0, padx=5, pady=4, sticky=W)

        terminacion_entry = ttk.Entry(ventana, font=('Gotham Book', 10))
        terminacion_entry.grid(row=7, column=0, padx=5, pady=4, sticky=W)

        tipocuenta_label = ttk.Label(ventana, text='Tipo de Cuenta', font=('Gotham Bold', 8, 'bold'))
        tipocuenta_label.grid(row=8, column=0, padx=5, pady=4, sticky=W)

        tipocuenta_combobox = ttk.Combobox(ventana, font=('Gotham Book', 10))
        tipocuenta_combobox.grid(row=9, column=0, padx=5, pady=4, sticky=W)

        cursor.execute("SELECT nombre FROM tipocuenta")
        tipos_cuenta = cursor.fetchall()
        tipocuenta_combobox['values'] = [tipo[0] for tipo in tipos_cuenta]

        saldo_label = ttk.Label(ventana, text='Saldo Inicial', font=('Gotham Bold', 8, 'bold'))
        saldo_label.grid(row=10, column=0, padx=5, pady=4, sticky=W)

        saldo_entry = ttk.Entry(ventana, font=('Gotham Book', 10))
        saldo_entry.grid(row=11, column=0, padx=5, pady=4, sticky=W)

        if id_registro is not None:
            cursor.execute("""
                SELECT 
                    c.nombrecuenta,
                    b.nombre,
                    c.termcuenta,
                    t.nombre,
                    c.saldoinicial
                FROM cuentas c
                LEFT JOIN bancos b ON b.idbanco = c.bancoid
                LEFT JOIN tipocuenta t ON t.idtipocuenta = c.tipocuentaid
                WHERE c.idcuentas = ?
            """, (id_registro,))

            datos = cursor.fetchone()

            if datos:
                nombre_entry.insert(0, datos[0])
                banco_combobox.set(datos[1])
                terminacion_entry.insert(0, datos[2])
                tipocuenta_combobox.set(datos[3])
                saldo_entry.insert(0, datos[4])

        def guardar_catalogo_cuentas():
            nombre = nombre_entry.get().strip()
            banco = banco_combobox.get().strip()
            terminacion = terminacion_entry.get().strip()
            tipocuenta = tipocuenta_combobox.get().strip()
            saldo = saldo_entry.get().strip()

            if not nombre or not banco or not tipocuenta or not saldo:
                messagebox.showwarning("Validacion", "Completa los campos obligatorios")
                return

            cursor.execute("SELECT idbanco FROM bancos WHERE nombre = ?", (banco,))
            banco_resultado = cursor.fetchone()

            cursor.execute("SELECT idtipocuenta FROM tipocuenta WHERE nombre = ?", (tipocuenta,))
            tipocuenta_resultado = cursor.fetchone()

            if not banco_resultado or not tipocuenta_resultado:
                messagebox.showwarning("Validacion", "Banco o tipo de cuenta no valido")
                return

            banco_id = banco_resultado[0]
            tipocuenta_id = tipocuenta_resultado[0]

            if id_registro is None:
                cursor.execute("""
                    INSERT INTO cuentas 
                    (nombrecuenta, bancoid, termcuenta, tipocuentaid, saldoinicial, saldoactual)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (nombre, banco_id, terminacion, tipocuenta_id, saldo, saldo))
            else:
                cursor.execute("""
                    UPDATE cuentas
                    SET nombrecuenta = ?,
                        bancoid = ?,
                        termcuenta = ?,
                        tipocuentaid = ?,
                        saldoinicial = ?
                    WHERE idcuentas = ?
                """, (nombre, banco_id, terminacion, tipocuenta_id, saldo, id_registro))

            conn.commit()
            ventana.destroy()
            cargar_catalogo()

        separator2 = ttk.Separator(ventana, orient='horizontal')
        separator2.grid(row=12, column=0, columnspan=3, sticky='ew', padx=5, pady=4)

        btn_guardar = ttk.Button(ventana, text="Guardar", command=guardar_catalogo_cuentas)
        btn_guardar.grid(row=13, column=0, padx=5, pady=4, sticky=W)

        btn_cancelar = ttk.Button(ventana, text="Cancelar", command=ventana.destroy)
        btn_cancelar.grid(row=13, column=0, padx=5, pady=4, sticky=E)
    
    def buscar(event):
        cargar_catalogo(busqueda_entry.get())
    
    mylabel1 = ttk.Label(frame2, text='Catalogos', font=('Gotham Bold', 12, 'bold'))
    mylabel1.grid(row=0, column=0, padx=5, pady=4, sticky=W)
    mylabel2 = ttk.Label(frame2, text='Seleccione una opción para comenzar', font=('Gotham Book', 10))
    mylabel2.grid(row=1, column=0, padx=5, pady=4, sticky=W)
    chk1 = ttk.Radiobutton(frame2, text="Bancos", value="Bancos", variable=Variable.catalogo, command=cargar_catalogo)
    chk1.grid(row=2, column=0, padx=5, pady=4, sticky=W)
    chk2 = ttk.Radiobutton(frame2, text="Cuentas", value="Cuentas", variable=Variable.catalogo, command=cargar_catalogo)
    chk2.grid(row=2, column=1, padx=5, pady=4, sticky=W)
    chk3 = ttk.Radiobutton(frame2, text="Categorias", value="Categorias", variable=Variable.catalogo, command=cargar_catalogo)
    chk3.grid(row=3, column=0, padx=5, pady=4, sticky=W)
    chk4 = ttk.Radiobutton(frame2, text="Comercios", value="Comercios", variable=Variable.catalogo, command=cargar_catalogo)
    chk4.grid(row=3, column=1, padx=5, pady=4, sticky=W)
    separator = ttk.Separator(frame2, orient='horizontal')
    separator.grid(row=4, column=0, columnspan=3, sticky='ew', padx=5, pady=4)
    busqueda_label = ttk.Label(frame2, text='Busqueda', font=('Gotham Bold', 8, 'bold'))
    busqueda_label.grid(row=5, column=0, padx=5, pady=4, sticky=W)
    busqueda_entry = ttk.Entry(frame2, font=('Gotham Book', 10))
    busqueda_entry.grid(row=5, column=0, padx=5, pady=4, sticky=E)
    busqueda_entry.bind("<KeyRelease>", buscar)
    style.configure("Treeview", 
	    background="#FFFFFF",
	    foreground="black",
	    rowheight=5,
	    fieldbackground="#D3D3D3"
	    )
        # Cambiar color seleccionado
    style.map('Treeview',
	    background=[('selected', 'grey')])
    tree = ttk.Treeview(frame2, show="headings", height=4)
    tree.grid(row=6, column=0, columnspan=2, padx=5, pady=4, sticky=W)
    tree.tag_configure("par", background="#FFFFFF")
    tree.tag_configure("impar", background="#F5F5F5")
    def obtener_id_seleccionado():
        seleccion = tree.selection()

        if not seleccion:
            messagebox.showwarning("Seleccion requerida", "Selecciona un registro primero")
            return None

        return seleccion[0]


    def nuevo_registro():
        tipo = Variable.catalogo.get()

        if tipo == "Cuentas":
            abrir_ventana_catalogo_cuentas()
        else:
            abrir_ventana_catalogo_simple(tipo)


    def editar_registro():
        tipo = Variable.catalogo.get()
        id_registro = obtener_id_seleccionado()

        if id_registro is None:
            return

        if tipo == "Cuentas":
            abrir_ventana_catalogo_cuentas(id_registro)
        else:
            abrir_ventana_catalogo_simple(tipo, id_registro)


    btn_nuevo = ttk.Button(frame2, text="Nuevo", command=nuevo_registro)
    btn_nuevo.grid(row=7, column=0, padx=5, pady=4, sticky=W)

    btn_editar = ttk.Button(frame2, text="Editar", command=editar_registro)
    btn_editar.grid(row=7, column=0, padx=5, pady=4, sticky=E)
    
    def activar_desactivar_registro():
        tipo = Variable.catalogo.get()
        id_registro = obtener_id_seleccionado()

        if id_registro is None:
            return

        if tipo == "Cuentas":
            cursor.execute("SELECT activo FROM cuentas WHERE idcuentas = ?", (id_registro,))
            estado_actual = cursor.fetchone()[0]
            nuevo_estado = 0 if estado_actual else 1
            cursor.execute("UPDATE cuentas SET activo = ? WHERE idcuentas = ?", (nuevo_estado, id_registro))
        else:
            tabla, idcampo, _ = {
                "Bancos": ("bancos", "idbanco", "nombre"),
                "Categorias": ("categorias", "idcategoria", "nombre"),
                "Comercios": ("comercios", "idcomercio", "nombre")
            }[tipo]

            cursor.execute(f"SELECT activo FROM {tabla} WHERE {idcampo} = ?", (id_registro,))
            estado_actual = cursor.fetchone()[0]
            nuevo_estado = 0 if estado_actual else 1
            cursor.execute(f"UPDATE {tabla} SET activo = ? WHERE {idcampo} = ?", (nuevo_estado, id_registro))

        conn.commit()
        cargar_catalogo()
        
    btn_activar = ttk.Button(frame2, text="Activar/Desactivar", command=activar_desactivar_registro)
    btn_activar.grid(row=7, column=1, padx=5, pady=4, sticky=W)
