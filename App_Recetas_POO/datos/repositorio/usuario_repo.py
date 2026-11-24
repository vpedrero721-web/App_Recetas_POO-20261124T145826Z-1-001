from peewee import fn

from datos.conexion import database
from datos.modelos.usuario import Usuario


def guardar_usuario(usuario: Usuario) -> Usuario:
    with database.connection_context():
        usuario.save()
    return usuario


def listar_usuarios(solo_activos: bool = False) -> list[Usuario]:
    with database.connection_context():
        consulta = Usuario.select().order_by(Usuario.id_usuario)
        if solo_activos:
            consulta = consulta.where(Usuario.activo == True)  # noqa: E712
        return list(consulta)


def buscar_usuario_por_id(id_usuario: int) -> Usuario | None:
    with database.connection_context():
        return Usuario.get_or_none(Usuario.id_usuario == id_usuario)


def buscar_usuario_por_email(email: str) -> Usuario | None:
    correo = email.strip().lower()
    with database.connection_context():
        return (
            Usuario.select()
            .where(fn.LOWER(Usuario.email) == correo)
            .first()
        )


def buscar_usuarios_por_nombre(texto: str) -> list[Usuario]:
    with database.connection_context():
        consulta = (
            Usuario.select()
            .where(
                (fn.LOWER(Usuario.nombre).contains(texto.strip().lower()))
                | (fn.LOWER(Usuario.email).contains(texto.strip().lower()))
            )
            .order_by(Usuario.id_usuario)
        )
        return list(consulta)


def cambiar_estado_usuario(id_usuario: int, activo: bool) -> bool:
    with database.connection_context():
        usuario = Usuario.get_or_none(Usuario.id_usuario == id_usuario)
        if usuario is None:
            return False
        usuario.activo = activo
        usuario.save()
        return True


def eliminar_usuario(id_usuario: int) -> bool:
    with database.connection_context():
        usuario = Usuario.get_or_none(Usuario.id_usuario == id_usuario)
        if usuario is None:
            return False
        usuario.delete_instance()
        return True
