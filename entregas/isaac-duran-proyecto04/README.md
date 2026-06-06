# 🏥 Sistema de Gestión - Consultorio Médico (Proyecto 04)

Este aplicativo de escritorio desarrollado en Python con Tkinter permite gestionar pacientes, médicos, agendar citas, registrar consultas y exportar historiales clínicos a PDF, utilizando una base de datos MySQL normalizada en 3FN.

---

Paso 1: Configurar la Base de Datos
1. Abre tu gestor de bases de datos (ej. MySQL Workbench).
2. Ejecuta primero el script **`ddl/01-crear-bd.sql`** para crear la estructura de las tablas.
3. Ejecuta después el script **`ddl/02-datos-prueba.sql`** para cargar los pacientes, médicos y citas de prueba.


Paso 2: Configurar las Credenciales
Para que el aplicativo se pueda conectar a tu base de datos local:
1. Entra a la carpeta `app/` y abre el archivo **`conexiones.py`**.
2. En la línea 7, cambia la contraseña `"359Id12435"` por la contraseña de tu servidor MySQL local.


Paso 3: Instalar Librerías
Abre una terminal en Visual Studio Code y ejecuta este comando para instalar todas las dependencias necesarias de un solo golpe:
```bash
pip install mysql-connector-python sv_ttk tkcalendar fpdf2

Paso 4: Ejecutar el aplicativo
Entra en la carpeta app y luego dentro del archivo app.py, ejecuta el progama.