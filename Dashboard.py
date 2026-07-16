import json
import os
import sqlite3
import webbrowser
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import Variable
from tkcalendar import DateEntry


TIPO_INGRESO = 1
TIPO_GASTO = 2
TIPO_TRANSFERENCIA = 3


def obtener_ruta_db():
    try:
        return Path(Variable.obtener_ruta_db())
    except Exception:
        pass

    carpeta_local = Path(os.getenv("LOCALAPPDATA", "")) / "Presupuesto"
    candidatos = [
        carpeta_local / "presupuesto.db",
        carpeta_local / "Presupuesto.db",
        Path(__file__).resolve().parent / "Presupuesto.db",
        Path(__file__).resolve().parent / "presupuesto.db",
    ]

    for candidato in candidatos:
        try:
            existe = candidato.exists()
        except PermissionError:
            existe = False

        if existe:
            return candidato

    return candidatos[0]


def parse_fecha(valor):
    if not valor:
        return None

    texto = str(valor).strip()
    formatos = ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y", "%d-%m-%Y")

    for formato in formatos:
        try:
            return datetime.strptime(texto[:19], formato).date().isoformat()
        except ValueError:
            pass

    try:
        return datetime.fromisoformat(texto).date().isoformat()
    except ValueError:
        return None


def cargar_movimientos(db_path, fecha_inicio=None, fecha_fin=None, cuenta_id=None):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row

    consulta = """
        SELECT
            m.fecha,
            m.tipodemovimientoid,
            tm.nombre AS tipo,
            m.monto,
            COALESCE(c.nombre, m.descripcion, 'Sin categoria') AS categoria,
            cu.nombrecuenta AS cuenta
        FROM movimientos m
        LEFT JOIN tipodemovimiento tm
            ON tm.idtipodemovimiento = m.tipodemovimientoid
        LEFT JOIN categorias c
            ON c.idcategoria = m.categoriaid
        LEFT JOIN cuentas cu
            ON cu.idcuentas = m.cuentaorigenid
        WHERE m.activo = 1
    """

    parametros = []

    if fecha_inicio:
        consulta += " AND date(m.fecha) >= date(?)"
        parametros.append(fecha_inicio)

    if fecha_fin:
        consulta += " AND date(m.fecha) <= date(?)"
        parametros.append(fecha_fin)

    if cuenta_id:
        consulta += " AND (m.cuentaorigenid = ? OR m.cuentadestinoid = ?)"
        parametros.extend([cuenta_id, cuenta_id])

    consulta += " ORDER BY m.fecha"

    movimientos = []

    for fila in con.execute(consulta, parametros):
        fecha = parse_fecha(fila["fecha"])
        if not fecha:
            continue

        monto = float(fila["monto"] or 0)
        tipo_id = fila["tipodemovimientoid"]

        if tipo_id == TIPO_INGRESO:
            efecto = monto
        elif tipo_id == TIPO_GASTO:
            efecto = -abs(monto)
        else:
            efecto = 0

        movimientos.append({
            "fecha": fecha,
            "mes": fecha[:7],
            "tipo_id": tipo_id,
            "tipo": fila["tipo"] or "Movimiento",
            "monto": monto,
            "efecto": efecto,
            "categoria": fila["categoria"] or "Sin categoria",
            "cuenta": fila["cuenta"] or "Sin cuenta",
        })

    con.close()
    return movimientos


def crear_datos_reporte(movimientos):
    balance_mes = defaultdict(float)
    ingresos_mes = defaultdict(float)
    gastos_mes = defaultdict(float)
    transferencias_mes = defaultdict(float)
    gastos_categoria = defaultdict(float)

    for mov in movimientos:
        balance_mes[mov["mes"]] += mov["efecto"]

        if mov["tipo_id"] == TIPO_INGRESO:
            ingresos_mes[mov["mes"]] += mov["monto"]
        elif mov["tipo_id"] == TIPO_GASTO:
            gastos_mes[mov["mes"]] += mov["monto"]
            gastos_categoria[mov["categoria"]] += mov["monto"]
        elif mov["tipo_id"] == TIPO_TRANSFERENCIA:
            transferencias_mes[mov["mes"]] += mov["monto"]

    meses = sorted(balance_mes)
    categorias = sorted(
        gastos_categoria,
        key=lambda categoria: gastos_categoria[categoria],
        reverse=True
    )

    return {
        "meses": meses,
        "balance": [round(balance_mes[mes], 2) for mes in meses],
        "ingresos": [round(ingresos_mes[mes], 2) for mes in meses],
        "gastos": [round(gastos_mes[mes], 2) for mes in meses],
        "transferencias": [round(transferencias_mes[mes], 2) for mes in meses],
        "categorias": categorias,
        "gastos_categoria": [round(gastos_categoria[categoria], 2) for categoria in categorias],
        "total_ingresos": round(sum(ingresos_mes.values()), 2),
        "total_gastos": round(sum(gastos_mes.values()), 2),
        "total_transferencias": round(sum(transferencias_mes.values()), 2),
        "balance_total": round(sum(balance_mes.values()), 2),
    }


