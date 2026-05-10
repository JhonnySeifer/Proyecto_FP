import tkinter as tk
from tkinter import messagebox

from views.principal import Principal


class Login:

    def __init__(self):

        # =========================================
        # VENTANA LOGIN
        # =========================================
        self.ventana = tk.Tk()

        self.configurar_ventana()

        self.crear_controles()

        self.ventana.mainloop()

    # =========================================
    # CONFIGURAR VENTANA
    # =========================================
    def configurar_ventana(self):

        self.ventana.title("Login")

        ancho = 1200
        alto = 700

        pantalla_ancho = self.ventana.winfo_screenwidth()
        pantalla_alto = self.ventana.winfo_screenheight()

        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)

        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.ventana.config(bg="#F5F5F5")

    # =========================================
    # CREAR CONTROLES
    # =========================================
    def crear_controles(self):

        titulo = tk.Label(
            self.ventana,
            text="LOGIN DEL SISTEMA",
            font=("Arial", 24, "bold"),
            bg="#F5F5F5"
        )

        titulo.pack(pady=40)

        frame = tk.Frame(
            self.ventana,
            bg="white",
            padx=40,
            pady=40
        )

        frame.pack()

        # Usuario
        tk.Label(
            frame,
            text="Usuario",
            bg="white"
        ).grid(row=0, column=0, pady=10)

        self.txt_usuario = tk.Entry(
            frame,
            width=30
        )

        self.txt_usuario.grid(row=0, column=1)

        # Password
        tk.Label(
            frame,
            text="Password",
            bg="white"
        ).grid(row=1, column=0, pady=10)

        self.txt_password = tk.Entry(
            frame,
            width=30,
            show="*"
        )

        self.txt_password.grid(row=1, column=1)

        # Botón
        btn_login = tk.Button(
            frame,
            text="Ingresar",
            width=20,
            command=self.validar
        )

        btn_login.grid(
            row=2,
            columnspan=2,
            pady=20
        )

    # =========================================
    # VALIDAR LOGIN
    # =========================================
    def validar(self):

        usuario = self.txt_usuario.get()
        password = self.txt_password.get()

        if usuario == "admin" and password == "123":

            messagebox.showinfo(
                "Correcto",
                "Bienvenido"
            )

            # Cerrar login
            self.ventana.destroy()

            # Abrir principal
            Principal()

        else:

            messagebox.showerror(
                "Error",
                "Credenciales incorrectas"
            )