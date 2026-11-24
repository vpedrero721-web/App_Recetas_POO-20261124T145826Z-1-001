from datetime import date

from auxiliares.validaciones import validar_puntuacion
from datos.modelos.valoracion import Valoracion
from datos.repositorio import receta_repo, usuario_repo, valoracion_repo


class ServicioValoraciones:
    def listar_valoraciones(self) -> list[Valoracion]:
        return valoracion_repo.listar_valoraciones()

    def listar_por_receta(self, id_receta: int) -> list[Valoracion]:
        return valoracion_repo.buscar_valoraciones_por_receta(id_receta)

    def obtener_valoracion(self, id_valoracion: int) -> Valoracion | None:
        return valoracion_repo.buscar_valoracion_por_id(id_valoracion)

    def crear_valoracion(
        self,
        id_usuario: int,
        id_receta: int,
        puntuacion: int | str,
        comentario: str | None = None,
    ) -> Valoracion:
        if usuario_repo.buscar_usuario_por_id(id_usuario) is None:
            raise ValueError("El usuario no existe.")
        if receta_repo.buscar_receta_por_id(id_receta) is None:
            raise ValueError("La receta no existe.")

        puntos = validar_puntuacion(puntuacion)
        existente = valoracion_repo.buscar_valoracion_usuario_receta(id_usuario, id_receta)
        if existente is not None:
            raise ValueError("Ya valoraste esta receta. Puedes editar tu valoración.")

        valoracion = Valoracion(
            usuario=id_usuario,
            receta=id_receta,
            puntuacion=puntos,
            comentario=(comentario or "").strip() or None,
            fecha=date.today(),
        )
        return valoracion_repo.guardar_valoracion(valoracion)

    def editar_valoracion(
        self,
        id_valoracion: int,
        puntuacion: int | str | None = None,
        comentario: str | None = None,
    ) -> Valoracion:
        valoracion = valoracion_repo.buscar_valoracion_por_id(id_valoracion)
        if valoracion is None:
            raise ValueError("La valoración no existe.")

        if puntuacion is not None and str(puntuacion).strip():
            valoracion.puntuacion = validar_puntuacion(puntuacion)
        if comentario is not None and comentario.strip():
            valoracion.comentario = comentario.strip()
        valoracion.fecha = date.today()
        return valoracion_repo.guardar_valoracion(valoracion)

    def eliminar_valoracion(self, id_valoracion: int) -> bool:
        return valoracion_repo.eliminar_valoracion(id_valoracion)
