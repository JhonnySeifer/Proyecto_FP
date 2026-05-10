from models.venta import Venta
from repositorios.venta_repository import VentaRepository
from repositorios.detalle_venta_repository import DetalleVentaRepository

class VentaService:
    """
    Lógica de negocio para ventas.
    """

    def __init__(self):
        self.venta_repo = VentaRepository()
        self.detalle_repo = DetalleVentaRepository()

    def listar_ventas(self) -> list:
        return [v for v in self.venta_repo.listar_ventas() if v["estado"] == "ACTIVO"]

    def guardar_venta(self, cliente, sucursal, subtotal, igv, total, detalles: list) -> None:
        ventas = self.venta_repo.listar_ventas()
        nuevo_id = max([v["id_venta"] for v in ventas], default=0) + 1
        venta = Venta(nuevo_id, cliente, sucursal, subtotal, igv, total)
        self.venta_repo.guardar_venta(venta.to_dict())

        for d in detalles:
            d["id_venta"] = nuevo_id
            self.detalle_repo.guardar_detalle(d)

    def editar_venta(self, id_venta, cliente, sucursal, subtotal, igv, total, estado) -> None:
        venta = Venta(id_venta, cliente, sucursal, subtotal, igv, total, estado)
        self.venta_repo.editar_venta(id_venta, venta.to_dict())

    def eliminar_venta(self, id_venta) -> None:
        self.venta_repo.cambiar_estado_venta(id_venta, "ANULADA")
        self.detalle_repo.eliminar_detalles_por_venta(id_venta)

    def obtener_venta_completa(self, id_venta) -> dict:
        venta = next((v for v in self.venta_repo.listar_ventas() if v["id_venta"] == id_venta), None)
        if not venta:
            return None
        detalles = self.detalle_repo.obtener_detalles_por_venta(id_venta)
        return {"venta": venta, "detalles": detalles}
