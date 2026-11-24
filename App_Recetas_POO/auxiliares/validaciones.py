from decimal import Decimal, InvalidOperation
import re

from auxiliares.configuracion import DIFICULTADES_VALIDAS, LARGO_MINIMO_CONTRASENA

PATRON_EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validar_texto(valor: str, campo: str) -> str:
    texto = (valor or "").strip()
    if not texto:
        raise ValueError(f"El campo '{campo}' es obligatorio.")
    return texto


def validar_email(email: str) -> str:
    correo = (email or "").strip().lower()
    if not PATRON_EMAIL.match(correo):
        raise ValueError("El correo electrónico no tiene un formato válido.")
    return correo


def validar_entero_positivo(valor: int | str, campo: str) -> int:
    try:
        numero = int(valor)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"El campo '{campo}' debe ser un número entero.") from exc
    if numero <= 0:
        raise ValueError(f"El campo '{campo}' debe ser mayor a 0.")
    return numero


def validar_decimal_positivo(valor: Decimal | int | float | str, campo: str) -> Decimal:
    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"El campo '{campo}' debe ser un número válido.") from exc
    if numero <= 0:
        raise ValueError(f"El campo '{campo}' debe ser mayor a 0.")
    return numero


def validar_dificultad(dificultad: str) -> str:
    texto = (dificultad or "").strip()
    mapa = {
        "facil": "Fácil",
        "fácil": "Fácil",
        "media": "Media",
        "dificil": "Difícil",
        "difícil": "Difícil",
    }
    normalizada = mapa.get(texto.lower())
    if normalizada not in DIFICULTADES_VALIDAS:
        opciones = ", ".join(DIFICULTADES_VALIDAS)
        raise ValueError(f"La dificultad debe ser una de: {opciones}.")
    return normalizada


def validar_puntuacion(puntuacion: int | str) -> int:
    try:
        valor = int(puntuacion)
    except (TypeError, ValueError) as exc:
        raise ValueError("La puntuación debe ser un número entero entre 1 y 5.") from exc
    if valor < 1 or valor > 5:
        raise ValueError("La puntuación debe estar entre 1 y 5.")
    return valor


def validar_contrasena(contrasena: str) -> str:
    if not contrasena or len(contrasena) < LARGO_MINIMO_CONTRASENA:
        raise ValueError(
            f"La contraseña debe tener al menos {LARGO_MINIMO_CONTRASENA} caracteres."
        )
    return contrasena
