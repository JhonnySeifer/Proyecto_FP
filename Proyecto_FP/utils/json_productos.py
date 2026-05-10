from utils.archivo import leer_json, guardar_json

RUTA_PRODUCTOS = "D:/Workspace/Python/Proyecto_FP/data/productos.json"

def leer_productos() -> list:
    return leer_json(RUTA_PRODUCTOS)

def guardar_productos(data: list) -> None:
    guardar_json(RUTA_PRODUCTOS, data)
