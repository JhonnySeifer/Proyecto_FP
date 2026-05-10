from utils.archivo import leer_json, guardar_json

class DetalleVentaRepository:
    """
    Repositorio encargado de la persistencia de detalles de venta en detalle_ventas.json
    """

    def __init__(self):
        self.ruta = "D:/Workspace/Python/Proyecto_FP/data/detalle_ventas.json"

    # LISTAR DETALLES
    def listar_detalles(self) -> list:
        """
        Devuelve todos los detalles de venta.
        """
        return leer_json(self.ruta)

    # GUARDAR DETALLE
    def guardar_detalle(self, detalle: dict) -> None:
        """
        Agrega un nuevo detalle de venta.
        """
        detalles = self.listar_detalles()
        detalles.append(detalle)
        guardar_json(self.ruta, detalles)

    # ELIMINAR DETALLES POR VENTA
    def eliminar_detalles_por_venta(self, id_venta: int) -> None:
        """
        Elimina todos los detalles asociados a una venta.
        """
        detalles = self.listar_detalles()
        detalles = [d for d in detalles if d["id_venta"] != id_venta]
        guardar_json(self.ruta, detalles)

    # OBTENER DETALLES POR VENTA
    def obtener_detalles_por_venta(self, id_venta: int) -> list:
        """
        Devuelve los detalles asociados a una venta específica.
        """
        return [d for d in self.listar_detalles() if d["id_venta"] == id_venta]
