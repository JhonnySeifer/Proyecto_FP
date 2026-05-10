from models.cliente import Cliente
from repositorios.cliente_repository import ClienteRepository

class ClienteService:
    """
    Lógica de negocio para clientes.
    """

    def __init__(self):
        self.repository = ClienteRepository()

    def listar_clientes(self) -> list:
        return [c for c in self.repository.listar_clientes() if c["estado"] == "ACTIVO"]

    def guardar_cliente(self, nombres, apellidos, dni, celular, direccion, correo) -> None:
        clientes = self.repository.listar_clientes()
        nuevo_id = max([c["id_cliente"] for c in clientes], default=0) + 1
        cliente = Cliente(nuevo_id, nombres, apellidos, dni, celular, direccion, correo)
        self.repository.guardar_cliente(cliente.to_dict())

    def editar_cliente(self, id_cliente, nombres, apellidos, dni, celular, direccion, correo, estado) -> None:
        cliente = Cliente(id_cliente, nombres, apellidos, dni, celular, direccion, correo, estado)
        self.repository.editar_cliente(id_cliente, cliente.to_dict())

    def eliminar_cliente(self, id_cliente) -> None:
        self.repository.cambiar_estado_cliente(id_cliente, "DADO DE BAJA")

    def listar_todos_clientes(self) -> list:
        """
        Devuelve todos los clientes sin importar estado.
        """
        return self.repository.listar_clientes()