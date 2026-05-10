from models.producto import Producto
from repositorios.producto_repository import ProductoRepository
from utils.archivo import guardar_json

class ProductoService:
    """
    Lógica de negocio para productos.
    """

    def __init__(self):
        self.repository = ProductoRepository()

    def listar_productos(self) -> list:
        return [p for p in self.repository.listar_productos() if p["estado"] == "ACTIVO"]

    def guardar_producto(self, codigo, nombre, categoria, precio, stock, estado="ACTIVO"):
        productos = self.repository.listar_productos()
        nuevo_id = max([p["id_producto"] for p in productos], default=0) + 1
        producto = {
            "id_producto": nuevo_id,
            "codigo": codigo,
            "nombre": nombre,
            "categoria": categoria,
            "precio": precio,
            "stock": stock,
            "estado": estado
        }
        self.repository.guardar_producto(producto)

    def editar_producto(self, id_producto, codigo, nombre, categoria, precio, stock, estado):
        producto = {
            "id_producto": id_producto,
            "codigo": codigo,
            "nombre": nombre,
            "categoria": categoria,
            "precio": precio,
            "stock": stock,
            "estado": estado
        }
        self.repository.editar_producto(id_producto, producto)

    def eliminar_producto(self, id_producto):
        productos = self.repository.listar_productos()
        for p in productos:
            if p["id_producto"] == id_producto:
                p["estado"] = "INACTIVO"
                break
        self.repository.guardar_productos(productos)

    def descontar_stock(self, id_producto, cantidad) -> None:
        productos = self.repository.listar_productos()
        for p in productos:
            if p["id_producto"] == id_producto:
                p["stock"] -= cantidad
                break
        guardar_json(self.repository.ruta, productos)
