from peewee import fn

from datos.conexion import database
from datos.modelos.ingrediente import Ingrediente


def guardar_ingrediente(ingrediente: Ingrediente) -> Ingrediente:
    with database.connection_context():
        ingrediente.save()
    return ingrediente


def listar_ingredientes() -> list[Ingrediente]:
    with database.connection_context():
        return list(Ingrediente.select().order_by(Ingrediente.id_ingrediente))


def buscar_ingrediente_por_id(id_ingrediente: int) -> Ingrediente | None:
    with database.connection_context():
        return Ingrediente.get_or_none(Ingrediente.id_ingrediente == id_ingrediente)


def buscar_ingrediente_por_nombre(nombre: str) -> Ingrediente | None:
    texto = nombre.strip().lower()
    with database.connection_context():
        return (
            Ingrediente.select()
            .where(fn.LOWER(Ingrediente.nombre) == texto)
            .first()
        )


def buscar_ingredientes(texto: str) -> list[Ingrediente]:
    termino = texto.strip().lower()
    with database.connection_context():
        consulta = (
            Ingrediente.select()
            .where(
                (fn.LOWER(Ingrediente.nombre).contains(termino))
                | (fn.LOWER(Ingrediente.categoria_ingrediente).contains(termino))
            )
            .order_by(Ingrediente.id_ingrediente)
        )
        return list(consulta)


def eliminar_ingrediente(id_ingrediente: int) -> bool:
    with database.connection_context():
        ingrediente = Ingrediente.get_or_none(Ingrediente.id_ingrediente == id_ingrediente)
        if ingrediente is None:
            return False
        ingrediente.delete_instance()
        return True
