
import os
import tempfile
from catalogo import (
    guardar_productos,
    cargar_productos,
    validar_producto,
    registrar_producto,
    actualizar_producto,
    eliminar_producto,
    buscar_productos,
    ordenar_por_descripcion,
    productos_stock_critico,
)


def ejecutar_pruebas():
    productos = []

    ok, p1 = validar_producto("P001", "Arroz extra 5 kg", "25", "24.90")
    assert ok
    assert registrar_producto(productos, p1)[0]

    ok, p2 = validar_producto("P002", "Aceite vegetal 1 L", "8", "10.50")
    assert ok
    assert registrar_producto(productos, p2)[0]

    # Código repetido
    assert not registrar_producto(productos, p2)[0]

    # Búsqueda
    assert len(buscar_productos(productos, "aceite")) == 1

    # Stock crítico
    assert len(productos_stock_critico(productos, 10)) == 1

    # Actualización
    ok, nuevo_p2 = validar_producto("P002", "Aceite vegetal 1 L", "18", "10.50")
    assert ok
    assert actualizar_producto(productos, "P002", nuevo_p2)[0]
    assert len(productos_stock_critico(productos, 10)) == 0

    # Ordenamiento por descripción
    ordenados = ordenar_por_descripcion(productos)
    assert ordenados[0]["descripcion"].startswith("Aceite")

    # Persistencia en archivo de texto
    with tempfile.TemporaryDirectory() as carpeta:
        ruta = os.path.join(carpeta, "catalogo_prueba.txt")
        guardar_productos(productos, ruta)
        recuperados = cargar_productos(ruta)
        assert recuperados == productos

    # Eliminación
    assert eliminar_producto(productos, "P001")[0]
    assert len(productos) == 1

    print("PRUEBAS COMPLETADAS CORRECTAMENTE")
    print("- Registro y validación: OK")
    print("- Control de código repetido: OK")
    print("- Búsqueda: OK")
    print("- Stock crítico: OK")
    print("- Actualización: OK")
    print("- Ordenamiento: OK")
    print("- Guardado y recuperación en archivo: OK")
    print("- Eliminación: OK")


if __name__ == "__main__":
    ejecutar_pruebas()
