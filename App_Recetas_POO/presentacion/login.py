from auxiliares.configuracion import MAX_INTENTOS_LOGIN, NOMBRE_APP
from auxiliares.mensajes import MSG_ENTRADA_CERRADA, MSG_MAX_INTENTOS
from auxiliares.seguridad import pedir_contrasena
from datos.modelos.usuario import Usuario
from negocio.servicio_auth import autenticar_usuario


def iniciar_login() -> Usuario | None:
    print(f"\n=== {NOMBRE_APP.upper()} - INICIO DE SESIÓN ===")

    for intento in range(1, MAX_INTENTOS_LOGIN + 1):
        try:
            email = input("Correo electrónico: ").strip()
            contrasena = pedir_contrasena("Contraseña: ")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{MSG_ENTRADA_CERRADA}")
            return None

        try:
            usuario = autenticar_usuario(email, contrasena)
            print(f"\nBienvenido/a, {usuario.nombre}.")
            return usuario
        except ValueError as exc:
            restantes = MAX_INTENTOS_LOGIN - intento
            print(f"Error: {exc}")
            if restantes > 0:
                print(f"Intentos restantes: {restantes}\n")

    print(MSG_MAX_INTENTOS)
    return None
