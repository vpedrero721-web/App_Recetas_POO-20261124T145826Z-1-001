# App_Recetas_POO

## Integrantes

- Valentina Pedrero 
- Kevin Reyes 

## Descripción general

Aplicación modular de gestión de recetas desarrollada en Python bajo arquitectura por capas y persistencia en MySQL/MariaDB con el ORM Peewee. Continúa el proyecto de la Evaluación N°2 incorporando gestión de usuarios, contraseñas protegidas con BCrypt, ingreso oculto con Maskpass, inicio de sesión obligatorio antes del menú principal y operaciones CRUD completas para recetas, categorías, ingredientes, usuarios y valoraciones.

## Estructura del proyecto

```text
App_Recetas_POO/
├── datos/
│   ├── conexion.py
│   ├── model_base.py
│   ├── modelos/
│   ├── repositorio/
│   ├── sql/
│   │   └── recetas.sql
│   ├── Recetas.py
│   └── orm_models.py
├── negocio/
├── presentacion/
│   ├── login.py
│   ├── menu.py
│   ├── web.py
│   └── web/
├── auxiliares/
├── Diagrama_UML.md
├── diagrama_uml_clases.png
├── requirements.txt
├── .env.example
├── README.md
└── main.py
```

## Dependencias

- Python 3.10 o superior
- MySQL 8.0+ o MariaDB 10.5+ (por ejemplo, XAMPP)
- `peewee`
- `PyMySQL`
- `python-dotenv`
- `bcrypt`
- `maskpass`

## Procedimiento de instalación

1. Clonar o descargar el repositorio y ubicarse en la carpeta del proyecto:

```powershell
cd App_Recetas_POO
```

2. Crear y activar un entorno virtual (opcional, recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instalar las dependencias:

```powershell
python -m pip install -r requirements.txt
```

4. Crear el archivo `.env` a partir de `.env.example` y ajustar los datos de conexión de tu servidor MySQL/MariaDB:

```powershell
Copy-Item .env.example .env
notepad .env
```

Variables disponibles en `.env`:

```env
RECETAS_DB_HOST=127.0.0.1
RECETAS_DB_PORT=3306
RECETAS_DB_USER=root
RECETAS_DB_PASSWORD=
RECETAS_DB_NAME=recetas
```

## Procedimiento de creación de base de datos

1. Iniciar el servicio de MySQL/MariaDB (por ejemplo desde el panel de XAMPP).
2. Abrir phpMyAdmin o la consola de MySQL e importar el archivo `datos/sql/recetas.sql`.
3. El script crea la base de datos `recetas`, todas las tablas (`Usuarios`, `Categorias`, `Recetas`, `Ingredientes`, `DetalleIngrediente`, `RecetasCategorias`, `Valoraciones`, `RecetasGuardadas`), la vista `vw_recetas_resumen` y los datos iniciales con contraseñas ya encriptadas con BCrypt.

Si prefieres importarlo desde consola:

```powershell
mysql -u root -p < datos/sql/recetas.sql
```

## Usuario inicial

El script SQL crea un usuario administrador inicial (y también se genera automáticamente al iniciar la aplicación si no existe):

- **Correo:** `admin@recetas.cl`
- **Contraseña:** `admin123`

Los usuarios de prueba cargados desde `recetas.sql` (`antonia@gmail.com`, `joaquin@gmail.com`, `fernanda@gmail.com`, `tomas@gmail.com`, `isidora@gmail.com` y `benjamin@gmail.com`) tienen como contraseña inicial `recetas123`.

## Instrucciones de ejecución

Para iniciar la aplicación en consola (solicita inicio de sesión antes de abrir el menú principal):

```powershell
python main.py
```

Desde el menú principal también es posible iniciar el servidor web (opción 6), accesible en `http://127.0.0.1:8000`.
