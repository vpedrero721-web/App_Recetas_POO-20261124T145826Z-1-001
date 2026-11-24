from auxiliares.configuracion import NOMBRE_APP
from auxiliares.mensajes import (
    MENU_CATEGORIAS,
    MENU_INGREDIENTES,
    MENU_PRINCIPAL,
    MENU_RECETAS,
    MENU_USUARIOS,
    MENU_VALORACIONES,
    MSG_ENTRADA_CERRADA,
    MSG_NO_ENCONTRADO,
    MSG_NUMERO_INVALIDO,
    MSG_OPCION_INVALIDA,
    MSG_PAUSA,
    MSG_SALIENDO,
)
from auxiliares.seguridad import pedir_contrasena
from datos.modelos.usuario import Usuario
from negocio.servicio_categorias import ServicioCategorias
from negocio.servicio_ingredientes import ServicioIngredientes
from negocio.servicio_recetas import ServicioRecetas
from negocio.servicio_usuarios import ServicioUsuarios
from negocio.servicio_valoraciones import ServicioValoraciones
from presentacion.web import iniciar_servidor


class MenuRecetas:
    def __init__(self, usuario_actual: Usuario) -> None:
        if usuario_actual is None:
            raise ValueError("Se requiere un usuario autenticado para acceder al menú.")
        self.usuario_actual = usuario_actual
        self.servicio_recetas = ServicioRecetas()
        self.servicio_categorias = ServicioCategorias()
        self.servicio_ingredientes = ServicioIngredientes()
        self.servicio_usuarios = ServicioUsuarios()
        self.servicio_valoraciones = ServicioValoraciones()

    def leer_entrada(self, mensaje: str) -> str:
        try:
            return input(mensaje).strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{MSG_ENTRADA_CERRADA}")
            raise SystemExit

    def leer_entero(self, mensaje: str) -> int | None:
        texto = self.leer_entrada(mensaje)
        try:
            return int(texto)
        except ValueError:
            print(MSG_NUMERO_INVALIDO)
            return None

    def _mostrar_opciones(self, titulo: str, opciones: tuple[str, ...]) -> None:
        print(f"\n=== {titulo} ===")
        for opcion in opciones:
            print(opcion)

    # ---------------- RECETAS ----------------

    def _menu_recetas(self) -> None:
        while True:
            self._mostrar_opciones("GESTIÓN DE RECETAS", MENU_RECETAS)
            opcion = self.leer_entrada("Seleccione una opción: ")

            if opcion == "1":
                self.listar_recetas()
            elif opcion == "2":
                id_receta = self.leer_entero("ID de la receta: ")
                if id_receta is not None:
                    self.mostrar_detalle_receta(id_receta)
            elif opcion == "3":
                self.buscar_receta_nombre()
            elif opcion == "4":
                self.buscar_receta_categoria()
            elif opcion == "5":
                self.crear_receta()
            elif opcion == "6":
                self.editar_receta()
            elif opcion == "7":
                self.eliminar_receta()
            elif opcion == "8":
                self.agregar_ingrediente_receta()
            elif opcion == "9":
                self.asignar_categoria_receta()
            elif opcion == "0":
                return
            else:
                print(MSG_OPCION_INVALIDA)

            self.leer_entrada(MSG_PAUSA)

    def listar_recetas(self) -> None:
        recetas = self.servicio_recetas.listar_recetas()
        if not recetas:
            print("No hay recetas registradas.")
            return
        print("\nRECETAS DISPONIBLES")
        for r in recetas:
            print(f"- [{r.id_receta}] {r.nombre} | {r.dificultad} | {r.tiempo_preparacion} min | Autor: {r.usuario.nombre}")
            print(f"  {r.descripcion}")

    def mostrar_detalle_receta(self, id_receta: int) -> None:
        receta = self.servicio_recetas.obtener_receta(id_receta)
        if receta is None:
            print(MSG_NO_ENCONTRADO)
            return

        print(f"\n=== {receta.nombre.upper()} ===")
        print(f"Autor: {receta.usuario.nombre}")
        print(f"Dificultad: {receta.dificultad}")
        print(f"Tiempo: {receta.tiempo_preparacion} min | Porciones: {receta.porciones}")
        print(f"Descripción: {receta.descripcion}")

        categorias = self.servicio_recetas.obtener_categorias(id_receta)
        if categorias:
            nombres_cat = ", ".join(c.nombre for c in categorias)
            print(f"Categorías: {nombres_cat}")

        print("\nIngredientes:")
        detalles = self.servicio_recetas.obtener_ingredientes(id_receta)
        if detalles:
            for d in detalles:
                print(f"- {d.ingrediente.nombre}: {d.cantidad} {d.unidad_medida}")
        else:
            print("- Sin ingredientes registrados.")

        print("\nPreparación:")
        pasos = (receta.instrucciones or "").splitlines()
        if pasos:
            for idx, paso in enumerate(pasos, start=1):
                print(f"{idx}. {paso.strip()}")
        else:
            print("Sin instrucciones.")

    def buscar_receta_nombre(self) -> None:
        texto = self.leer_entrada("Nombre o palabra clave: ")
        recetas = self.servicio_recetas.buscar_por_nombre(texto)
        if not recetas:
            print("No se encontraron recetas.")
            return
        for r in recetas:
            print(f"- [{r.id_receta}] {r.nombre} | {r.dificultad} | {r.tiempo_preparacion} min")

    def buscar_receta_categoria(self) -> None:
        texto = self.leer_entrada("Nombre de la categoría: ")
        recetas = self.servicio_recetas.buscar_por_categoria(texto)
        if not recetas:
            print("No se encontraron recetas en esa categoría.")
            return
        for r in recetas:
            print(f"- [{r.id_receta}] {r.nombre} | {r.dificultad} | {r.tiempo_preparacion} min")

    def crear_receta(self) -> None:
        print("\nNUEVA RECETA")
        nombre = self.leer_entrada("Nombre: ")
        descripcion = self.leer_entrada("Descripción: ")
        tiempo = self.leer_entero("Tiempo de preparación (min): ")
        if tiempo is None:
            return
        dificultad = self.leer_entrada("Dificultad (Fácil/Media/Difícil): ")
        instrucciones = self.leer_entrada("Instrucciones: ")
        porciones = self.leer_entero("Porciones: ")
        if porciones is None:
            return

        try:
            receta = self.servicio_recetas.crear_receta(
                nombre=nombre,
                descripcion=descripcion,
                tiempo=tiempo,
                dificultad=dificultad,
                instrucciones=instrucciones,
                porciones=porciones,
                id_usuario=self.usuario_actual.id_usuario,
            )
            print(f"Receta creada con ID {receta.id_receta}: {receta.nombre}")
        except ValueError as exc:
            print(f"Error: {exc}")

    def editar_receta(self) -> None:
        id_receta = self.leer_entero("ID de la receta a editar: ")
        if id_receta is None:
            return
        receta = self.servicio_recetas.obtener_receta(id_receta)
        if receta is None:
            print(MSG_NO_ENCONTRADO)
            return

        print(f"\nEditando: {receta.nombre} (deja vacío para mantener el valor actual)")
        nombre = self.leer_entrada(f"Nombre ({receta.nombre}): ")
        descripcion = self.leer_entrada(f"Descripción ({receta.descripcion}): ")
        tiempo_txt = self.leer_entrada(f"Tiempo en min ({receta.tiempo_preparacion}): ")
        dificultad = self.leer_entrada(f"Dificultad ({receta.dificultad}): ")
        resumen_inst = (receta.instrucciones or "")[:40]
        instrucciones = self.leer_entrada(f"Instrucciones ({resumen_inst}...): ")
        porciones_txt = self.leer_entrada(f"Porciones ({receta.porciones}): ")

        try:
            tiempo = int(tiempo_txt) if tiempo_txt else None
            porciones = int(porciones_txt) if porciones_txt else None
            editada = self.servicio_recetas.editar_receta(
                id_receta,
                nombre=nombre or None,
                descripcion=descripcion or None,
                tiempo=tiempo,
                dificultad=dificultad or None,
                instrucciones=instrucciones or None,
                porciones=porciones,
            )
            print(f"Receta actualizada: {editada.nombre}")
        except ValueError as exc:
            print(f"Error: {exc}")

    def eliminar_receta(self) -> None:
        id_receta = self.leer_entero("ID de la receta a eliminar: ")
        if id_receta is None:
            return
        if self.servicio_recetas.eliminar_receta(id_receta):
            print("Receta eliminada.")
        else:
            print(MSG_NO_ENCONTRADO)

    def agregar_ingrediente_receta(self) -> None:
        id_receta = self.leer_entero("ID de la receta: ")
        if id_receta is None:
            return
        nombre_ing = self.leer_entrada("Nombre del ingrediente: ")
        cantidad = self.leer_entrada("Cantidad (ej: 200 o 1.5): ")
        unidad = self.leer_entrada("Unidad de medida (ej: g, ml, unidades): ")
        try:
            self.servicio_recetas.agregar_ingrediente(id_receta, nombre_ing, cantidad, unidad)
            print("Ingrediente agregado a la receta.")
        except ValueError as exc:
            print(f"Error: {exc}")

    def asignar_categoria_receta(self) -> None:
        id_receta = self.leer_entero("ID de la receta: ")
        if id_receta is None:
            return
        self.listar_categorias()
        id_categoria = self.leer_entero("ID de la categoría a asignar: ")
        if id_categoria is None:
            return
        try:
            self.servicio_recetas.asignar_categoria(id_receta, id_categoria)
            print("Categoría asignada a la receta.")
        except ValueError as exc:
            print(f"Error: {exc}")

    # ---------------- CATEGORÍAS ----------------

    def _menu_categorias(self) -> None:
        while True:
            self._mostrar_opciones("GESTIÓN DE CATEGORÍAS", MENU_CATEGORIAS)
            opcion = self.leer_entrada("Seleccione una opción: ")

            if opcion == "1":
                self.listar_categorias()
            elif opcion == "2":
                texto = self.leer_entrada("Texto a buscar: ")
                resultados = self.servicio_categorias.buscar_categorias(texto)
                if not resultados:
                    print("No se encontraron categorías.")
                for c in resultados:
                    print(f"- [{c.id_categoria}] {c.nombre}: {c.descripcion}")
            elif opcion == "3":
                nombre = self.leer_entrada("Nombre: ")
                descripcion = self.leer_entrada("Descripción: ")
                try:
                    c = self.servicio_categorias.crear_categoria(nombre, descripcion)
                    print(f"Categoría creada: [{c.id_categoria}] {c.nombre}")
                except ValueError as exc:
                    print(f"Error: {exc}")
            elif opcion == "4":
                id_cat = self.leer_entero("ID de la categoría a editar: ")
                if id_cat is not None:
                    actual = self.servicio_categorias.obtener_categoria(id_cat)
                    if actual is None:
                        print(MSG_NO_ENCONTRADO)
                    else:
                        nombre = self.leer_entrada(f"Nuevo nombre ({actual.nombre}): ")
                        descripcion = self.leer_entrada(f"Nueva descripción ({actual.descripcion}): ")
                        try:
                            c = self.servicio_categorias.editar_categoria(
                                id_cat, nombre=nombre or None, descripcion=descripcion or None
                            )
                            print(f"Categoría actualizada: {c.nombre}")
                        except ValueError as exc:
                            print(f"Error: {exc}")
            elif opcion == "5":
                id_cat = self.leer_entero("ID de la categoría a eliminar: ")
                if id_cat is not None:
                    if self.servicio_categorias.eliminar_categoria(id_cat):
                        print("Categoría eliminada.")
                    else:
                        print(MSG_NO_ENCONTRADO)
            elif opcion == "0":
                return
            else:
                print(MSG_OPCION_INVALIDA)

            self.leer_entrada(MSG_PAUSA)

    def listar_categorias(self) -> None:
        categorias = self.servicio_categorias.listar_categorias()
        if not categorias:
            print("No hay categorías registradas.")
            return
        print("\nCATEGORÍAS")
        for c in categorias:
            print(f"- [{c.id_categoria}] {c.nombre}: {c.descripcion}")

    # ---------------- INGREDIENTES ----------------

    def _menu_ingredientes(self) -> None:
        while True:
            self._mostrar_opciones("GESTIÓN DE INGREDIENTES", MENU_INGREDIENTES)
            opcion = self.leer_entrada("Seleccione una opción: ")

            if opcion == "1":
                ingredientes = self.servicio_ingredientes.listar_ingredientes()
                if not ingredientes:
                    print("No hay ingredientes registrados.")
                for i in ingredientes:
                    print(f"- [{i.id_ingrediente}] {i.nombre} ({i.categoria_ingrediente})")
            elif opcion == "2":
                texto = self.leer_entrada("Texto a buscar: ")
                resultados = self.servicio_ingredientes.buscar_ingredientes(texto)
                if not resultados:
                    print("No se encontraron ingredientes.")
                for i in resultados:
                    print(f"- [{i.id_ingrediente}] {i.nombre} ({i.categoria_ingrediente})")
            elif opcion == "3":
                nombre = self.leer_entrada("Nombre del ingrediente: ")
                categoria = self.leer_entrada("Categoría (ej: Frutas, Verduras, Proteínas): ")
                try:
                    i = self.servicio_ingredientes.crear_ingrediente(nombre, categoria)
                    print(f"Ingrediente creado: [{i.id_ingrediente}] {i.nombre}")
                except ValueError as exc:
                    print(f"Error: {exc}")
            elif opcion == "4":
                id_ing = self.leer_entero("ID del ingrediente a editar: ")
                if id_ing is not None:
                    actual = self.servicio_ingredientes.obtener_ingrediente(id_ing)
                    if actual is None:
                        print(MSG_NO_ENCONTRADO)
                    else:
                        nombre = self.leer_entrada(f"Nuevo nombre ({actual.nombre}): ")
                        categoria = self.leer_entrada(
                            f"Nueva categoría ({actual.categoria_ingrediente}): "
                        )
                        try:
                            i = self.servicio_ingredientes.editar_ingrediente(
                                id_ing,
                                nombre=nombre or None,
                                categoria_ingrediente=categoria or None,
                            )
                            print(f"Ingrediente actualizado: {i.nombre}")
                        except ValueError as exc:
                            print(f"Error: {exc}")
            elif opcion == "5":
                id_ing = self.leer_entero("ID del ingrediente a eliminar: ")
                if id_ing is not None:
                    try:
                        if self.servicio_ingredientes.eliminar_ingrediente(id_ing):
                            print("Ingrediente eliminado.")
                        else:
                            print(MSG_NO_ENCONTRADO)
                    except ValueError as exc:
                        print(f"Error: {exc}")
            elif opcion == "0":
                return
            else:
                print(MSG_OPCION_INVALIDA)

            self.leer_entrada(MSG_PAUSA)

    # ---------------- USUARIOS ----------------

    def _menu_usuarios(self) -> None:
        while True:
            self._mostrar_opciones("GESTIÓN DE USUARIOS", MENU_USUARIOS)
            opcion = self.leer_entrada("Seleccione una opción: ")

            if opcion == "1":
                usuarios = self.servicio_usuarios.listar_usuarios()
                if not usuarios:
                    print("No hay usuarios registrados.")
                for u in usuarios:
                    print(f"- {u}")
            elif opcion == "2":
                texto = self.leer_entrada("Nombre o correo a buscar: ")
                resultados = self.servicio_usuarios.buscar_usuarios(texto)
                if not resultados:
                    print("No se encontraron usuarios.")
                for u in resultados:
                    print(f"- {u}")
            elif opcion == "3":
                nombre = self.leer_entrada("Nombre: ")
                email = self.leer_entrada("Correo electrónico: ")
                contrasena = pedir_contrasena("Contraseña (mínimo 6 caracteres): ")
                confirmar = pedir_contrasena("Confirmar contraseña: ")
                if contrasena != confirmar:
                    print("Error: Las contraseñas no coinciden.")
                else:
                    try:
                        u = self.servicio_usuarios.crear_usuario(nombre, email, contrasena)
                        print(f"Usuario creado: {u}")
                    except ValueError as exc:
                        print(f"Error: {exc}")
            elif opcion == "4":
                id_usr = self.leer_entero("ID del usuario a modificar: ")
                if id_usr is not None:
                    actual = self.servicio_usuarios.obtener_usuario(id_usr)
                    if actual is None:
                        print(MSG_NO_ENCONTRADO)
                    else:
                        nombre = self.leer_entrada(f"Nuevo nombre ({actual.nombre}): ")
                        email = self.leer_entrada(f"Nuevo correo ({actual.email}): ")
                        cambiar_clave = self.leer_entrada("¿Cambiar contraseña? (s/n): ").lower()
                        nueva_clave = None
                        if cambiar_clave == "s":
                            nueva_clave = pedir_contrasena("Nueva contraseña: ")
                        try:
                            u = self.servicio_usuarios.editar_usuario(
                                id_usr,
                                nombre=nombre or None,
                                email=email or None,
                                contrasena=nueva_clave,
                            )
                            print(f"Usuario actualizado: {u}")
                        except ValueError as exc:
                            print(f"Error: {exc}")
            elif opcion == "5":
                id_usr = self.leer_entero("ID del usuario a deshabilitar: ")
                if id_usr is not None:
                    try:
                        if self.servicio_usuarios.deshabilitar_usuario(
                            id_usr, self.usuario_actual.id_usuario
                        ):
                            print("Usuario deshabilitado.")
                        else:
                            print(MSG_NO_ENCONTRADO)
                    except ValueError as exc:
                        print(f"Error: {exc}")
            elif opcion == "6":
                id_usr = self.leer_entero("ID del usuario a habilitar: ")
                if id_usr is not None:
                    if self.servicio_usuarios.habilitar_usuario(id_usr):
                        print("Usuario habilitado.")
                    else:
                        print(MSG_NO_ENCONTRADO)
            elif opcion == "7":
                id_usr = self.leer_entero("ID del usuario a eliminar: ")
                if id_usr is not None:
                    try:
                        if self.servicio_usuarios.eliminar_usuario(
                            id_usr, self.usuario_actual.id_usuario
                        ):
                            print("Usuario eliminado.")
                        else:
                            print(MSG_NO_ENCONTRADO)
                    except ValueError as exc:
                        print(f"Error: {exc}")
            elif opcion == "0":
                return
            else:
                print(MSG_OPCION_INVALIDA)

            self.leer_entrada(MSG_PAUSA)

    # ---------------- VALORACIONES ----------------

    def _menu_valoraciones(self) -> None:
        while True:
            self._mostrar_opciones("GESTIÓN DE VALORACIONES", MENU_VALORACIONES)
            opcion = self.leer_entrada("Seleccione una opción: ")

            if opcion == "1":
                valoraciones = self.servicio_valoraciones.listar_valoraciones()
                if not valoraciones:
                    print("No hay valoraciones registradas.")
                for v in valoraciones:
                    print(
                        f"- [{v.id_valoracion}] {v.receta.nombre} | {v.puntuacion}/5 | "
                        f"{v.usuario.nombre} ({v.fecha}): {v.comentario or 'Sin comentario'}"
                    )
            elif opcion == "2":
                id_receta = self.leer_entero("ID de la receta: ")
                if id_receta is not None:
                    valoraciones = self.servicio_valoraciones.listar_por_receta(id_receta)
                    if not valoraciones:
                        print("Esta receta aún no tiene valoraciones.")
                    for v in valoraciones:
                        print(
                            f"- [{v.id_valoracion}] {v.puntuacion}/5 por {v.usuario.nombre} "
                            f"({v.fecha}): {v.comentario or 'Sin comentario'}"
                        )
            elif opcion == "3":
                id_receta = self.leer_entero("ID de la receta a valorar: ")
                if id_receta is not None:
                    puntuacion = self.leer_entrada("Puntuación (1 a 5): ")
                    comentario = self.leer_entrada("Comentario (opcional): ")
                    try:
                        v = self.servicio_valoraciones.crear_valoracion(
                            self.usuario_actual.id_usuario,
                            id_receta,
                            puntuacion,
                            comentario,
                        )
                        print(f"Valoración registrada con ID {v.id_valoracion}.")
                    except ValueError as exc:
                        print(f"Error: {exc}")
            elif opcion == "4":
                id_val = self.leer_entero("ID de la valoración a editar: ")
                if id_val is not None:
                    actual = self.servicio_valoraciones.obtener_valoracion(id_val)
                    if actual is None:
                        print(MSG_NO_ENCONTRADO)
                    else:
                        puntuacion = self.leer_entrada(f"Nueva puntuación ({actual.puntuacion}): ")
                        comentario = self.leer_entrada(
                            f"Nuevo comentario ({actual.comentario or ''}): "
                        )
                        try:
                            v = self.servicio_valoraciones.editar_valoracion(
                                id_val,
                                puntuacion=puntuacion or None,
                                comentario=comentario or None,
                            )
                            print(f"Valoración actualizada: {v.puntuacion}/5")
                        except ValueError as exc:
                            print(f"Error: {exc}")
            elif opcion == "5":
                id_val = self.leer_entero("ID de la valoración a eliminar: ")
                if id_val is not None:
                    if self.servicio_valoraciones.eliminar_valoracion(id_val):
                        print("Valoración eliminada.")
                    else:
                        print(MSG_NO_ENCONTRADO)
            elif opcion == "0":
                return
            else:
                print(MSG_OPCION_INVALIDA)

            self.leer_entrada(MSG_PAUSA)

    # ---------------- LOOP PRINCIPAL ----------------

    def ejecutar(self) -> None:
        while True:
            titulo = f"{NOMBRE_APP.upper()} (Sesión: {self.usuario_actual.nombre})"
            self._mostrar_opciones(titulo, MENU_PRINCIPAL)
            try:
                opcion = self.leer_entrada("Seleccione una opción: ")
            except SystemExit:
                break

            try:
                if opcion == "1":
                    self._menu_recetas()
                elif opcion == "2":
                    self._menu_categorias()
                elif opcion == "3":
                    self._menu_ingredientes()
                elif opcion == "4":
                    self._menu_usuarios()
                elif opcion == "5":
                    self._menu_valoraciones()
                elif opcion == "6":
                    iniciar_servidor()
                elif opcion == "7":
                    print(MSG_SALIENDO)
                    break
                else:
                    print(MSG_OPCION_INVALIDA)
            except SystemExit:
                break
