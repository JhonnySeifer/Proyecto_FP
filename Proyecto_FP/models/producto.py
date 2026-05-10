class Producto:
    """
    Representa un producto disponible para la venta.
    """

    def __init__(
        self,
        id_producto: int,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int,
        descripcion: str = "",
        estado: str = "ACTIVO"
    ):
        self.id_producto = id_producto
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.descripcion = descripcion
        self.estado = estado

    def to_dict(self) -> dict:
        return {
            "id_producto": self.id_producto,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
            "descripcion": self.descripcion,
            "estado": self.estado
        }
