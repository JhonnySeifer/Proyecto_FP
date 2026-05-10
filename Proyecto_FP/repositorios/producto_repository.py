from utils.archivo import leer_json, guardar_json

class ProductoRepository:
    """
    Repositorio encargado de la persistencia de productos en productos.json
    """

    def __init__(self):
        self.ruta = "D:/Workspace/Python/Proyecto_FP/data/productos.json"

    def listar_productos(self) -> list:
        return leer_json(self.ruta)

    def guardar_producto(self, producto: dict) -> None:
        productos = self.listar_productos()
        productos.append(producto)
        guardar_json(self.ruta, productos)

    def editar_producto(self, id_producto: int, nuevo_producto: dict) -> None:
        productos = self.listar_productos()
        for i, producto in enumerate(productos):
            if producto["id_producto"] == id_producto:
                productos[i] = nuevo_producto
                break
        guardar_json(self.ruta, productos)

    def cambiar_estado_producto(self, id_producto: int, estado: str) -> None:
        productos = self.listar_productos()
        for producto in productos:
            if producto["id_producto"] == id_producto:
                producto["estado"] = estado
                break
        guardar_json(self.ruta, productos)
