from decimal import Decimal
from peewee import fn

from datos.conexion import database
from datos.modelos.categoria import Categoria
from datos.modelos.detalle_ingrediente import DetalleIngrediente
from datos.modelos.ingrediente import Ingrediente
from datos.modelos.receta import Receta
from datos.modelos.receta_categoria import RecetaCategoria
from datos.modelos.usuario import Usuario


def guardar_receta(receta: Receta) -> Receta:
    with database.connection_context():
        receta.save()
    return receta


def listar_recetas() -> list[Receta]:
    with database.connection_context():
        return list(
            Receta.select(Receta, Usuario)
            .join(Usuario)
            .order_by(Receta.id_receta)
        )


def buscar_receta_por_id(id_receta: int) -> Receta | None:
    with database.connection_context():
        return (
            Receta.select(Receta, Usuario)
            .join(Usuario)
            .where(Receta.id_receta == id_receta)
            .first()
        )


def buscar_recetas_por_nombre(texto: str) -> list[Receta]:
    termino = texto.strip().lower()
    with database.connection_context():
        if not termino:
            return listar_recetas()
        return list(
            Receta.select(Receta, Usuario)
            .join(Usuario)
            .where(
                (fn.LOWER(Receta.nombre).contains(termino))
                | (fn.LOWER(Receta.descripcion).contains(termino))
            )
            .order_by(Receta.id_receta)
        )


def buscar_recetas_por_categoria(nombre_categoria: str) -> list[Receta]:
    termino = nombre_categoria.strip().lower()
    with database.connection_context():
        if not termino:
            return listar_recetas()
        return list(
            Receta.select(Receta, Usuario)
            .join(Usuario)
            .switch(Receta)
            .join(RecetaCategoria)
            .join(Categoria)
            .where(fn.LOWER(Categoria.nombre).contains(termino))
            .distinct()
            .order_by(Receta.id_receta)
        )


def buscar_recetas_por_usuario(id_usuario: int) -> list[Receta]:
    with database.connection_context():
        return list(
            Receta.select(Receta, Usuario)
            .join(Usuario)
            .where(Receta.usuario == id_usuario)
            .order_by(Receta.id_receta)
        )


def eliminar_receta(id_receta: int) -> bool:
    with database.connection_context(), database.atomic():
        receta = Receta.get_or_none(Receta.id_receta == id_receta)
        if receta is None:
            return False
        DetalleIngrediente.delete().where(DetalleIngrediente.receta == id_receta).execute()
        RecetaCategoria.delete().where(RecetaCategoria.receta == id_receta).execute()
        receta.delete_instance()
        return True


def obtener_detalles_ingredientes(id_receta: int) -> list[DetalleIngrediente]:
    with database.connection_context():
        return list(
            DetalleIngrediente.select(DetalleIngrediente, Ingrediente)
            .join(Ingrediente)
            .where(DetalleIngrediente.receta == id_receta)
            .order_by(Ingrediente.nombre)
        )


def guardar_detalle_ingrediente(
    id_receta: int,
    id_ingrediente: int,
    cantidad: Decimal,
    unidad_medida: str,
) -> DetalleIngrediente:
    with database.connection_context():
        existente = DetalleIngrediente.get_or_none(
            (DetalleIngrediente.receta == id_receta)
            & (DetalleIngrediente.ingrediente == id_ingrediente)
        )
        if existente is None:
            detalle = DetalleIngrediente(
                receta=id_receta,
                ingrediente=id_ingrediente,
                cantidad=cantidad,
                unidad_medida=unidad_medida,
            )
            detalle.save(force_insert=True)
            return detalle

        existente.cantidad = cantidad
        existente.unidad_medida = unidad_medida
        existente.save()
        return existente


def limpiar_ingredientes_receta(id_receta: int) -> None:
    with database.connection_context():
        DetalleIngrediente.delete().where(DetalleIngrediente.receta == id_receta).execute()


def obtener_categorias_receta(id_receta: int) -> list[Categoria]:
    with database.connection_context():
        return list(
            Categoria.select()
            .join(RecetaCategoria)
            .where(RecetaCategoria.receta == id_receta)
            .order_by(Categoria.nombre)
        )


def asignar_categoria_receta(id_receta: int, id_categoria: int) -> RecetaCategoria:
    with database.connection_context():
        existente = RecetaCategoria.get_or_none(
            (RecetaCategoria.receta == id_receta)
            & (RecetaCategoria.categoria == id_categoria)
        )
        if existente is not None:
            return existente
        relacion = RecetaCategoria(receta=id_receta, categoria=id_categoria)
        relacion.save(force_insert=True)
        return relacion
