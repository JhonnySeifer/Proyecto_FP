from models.detalle_venta import DetalleVenta
from repositorios.detalle_venta_repository import DetalleVentaRepository

class DetalleVentaService:
    """
    Lógica de negocio para los detalles de venta.
    """

    def __init__(self):
        self.repository = DetalleVentaRepository()

    def listar_detalles(self) -> list:
        """
        Devuelve todos los detalles de venta.
        """
        return self.repository.listar_detalles()

    def guardar_detalle(self, id_venta: int, id_producto: int, producto: str, cantidad: int, precio: float, subtotal: float) -> None:
        """
        Guarda un nuevo detalle de venta.
        """
        detalle = DetalleVenta(id_venta, id_producto, producto, cantidad, precio, subtotal)
        self.repository.guardar_detalle(detalle.to_dict())

    def eliminar_detalles_por_venta(self, id_venta: int) -> None:
        """
        Elimina todos los detalles asociados a una venta.
        """
        self.repository.eliminar_detalles_por_venta(id_venta)

    def obtener_detalles_por_venta(self, id_venta: int) -> list:
        """
        Devuelve los detalles asociados a una venta específica.
        """
        return self.repository.obtener_detalles_por_venta(id_venta)
