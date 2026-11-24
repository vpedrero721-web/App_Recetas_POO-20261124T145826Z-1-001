from datos.conexion import database
from datos.modelos.receta import Receta
from datos.modelos.usuario import Usuario
from datos.modelos.valoracion import Valoracion


def guardar_valoracion(valoracion: Valoracion) -> Valoracion:
    with database.connection_context():
        valoracion.save()
    return valoracion


def listar_valoraciones() -> list[Valoracion]:
    with database.connection_context():
        return list(
            Valoracion.select(Valoracion, Usuario, Receta)
            .join(Usuario)
            .switch(Valoracion)
            .join(Receta)
            .order_by(Valoracion.fecha.desc(), Valoracion.id_valoracion.desc())
        )


def buscar_valoracion_por_id(id_valoracion: int) -> Valoracion | None:
    with database.connection_context():
        return (
            Valoracion.select(Valoracion, Usuario, Receta)
            .join(Usuario)
            .switch(Valoracion)
            .join(Receta)
            .where(Valoracion.id_valoracion == id_valoracion)
            .first()
        )


def buscar_valoraciones_por_receta(id_receta: int) -> list[Valoracion]:
    with database.connection_context():
        return list(
            Valoracion.select(Valoracion, Usuario, Receta)
            .join(Usuario)
            .switch(Valoracion)
            .join(Receta)
            .where(Valoracion.receta == id_receta)
            .order_by(Valoracion.fecha.desc())
        )


def buscar_valoracion_usuario_receta(id_usuario: int, id_receta: int) -> Valoracion | None:
    with database.connection_context():
        return Valoracion.get_or_none(
            (Valoracion.usuario == id_usuario) & (Valoracion.receta == id_receta)
        )


def eliminar_valoracion(id_valoracion: int) -> bool:
    with database.connection_context():
        valoracion = Valoracion.get_or_none(Valoracion.id_valoracion == id_valoracion)
        if valoracion is None:
            return False
        valoracion.delete_instance()
        return True
