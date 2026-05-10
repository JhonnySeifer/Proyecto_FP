from utils.archivo import leer_json, guardar_json

RUTA_CLIENTES = "D:/Workspace/Python/Proyecto_FP/data/clientes.json"

def leer_clientes() -> list:
    return leer_json(RUTA_CLIENTES)

def guardar_clientes(data: list) -> None:
    guardar_json(RUTA_CLIENTES, data)
