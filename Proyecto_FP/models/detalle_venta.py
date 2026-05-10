class DetalleVenta:
    """
    Representa el detalle de un producto dentro de una venta.
    """

    def __init__(
        self,
        id_venta: int,
        id_producto: int,
        producto: str,
        cantidad: int,
        precio: float,
        subtotal: float
    ):
        self.id_venta = id_venta
        self.id_producto = id_producto
        self.producto = producto
        self.cantidad = cantidad
        self.precio = precio
        self.subtotal = subtotal

    def to_dict(self) -> dict:
        return {
            "id_venta": self.id_venta,
            "id_producto": self.id_producto,
            "producto": self.producto,
            "cantidad": self.cantidad,
            "precio": self.precio,
            "subtotal": self.subtotal
        }
