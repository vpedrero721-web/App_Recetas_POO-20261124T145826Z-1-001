from auxiliares.validaciones import validar_texto
from datos.modelos.categoria import Categoria
from datos.repositorio import categoria_repo


class ServicioCategorias:
    def listar_categorias(self) -> list[Categoria]:
        return categoria_repo.listar_categorias()

    def obtener_categoria(self, id_categoria: int) -> Categoria | None:
        return categoria_repo.buscar_categoria_por_id(id_categoria)

    def buscar_categorias(self, texto: str) -> list[Categoria]:
        termino = (texto or "").strip()
        if not termino:
            return self.listar_categorias()
        return categoria_repo.buscar_categorias(termino)

    def crear_categoria(self, nombre: str, descripcion: str) -> Categoria:
        nombre_limpio = validar_texto(nombre, "nombre")
        desc_limpia = validar_texto(descripcion, "descripción")

        if categoria_repo.buscar_categoria_por_nombre(nombre_limpio) is not None:
            raise ValueError("Ya existe una categoría con ese nombre.")

        categoria = Categoria(nombre=nombre_limpio, descripcion=desc_limpia)
        return categoria_repo.guardar_categoria(categoria)

    def editar_categoria(
        self,
        id_categoria: int,
        nombre: str | None = None,
        descripcion: str | None = None,
    ) -> Categoria:
        categoria = categoria_repo.buscar_categoria_por_id(id_categoria)
        if categoria is None:
            raise ValueError("La categoría no existe.")

        if nombre is not None and nombre.strip():
            nuevo_nombre = validar_texto(nombre, "nombre")
            otra = categoria_repo.buscar_categoria_por_nombre(nuevo_nombre)
            if otra is not None and otra.id_categoria != id_categoria:
                raise ValueError("Ya existe otra categoría con ese nombre.")
            categoria.nombre = nuevo_nombre

        if descripcion is not None and descripcion.strip():
            categoria.descripcion = validar_texto(descripcion, "descripción")

        return categoria_repo.guardar_categoria(categoria)

    def eliminar_categoria(self, id_categoria: int) -> bool:
        return categoria_repo.eliminar_categoria(id_categoria)
