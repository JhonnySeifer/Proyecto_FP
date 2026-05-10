from repositorios.venta_repository import VentaRepository

class ReporteService:
    """
    Lógica de negocio para reportes.
    """

    def __init__(self):
        self.venta_repo = VentaRepository()

    def total_ventas(self) -> float:
        ventas = self.venta_repo.listar_ventas()
        return sum(v["total"] for v in ventas if v["estado"] == "ACTIVO")

    def cliente_top(self) -> str:
        ventas = self.venta_repo.listar_ventas()
        conteo = {}
        for v in ventas:
            cliente = v["cliente"]
            conteo[cliente] = conteo.get(cliente, 0) + 1
        return max(conteo, key=conteo.get) if conteo else "Ninguno"
