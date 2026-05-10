from utils.archivo import leer_json, guardar_json

class ClienteRepository:
    """
    Repositorio encargado de la persistencia de clientes en clientes.json
    """

    def __init__(self):
        self.ruta = "D:/Workspace/Python/Proyecto_FP/data/clientes.json"

    def listar_clientes(self) -> list:
        return leer_json(self.ruta)

    def guardar_cliente(self, cliente: dict) -> None:
        clientes = self.listar_clientes()
        clientes.append(cliente)
        guardar_json(self.ruta, clientes)

    def editar_cliente(self, id_cliente: int, nuevo_cliente: dict) -> None:
        clientes = self.listar_clientes()
        for i, cliente in enumerate(clientes):
            if cliente["id_cliente"] == id_cliente:
                clientes[i] = nuevo_cliente
                break
        guardar_json(self.ruta, clientes)

    def cambiar_estado_cliente(self, id_cliente: int, estado: str) -> None:
        clientes = self.listar_clientes()
        for cliente in clientes:
            if cliente["id_cliente"] == id_cliente:
                cliente["estado"] = estado
                break
        guardar_json(self.ruta, clientes)
