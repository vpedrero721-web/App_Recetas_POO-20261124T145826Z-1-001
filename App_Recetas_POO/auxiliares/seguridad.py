import bcrypt
import maskpass


def hashear_contrasena(contrasena: str) -> str:
    datos = contrasena.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(datos, salt).decode("utf-8")


def verificar_contrasena(contrasena: str, password_hash: str) -> bool:
    if not contrasena or not password_hash:
        return False
    try:
        return bcrypt.checkpw(
            contrasena.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except ValueError:
        return False


def pedir_contrasena(mensaje: str = "Contraseña: ") -> str:
    return maskpass.askpass(prompt=mensaje, mask="*")
