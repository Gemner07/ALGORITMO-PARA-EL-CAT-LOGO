"""Funciones del sistema de catálogo.
Se usan listas, funciones y un archivo de texto para guardar la información.
"""

import os

ARCHIVO_DEFECTO = os.path.join(os.path.dirname(__file__), "catalogo.txt")


def cargar_productos(ruta=ARCHIVO_DEFECTO):
    productos = []
    if not os.path.exists(ruta):
        return productos

    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(";")
            if len(partes) != 4:
                continue
            codigo, descripcion, cantidad, precio = partes
            try:
                productos.append({
                    "codigo": codigo,
                    "descripcion": descripcion,
                    "cantidad": int(cantidad),
                    "precio": float(precio),
                })
            except ValueError:
                # Si una línea está dañada, se ignora para no detener el programa.
                continue
    return productos


def guardar_productos(productos, ruta=ARCHIVO_DEFECTO):
    with open(ruta, "w", encoding="utf-8") as archivo:
        for producto in productos:
            linea = (
                f"{producto['codigo']};{producto['descripcion']};"
                f"{producto['cantidad']};{producto['precio']:.2f}\n"
            )
            archivo.write(linea)


def buscar_indice(productos, codigo):
    codigo = codigo.strip().lower()
    for i, producto in enumerate(productos):
        if producto["codigo"].lower() == codigo:
            return i
    return -1


def validar_producto(codigo, descripcion, cantidad_texto, precio_texto):
    codigo = codigo.strip()
    descripcion = descripcion.strip()

    if codigo == "":
        return False, "Ingrese el código del producto."
    if descripcion == "":
        return False, "Ingrese la descripción del producto."

    try:
        cantidad = int(cantidad_texto)
    except ValueError:
        return False, "La cantidad debe ser un número entero."

    try:
        precio = float(precio_texto)
    except ValueError:
        return False, "El precio debe ser un número."

    if cantidad < 0:
        return False, "La cantidad no puede ser negativa."
    if precio <= 0:
        return False, "El precio debe ser mayor que cero."

    return True, {
        "codigo": codigo,
        "descripcion": descripcion,
        "cantidad": cantidad,
        "precio": precio,
    }


def registrar_producto(productos, nuevo):
    if buscar_indice(productos, nuevo["codigo"]) != -1:
        return False, "Ya existe un producto con ese código."
    productos.append(nuevo)
    return True, "Producto registrado correctamente."


def actualizar_producto(productos, codigo_original, actualizado):
    indice = buscar_indice(productos, codigo_original)
    if indice == -1:
        return False, "No se encontró el producto a actualizar."

    # Si cambió el código, se revisa que no se repita.
    if actualizado["codigo"].lower() != codigo_original.lower():
        if buscar_indice(productos, actualizado["codigo"]) != -1:
            return False, "El nuevo código ya pertenece a otro producto."

    productos[indice] = actualizado
    return True, "Producto actualizado correctamente."


def eliminar_producto(productos, codigo):
    indice = buscar_indice(productos, codigo)
    if indice == -1:
        return False, "No se encontró el producto."
    eliminado = productos.pop(indice)
    return True, f"Se eliminó: {eliminado['descripcion']}"


def buscar_productos(productos, texto):
    texto = texto.strip().lower()
    if texto == "":
        return productos[:]
    encontrados = []
    for producto in productos:
        if (
            texto in producto["codigo"].lower()
            or texto in producto["descripcion"].lower()
        ):
            encontrados.append(producto)
    return encontrados


def ordenar_por_descripcion(productos):
    # Selection sort, visto en clase.
    ordenados = productos[:]
    n = len(ordenados)
    for i in range(n):
        minimo = i
        for j in range(i + 1, n):
            if ordenados[j]["descripcion"].lower() < ordenados[minimo]["descripcion"].lower():
                minimo = j
        ordenados[i], ordenados[minimo] = ordenados[minimo], ordenados[i]
    return ordenados


def productos_stock_critico(productos, limite=10):
    return [p for p in productos if p["cantidad"] < limite]


def resumen_catalogo(productos):
    total_productos = len(productos)
    total_unidades = sum(p["cantidad"] for p in productos)
    valor_inventario = sum(p["cantidad"] * p["precio"] for p in productos)
    return total_productos, total_unidades, valor_inventario
