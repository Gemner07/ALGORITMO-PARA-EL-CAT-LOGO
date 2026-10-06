import tkinter as tk
from tkinter import ttk, messagebox

from catalogo import (
    cargar_productos,
    guardar_productos,
    validar_producto,
    registrar_producto,
    actualizar_producto,
    eliminar_producto,
    buscar_productos,
    ordenar_por_descripcion,
    productos_stock_critico,
    resumen_catalogo,
)

productos = cargar_productos()
codigo_seleccionado = None


def limpiar_campos():
    global codigo_seleccionado
    codigo_seleccionado = None
    ent_codigo.delete(0, tk.END)
    ent_descripcion.delete(0, tk.END)
    ent_cantidad.delete(0, tk.END)
    ent_precio.delete(0, tk.END)
    ent_codigo.focus()


def cargar_tabla(lista=None):
    if lista is None:
        lista = productos

    for item in tabla.get_children():
        tabla.delete(item)

    for producto in lista:
        tabla.insert(
            "",
            tk.END,
            values=(
                producto["codigo"],
                producto["descripcion"],
                producto["cantidad"],
                f"S/ {producto['precio']:.2f}",
            ),
        )
    actualizar_resumen()


def actualizar_resumen():
    total, unidades, valor = resumen_catalogo(productos)
    lbl_resumen.config(
        text=f"Productos: {total}     Unidades: {unidades}     Valor estimado: S/ {valor:.2f}"
    )


def registrar():
    valido, resultado = validar_producto(
        ent_codigo.get(), ent_descripcion.get(), ent_cantidad.get(), ent_precio.get()
    )
    if not valido:
        messagebox.showwarning("Dato incorrecto", resultado)
        return

    ok, mensaje = registrar_producto(productos, resultado)
    if not ok:
        messagebox.showwarning("Registro", mensaje)
        return

    guardar_productos(productos)
    cargar_tabla()
    limpiar_campos()
    messagebox.showinfo("Registro", mensaje)


def actualizar():
    global codigo_seleccionado
    if codigo_seleccionado is None:
        messagebox.showwarning("Actualizar", "Seleccione primero un producto de la tabla.")
        return

    valido, resultado = validar_producto(
        ent_codigo.get(), ent_descripcion.get(), ent_cantidad.get(), ent_precio.get()
    )
    if not valido:
        messagebox.showwarning("Dato incorrecto", resultado)
        return

    ok, mensaje = actualizar_producto(productos, codigo_seleccionado, resultado)
    if not ok:
        messagebox.showwarning("Actualizar", mensaje)
        return

    guardar_productos(productos)
    codigo_seleccionado = resultado["codigo"]
    cargar_tabla()
    limpiar_campos()
    messagebox.showinfo("Actualizar", mensaje)


def eliminar():
    global codigo_seleccionado
    if codigo_seleccionado is None:
        messagebox.showwarning("Eliminar", "Seleccione primero un producto de la tabla.")
        return

    if not messagebox.askyesno("Confirmar", "¿Desea eliminar el producto seleccionado?"):
        return

    ok, mensaje = eliminar_producto(productos, codigo_seleccionado)
    if ok:
        guardar_productos(productos)
        cargar_tabla()
        limpiar_campos()
        messagebox.showinfo("Eliminar", mensaje)


def buscar():
    texto = ent_buscar.get()
    encontrados = buscar_productos(productos, texto)
    cargar_tabla(encontrados)
    if not encontrados:
        messagebox.showinfo("Búsqueda", "No se encontraron productos con ese dato.")


def mostrar_todos():
    ent_buscar.delete(0, tk.END)
    cargar_tabla()


def mostrar_stock_critico():
    criticos = productos_stock_critico(productos, 10)
    cargar_tabla(criticos)
    if not criticos:
        messagebox.showinfo("Stock crítico", "No hay productos con stock menor a 10 unidades.")


def ordenar():
    ordenados = ordenar_por_descripcion(productos)
    cargar_tabla(ordenados)


def seleccionar_fila(event=None):
    global codigo_seleccionado
    seleccion = tabla.selection()
    if not seleccion:
        return
    valores = tabla.item(seleccion[0], "values")
    codigo_seleccionado = valores[0]

    ent_codigo.delete(0, tk.END)
    ent_codigo.insert(0, valores[0])
    ent_descripcion.delete(0, tk.END)
    ent_descripcion.insert(0, valores[1])
    ent_cantidad.delete(0, tk.END)
    ent_cantidad.insert(0, valores[2])
    ent_precio.delete(0, tk.END)
    ent_precio.insert(0, str(valores[3]).replace("S/ ", ""))


