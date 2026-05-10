import re

# =========================================
# VALIDACIONES GENERALES
# =========================================
def validar_requerido(valor: str) -> bool:
    return valor.strip() != ""

def validar_entero(valor: str) -> bool:
    return valor.isdigit()

def validar_stock(valor: str) -> bool:
    return valor.isdigit()

def validar_dni(valor: str) -> bool:
    return valor.isdigit() and len(valor) == 8

def validar_celular(valor: str) -> bool:
    return valor.isdigit() and len(valor) == 9

def validar_correo(correo: str) -> bool:
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo) is not None

def validar_precio(valor: str) -> bool:
    patron = r'^\d+(\.\d{1,2})?$'
    return re.match(patron, valor) is not None

# =========================================
# INPUT (Tkinter validatecommand)
# =========================================
def validar_input_precio(valor: str) -> bool:
    if valor == "":
        return True
    return re.match(r'^\d*\.?\d{0,2}$', valor) is not None

def validar_input_stock(valor: str) -> bool:
    if valor == "":
        return True
    return valor.isdigit()

# =========================================
# VENTAS
# =========================================
def validar_cantidad(valor: str) -> bool:
    """
    Valida que la cantidad sea un número entero mayor a 0.
    """
    return valor.isdigit() and int(valor) > 0

def validar_detalle_no_vacio(lista: list) -> bool:
    """
    Valida que la lista de detalles de venta no esté vacía.
    """
    return len(lista) > 0
