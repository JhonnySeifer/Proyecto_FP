# =========================================
# ARCHIVO: views/productos.py (REFORMADO)
# =========================================

import tkinter as tk
from tkinter import ttk

from services.producto_service import ProductoService
from utils.validaciones import (
    validar_input_precio,
    validar_input_stock
)


class FrmProductos:

    def __init__(self, parent):

        self.parent = parent
        self.parent.withdraw()

        self.service = ProductoService()

        self.producto_id = None
        self.productos_tabla = []

        self.ventana = tk.Toplevel()

        self.configurar_ventana()
        self.crear_estilos()
        self.crear_controles()
        self.cargar_productos()

        self.ventana.protocol("WM_DELETE_WINDOW", self.retornar)

    # =========================================
    # VENTANA
    # =========================================
    def configurar_ventana(self):

        self.ventana.title("Mantenimiento de Productos")
        self.ventana.state("zoomed")
        self.ventana.config(bg="#F3F4F6")

    # =========================================
    # ESTILOS
    # =========================================
    def crear_estilos(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            rowheight=35,
            font=("Segoe UI", 10),
            background="white",
            fieldbackground="white"
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

    # =========================================
    # CONTROLES
    # =========================================
    def crear_controles(self):

        # ================= TITULO =================
        titulo = tk.Label(
            self.ventana,
            text="MANTENIMIENTO DE PRODUCTOS",
            font=("Segoe UI", 24, "bold"),
            bg="#F3F4F6",
            fg="#111827"
        )
        titulo.pack(pady=20)

        # ================= BUSQUEDA =================
        frame_busqueda = tk.Frame(self.ventana, bg="#F3F4F6")
        frame_busqueda.pack(fill="x", padx=40, pady=(0, 20))

        self.txt_buscar = tk.Entry(
            frame_busqueda,
            font=("Segoe UI", 14),
            relief="solid",
            bd=1
        )
        self.txt_buscar.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))

        self.txt_buscar.bind("<KeyRelease>", lambda e: self.buscar())

        tk.Button(
            frame_busqueda,
            text="Buscar",
            bg="#2563EB",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.buscar
        ).pack(side="left")

        tk.Button(
            frame_busqueda,
            text="Retornar",
            bg="#6B7280",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.retornar
        ).pack(side="left", padx=10)

        # ================= CONTENIDO =================
        frame_contenido = tk.Frame(self.ventana, bg="#F3F4F6")
        frame_contenido.pack(fill="x", padx=40)

        # ================= FORMULARIO =================
        frame_formulario = tk.Frame(
            frame_contenido,
            bg="white",
            bd=1,
            relief="solid",
            padx=30,
            pady=30
        )
        frame_formulario.pack(side="left", anchor="n")

        # CODIGO
        self._label(frame_formulario, "Código", 0, 0)
        self.txt_codigo = self._entry(frame_formulario)
        self.txt_codigo.grid(row=1, column=0, pady=5)

        # PRODUCTO
        self._label(frame_formulario, "Producto", 0, 1, 20)
        self.txt_producto = self._entry(frame_formulario)
        self.txt_producto.grid(row=1, column=1, padx=(20, 0), pady=5)

        # CATEGORIA
        self._label(frame_formulario, "Categoría", 2, 0)
        self.cbo_categoria = ttk.Combobox(
            frame_formulario,
            state="readonly",
            width=28,
            font=("Segoe UI", 11),
            values=[
                "CAUCHO NATURAL",
                "CAUCHO SINTÉTICO",
                "PIGMENTOS",
                "SOLVENTES",
                "ADITIVOS"
            ]
        )
        self.cbo_categoria.grid(row=3, column=0, pady=5)

        # PRECIO
        self._label(frame_formulario, "Precio", 2, 1, 20)
        self.txt_precio = self._entry(frame_formulario)
        self.txt_precio.grid(row=3, column=1, padx=(20, 0), pady=5)

        # STOCK
        self._label(frame_formulario, "Stock", 4, 0)
        self.txt_stock = self._entry(frame_formulario)
        self.txt_stock.grid(row=5, column=0, pady=5)

        # ESTADO
        self._label(frame_formulario, "Estado", 4, 1, 20)
        self.cbo_estado = ttk.Combobox(
            frame_formulario,
            state="readonly",
            width=28,
            font=("Segoe UI", 11),
            values=["ACTIVO", "INACTIVO"]
        )
        self.cbo_estado.set("ACTIVO")
        self.cbo_estado.grid(row=5, column=1, padx=(20, 0), pady=5)

        # ================= BOTONES =================
        frame_botones = tk.Frame(frame_contenido, bg="#F3F4F6")
        frame_botones.pack(side="left", padx=40, anchor="n")

        self.btn_guardar = tk.Button(frame_botones, text="Guardar", bg="#16A34A", fg="white",
                                    command=self.guardar, width=15)
        self.btn_guardar.grid(row=0, column=0, padx=5, pady=5)

        tk.Button(frame_botones, text="Editar", bg="#D97706", fg="white",
                  command=self.editar, width=15).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(frame_botones, text="Eliminar", bg="#DC2626", fg="white",
                  command=self.eliminar, width=15).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(frame_botones, text="Listar", bg="#4B5563", fg="white",
                  command=self.cargar_productos, width=15).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(frame_botones, text="Limpiar", bg="#6B7280", fg="white",
                  command=self.limpiar, width=32).grid(row=2, column=0, columnspan=2, pady=5)

        # ================= TABLA =================
        frame_tabla = tk.Frame(self.ventana, bg="white", bd=1, relief="solid")
        frame_tabla.pack(fill="both", expand=True, padx=40, pady=30)

        columnas = (
            "numero", "codigo", "producto",
            "categoria", "precio", "stock", "estado"
        )

        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        headers = [
            ("numero", "N°"),
            ("codigo", "Código"),
            ("producto", "Producto"),
            ("categoria", "Categoría"),
            ("precio", "Precio"),
            ("stock", "Stock"),
            ("estado", "Estado")
        ]

        for c, t in headers:
            self.tabla.heading(c, text=t)
            self.tabla.column(c, width=120, anchor="center")

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    # =========================================
    # HELPERS UI
    # =========================================
    def _label(self, f, t, r, c, p=0):
        tk.Label(
            f,
            text=t,
            bg="white",
            font=("Segoe UI", 10, "bold")
        ).grid(row=r, column=c, padx=(p, 0), sticky="w")

    def _entry(self, f):
        return tk.Entry(
            f,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1
        )

    # =========================================
    # CARGAR
    # =========================================
    def cargar_productos(self):
        self.tabla.delete(*self.tabla.get_children())
        self.productos_tabla = self.service.listar_productos()  # solo activos
        for p in self.productos_tabla:
            self.tabla.insert(
                "",
                "end",
                iid=p["id_producto"],
                values=(
                    p["id_producto"],
                    p["codigo"],
                    p["nombre"],
                    p["categoria"],
                    p["precio"],
                    p["stock"],
                    p["estado"]
                )
            )

    # =========================================
    # BUSCAR
    # =========================================
    def buscar(self):

        txt = self.txt_buscar.get().lower()

        filtrados = [
            p for p in self.productos_tabla
            if txt in f"{p['codigo']} {p['nombre']} {p['categoria']}".lower()
        ]

        self.tabla.delete(*self.tabla.get_children())

        for p in filtrados:
            self.tabla.insert(
                "",
                "end",
                iid=p["id"],
                values=(
                    p["id"],
                    p["codigo"],
                    p["nombre"],
                    p["categoria"],
                    p["precio"],
                    p["stock"],
                    p["estado"]
                )
            )

    # =========================================
    # SELECCIONAR
    # =========================================
    def seleccionar(self, event):
        sel = self.tabla.selection()
        if not sel:
            return

        producto_id = int(sel[0])
        p = next((x for x in self.productos_tabla if x["id_producto"] == producto_id), None)
        if not p:
            return

        self.producto_id = p["id_producto"]

        self.txt_codigo.delete(0, tk.END)
        self.txt_codigo.insert(0, p["codigo"])
        self.txt_producto.delete(0, tk.END)
        self.txt_producto.insert(0, p["nombre"])
        self.cbo_categoria.set(p["categoria"])
        self.txt_precio.delete(0, tk.END)
        self.txt_precio.insert(0, p["precio"])
        self.txt_stock.delete(0, tk.END)
        self.txt_stock.insert(0, p["stock"])
        self.cbo_estado.set(p["estado"])

        # 👇 Deshabilitar Guardar
        self.btn_guardar.config(state="disabled")

    # =========================================
    # CRUD
    # =========================================
    def guardar(self):
        self.service.guardar_producto(
            self.txt_codigo.get(),
            self.txt_producto.get(),
            self.cbo_categoria.get(),
            float(self.txt_precio.get()),
            int(self.txt_stock.get()),
            "ACTIVO"
        )
        self.cargar_productos()
        self.limpiar()

    def editar(self):
        if self.producto_id is None:
            return
        self.service.editar_producto(
            self.producto_id,
            self.txt_codigo.get(),
            self.txt_producto.get(),
            self.cbo_categoria.get(),
            float(self.txt_precio.get()),
            int(self.txt_stock.get()),
            self.cbo_estado.get()
        )
        self.cargar_productos()
        self.limpiar()

    def eliminar(self):
        if self.producto_id is None:
            return
        self.service.eliminar_producto(self.producto_id)
        self.productos_tabla = self.service.listar_productos()  # solo activos
        self._llenar_tabla(self.productos_tabla)
        self.limpiar()

    # =========================================
    # LIMPIAR
    # =========================================
    def limpiar(self):
        self.producto_id = None
        for e in [self.txt_codigo, self.txt_producto, self.txt_precio, self.txt_stock]:
            e.delete(0, tk.END)

        self.cbo_categoria.set("")
        self.cbo_estado.set("ACTIVO")

        # Habilitar Guardar nuevamente
        self.btn_guardar.config(state="normal")

    # =========================================
    # RETORNAR
    # =========================================
    def retornar(self):
        self.parent.deiconify()
        self.ventana.destroy()