import json

def leer_json(ruta: str) -> list:
    """
    Lee un archivo JSON y devuelve su contenido como lista.
    """
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def guardar_json(ruta: str, data: list) -> None:
    """
    Guarda una lista en un archivo JSON.
    """
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
