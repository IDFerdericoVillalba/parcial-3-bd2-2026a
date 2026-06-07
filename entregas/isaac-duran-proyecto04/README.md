# 🏥 Sistema de Gestión - Consultorio Médico

Este es un aplicativo de escritorio desarrollado en Python (Tkinter) y MySQL para la gestión de citas médicas, pacientes, médicos y sus historiales clínicos.

## ⚙️ Instrucciones de Despliegue

### Paso 1: Configurar la Base de Datos
1. Abre tu gestor de bases de datos (ej. MySQL Workbench o DBeaver).
2. Ejecuta primero el script **`ddl/01-crear-bd.sql`** para crear la estructura de las tablas y relaciones.
3. Ejecuta después el script **`ddl/02-datos-prueba.sql`** para poblar el sistema con los datos requeridos (pacientes, médicos, horarios y citas).

### Paso 2: Configurar las Credenciales de Conexión
Para que el aplicativo pueda comunicarse con tu base de datos local:
1. Navega a la carpeta `app/`.
2. Abre el archivo **`conexiones.py`** (o `config.py` si separaste las credenciales).
3. Modifica los valores de `host`, `user`, `passwd` y `database` para que coincidan con las credenciales de tu servidor MySQL local.

### Paso 3: Crear Entorno Virtual e Instalar Librerías
Para evitar conflictos de dependencias (especialmente en entornos Linux), se recomienda usar un entorno virtual. Abre una terminal en la carpeta raíz del proyecto y ejecuta:

**En Windows:**
```bash
python -m venv env
env\Scripts\activate
pip install mysql-connector-python sv_ttk tkcalendar fpdf2

**En linux/MAC**
python3 -m venv env
source env/bin/activate
pip install mysql-connector-python sv_ttk tkcalendar fpdf2