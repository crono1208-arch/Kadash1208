import tkinter as tk
from tkinter import *
import sqlite3
import Variable
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
import Movimientos
import Catalogo
import Dashboard


db_path = Variable.obtener_ruta_db()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

#Configuración de la ventana principal
Variable.app_root = tk.Tk()
Variable.app_root.title("Presupuestador Personal")
Variable.app_root.geometry("800x750")
bold_font1 = Font(family="Gotham Book",size=8, weight="bold")
style = ttk.Style()
style.configure("Bold.TButton", font=bold_font1)
Variable.app_root.grid_columnconfigure(0, weight=1)
Variable.app_root.grid_columnconfigure(1, weight=3)
Variable.app_root.grid_rowconfigure(3, weight=0)
   
#Declaracion de variables globales
Variable.movimientos = tk.StringVar(value="")
Variable.catalogo = tk.StringVar(value="")


#Encabezado
mylabel = ttk.Label(Variable.app_root, text='Presupuestador Personal', font=('Gotham Bold', 16, 'bold'))
mylabel.grid(row=0, column=1, columnspan=2, padx=5, pady=4, sticky=W)
mylabel2 = ttk.Label(Variable.app_root, text='Bienvenido', font=('Gotham Book', 12, 'bold'))
mylabel2.grid(row=1, column=0, columnspan=2, padx=5, pady=4, sticky=W)
mylabel3 = ttk.Label(Variable.app_root, text='Seleccione una opción para comenzar', font=('Gotham Book', 8))
mylabel3.grid(row=2, column=0, columnspan=2, padx=5, pady=4, sticky=W)

def balancetotal():
    cursor.execute("""
        SELECT IFNULL(SUM(saldoactual), 0)
        FROM cuentas
    """)

    return cursor.fetchone()[0]

def total_ingresos_hoy():
    cursor.execute("""SELECT IFNULL(SUM(monto),0)
		FROM movimientos
		WHERE tipodemovimientoid = 1
		AND fecha = DATE('now','localtime')
		AND activo = 1""")
    return cursor.fetchone()[0]

def total_gastos_hoy():
    cursor.execute("""SELECT IFNULL(SUM(monto),0)
		FROM movimientos
		WHERE tipodemovimientoid = 2
		AND fecha = DATE('now','localtime')
		AND activo = 1""")
    return cursor.fetchone()[0]

def actualizar_resumen():
    mylabel6.config(text=f"${balancetotal():,.2f}")
    mylabel8.config(text=f"${total_ingresos_hoy():,.2f}")
    mylabel10.config(text=f"${total_gastos_hoy():,.2f}")
    

def actualizar_saldos_cuentas():

    # Borrar lo que ya exista
    for widget in frame_cuentas.winfo_children():
        widget.destroy()

    cursor.execute("""
        SELECT nombrecuenta,
               termcuenta,
               saldoactual
        FROM cuentas
        WHERE activo = 1
        ORDER BY nombrecuenta DESC
    """)

    fila = 0

    for nombre, terminacion, saldo in cursor.fetchall():

        ttk.Label(
            frame_cuentas,
            text=f"{nombre} - {terminacion}",
            font=("Gotham Book",8)
        ).grid(row=fila, column=0, sticky="w")

        ttk.Label(
            frame_cuentas,
            text=f"${saldo:,.2f}",
            font=("Gotham Book",8,"bold")
        ).grid(row=fila, column=1, sticky="e", padx=10)

        fila += 1

