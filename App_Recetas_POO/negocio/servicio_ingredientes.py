from peewee import IntegrityError

from auxiliares.validaciones import validar_texto
from datos.modelos.ingrediente import Ingrediente
from datos.repositorio import ingrediente_repo


class ServicioIngredientes:
    def listar_ingredientes(self) -> list[Ingrediente]:
        return ingrediente_repo.listar_ingredientes()

    def obtener_ingrediente(self, id_ingrediente: int) -> Ingrediente | None:
        return ingrediente_repo.buscar_ingrediente_por_id(id_ingrediente)

    def buscar_ingredientes(self, texto: str) -> list[Ingrediente]:
        termino = (texto or "").strip()
        if not termino:
            return self.listar_ingredientes()
        return ingrediente_repo.buscar_ingredientes(termino)

    def crear_ingrediente(self, nombre: str, categoria_ingrediente: str) -> Ingrediente:
        nombre_limpio = validar_texto(nombre, "nombre")
        categoria_limpia = validar_texto(categoria_ingrediente, "categoría del ingrediente")

        if ingrediente_repo.buscar_ingrediente_por_nombre(nombre_limpio) is not None:
            raise ValueError("Ya existe un ingrediente con ese nombre.")

        ingrediente = Ingrediente(
            nombre=nombre_limpio,
            categoria_ingrediente=categoria_limpia,
        )
        return ingrediente_repo.guardar_ingrediente(ingrediente)

    def editar_ingrediente(
        self,
        id_ingrediente: int,
        nombre: str | None = None,
        categoria_ingrediente: str | None = None,
    ) -> Ingrediente:
        ingrediente = ingrediente_repo.buscar_ingrediente_por_id(id_ingrediente)
        if ingrediente is None:
            raise ValueError("El ingrediente no existe.")

        if nombre is not None and nombre.strip():
            nuevo_nombre = validar_texto(nombre, "nombre")
            otro = ingrediente_repo.buscar_ingrediente_por_nombre(nuevo_nombre)
            if otro is not None and otro.id_ingrediente != id_ingrediente:
                raise ValueError("Ya existe otro ingrediente con ese nombre.")
            ingrediente.nombre = nuevo_nombre

        if categoria_ingrediente is not None and categoria_ingrediente.strip():
            ingrediente.categoria_ingrediente = validar_texto(
                categoria_ingrediente, "categoría del ingrediente"
            )

        return ingrediente_repo.guardar_ingrediente(ingrediente)

    def eliminar_ingrediente(self, id_ingrediente: int) -> bool:
        try:
            return ingrediente_repo.eliminar_ingrediente(id_ingrediente)
        except IntegrityError as exc:
            raise ValueError(
                "No se puede eliminar el ingrediente porque está asociado a una o más recetas."
            ) from exc
