import tkinter as tk
from tkinter import ttk, messagebox

from services.venta_service import VentaService
from services.producto_service import ProductoService
from services.cliente_service import ClienteService

from utils.validaciones import validar_cantidad


class FrmVentas:

    def __init__(self, parent):

        self.parent = parent
        self.parent.withdraw()

        self.venta_service = VentaService()
        self.producto_service = ProductoService()
        self.cliente_service = ClienteService()

        # ================= ESTADO =================
        self.cliente_actual = None
        self.producto_actual = None
        self.detalles = []

        self.clientes = []
        self.productos = []          # FIX CLAVE
        self.filtro_clientes = []

        # ================= VENTANA =================
        self.ventana = tk.Toplevel()
        self.configurar_ventana()
        self.crear_controles()

        self.cargar_datos()

        self.ventana.protocol("WM_DELETE_WINDOW", self.retornar)

    # =========================================
    # VENTANA
    # =========================================
    def configurar_ventana(self):
        self.ventana.title("Mantenimiento de Ventas")
        self.ventana.state("zoomed")
        self.ventana.config(bg="#F3F4F6")

    # =========================================
    # UI
    # =========================================
    def crear_controles(self):

        tk.Label(
            self.ventana,
            text="MANTENIMIENTO DE VENTAS",
            font=("Segoe UI", 22, "bold"),
            bg="#F3F4F6"
        ).pack(pady=10)

        frame_top = tk.Frame(self.ventana, bg="#F3F4F6")
        frame_top.pack(fill="x", padx=40)

        tk.Button(frame_top, text="Buscar General",
                  bg="#2563EB", fg="white",
                  command=self.buscar_general).pack(side="left")

        tk.Button(frame_top, text="Retornar",
                  bg="#6B7280", fg="white",
                  command=self.retornar).pack(side="right")

        # ================= CLIENTES =================
        frame_cli = tk.LabelFrame(self.ventana, text="CLIENTES",
                                bg="white", font=("Segoe UI", 12, "bold"))
        frame_cli.pack(fill="x", padx=40, pady=10)

        tk.Label(frame_cli, text="Cliente", bg="white").grid(row=0, column=0, sticky="w")
        self.txt_cliente = tk.Entry(frame_cli, width=40)
        self.txt_cliente.grid(row=0, column=1, padx=10)
        self.txt_cliente.bind("<KeyRelease>", self.buscar_clientes)

        self.lbl_dni = tk.Label(frame_cli, text="DNI: ---", bg="white")
        self.lbl_dni.grid(row=0, column=2, padx=20)

        tk.Label(frame_cli, text="Sucursal", bg="white").grid(row=1, column=0, sticky="w")
        self.txt_sucursal = tk.Entry(frame_cli, width=40)
        self.txt_sucursal.grid(row=1, column=1, padx=10)

        self.lst_clientes = tk.Listbox(self.ventana, height=4)
        self.lst_clientes.pack(fill="x", padx=40)
        self.lst_clientes.bind("<<ListboxSelect>>", self.seleccionar_cliente)

        # ================= PRODUCTOS =================
        frame_prod = tk.LabelFrame(self.ventana, text="PRODUCTOS",
                                bg="white", font=("Segoe UI", 12, "bold"))
        frame_prod.pack(fill="x", padx=40, pady=10)

        # Código y Nombre
        tk.Label(frame_prod, text="Código", bg="white").grid(row=0, column=0, sticky="w")
        self.txt_codigo = tk.Entry(frame_prod, width=20)
        self.txt_codigo.grid(row=0, column=1, padx=10)
        self.txt_codigo.bind("<KeyRelease>", self.buscar_productos)

        tk.Label(frame_prod, text="Nombre", bg="white").grid(row=0, column=2, sticky="w")
        self.txt_nombre = tk.Entry(frame_prod, width=30)
        self.txt_nombre.grid(row=0, column=3, padx=10)
        self.txt_nombre.bind("<KeyRelease>", self.buscar_productos)

        # Categoría y Precio
        tk.Label(frame_prod, text="Categoría", bg="white").grid(row=1, column=0, sticky="w")
        self.txt_categoria = tk.Entry(frame_prod, width=20)
        self.txt_categoria.grid(row=1, column=1, padx=10)

        tk.Label(frame_prod, text="Precio", bg="white").grid(row=1, column=2, sticky="w")
        self.txt_precio = tk.Entry(frame_prod, width=10)
        self.txt_precio.grid(row=1, column=3, padx=10)

        # Stock y Cantidad
        tk.Label(frame_prod, text="Stock", bg="white").grid(row=2, column=0, sticky="w")
        self.txt_stock = tk.Entry(frame_prod, width=10)
        self.txt_stock.grid(row=2, column=1, padx=10)

        tk.Label(frame_prod, text="Cantidad", bg="white").grid(row=2, column=2, sticky="w")
        self.txt_cantidad = tk.Entry(frame_prod, width=10)
        self.txt_cantidad.grid(row=2, column=3, padx=10)

        # 👇 Botón Agregar en su propia fila
        tk.Button(frame_prod, text="Agregar", bg="#16A34A", fg="white",
                command=self.agregar_producto).grid(row=3, column=0, columnspan=4, pady=10)

        # Tabla de productos debajo de todo
        self.tabla_productos = ttk.Treeview(
            frame_prod,
            columns=("id", "codigo", "nombre", "categoria", "precio", "stock"),
            show="headings",
            height=5
        )
        for c in self.tabla_productos["columns"]:
            self.tabla_productos.heading(c, text=c.upper())
        self.tabla_productos.grid(row=4, column=0, columnspan=4, pady=10)
        self.tabla_productos.bind("<<TreeviewSelect>>", self.seleccionar_producto)


        # ================= DETALLE =================
        self.tabla_detalle = ttk.Treeview(
            self.ventana,
            columns=("producto", "cantidad", "precio", "subtotal"),
            show="headings"
        )

        for c in self.tabla_detalle["columns"]:
            self.tabla_detalle.heading(c, text=c.upper())

        self.tabla_detalle.pack(fill="x", padx=40, pady=10)

        frame_total = tk.Frame(self.ventana, bg="#F3F4F6")
        frame_total.pack(fill="x", padx=40, pady=10)

        self.lbl_total = tk.Label(
            self.ventana,
            text="TOTAL: 0.00",
            font=("Segoe UI", 18, "bold"),
            bg="#F3F4F6"
        )
        self.lbl_total.pack(side="right")

        frame_botones = tk.Frame(self.ventana, bg="#F3F4F6")
        frame_botones.pack(fill="x", padx=40, pady=10)

        tk.Button(frame_botones, text="Guardar", bg="#16A34A", fg="white",
                command=self.guardar_venta, width=15).pack(side="left", padx=5)

        tk.Button(frame_botones, text="Editar", bg="#D97706", fg="white",
                command=self.editar_venta, width=15).pack(side="left", padx=5)

        tk.Button(frame_botones, text="Eliminar", bg="#DC2626", fg="white",
                command=self.eliminar_venta, width=15).pack(side="left", padx=5)

        tk.Button(frame_botones, text="Listar", bg="#4B5563", fg="white",
                command=self.listar_ventas, width=15).pack(side="left", padx=5)

        tk.Button(frame_botones, text="Limpiar", bg="#6B7280", fg="white",
                command=self.limpiar, width=15).pack(side="left", padx=5)


    # =========================================
    # CARGA INICIAL (IMPORTANTE)
    # =========================================
    def cargar_datos(self):

        self.clientes = self.cliente_service.listar_clientes() or []
        self.productos = self.producto_service.listar_productos() or []

        self.llenar_productos(self.productos)

        if not self.productos:
            messagebox.showwarning("Aviso", "No hay productos activos")

    # =========================================
    # CLIENTES
    # =========================================
    def buscar_clientes(self, e):

        txt = self.txt_cliente.get().lower()

        self.lst_clientes.delete(0, tk.END)

        self.filtro_clientes = [
            c for c in self.clientes
            if txt in f"{c['nombres']} {c['apellidos']}".lower()
        ]

        for c in self.filtro_clientes:
            self.lst_clientes.insert(
                tk.END,
                f"{c['nombres']} {c['apellidos']} - {c['dni']}"
            )

    def seleccionar_cliente(self, e):

        if not self.lst_clientes.curselection():
            return

        self.cliente_actual = self.filtro_clientes[
            self.lst_clientes.curselection()[0]
        ]

        self.txt_cliente.delete(0, tk.END)
        self.txt_cliente.insert(0,
                                f"{self.cliente_actual['nombres']} {self.cliente_actual['apellidos']}")

        self.lbl_dni.config(text=f"DNI: {self.cliente_actual['dni']}")

    # =========================================
    # PRODUCTOS (FIX CENTRAL)
    # =========================================
    def llenar_productos(self, data):
        self.tabla_productos.delete(*self.tabla_productos.get_children())
        for p in data:
            self.tabla_productos.insert(
                "",
                "end",
                iid=p["id_producto"],   # Id Productos
                values=(
                    p["id_producto"],
                    p["codigo"],
                    p["nombre"],
                    p["categoria"],
                    p["precio"],
                    p["stock"]
                )
            )

    def buscar_productos(self, e):
        txt = self.txt_buscar_producto.get().lower()
        filtrados = [
            p for p in self.productos
            if txt in f"{p['codigo']} {p['nombre']} {p['categoria']}".lower()
        ]

        self.llenar_productos(filtrados)

    def seleccionar_producto(self, e):
        sel = self.tabla_productos.selection()
        if not sel:
            return
        pid = int(sel[0])
        self.producto_actual = next(
            (p for p in self.productos if p["id_producto"] == pid),
            None
        )
        if self.producto_actual:
            self.txt_codigo.delete(0, tk.END)
            self.txt_codigo.insert(0, self.producto_actual["codigo"])
            self.txt_nombre.delete(0, tk.END)
            self.txt_nombre.insert(0, self.producto_actual["nombre"])
            self.txt_categoria.delete(0, tk.END)
            self.txt_categoria.insert(0, self.producto_actual["categoria"])
            self.txt_precio.delete(0, tk.END)
            self.txt_precio.insert(0, self.producto_actual["precio"])
            self.txt_stock.delete(0, tk.END)
            self.txt_stock.insert(0, self.producto_actual["stock"])


    # =========================================
    # DETALLE
    # =========================================
    def agregar_producto(self):
        if not self.producto_actual:
            messagebox.showwarning("Validación", "Seleccione producto en la tabla")
            return

        cantidad = self.txt_cantidad.get()
        if not validar_cantidad(cantidad):
            return

        cantidad = int(cantidad)
        if cantidad > self.producto_actual["stock"]:
            messagebox.showerror("Stock", "Stock insuficiente")
            return

        subtotal = cantidad * float(self.producto_actual["precio"])

        self.detalles.append({
            "id_producto": self.producto_actual["id_producto"],
            "producto": self.producto_actual["nombre"],
            "cantidad": cantidad,
            "precio": self.producto_actual["precio"],
            "subtotal": subtotal
        })

        self.tabla_detalle.insert("", "end", values=(
            self.producto_actual["nombre"],
            cantidad,
            self.producto_actual["precio"],
            subtotal
        ))

        self.calcular_total()

    def calcular_total(self):
        total = sum(d["subtotal"] for d in self.detalles)
        self.lbl_total.config(text=f"TOTAL: {round(total,2)}")

    # =========================================
    # GENERAL
    # =========================================
    def buscar_general(self):
        messagebox.showinfo("Info", "Pendiente implementación")

    def limpiar(self):
        self.detalles = []
        self.tabla_detalle.delete(*self.tabla_detalle.get_children())
        self.lbl_total.config(text="TOTAL: 0.00")

        # limpiar cliente y sucursal
        self.txt_cliente.delete(0, tk.END)
        self.txt_sucursal.delete(0, tk.END)
        self.lbl_dni.config(text="DNI: ---")
        self.cliente_actual = None

        # limpiar producto
        for e in [self.txt_codigo, self.txt_nombre, self.txt_categoria, self.txt_precio, self.txt_stock, self.txt_cantidad]:
            e.delete(0, tk.END)
        self.producto_actual = None

    def retornar(self):
        self.parent.deiconify()
        self.ventana.destroy()

    # =========================================
    # VENTAS CRUD
    # =========================================
    def guardar_venta(self):
        if not self.cliente_actual or not self.detalles:
            messagebox.showwarning("Validación", "Seleccione cliente y productos")
            return

        sucursal = self.txt_sucursal.get()
        subtotal = sum(d["subtotal"] for d in self.detalles)
        igv = round(subtotal * 0.18, 2)
        total = subtotal + igv

        self.venta_service.guardar_venta(
            self.cliente_actual["id_cliente"],
            sucursal,
            subtotal,
            igv,
            total,
            self.detalles
        )

        messagebox.showinfo("Éxito", "Venta registrada correctamente")
        self.limpiar()

    def editar_venta(self):
        messagebox.showinfo("Info", "Funcionalidad de edición pendiente")

    def eliminar_venta(self):
        messagebox.showinfo("Info", "Funcionalidad de eliminación pendiente")

    def listar_ventas(self):
        ventas = self.venta_service.listar_ventas()
        if not ventas:
            messagebox.showwarning("Aviso", "No hay ventas registradas")
            return

        popup = tk.Toplevel(self.ventana)
        popup.title("Listado de Ventas")

        tabla = ttk.Treeview(popup, columns=("id", "cliente", "sucursal", "total"), show="headings")
        for c in ("id", "cliente", "sucursal", "total"):
            tabla.heading(c, text=c.upper())
        tabla.pack(fill="both", expand=True)

        for v in ventas:
            tabla.insert("", "end", values=(v["id_venta"], v["cliente"], v["sucursal"], v["total"]))

        # Botón Editar dentro del popup
        def editar_seleccion():
            sel = tabla.selection()
            if not sel:
                messagebox.showwarning("Aviso", "Seleccione una venta")
                return
            vid = tabla.item(sel[0])["values"][0]
            venta = next((x for x in ventas if x["id_venta"] == vid), None)
            if venta:
                # 👇 aquí cargas los datos de la venta en el formulario principal
                self.txt_cliente.delete(0, tk.END)
                self.txt_cliente.insert(0, venta["cliente"])
                self.txt_sucursal.delete(0, tk.END)
                self.txt_sucursal.insert(0, venta["sucursal"])
                self.lbl_total.config(text=f"TOTAL: {venta['total']}")
                # detalles se deberían cargar también si tu service los devuelve
                popup.destroy()

        tk.Button(popup, text="Editar Seleccionada", bg="#D97706", fg="white",
                command=editar_seleccion).pack(pady=10)


