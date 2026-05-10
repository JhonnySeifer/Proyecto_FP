import tkinter as tk

from services.reporte_service import ReporteService


class FrmReportes:

    def __init__(self, parent):

        self.service = ReporteService()

        self.ventana = tk.Toplevel(parent)

        self.configurar_ventana()

        self.crear_controles()

    # =========================================
    # CONFIGURAR
    # =========================================
    def configurar_ventana(self):

        self.ventana.title("Reportes")

        self.ventana.geometry("700x400")

    # =========================================
    # CONTROLES
    # =========================================
    def crear_controles(self):

        total = self.service.total_ventas()

        cliente_top = self.service.cliente_top()

        tk.Label(
            self.ventana,
            text=f"Ventas Totales: S/. {total}",
            font=("Arial", 16, "bold")
        ).pack(pady=30)

        tk.Label(
            self.ventana,
            text=f"Cliente Top: {cliente_top}",
            font=("Arial", 16)
        ).pack(pady=20)