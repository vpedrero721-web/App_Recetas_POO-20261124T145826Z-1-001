from peewee import fn

from datos.conexion import database
from datos.modelos.categoria import Categoria


def guardar_categoria(categoria: Categoria) -> Categoria:
    with database.connection_context():
        categoria.save()
    return categoria


def listar_categorias() -> list[Categoria]:
    with database.connection_context():
        return list(Categoria.select().order_by(Categoria.id_categoria))


def buscar_categoria_por_id(id_categoria: int) -> Categoria | None:
    with database.connection_context():
        return Categoria.get_or_none(Categoria.id_categoria == id_categoria)


def buscar_categoria_por_nombre(nombre: str) -> Categoria | None:
    texto = nombre.strip().lower()
    with database.connection_context():
        return (
            Categoria.select()
            .where(fn.LOWER(Categoria.nombre) == texto)
            .first()
        )


def buscar_categorias(texto: str) -> list[Categoria]:
    termino = texto.strip().lower()
    with database.connection_context():
        consulta = (
            Categoria.select()
            .where(
                (fn.LOWER(Categoria.nombre).contains(termino))
                | (fn.LOWER(Categoria.descripcion).contains(termino))
            )
            .order_by(Categoria.id_categoria)
        )
        return list(consulta)


def eliminar_categoria(id_categoria: int) -> bool:
    with database.connection_context():
        categoria = Categoria.get_or_none(Categoria.id_categoria == id_categoria)
        if categoria is None:
            return False
        categoria.delete_instance()
        return True
