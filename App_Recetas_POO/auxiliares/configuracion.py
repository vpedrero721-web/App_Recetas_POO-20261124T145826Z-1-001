import os
from dotenv import load_dotenv

load_dotenv()

NOMBRE_APP = "App de Recetas"
DIFICULTADES_VALIDAS = ("Fácil", "Media", "Difícil")
MAX_INTENTOS_LOGIN = 3
LARGO_MINIMO_CONTRASENA = 6

DB_HOST = os.getenv("RECETAS_DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("RECETAS_DB_PORT", "3306"))
DB_USER = os.getenv("RECETAS_DB_USER", "root")
DB_PASSWORD = os.getenv("RECETAS_DB_PASSWORD", "")
DB_NAME = os.getenv("RECETAS_DB_NAME", "recetas")

WEB_HOST = os.getenv("RECETAS_WEB_HOST", "127.0.0.1")
WEB_PORT = int(os.getenv("RECETAS_WEB_PORT", "8000"))

USUARIO_INICIAL_NOMBRE = "Administrador"
USUARIO_INICIAL_EMAIL = "admin@recetas.cl"
USUARIO_INICIAL_CONTRASENA = os.getenv("RECETAS_ADMIN_PASSWORD", "admin123")
