from peewee import IntegrityError

from auxiliares.seguridad import hashear_contrasena
from auxiliares.validaciones import validar_contrasena, validar_email, validar_texto
from datos.modelos.usuario import Usuario
from datos.repositorio import usuario_repo


class ServicioUsuarios:
    def listar_usuarios(self, solo_activos: bool = False) -> list[Usuario]:
        return usuario_repo.listar_usuarios(solo_activos=solo_activos)

    def obtener_usuario(self, id_usuario: int) -> Usuario | None:
        return usuario_repo.buscar_usuario_por_id(id_usuario)

    def buscar_usuarios(self, texto: str) -> list[Usuario]:
        termino = (texto or "").strip()
        if not termino:
            return self.listar_usuarios()
        return usuario_repo.buscar_usuarios_por_nombre(termino)

    def crear_usuario(self, nombre: str, email: str, contrasena: str) -> Usuario:
        nombre_limpio = validar_texto(nombre, "nombre")
        correo = validar_email(email)
        clave = validar_contrasena(contrasena)

        if usuario_repo.buscar_usuario_por_email(correo) is not None:
            raise ValueError("Ya existe un usuario registrado con ese correo.")

        usuario = Usuario(
            nombre=nombre_limpio,
            email=correo,
            password_hash=hashear_contrasena(clave),
            activo=True,
        )
        return usuario_repo.guardar_usuario(usuario)

    def editar_usuario(
        self,
        id_usuario: int,
        nombre: str | None = None,
        email: str | None = None,
        contrasena: str | None = None,
    ) -> Usuario:
        usuario = usuario_repo.buscar_usuario_por_id(id_usuario)
        if usuario is None:
            raise ValueError("El usuario no existe.")

        if nombre is not None and nombre.strip():
            usuario.nombre = validar_texto(nombre, "nombre")

        if email is not None and email.strip():
            nuevo_email = validar_email(email)
            otro = usuario_repo.buscar_usuario_por_email(nuevo_email)
            if otro is not None and otro.id_usuario != id_usuario:
                raise ValueError("Ese correo ya pertenece a otro usuario.")
            usuario.email = nuevo_email

        if contrasena is not None and contrasena:
            clave = validar_contrasena(contrasena)
            usuario.password_hash = hashear_contrasena(clave)

        return usuario_repo.guardar_usuario(usuario)

    def deshabilitar_usuario(self, id_usuario: int, id_usuario_actual: int | None = None) -> bool:
        if id_usuario_actual is not None and id_usuario == id_usuario_actual:
            raise ValueError("No puedes deshabilitar tu propio usuario con sesión activa.")
        return usuario_repo.cambiar_estado_usuario(id_usuario, activo=False)

    def habilitar_usuario(self, id_usuario: int) -> bool:
        return usuario_repo.cambiar_estado_usuario(id_usuario, activo=True)

    def eliminar_usuario(self, id_usuario: int, id_usuario_actual: int | None = None) -> bool:
        if id_usuario_actual is not None and id_usuario == id_usuario_actual:
            raise ValueError("No puedes eliminar tu propio usuario con sesión activa.")
        try:
            return usuario_repo.eliminar_usuario(id_usuario)
        except IntegrityError as exc:
            raise ValueError(
                "No se puede eliminar el usuario porque tiene recetas asociadas. "
                "Puedes deshabilitarlo en su lugar."
            ) from exc