def al_cerrar():
    guardar_productos(productos)
    ventana.destroy()


ventana = tk.Tk()
ventana.title("Catálogo de Productos - Tienda Piloto")
ventana.geometry("1000x650")
ventana.minsize(900, 600)

estilo = ttk.Style()
try:
    estilo.theme_use("clam")
except tk.TclError:
    pass

contenedor = ttk.Frame(ventana, padding=15)
contenedor.pack(fill="both", expand=True)

lbl_titulo = ttk.Label(
    contenedor,
    text="MÓDULO DE CATÁLOGO DE PRODUCTOS",
    font=("Arial", 18, "bold"),
)
lbl_titulo.pack(pady=(0, 12))

frm_datos = ttk.LabelFrame(contenedor, text="Datos del producto", padding=12)
frm_datos.pack(fill="x")

campos = [
    ("Código:", 0, 0),
    ("Descripción:", 0, 2),
    ("Cantidad:", 1, 0),
    ("Precio de venta:", 1, 2),
]
for texto, fila, col in campos:
    ttk.Label(frm_datos, text=texto).grid(row=fila, column=col, padx=6, pady=6, sticky="e")

ent_codigo = ttk.Entry(frm_datos, width=22)
ent_codigo.grid(row=0, column=1, padx=6, pady=6, sticky="ew")
ent_descripcion = ttk.Entry(frm_datos, width=42)
ent_descripcion.grid(row=0, column=3, padx=6, pady=6, sticky="ew")
ent_cantidad = ttk.Entry(frm_datos, width=22)
ent_cantidad.grid(row=1, column=1, padx=6, pady=6, sticky="ew")
ent_precio = ttk.Entry(frm_datos, width=22)
ent_precio.grid(row=1, column=3, padx=6, pady=6, sticky="ew")
frm_datos.columnconfigure(1, weight=1)
frm_datos.columnconfigure(3, weight=2)

frm_botones = ttk.Frame(contenedor)
frm_botones.pack(fill="x", pady=10)

ttk.Button(frm_botones, text="Registrar", command=registrar).pack(side="left", padx=4)
ttk.Button(frm_botones, text="Actualizar", command=actualizar).pack(side="left", padx=4)
ttk.Button(frm_botones, text="Eliminar", command=eliminar).pack(side="left", padx=4)
ttk.Button(frm_botones, text="Limpiar", command=limpiar_campos).pack(side="left", padx=4)

frm_busqueda = ttk.LabelFrame(contenedor, text="Consulta del catálogo", padding=10)
frm_busqueda.pack(fill="x", pady=(0, 10))
ttk.Label(frm_busqueda, text="Código o descripción:").pack(side="left", padx=4)
ent_buscar = ttk.Entry(frm_busqueda, width=35)
ent_buscar.pack(side="left", padx=4)
ent_buscar.bind("<Return>", lambda event: buscar())
ttk.Button(frm_busqueda, text="Buscar", command=buscar).pack(side="left", padx=4)
ttk.Button(frm_busqueda, text="Mostrar todos", command=mostrar_todos).pack(side="left", padx=4)
ttk.Button(frm_busqueda, text="Ordenar A-Z", command=ordenar).pack(side="left", padx=4)
ttk.Button(frm_busqueda, text="Stock crítico (<10)", command=mostrar_stock_critico).pack(side="left", padx=4)

frm_tabla = ttk.Frame(contenedor)
frm_tabla.pack(fill="both", expand=True)

columnas = ("codigo", "descripcion", "cantidad", "precio")
tabla = ttk.Treeview(frm_tabla, columns=columnas, show="headings", height=14)
tabla.heading("codigo", text="Código")
tabla.heading("descripcion", text="Descripción")
tabla.heading("cantidad", text="Cantidad")
tabla.heading("precio", text="Precio")
tabla.column("codigo", width=130, anchor="center")
tabla.column("descripcion", width=460)
tabla.column("cantidad", width=110, anchor="center")
tabla.column("precio", width=120, anchor="e")
tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

scroll = ttk.Scrollbar(frm_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scroll.set)
tabla.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

lbl_resumen = ttk.Label(contenedor, text="", font=("Arial", 10, "bold"))
lbl_resumen.pack(anchor="w", pady=(8, 0))

lbl_pie = ttk.Label(
    contenedor,
    text="Los datos se guardan automáticamente en el archivo catalogo.txt",
)
lbl_pie.pack(anchor="w", pady=(4, 0))

cargar_tabla()
ent_codigo.focus()
ventana.protocol("WM_DELETE_WINDOW", al_cerrar)

if __name__ == "__main__":
    ventana.mainloop()
