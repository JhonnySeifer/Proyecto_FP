class Venta:
    """
    Representa una transacción de venta.
    """

    def __init__(
        self,
        id_venta: int,
        cliente: str,
        sucursal: str,
        subtotal: float,
        igv: float,
        total: float,
        estado: str = "ACTIVO"
    ):
        self.id_venta = id_venta
        self.cliente = cliente
        self.sucursal = sucursal
        self.subtotal = subtotal
        self.igv = igv
        self.total = total
        self.estado = estado

    def to_dict(self) -> dict:
        return {
            "id_venta": self.id_venta,
            "cliente": self.cliente,
            "sucursal": self.sucursal,
            "subtotal": self.subtotal,
            "igv": self.igv,
            "total": self.total,
            "estado": self.estado
        }