#Resumen
resumen_frame = ttk.LabelFrame(Variable.app_root, text="Resumen", padding=10)
resumen_frame.grid( row=3, column=0, sticky="ns", padx=5, pady=4,ipadx=30, ipady=10)
mylabel4= ttk.Label(resumen_frame,	text="Resumen", font=('Gotham Book', 8, 'bold'))
mylabel4.grid(row=3, column=0, padx=5, pady=4, sticky=W)
separator = ttk.Separator(resumen_frame, orient='horizontal')
separator.grid(row=4, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
mylabel5 = ttk.Label(resumen_frame, text="Balance total:", font=('Gotham Book', 8, 'bold'))
mylabel5.grid(row=5, column=0, padx=5, pady=4, sticky=W)
mylabel6 = ttk.Label(resumen_frame, text=f"${balancetotal():,.2f}")
mylabel6.grid(row=6, column=0, padx=5, pady=4, sticky=W)
mylabel7 = ttk.Label(resumen_frame, text="Ingresos Dia de Hoy:", font=('Gotham Book', 8, 'bold'))
mylabel7.grid(row=7, column=0, padx=5, pady=4, sticky=W)
mylabel8 = ttk.Label(resumen_frame, text=f"${total_ingresos_hoy():,.2f}")
mylabel8.grid(row=8, column=0, padx=5, pady=4, sticky=W)
mylabel9 = ttk.Label(resumen_frame, text="Gastos Dia de Hoy:", font=('Gotham Book', 8, 'bold'))
mylabel9.grid(row=9, column=0, padx=5, pady=4, sticky=W)
mylabel10 = ttk.Label(resumen_frame, text=f"${total_gastos_hoy():,.2f}")
mylabel10.grid(row=10, column=0, padx=5, pady=4, sticky=W)
frame_cuentas = ttk.Frame(resumen_frame)
frame_cuentas.grid(row=13, column=0, sticky="w", padx=5, pady=4)
separator2 = ttk.Separator(resumen_frame, orient='horizontal')
separator2.grid(row=12, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
mylabel11 = ttk.Label(resumen_frame, text="Saldos por Cuenta:", font=('Gotham Book', 8, 'bold'))
mylabel11.grid(row=11, column=0, padx=5, pady=4, sticky=W)

    # Crear el Notebook (contenedor de pestañas)
notebook = ttk.Notebook(Variable.app_root)
notebook.grid(
    row=3,
    column=1,
    sticky="nsew",
    padx=5,
    pady=4
)

# Crear los marcos (frames) para cada pestaña
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
frame3 = ttk.Frame(notebook)

# Añadir los marcos al notebook
notebook.add(frame1, text="Movimientos")
notebook.add(frame2, text="Catalogos")
notebook.add(frame3, text="Reportes")

Movimientos.movimientos(frame1)
Catalogo.catalogos(frame2)
Dashboard.dashboard(frame3)

mylabel12 = ttk.Label(Variable.app_root, text='Movimientos Recientes', font=('Gotham Bold', 10, 'bold'), width=20)
mylabel12.grid(row=13, column=0, padx=5, pady=4, sticky=W)
style.configure("Treeview", 
	    background="#FFFFFF",
	    foreground="black",
	    rowheight=18,
	    fieldbackground="#D3D3D3"
	    )
        # Cambiar color seleccionado
style.map('Treeview', 
	background=[('selected', 'grey')]) 
tree = ttk.Treeview(Variable.app_root, columns=("Fecha", "Tipo", "Monto"), show="headings", selectmode="extended")
tree.heading("Fecha", text="Fecha")
tree.heading("Tipo", text="Tipo")
tree.heading("Monto", text="Monto")

tree.grid(row=14, column=0, columnspan=2, padx=5, pady=4, sticky=W)
tree.tag_configure("par", background="#FFFFFF")
tree.tag_configure("impar", background="#F5F5F5")
tree.tag_configure("ingreso", foreground="green")
tree.tag_configure("gasto", foreground="red")
tree.tag_configure("transferencia", foreground="blue")
tree.bind("<Double-1>", lambda event: editar_movimiento())


TIPO_INGRESO = 1
TIPO_GASTO = 2
TIPO_TRANSFERENCIA = 3


def ajustar_saldo_movimiento(movimiento, signo):
    tipo = movimiento["tipodemovimientoid"]
    monto = float(movimiento["monto"])

    cuenta_origen = movimiento["cuentaorigenid"]
    cuenta_destino = movimiento["cuentadestinoid"]

    if tipo == TIPO_INGRESO:
        cursor.execute(
            "UPDATE cuentas SET saldoactual = saldoactual + ? WHERE idcuentas = ?",
            (monto * signo, cuenta_destino)
        )

    elif tipo == TIPO_GASTO:
        cursor.execute(
            "UPDATE cuentas SET saldoactual = saldoactual - ? WHERE idcuentas = ?",
            (monto * signo, cuenta_origen)
        )

    elif tipo == TIPO_TRANSFERENCIA:
        cursor.execute(
            "UPDATE cuentas SET saldoactual = saldoactual - ? WHERE idcuentas = ?",
            (monto * signo, cuenta_origen)
        )
        cursor.execute(
            "UPDATE cuentas SET saldoactual = saldoactual + ? WHERE idcuentas = ?",
            (monto * signo, cuenta_destino)
        )

def editar_movimiento():
    seleccion = tree.selection()

    if not seleccion:
        messagebox.showwarning("Seleccion requerida", "Selecciona un movimiento primero")
        return

    id_movimiento = seleccion[0]

    cursor.execute("""
        SELECT 
            fecha,
            tipodemovimientoid,
            monto,
            cuentaorigenid,
            cuentadestinoid,
            categoriaid,
            comercioid,
            descripcion,
            activo
        FROM movimientos
        WHERE idmovimiento = ?
    """, (id_movimiento,))

    datos = cursor.fetchone()

    if not datos:
        messagebox.showwarning("No encontrado", "No se encontro el movimiento seleccionado")
        return

    movimiento_original = {
        "fecha": datos[0],
        "tipodemovimientoid": datos[1],
        "monto": datos[2],
        "cuentaorigenid": datos[3],
        "cuentadestinoid": datos[4],
        "categoriaid": datos[5],
        "comercioid": datos[6],
        "descripcion": datos[7],
        "activo": datos[8]
    }

    def mostrar_campos_por_tipo(event=None):
        tipo_id = obtener_id_combo(tipo_combobox)

        cuenta_origen_label.grid_remove()
        cuenta_origen_combobox.grid_remove()
        cuenta_destino_label.grid_remove()
        cuenta_destino_combobox.grid_remove()
        categoria_label.grid_remove()
        categoria_combobox.grid_remove()
        comercio_label.grid_remove()
        comercio_combobox.grid_remove()

        if tipo_id == TIPO_INGRESO:
            cuenta_destino_label.grid()
            cuenta_destino_combobox.grid()

        elif tipo_id == TIPO_GASTO:
            cuenta_origen_label.grid()
            cuenta_origen_combobox.grid()
            categoria_label.grid()
            categoria_combobox.grid()
            comercio_label.grid()
            comercio_combobox.grid()

        elif tipo_id == TIPO_TRANSFERENCIA:
            cuenta_origen_label.grid()
            cuenta_origen_combobox.grid()
            cuenta_destino_label.grid()
            cuenta_destino_combobox.grid()
        
    ventana_editar = tk.Toplevel(Variable.app_root)
    ventana_editar.title("Editar Movimiento")
    ventana_editar.geometry("350x300")
    
    def cargar_opciones(combo, consulta, id_actual=None):
        cursor.execute(consulta)
        registros = cursor.fetchall()

        valores = [f"{registro[0]} - {registro[1]}" for registro in registros]
        combo["values"] = valores

        if id_actual is not None:
            for valor in valores:
                if valor.startswith(f"{id_actual} - "):
                    combo.set(valor)
                    break


    def obtener_id_combo(combo):
        valor = combo.get()

        if not valor:
            return None

        return int(valor.split(" - ")[0])


    ttk.Label(ventana_editar, text="Fecha").grid(row=0, column=0, padx=5, pady=5, sticky=W)
    fecha_entry = ttk.Entry(ventana_editar)
    fecha_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)    
    fecha_entry.insert(0, movimiento_original["fecha"])

    ttk.Label(ventana_editar, text="Tipo").grid(row=1, column=0, padx=5, pady=5, sticky=W) 
    tipo_combobox = ttk.Combobox(ventana_editar, state="readonly")
    tipo_combobox.grid(row=1, column=1, padx=5, pady=5, sticky=W)
    cargar_opciones(
        tipo_combobox,
        "SELECT idtipodemovimiento, nombre FROM tipodemovimiento",
        movimiento_original["tipodemovimientoid"]
    )

    ttk.Label(ventana_editar, text="Monto").grid(row=2, column=0, padx=5, pady=5, sticky=W)
    monto_entry = ttk.Entry(ventana_editar)
    monto_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)
    monto_entry.insert(0, movimiento_original["monto"])

    cuenta_origen_label = ttk.Label(ventana_editar, text="Cuenta Origen")
    cuenta_origen_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)
    cuenta_origen_combobox = ttk.Combobox(ventana_editar, state="readonly")
    cuenta_origen_combobox.grid(row=3, column=1, padx=5, pady=5, sticky=W)
    cargar_opciones(
        cuenta_origen_combobox,
        "SELECT idcuentas, nombrecuenta FROM cuentas WHERE activo = 1",
        movimiento_original["cuentaorigenid"]
    )

    cuenta_destino_label = ttk.Label(ventana_editar, text="Cuenta Destino")
    cuenta_destino_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)
    cuenta_destino_combobox = ttk.Combobox(ventana_editar, state="readonly")
    cuenta_destino_combobox.grid(row=4, column=1, padx=5, pady=5, sticky=W)
    cargar_opciones(
        cuenta_destino_combobox,
        "SELECT idcuentas, nombrecuenta FROM cuentas WHERE activo = 1",
        movimiento_original["cuentadestinoid"]
    )

    categoria_label = ttk.Label(ventana_editar, text="Categoria")
    categoria_label.grid(row=5, column=0, padx=5, pady=5, sticky=W)
    categoria_combobox = ttk.Combobox(ventana_editar, state="readonly")
    categoria_combobox.grid(row=5, column=1, padx=5, pady=5, sticky=W)
    cargar_opciones(
        categoria_combobox,
        "SELECT idcategoria, nombre FROM categorias WHERE activo = 1",
        movimiento_original["categoriaid"]
    )

    comercio_label = ttk.Label(ventana_editar, text="Comercio")
    comercio_label.grid(row=6, column=0, padx=5, pady=5, sticky=W)
    comercio_combobox = ttk.Combobox(ventana_editar, state="readonly")
    comercio_combobox.grid(row=6, column=1, padx=5, pady=5, sticky=W)
    cargar_opciones(
        comercio_combobox,
        "SELECT idcomercio, nombre FROM comercios WHERE activo = 1",
        movimiento_original["comercioid"]
    )

    ttk.Label(ventana_editar, text="Descripcion").grid(row=7, column=0, padx=5, pady=5, sticky=W)
    descripcion_entry = ttk.Entry(ventana_editar)
    descripcion_entry.grid(row=7, column=1, padx=5, pady=5, sticky=W)
    descripcion_entry.insert(0, movimiento_original["descripcion"] or "")

    def guardar_movimiento_editado():
        tipo_id = obtener_id_combo(tipo_combobox)

        movimiento_nuevo = {
            "fecha": fecha_entry.get(),
            "tipodemovimientoid": tipo_id,
            "monto": float(monto_entry.get()),
            "cuentaorigenid": None,
            "cuentadestinoid": None,
            "categoriaid": None,
            "comercioid": None,
            "descripcion": descripcion_entry.get(),
            "activo": 1
        }

        if tipo_id == TIPO_INGRESO:
            movimiento_nuevo["cuentadestinoid"] = obtener_id_combo(cuenta_destino_combobox)

        elif tipo_id == TIPO_GASTO:
            movimiento_nuevo["cuentaorigenid"] = obtener_id_combo(cuenta_origen_combobox)
            movimiento_nuevo["categoriaid"] = obtener_id_combo(categoria_combobox)
            movimiento_nuevo["comercioid"] = obtener_id_combo(comercio_combobox)

        elif tipo_id == TIPO_TRANSFERENCIA:
            movimiento_nuevo["cuentaorigenid"] = obtener_id_combo(cuenta_origen_combobox)
            movimiento_nuevo["cuentadestinoid"] = obtener_id_combo(cuenta_destino_combobox)
            
        try:
            if movimiento_original["activo"]:
                ajustar_saldo_movimiento(movimiento_original, -1)

            cursor.execute("""
                UPDATE movimientos
                SET fecha = ?,
                    tipodemovimientoid = ?,
                    monto = ?,
                    cuentaorigenid = ?,
                    cuentadestinoid = ?,
                    categoriaid = ?,
                    comercioid = ?,
                    descripcion = ?
                WHERE idmovimiento = ?
            """, (
                movimiento_nuevo["fecha"],
                movimiento_nuevo["tipodemovimientoid"],
                movimiento_nuevo["monto"],
                movimiento_nuevo["cuentaorigenid"],
                movimiento_nuevo["cuentadestinoid"],
                movimiento_nuevo["categoriaid"],
                movimiento_nuevo["comercioid"],
                movimiento_nuevo["descripcion"],
                id_movimiento
            ))

            ajustar_saldo_movimiento(movimiento_nuevo, 1)

            conn.commit()
            ventana_editar.destroy()
            load_recent_movements()

        except Exception as error:
            conn.rollback()
            messagebox.showerror("Error", f"No se pudo guardar el movimiento:\n{error}")
            
    tipo_combobox.bind("<<ComboboxSelected>>", mostrar_campos_por_tipo)
    mostrar_campos_por_tipo()        
    
    btn_guardar = ttk.Button(ventana_editar, text="Guardar", command=guardar_movimiento_editado)
    btn_guardar.grid(row=8, column=0, padx=5, pady=15, sticky=W)
    btn_cancelar = ttk.Button( ventana_editar, text="Cancelar", command=ventana_editar.destroy)
    btn_cancelar.grid(row=8, column=1, padx=5, pady=15, sticky=E)

def load_recent_movements():
    tree.delete(*tree.get_children())

    cursor.execute("""
        SELECT idmovimiento, fecha, tipodemovimientoid, monto
        FROM movimientos
        WHERE activo = 1
        ORDER BY fecha DESC
        LIMIT 10
    """)

    for row in cursor.fetchall():
        id_movimiento = row[0]
        fecha = row[1]
        tipo_id = row[2]
        monto = row[3]

        tipo = "Ingreso" if tipo_id == 1 else "Gasto" if tipo_id == 2 else "Transferencia"
        color = "par" if len(tree.get_children()) % 2 == 0 else "impar"
        tuple_color = "ingreso" if tipo_id == 1 else "gasto" if tipo_id == 2 else "transferencia"

        tree.insert(
            "",
            "end",
            iid=id_movimiento,
            values=(fecha, tipo, f"${monto:,.2f}"),
            tags=(color, tuple_color)
        )
    
def actualizar_todo():
    actualizar_resumen()
    actualizar_saldos_cuentas()
    load_recent_movements()
    Variable.app_root.after(10000, actualizar_todo)  # Actualiza cada 10 segundos

actualizar_todo()  # Llamada inicial para actualizar todo al inicio
load_recent_movements()
Variable.app_root.mainloop() 
