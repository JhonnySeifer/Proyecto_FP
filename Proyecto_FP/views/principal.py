# =========================================
# ARCHIVO: views/principal.py
# =========================================

import tkinter as tk

from views.clientes import FrmClientes
from views.productos import FrmProductos
from views.ventas import FrmVentas
from views.reportes import FrmReportes


class Principal:

    def __init__(self):

        self.ventana = tk.Tk()

        self.configurar_ventana()

        self.crear_menu()

        self.crear_dashboard()

        self.ventana.mainloop()

    # =========================================
    # CONFIGURAR VENTANA
    # =========================================
    def configurar_ventana(self):

        self.ventana.title("Sistema Facturación")

        ancho = 1200
        alto = 700

        pantalla_ancho = self.ventana.winfo_screenwidth()
        pantalla_alto = self.ventana.winfo_screenheight()

        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)

        self.ventana.geometry(
            f"{ancho}x{alto}+{x}+{y}"
        )

        self.ventana.config(bg="#ECEFF1")

    # =========================================
    # CREAR MENÚ
    # =========================================
    def crear_menu(self):

        menu = tk.Menu(self.ventana)

        menu.add_command(
            label="Clientes",
            command=self.abrir_clientes
        )

        menu.add_command(
            label="Productos",
            command=self.abrir_productos
        )

        menu.add_command(
            label="Ventas",
            command=self.abrir_ventas
        )

        menu.add_command(
            label="Reportes",
            command=self.abrir_reportes
        )

        self.ventana.config(menu=menu)

    # =========================================
    # DASHBOARD
    # =========================================
    def crear_dashboard(self):

        titulo = tk.Label(
            self.ventana,
            text="SISTEMA DE FACTURACIÓN",
            font=("Arial", 28, "bold"),
            bg="#ECEFF1"
        )

        titulo.pack(pady=40)

    # =========================================
    # NAVEGACIÓN
    # =========================================
    def abrir_clientes(self):

        FrmClientes(self.ventana)

    def abrir_productos(self):

        FrmProductos(self.ventana)

    def abrir_ventas(self):

        FrmVentas(self.ventana)

    def abrir_reportes(self):

        FrmReportes(self.ventana)