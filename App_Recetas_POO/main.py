from datos.conexion import cerrar_bd, verificar_tablas
from negocio.servicio_auth import asegurar_usuario_inicial
from presentacion.login import iniciar_login
from presentacion.menu import MenuRecetas


def main() -> None:
    try:
        verificar_tablas()
        asegurar_usuario_inicial()
    except Exception as exc:
        print(f"Error al inicializar la base de datos: {exc}")
        return

    try:
        usuario = iniciar_login()
        if usuario is None:
            return
        app = MenuRecetas(usuario)
        app.ejecutar()
    finally:
        cerrar_bd()


if __name__ == "__main__":
    main()
