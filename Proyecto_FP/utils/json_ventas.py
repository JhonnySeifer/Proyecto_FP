from utils.archivo import leer_json, guardar_json

RUTA_VENTAS = "D:/Workspace/Python/Proyecto_FP/data/ventas.json"
RUTA_DETALLES = "D:/Workspace/Python/Proyecto_FP/data/detalle_ventas.json"

def leer_ventas() -> list:
    return leer_json(RUTA_VENTAS)

def guardar_ventas(data: list) -> None:
    guardar_json(RUTA_VENTAS, data)

def leer_detalles() -> list:
    return leer_json(RUTA_DETALLES)

def guardar_detalles(data: list) -> None:
    guardar_json(RUTA_DETALLES, data)
