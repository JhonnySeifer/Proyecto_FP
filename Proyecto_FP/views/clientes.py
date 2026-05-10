# =========================================
# ARCHIVO: views/clientes.py
# =========================================

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from services.cliente_service import ClienteService
from utils.validaciones import (
    validar_dni,
    validar_celular,
    validar_correo,
    validar_requerido
)


class FrmClientes:

    def __init__(self, parent):
        self.parent = parent
        self.parent.withdraw()

        self.service = ClienteService()
        self.cliente_id = None
        self.clientes_tabla = []
        self.modo_busqueda = False

        self.ventana = tk.Toplevel()

        self.configurar_ventana()
        self.crear_estilos()
        self.crear_controles()
        self.cargar_clientes()

        self.ventana.protocol("WM_DELETE_WINDOW", self.retornar)

    # =========================================
    # VENTANA
    # =========================================
    def configurar_ventana(self):
        self.ventana.title("Mantenimiento de Clientes")
        self.ventana.state("zoomed")
        self.ventana.config(bg="#F3F4F6")

    # =========================================
    # ESTILOS
    # =========================================
    def crear_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=35, font=("Segoe UI", 10),
                        background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    # =========================================
    # CONTROLES
    # =========================================
    def crear_controles(self):
        titulo = tk.Label(self.ventana, text="MANTENIMIENTO DE CLIENTES", 
                          font=("Segoe UI", 24, "bold"), bg="#F3F4F6", fg="#111827")
        titulo.pack(pady=20)

        # BUSQUEDA
        frame_busqueda = tk.Frame(self.ventana, bg="#F3F4F6")
        frame_busqueda.pack(fill="x", padx=40, pady=(0, 20))

        self.txt_buscar = tk.Entry(frame_busqueda, font=("Segoe UI", 14), relief="solid", bd=1)
        self.txt_buscar.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))
        self.txt_buscar.bind("<KeyRelease>", lambda e: self.buscar())

        tk.Button(frame_busqueda, text="Buscar", bg="#2563EB", fg="white",
                  font=("Segoe UI", 10, "bold"), command=self.buscar).pack(side="left")

        tk.Button(frame_busqueda, text="Retornar", bg="#6B7280", fg="white",
                  font=("Segoe UI", 10, "bold"), command=self.retornar).pack(side="left", padx=10)

        # FORMULARIO
        frame_formulario = tk.Frame(self.ventana, bg="white", bd=1,
                                    relief="solid", padx=30, pady=30)
        frame_formulario.pack(side="left", anchor="n")

        self._label(frame_formulario, "Nombres", 0, 0)
        self.txt_nombres = self._entry(frame_formulario); self.txt_nombres.grid(row=1, column=0, pady=5)

        self._label(frame_formulario, "Apellidos", 0, 1, 20)
        self.txt_apellidos = self._entry(frame_formulario); self.txt_apellidos.grid(row=1, column=1, padx=(20,0), pady=5)

        self._label(frame_formulario, "DNI", 2, 0)
        self.txt_dni = self._entry(frame_formulario); self.txt_dni.grid(row=3, column=0, pady=5)

        self._label(frame_formulario, "Celular", 2, 1, 20)
        self.txt_celular = self._entry(frame_formulario); self.txt_celular.grid(row=3, column=1, padx=(20,0), pady=5)

        self._label(frame_formulario, "Dirección", 4, 0)
        self.txt_direccion = self._entry(frame_formulario, 65); self.txt_direccion.grid(row=5, column=0, columnspan=2, sticky="we", pady=5)

        self._label(frame_formulario, "Correo", 6, 0)
        self.txt_correo = self._entry(frame_formulario, 65); self.txt_correo.grid(row=7, column=0, columnspan=2, sticky="we", pady=5)

        self._label(frame_formulario, "Estado", 8, 0)
        self.cbo_estado = ttk.Combobox(frame_formulario, state="disabled", width=28,
                                       font=("Segoe UI", 11), values=["ACTIVO", "DADO DE BAJA", "PENALIZADO"])
        self.cbo_estado.set("ACTIVO"); self.cbo_estado.grid(row=9, column=0, sticky="w")

        # BOTONES
        frame_botones = tk.Frame(self.ventana, bg="#F3F4F6")
        frame_botones.pack(side="left", padx=40, anchor="n")

        self.btn_guardar = tk.Button(frame_botones, text="Guardar", bg="#16A34A", fg="white",
                                    command=self.guardar, width=15)
        self.btn_guardar.grid(row=0, column=0, padx=5, pady=5)

        tk.Button(frame_botones, text="Editar", bg="#D97706", fg="white",
                command=self.editar, width=15).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame_botones, text="Eliminar", bg="#DC2626", fg="white",
                  command=self.eliminar, width=15).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(frame_botones, text="Listar Activos", bg="#4B5563", fg="white",
                  command=self.cargar_clientes, width=15).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(frame_botones, text="Listar Todos", bg="#374151", fg="white",
                  command=self.listar_todos, width=15).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(frame_botones, text="Limpiar", bg="#6B7280", fg="white",
                  command=self.limpiar, width=15).grid(row=2, column=1, padx=5, pady=5)

        # TABLA
        frame_tabla = tk.Frame(self.ventana, bg="white", bd=1, relief="solid")
        frame_tabla.pack(fill="both", expand=True, padx=40, pady=30)

        columnas = ("numero", "nombres", "apellidos", "dni", "celular", "direccion", "correo")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        headers = [("numero", "N°"), ("nombres", "Nombres"), ("apellidos", "Apellidos"),
                   ("dni", "DNI"), ("celular", "Celular"), ("direccion", "Dirección"), ("correo", "Correo")]

        for c, t in headers:
            self.tabla.heading(c, text=t)
            self.tabla.column(c, width=120, anchor="center")

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

    # =========================================
    # HELPERS UI
    # =========================================
    def _label(self, f, t, r, c, p=0):
        tk.Label(f, text=t, bg="white", font=("Segoe UI",10,"bold")).grid(row=r, column=c, padx=(p,0), sticky="w")

    def _entry(self, f, w=30):
        return tk.Entry(f, width=w, font=("Segoe UI",11), relief="solid", bd=1)

    # =========================================
    # CARGAR
    # =========================================
    def cargar_clientes(self):
        # Solo clientes activos
        data = self.service.listar_clientes()
        self._llenar_tabla(data)

    def listar_todos(self):
        # Todos los clientes sin importar estado
        self.clientes_tabla = self.service.listar_todos_clientes()
        self._llenar_tabla(self.clientes_tabla)

    def _llenar_tabla(self, data):
        self.tabla.delete(*self.tabla.get_children())
        for c in data:
            self.tabla.insert(
                "",
                "end",
                iid=c["id_cliente"],
                values=(
                    c["id_cliente"],
                    c["nombres"],
                    c["apellidos"],
                    c["dni"],
                    c["celular"],
                    c["direccion"],
                    c["correo"],
                )
            )

    # =========================================
    # BUSCAR
    # =========================================
    def buscar(self):
        txt = self.txt_buscar.get().lower()
        data = self.service.listar_todos_clientes()
        filtrados = [
            c for c in data
            if txt in f"{c['nombres']} {c['apellidos']} {c['dni']} {c['celular']}".lower()
        ]
        self._llenar_tabla(filtrados)

    # =========================================
    # SELECCION
    # =========================================
    def seleccionar_cliente(self, event):
        sel = self.tabla.selection()
        if not sel:
            return

        cliente_id = int(sel[0])  # el iid es el id_cliente
        clientes = self.service.listar_todos_clientes()

        c = next((x for x in clientes if x["id_cliente"] == cliente_id), None)
        if not c:
            return

        self.cliente_id = c["id_cliente"]

        # Cargar datos en los textfields
        self.limpiar_campos()
        self.txt_nombres.insert(0, c["nombres"])
        self.txt_apellidos.insert(0, c["apellidos"])
        self.txt_dni.insert(0, c["dni"])
        self.txt_celular.insert(0, c["celular"])
        self.txt_direccion.insert(0, c["direccion"])
        self.txt_correo.insert(0, c["correo"])

        self.cbo_estado.config(state="readonly")
        self.cbo_estado.set(c["estado"])

        # Deshabilitar Guardar
        self.btn_guardar.config(state="disabled")

    # =========================================
    # LIMPIAR
    # =========================================
    def limpiar(self):
        self.cliente_id = None
        self.limpiar_campos()
        self.cbo_estado.set("ACTIVO")
        self.cbo_estado.config(state="disabled")
        self.tabla.selection_remove(self.tabla.selection())

        self.btn_guardar.config(state="normal")

    def limpiar_campos(self):
        for w in [self.txt_nombres, self.txt_apellidos, self.txt_dni,
                  self.txt_celular, self.txt_direccion, self.txt_correo]:
            w.delete(0, tk.END)

    # =========================================
    # CRUD
    # =========================================
    def guardar(self):
        self.service.guardar_cliente(
            self.txt_nombres.get(), self.txt_apellidos.get(),
            self.txt_dni.get(), self.txt_celular.get(),
            self.txt_direccion.get(), self.txt_correo.get()
        )
        self.cargar_clientes()
        self.limpiar()

    def editar(self):
        if self.cliente_id is None:
            return

        self.service.editar_cliente(
            self.cliente_id,
            self.txt_nombres.get(), self.txt_apellidos.get(),
            self.txt_dni.get(), self.txt_celular.get(),
            self.txt_direccion.get(), self.txt_correo.get(),
            self.cbo_estado.get()
        )
        self.cargar_clientes()
        self.limpiar()

    def eliminar(self):
        if self.cliente_id is None:
            return

        self.service.eliminar_cliente(self.cliente_id)
        # refrescar solo con clientes activos
        self.clientes_tabla = self.service.listar_clientes()
        self._llenar_tabla(self.clientes_tabla)
        self.limpiar()

    # =========================================
    # RETORNAR
    # =========================================
    def retornar(self):
        self.parent.deiconify()
        self.ventana.destroy()