def crear_html_reporte(datos):
    payload = json.dumps(datos, ensure_ascii=True)
    fecha_generacion = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Reportes de presupuesto</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f6f7f9; color: #1f2937; }}
    header {{ padding: 20px 24px; background: #fff; border-bottom: 1px solid #d7dde5; }}
    h1 {{ margin: 0 0 6px; font-size: 24px; }}
    p {{ margin: 0; color: #5b6675; }}
    main {{ display: grid; gap: 16px; padding: 18px; max-width: 1100px; margin: 0 auto; }}
    .grid {{ display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(min(320px, 100%), 1fr)); }}
    .panel {{ background: #fff; border: 1px solid #d7dde5; border-radius: 8px; padding: 10px; min-height: 360px; min-width: 0; overflow: hidden; }}
    .wide {{ min-height: 400px; }}
  </style>
</head>
<body>
  <header>
    <h1>Reportes de presupuesto</h1>
    <p>Generado el {fecha_generacion}</p>
  </header>
  <main>
    <section id="balance" class="panel wide"></section>
    <section class="grid">
      <div id="ingresos-gastos" class="panel"></div>
      <div id="categorias" class="panel"></div>
    </section>
  </main>
  <script>
    const datos = {payload};
    const common = {{
      paper_bgcolor: "#ffffff",
      plot_bgcolor: "#ffffff",
      margin: {{ l: 55, r: 24, t: 54, b: 50 }},
      font: {{ family: "Arial, sans-serif", color: "#1f2937" }}
    }};

    Plotly.newPlot("balance", [{{
      x: datos.meses,
      y: datos.balance,
      type: "scatter",
      mode: "lines+markers",
      line: {{ color: "#2563eb", width: 3 }},
      marker: {{ size: 7 }}
    }}], {{ ...common, title: "Balance mensual" }}, {{ responsive: true }});

    Plotly.newPlot("ingresos-gastos", [
      {{ x: datos.meses, y: datos.ingresos, type: "bar", name: "Ingresos", marker: {{ color: "#0f766e" }} }},
      {{ x: datos.meses, y: datos.gastos, type: "bar", name: "Gastos", marker: {{ color: "#b91c1c" }} }},
      {{ x: datos.meses, y: datos.transferencias, type: "bar", name: "Transferencias", marker: {{ color: "#7c3aed" }} }}
    ], {{ ...common, title: "Ingresos vs gastos", barmode: "group" }}, {{ responsive: true }});

    Plotly.newPlot("categorias", [{{
      labels: datos.categorias,
      values: datos.gastos_categoria,
      type: "pie",
      hole: 0.45
    }}], {{ ...common, title: "Gastos por categoria" }}, {{ responsive: true }});
  </script>
</body>
</html>
"""


def guardar_reporte_html(datos, db_path):
    salida = db_path.parent / "reportes_presupuesto.html"
    salida = salida.resolve()
    salida.write_text(crear_html_reporte(datos), encoding="utf-8")
    return salida


def dashboard(frame3):
    db_path = obtener_ruta_db()
    reporte_path = tk.StringVar(value="")
    resumen_vars = {
        "movimientos": tk.StringVar(value="0"),
        "ingresos": tk.StringVar(value="$0.00"),
        "gastos": tk.StringVar(value="$0.00"),
        "transferencias": tk.StringVar(value="$0.00"),
        "balance": tk.StringVar(value="$0.00"),
    }

    frame3.grid_columnconfigure(0, weight=1)
    frame3.grid_rowconfigure(4, weight=1)
    frame3.grid_rowconfigure(5, weight=2)
    
      
    fecha_inicio_var = tk.StringVar()
    fecha_fin_var = tk.StringVar()
    cuenta_var = tk.StringVar(value="Todas")
    
    acciones = ttk.Frame(frame3)
    acciones.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    acciones.grid_columnconfigure(2, weight=1)

    ttk.Label(acciones, text="Desde").grid(row=0, column=0, padx=(0, 4))
    fecha_inicio = DateEntry(acciones, textvariable=fecha_inicio_var, date_pattern="yyyy-mm-dd")
    fecha_inicio.grid(row=0, column=1, padx=(0, 8))

    ttk.Label(acciones, text="Hasta").grid(row=0, column=2, padx=(0, 4))
    fecha_fin = DateEntry(acciones, textvariable=fecha_fin_var, date_pattern="yyyy-mm-dd")
    fecha_fin.grid(row=0, column=3, padx=(0, 8))

    cuentas_dict = {"Todas": None}

    with sqlite3.connect(db_path) as con:
        con.row_factory = sqlite3.Row
        for fila in con.execute("""
            SELECT idcuentas, nombrecuenta, termcuenta
            FROM cuentas
            WHERE activo = 1
            ORDER BY nombrecuenta
        """):
            texto = f"{fila['nombrecuenta']} - {fila['termcuenta']}"
            cuentas_dict[texto] = fila["idcuentas"]

    ttk.Label(acciones, text="Tarjeta/Cuenta").grid(row=0, column=4, padx=(0, 4))

    combo_cuenta = ttk.Combobox(
        acciones,
        textvariable=cuenta_var,
        values=list(cuentas_dict.keys()),
        state="readonly",
        width=22
    )
    combo_cuenta.grid(row=0, column=5, padx=(0, 8))
    combo_cuenta.current(0)

    ttk.Label(
        frame3,
        text="Reportes",
        font=("Gotham Bold", 12, "bold")
    ).grid(row=0, column=0, padx=5, pady=4, sticky="w")

    resumen = ttk.LabelFrame(frame3, text="Resumen de movimientos", padding=10)
    resumen.grid(row=2, column=0, padx=5, pady=4, sticky="ew")

    etiquetas = [
        ("Movimientos", "movimientos"),
        ("Ingresos", "ingresos"),
        ("Gastos", "gastos"),
        ("Transferencias", "transferencias"),
        ("Balance", "balance"),
    ]

    for columna, (texto, clave) in enumerate(etiquetas):
        ttk.Label(resumen, text=texto, font=("Gotham Book", 8, "bold")).grid(
            row=0, column=columna, padx=8, pady=4, sticky="w"
        )
        ttk.Label(resumen, textvariable=resumen_vars[clave]).grid(
            row=1, column=columna, padx=8, pady=4, sticky="w"
        )

    ttk.Label(
        frame3,
        text="Gastos por categoria",
        font=("Gotham Book", 8, "bold")
    ).grid(row=3, column=0, padx=5, pady=(8, 0), sticky="w")

    tabla = ttk.Treeview(
        frame3,
        columns=("Categoria", "Monto"),
        show="headings",
        height=7
    )
    tabla.heading("Categoria", text="Categoria")
    tabla.heading("Monto", text="Monto")
    tabla.column("Categoria", width=180)
    tabla.column("Monto", width=100, anchor=tk.E)
    tabla.grid(row=4, column=0, padx=5, pady=8, sticky="nsew")

    def actualizar_tabla(datos):
        tabla.delete(*tabla.get_children())

        for categoria, monto in zip(datos["categorias"], datos["gastos_categoria"]):
            tabla.insert("", "end", values=(categoria, f"${monto:,.2f}"))

    def actualizar_resumen(datos, total_movimientos):
        resumen_vars["movimientos"].set(str(total_movimientos))
        resumen_vars["ingresos"].set(f"${datos['total_ingresos']:,.2f}")
        resumen_vars["gastos"].set(f"${datos['total_gastos']:,.2f}")
        resumen_vars["transferencias"].set(f"${datos['total_transferencias']:,.2f}")
        resumen_vars["balance"].set(f"${datos['balance_total']:,.2f}")

    def generar_reporte():
        try:
            cuenta_id = cuentas_dict.get(cuenta_var.get())

            movimientos = cargar_movimientos(
                db_path,
                fecha_inicio=fecha_inicio_var.get(),
                fecha_fin=fecha_fin_var.get(),
                cuenta_id=cuenta_id
            )

            datos = crear_datos_reporte(movimientos)
            salida = guardar_reporte_html(datos, db_path)

            reporte_path.set(str(salida))
            actualizar_resumen(datos, len(movimientos))
            actualizar_tabla(datos)

        except Exception as error:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Reportes", f"No se pudo generar el reporte:\n{os.errorror}")

    def abrir_reporte():
        if not reporte_path.get():
            generar_reporte()

        if reporte_path.get():
            ruta = Path(reporte_path.get()).resolve()
            webbrowser.open(ruta.as_uri())

    ttk.Button(
        acciones,
        text="Generar reporte",
        command=generar_reporte
    ).grid(row=1, column=0, padx=(0, 8), sticky="w")

    ttk.Button(
        acciones,
        text="Abrir reporte",
        command=abrir_reporte
    ).grid(row=1, column=1, padx=(0, 8), sticky="w")


    generar_reporte()
