from utils.archivo import leer_json, guardar_json

class VentaRepository:
    """
    Repositorio encargado de la persistencia de ventas y detalles en ventas.json y detalle_ventas.json
    """

    def __init__(self):
        self.ruta = "D:/Workspace/Python/Proyecto_FP/data/ventas.json"
        self.ruta_detalle = "D:/Workspace/Python/Proyecto_FP/data/detalle_ventas.json"

    # VENTAS
    def listar_ventas(self) -> list:
        return leer_json(self.ruta)

    def guardar_venta(self, venta: dict) -> None:
        ventas = self.listar_ventas()
        ventas.append(venta)
        guardar_json(self.ruta, ventas)

    def editar_venta(self, id_venta: int, nueva_venta: dict) -> None:
        ventas = self.listar_ventas()
        for i, v in enumerate(ventas):
            if v["id_venta"] == id_venta:
                ventas[i] = nueva_venta
                break
        guardar_json(self.ruta, ventas)

    def cambiar_estado_venta(self, id_venta: int, estado: str) -> None:
        ventas = self.listar_ventas()
        for v in ventas:
            if v["id_venta"] == id_venta:
                v["estado"] = estado
                break
        guardar_json(self.ruta, ventas)

    # DETALLE
    def listar_detalles(self) -> list:
        return leer_json(self.ruta_detalle)

    def guardar_detalle(self, detalle: dict) -> None:
        detalles = self.listar_detalles()
        detalles.append(detalle)
        guardar_json(self.ruta_detalle, detalles)

    def eliminar_detalles_por_venta(self, id_venta: int) -> None:
        detalles = self.listar_detalles()
        detalles = [d for d in detalles if d["id_venta"] != id_venta]
        guardar_json(self.ruta_detalle, detalles)

    def obtener_detalles_por_venta(self, id_venta: int) -> list:
        return [d for d in self.listar_detalles() if d["id_venta"] == id_venta]
