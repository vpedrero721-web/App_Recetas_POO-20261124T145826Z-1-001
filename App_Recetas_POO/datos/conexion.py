from peewee import DatabaseProxy, MySQLDatabase

from auxiliares.configuracion import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
)

database = DatabaseProxy()
database.initialize(
    MySQLDatabase(
        DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        charset="utf8mb4",
        connect_timeout=5,
    )
)


def conectar_bd() -> None:
    if database.is_closed():
        database.connect(reuse_if_open=True)


def cerrar_bd() -> None:
    if not database.is_closed():
        database.close()


def verificar_tablas() -> None:
    tablas_requeridas = {
        "usuarios",
        "categorias",
        "recetas",
        "ingredientes",
        "detalleingrediente",
        "recetascategorias",
        "valoraciones",
        "recetasguardadas",
    }
    with database.connection_context():
        existentes = {nombre.lower() for nombre in database.get_tables()}
        faltantes = tablas_requeridas - existentes
        if faltantes:
            nombres = ", ".join(sorted(faltantes))
            raise RuntimeError(
                f"Faltan tablas en la base de datos '{database.database}': {nombres}. "
                "Importa datos/sql/recetas.sql en MySQL/MariaDB."
            )


__all__ = ["database", "conectar_bd", "cerrar_bd", "verificar_tablas"]
