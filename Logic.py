import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkinter.font import Font
import Variable
import sqlite3
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

ruta = os.path.join(os.getenv("LOCALAPPDATA"), "CotizadorTaller")

db_path = os.path.join(ruta, "taller.db")

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def crear_ventana_cotizacion(parent):
    # Usamos Toplevel para crear una ventana dependiente de la principal
    new_window = tk.Toplevel(parent)
    new_window.title("Cotización")
    new_window.geometry("585x480")
    new_window.iconbitmap('images.ico')
    new_window.grid_columnconfigure(0, weight=2)
    new_window.grid_columnconfigure(1, weight=1)
    new_window.grid_columnconfigure(2, weight=1)
    bold_font1 = Font(family="Gotham Book", size=10, weight="bold")
    style = ttk.Style()
    style.configure("Bold.TButton", font=bold_font1)
    mylabel = ttk.Label(new_window, text='Cotización', font=('Gotham Book', 14, 'bold'), width=12)
    mylabel.grid(row=0, column=0, sticky="E", padx=10)
    mylabel1 = ttk.Label(new_window, text='', font=('Gotham Book', 10, 'bold'))
    mylabel1.grid(row=1, column=0, sticky="W", padx=10)
    mylabel2 = ttk.Label(new_window, text='Taller Midas Ruiz Cortines', font=('Gotham Book', 12, 'bold'),width=28)
    mylabel2.grid(row=2, column=0, sticky="E", padx=10)
    mylabel3 = ttk.Label(new_window, text='', font=('Gotham Book', 10, 'bold'))
    mylabel3.grid(row=3, column=0, sticky="W", padx=10)
    mylabel4 = ttk.Label(new_window, text='Envió cotización solicitada para su Auto:', font=('Gotham Book', 10,),width=42)
    mylabel4.grid(row=4, column=0, sticky="W", padx=10)
    texto_auto = f"{Variable.marca_var.get()} {Variable.modelo_var.get()} {Variable.anio_var.get()}"
    mylabel5 = ttk.Label(new_window, text=texto_auto, font=('Gotham Book', 10, 'bold'))
    mylabel5.grid(row=5, column=0, sticky="W", padx=10)
    tabla_frame = ttk.Frame(new_window)
    tabla_frame.grid(row=7, column=0, columnspan=3, padx=20, pady=10)
    mylabel6 = ttk.Label(tabla_frame, text='Servicio', font=('Gotham Book', 10, 'bold'), width=10)
    mylabel6.grid(row=8, column=0, sticky="w", padx=10)
    mylabel7 = ttk.Label(tabla_frame, text='Cantidad', font=('Gotham Book', 10, 'bold'), width=10)
    mylabel7.grid(row=8, column=1, sticky="W", padx=10)
    mylabel8 = ttk.Label(tabla_frame, text='Subtotal', font=('Gotham Book', 10, 'bold'), width=10)
    mylabel8.grid(row=8, column=2, sticky="E", padx=10)
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
    
    total_cotizacion = 0

    cursor.execute("SELECT * FROM servicios")
    servicios = cursor.fetchall()

    def numero(valor, default=0):

        if hasattr(valor, "get"):
            try:
                valor = valor.get()
            except Exception:
                return default

        if valor in ("", None):
            return default

        try:
            return int(valor)
        except (ValueError, TypeError):
            return default

    def obtener_costo(parte):
        cursor.execute("SELECT precio FROM refacciones WHERE numero_parte = ?", (parte,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            messagebox.showerror("Error", f"No se encontró el costo para la parte: {parte}")
        return 0

    def calcular_precio(costo, ganancia, horas, cantidad):

        costo = float(costo)
        ganancia = float(ganancia)
        horas = float(horas)
        cantidad = int(cantidad)
        mano_obra = float(Variable.mano_obra)

        costo_ref = costo / ganancia
        mano_obra_total = horas * cantidad * mano_obra
        subtotal = costo_ref + mano_obra_total
        total = subtotal * (1 + Variable.iva)

        return total, total

    fila = 9
    
    fecha = datetime.now().strftime("%d/%m/%Y")
    
    texto_cotizacion = ""
    texto_cotizacion = "Taller Midas Ruiz Cortines\n\n"
    texto_cotizacion += f"Fecha: {fecha}\n\n"
    texto_cotizacion += "Envío cotización solicitada para su Auto:\n"
    texto_cotizacion += f"{Variable.marca_var.get()} {Variable.modelo_var.get()} {Variable.anio_var.get()}\n\n"

    for servicio in servicios:

        id_servicio = servicio["id_servicio"]
        descripcion = servicio["servicio"]
        check_var = servicio["check"]
        horas = servicio["horas"]
        ganancia = servicio["ganancia"]
        cantidad_valor = servicio["cantidad_serv"]

        if isinstance(cantidad_valor, str) and hasattr(Variable, cantidad_valor):
            cantidad_servicio = numero(getattr(Variable, cantidad_valor), 1)
        else:
            cantidad_servicio = numero(cantidad_valor, 1)

        check = getattr(Variable, check_var, None)

        if check and check.get() == 1:

            costo_total_partes = 0

            cursor.execute("""
            SELECT parte, cantidad
            FROM partes_servicio
            WHERE id_servicio = ?
            """, (id_servicio,))

            partes = cursor.fetchall()

            for parte, cantidad_valor in partes:

                if isinstance(cantidad_valor, str) and hasattr(Variable, cantidad_valor):
                    cantidad_var = getattr(Variable, cantidad_valor)
                    cantidad = numero(cantidad_var, 1)
                else:
                    cantidad = numero(cantidad_valor, 1)

                if isinstance(parte, str) and hasattr(Variable, parte):

                    valor = getattr(Variable, parte)

                    if hasattr(valor, "get"):
                        parte = valor.get()
                    else:
                        parte = valor

                costo = obtener_costo(parte)

                costo_total_partes += int(costo) * int(cantidad)

            total = calcular_precio(
                costo_total_partes,
                ganancia,
                horas,
                    cantidad_servicio
            )

            subtotal_servicio = total[0]

            ttk.Label(
                tabla_frame,
                text=f"{descripcion}", width=25
            ).grid(row=fila, column=0, sticky="W", padx=10)

            ttk.Label(
                tabla_frame,
                text=f"{cantidad_servicio}", width=25
            ).grid(row=fila, column=1, sticky="W", padx=10)

            ttk.Label(
                tabla_frame,
                text=f"${subtotal_servicio:,.2f}", width=10
            ).grid(row=fila, column=2, sticky="W", padx=10)
            
            # guardar texto para copiar
            texto_cotizacion += f"{descripcion:<22} x{cantidad_servicio:<2} ${subtotal_servicio:>10,.2f}\n"

            fila += 1

            total_cotizacion += subtotal_servicio

    ttk.Separator(new_window, orient="horizontal").grid(
            row=fila, column=0, columnspan=3, sticky="EW", pady=10
    )
    ttk.Label(
        new_window,
        text=f"TOTAL: ${total_cotizacion:,.2f}",
        font=('Gotham Book',12,'bold')
        ).grid(row=fila+1, column=1, sticky="W", padx=10)
    
    texto_cotizacion += "-----------------------------\n"
    texto_cotizacion += f"\nTOTAL: ${total_cotizacion:,.2f}"

    def copiar_cotizacion():
        new_window.clipboard_clear()
        new_window.clipboard_append(texto_cotizacion)
        new_window.update()
        
    nombre = datetime.now().strftime("cotizacion_%Y%m%d_%H%M%S.pdf")
    
    def generar_pdf():

        texto = texto_cotizacion

        ruta = os.path.join(os.getenv("USERPROFILE"), "Documents", nombre)

        c = canvas.Canvas(ruta, pagesize=letter)

        y = 750

        for linea in texto.split("\n"):
            c.drawString(50, y, linea)
            y -= 20

        c.save()

        messagebox.showinfo("PDF generado", "Cotización guardada en Documents")
        os.startfile(ruta)
    
    boton_copiar = ttk.Button(new_window, text="Copiar cotización", command=copiar_cotizacion, style="Bold.TButton")
    boton_copiar.grid(row=fila+2, column=0)    
    button_close = ttk.Button(new_window, text="Cerrar", command=new_window.destroy, style="Bold.TButton")
    button_close.grid(row=fila+4, column=1, sticky="W", padx=10)
    boton_pdf = ttk.Button(new_window, text="Generar PDF", command=generar_pdf, style="Bold.TButton")
    boton_pdf.grid(row=fila+2, column=1, sticky="W", padx=10)
    
    