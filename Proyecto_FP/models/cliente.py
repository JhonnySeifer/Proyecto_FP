class Cliente:
    """
    Representa un cliente dentro del sistema de facturación.
    """

    def __init__(
        self,
        id_cliente: int,
        nombres: str,
        apellidos: str,
        dni: str,
        celular: str,
        direccion: str,
        correo: str,
        estado: str = "ACTIVO"
    ):
        self.id_cliente = id_cliente
        self.nombres = nombres
        self.apellidos = apellidos
        self.dni = dni
        self.celular = celular
        self.direccion = direccion
        self.correo = correo
        self.estado = estado

    def to_dict(self) -> dict:
        """
        Convierte el objeto Cliente en un diccionario listo para guardar en JSON.
        """
        return {
            "id_cliente": self.id_cliente,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "dni": self.dni,
            "celular": self.celular,
            "direccion": self.direccion,
            "correo": self.correo,
            "estado": self.estado
        }
