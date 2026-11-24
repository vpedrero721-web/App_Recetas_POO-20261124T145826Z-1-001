from auxiliares.validaciones import (
    validar_decimal_positivo,
    validar_dificultad,
    validar_entero_positivo,
    validar_texto,
)
from datos.modelos.ingrediente import Ingrediente
from datos.modelos.receta import Receta
from datos.repositorio import categoria_repo, ingrediente_repo, receta_repo, usuario_repo


class ServicioRecetas:
    def listar_recetas(self) -> list[Receta]:
        return receta_repo.listar_recetas()

    def obtener_receta(self, id_receta: int) -> Receta | None:
        return receta_repo.buscar_receta_por_id(id_receta)

    def buscar_por_nombre(self, texto: str) -> list[Receta]:
        return receta_repo.buscar_recetas_por_nombre(texto)

    def buscar_por_categoria(self, texto: str) -> list[Receta]:
        return receta_repo.buscar_recetas_por_categoria(texto)

    def obtener_ingredientes(self, id_receta: int):
        return receta_repo.obtener_detalles_ingredientes(id_receta)

    def obtener_categorias(self, id_receta: int):
        return receta_repo.obtener_categorias_receta(id_receta)

    def crear_receta(
        self,
        nombre: str,
        descripcion: str,
        tiempo: int,
        dificultad: str,
        instrucciones: str,
        porciones: int,
        id_usuario: int | None = None,
        imagen_url: str | None = None,
    ) -> Receta:
        nombre_limpio = validar_texto(nombre, "nombre")
        desc_limpia = (descripcion or "").strip() or "Sin descripción."
        tiempo_valido = validar_entero_positivo(tiempo, "tiempo de preparación")
        dificultad_valida = validar_dificultad(dificultad or "Fácil")
        instrucciones_limpias = (instrucciones or "").strip() or "Sin instrucciones."
        porciones_validas = validar_entero_positivo(porciones, "porciones")

        autor = None
        if id_usuario is not None:
            autor = usuario_repo.buscar_usuario_por_id(id_usuario)
        if autor is None:
            usuarios = usuario_repo.listar_usuarios(solo_activos=True)
            if not usuarios:
                raise ValueError("No existe un usuario válido para asociar la receta.")
            autor = usuarios[0]

        receta = Receta(
            nombre=nombre_limpio,
            descripcion=desc_limpia,
            tiempo_preparacion=tiempo_valido,
            dificultad=dificultad_valida,
            instrucciones=instrucciones_limpias,
            porciones=porciones_validas,
            imagen_url=imagen_url,
            usuario=autor,
        )
        return receta_repo.guardar_receta(receta)

    def editar_receta(
        self,
        id_receta: int,
        nombre: str | None = None,
        descripcion: str | None = None,
        tiempo: int | None = None,
        dificultad: str | None = None,
        instrucciones: str | None = None,
        porciones: int | None = None,
    ) -> Receta:
        receta = receta_repo.buscar_receta_por_id(id_receta)
        if receta is None:
            raise ValueError("La receta no existe.")

        if nombre is not None and nombre.strip():
            receta.nombre = validar_texto(nombre, "nombre")
        if descripcion is not None and descripcion.strip():
            receta.descripcion = descripcion.strip()
        if tiempo is not None:
            receta.tiempo_preparacion = validar_entero_positivo(tiempo, "tiempo de preparación")
        if dificultad is not None and dificultad.strip():
            receta.dificultad = validar_dificultad(dificultad)
        if instrucciones is not None and instrucciones.strip():
            receta.instrucciones = instrucciones.strip()
        if porciones is not None:
            receta.porciones = validar_entero_positivo(porciones, "porciones")

        return receta_repo.guardar_receta(receta)

    def eliminar_receta(self, id_receta: int) -> bool:
        return receta_repo.eliminar_receta(id_receta)

    def agregar_ingrediente(
        self,
        id_receta: int,
        nombre_ingrediente: str,
        cantidad: str | int | float,
        unidad: str,
        categoria_ingrediente: str = "General",
    ):
        if receta_repo.buscar_receta_por_id(id_receta) is None:
            raise ValueError("La receta no existe.")

        nombre_limpio = validar_texto(nombre_ingrediente, "ingrediente")
        cantidad_valida = validar_decimal_positivo(cantidad, "cantidad")
        unidad_limpia = validar_texto(unidad or "unidad", "unidad de medida")

        ingrediente = ingrediente_repo.buscar_ingrediente_por_nombre(nombre_limpio)
        if ingrediente is None:
            ingrediente = ingrediente_repo.guardar_ingrediente(
                Ingrediente(
                    nombre=nombre_limpio,
                    categoria_ingrediente=categoria_ingrediente.strip() or "General",
                )
            )

        return receta_repo.guardar_detalle_ingrediente(
            id_receta,
            ingrediente.id_ingrediente,
            cantidad_valida,
            unidad_limpia,
        )

    def reemplazar_ingredientes(self, id_receta: int, lista_ingredientes: list[str]) -> None:
        if receta_repo.buscar_receta_por_id(id_receta) is None:
            raise ValueError("La receta no existe.")
        receta_repo.limpiar_ingredientes_receta(id_receta)
        for item in lista_ingredientes:
            nombre = item.strip()
            if nombre:
                self.agregar_ingrediente(id_receta, nombre, "1", "unidad")

    def asignar_categoria(self, id_receta: int, id_categoria: int):
        if receta_repo.buscar_receta_por_id(id_receta) is None:
            raise ValueError("La receta no existe.")
        if categoria_repo.buscar_categoria_por_id(id_categoria) is None:
            raise ValueError("La categoría no existe.")
        return receta_repo.asignar_categoria_receta(id_receta, id_categoria)
