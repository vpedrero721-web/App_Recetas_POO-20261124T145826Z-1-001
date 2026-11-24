from auxiliares.configuracion import (
    USUARIO_INICIAL_CONTRASENA,
    USUARIO_INICIAL_EMAIL,
    USUARIO_INICIAL_NOMBRE,
)
from auxiliares.seguridad import hashear_contrasena, verificar_contrasena
from auxiliares.validaciones import validar_email
from datos.modelos.usuario import Usuario
from datos.repositorio import usuario_repo


def asegurar_usuario_inicial() -> Usuario:
    existente = usuario_repo.buscar_usuario_por_email(USUARIO_INICIAL_EMAIL)
    if existente is not None:
        return existente

    admin = Usuario(
        nombre=USUARIO_INICIAL_NOMBRE,
        email=USUARIO_INICIAL_EMAIL,
        password_hash=hashear_contrasena(USUARIO_INICIAL_CONTRASENA),
        activo=True,
    )
    return usuario_repo.guardar_usuario(admin)


def autenticar_usuario(email: str, contrasena: str) -> Usuario:
    correo = validar_email(email)
    usuario = usuario_repo.buscar_usuario_por_email(correo)
    if usuario is None:
        raise ValueError("Correo o contraseña incorrectos.")
    if not usuario.activo:
        raise ValueError("Este usuario se encuentra deshabilitado.")
    if not verificar_contrasena(contrasena, usuario.password_hash):
        raise ValueError("Correo o contraseña incorrectos.")
    return usuario
