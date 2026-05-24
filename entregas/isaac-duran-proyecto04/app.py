import tkinter as tk
from tkinter import ttk, messagebox
from conexiones import conectar_bd

def cargar_pacientes(tree):
    for item in tree.get_children():
        tree.delete(item)
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_paciente, nombre, apellido, documento, telefono FROM pacientes")
            registros = cursor.fetchall()
            for fila in registros:
                tree.insert("", tk.END, values=fila)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pacientes: {e}")
        finally:
            conexion.close()

################################################################

def guardar_paciente(entradas, tree):
    nombre = entradas['nombre'].get()
    apelido = entradas['apellido'].get()
    docuemnto = entradas['documento'].get()
    fecha_nacimiento = entradas['fecha_nacimiento'].get()
    telefono = entradas['telefono'].get()
    correo = entradas['correo'].get()
    direccion = entradas['direccion'].get()


    #validar que todos los campos de paciente no esten vacios
    if not (nombre and apelido and docuemnto and fecha_nacimiento and telefono):
        messagebox.showerror("Advertencia", "Los campos con * son obligatorios")
        return
    
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """INSERT INTO pacientes (nombre, apellido, documento, fecha_nacimiento, telefono, correo, direccion) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            valores = (nombre, apelido, docuemnto, fecha_nacimiento, telefono, correo, direccion)

            cursor.execute(sql, valores)
            conexion.commit()

            messagebox.showinfo("Éxito", f"Paciente {nombre} guardado correctamente")

            for key in entradas:
                entradas[key].delete(0, tk.END)
            cargar_pacientes(tree)

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el paciente: {e}")
        finally:
            conexion.close()

################################################################

def cargar_especialidades():
    conexion = conectar_bd()
    especialidades = []
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_especialidad, nombre FROM especialidades")
            especialidades = cursor.fetchall()
        finally:
            conexion.close()
            return especialidades

def guardar_medico(entradas, combo_esp, lista_especialidades, tree):
    nombre = entradas['nombre'].get()
    apellido = entradas['apellido'].get()
    documento = entradas['documento'].get()
    telefono = entradas['telefono'].get()
    correo = entradas['correo'].get()
    nombre_esp_selecionada = combo_esp.get()

    if not nombre or not apellido or not documento or not telefono or not nombre_esp_selecionada:
        messagebox.showerror("Advertencia", "Los campos con * son obligatorios")
        return
    
    id_especialidad = None
    for esp in lista_especialidades:
        if esp[1] == nombre_esp_selecionada:
            id_especialidad = esp[0]
            break

    conexion = conectar_bd()
    if conexion:
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            sql = """INSERT INTO medicos (nombre, apellido, documento, telefono, correo) 
            VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (nombre, apellido, documento, telefono, correo))

            id_medico_nuevo = cursor.lastrowid

            sql_relacion = """INSERT INTO medicos_especialidades (id_medico, id_especialidad) VALUES (%s, %s)"""
            cursor.execute(sql_relacion, (id_medico_nuevo, id_especialidad))

            conexion.commit()
            messagebox.showinfo("Éxito", f"Dr/Dra {apellido} guardado con su especialidad {nombre_esp_selecionada}")

            for key in entradas:
                entradas[key].delete(0, tk.END)
                combo_esp.set('')

        except Exception as e:
            conexion.rollback()
            messagebox.showerror("Error", f"Error al guardar el médico: {e}")
        finally:
            conexion.auto_commit = True
            conexion.close()

################################################################


def inicar_app():

    #ventana principal
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión - Consulta Médico")
    ventana.geometry("900x700")

    #controlador de pestañas
    notebook = ttk.Notebook(ventana)
    notebook.pack(expand=True, fill='both', padx=10, pady=10)

    #frames para cada pestaña
    frame_pacientes = ttk.Frame(notebook)
    frame_medicos = ttk.Frame(notebook)
    frame_citas = ttk.Frame(notebook)

    #agrager frames al notebook
    notebook.add(frame_pacientes, text="👨‍⚕️ Gestion de Pacientes")
    notebook.add(frame_medicos, text="⚕️ Gestion de Médicos")
    notebook.add(frame_citas, text="📅 Gestion de Citas")

    #pestaña para agregar pacientes
    tk.Label(frame_pacientes, text="Registro de nuevo paciente", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
    entradas = {}
    campos = [
        ("Nombre *", "nombre"),
        ("Apellido *", "apellido"),
        ("Documento *", "documento"),
        ("Fecha de Nacimiento (YYYY-MM-DD) *", "fecha_nacimiento"),
        ("Teléfono *", "telefono"),
        ("Correo", "correo"),
        ("Dirección", "direccion")
    ]
    for i, (texto_label, nombre_variable) in enumerate(campos, start=1):    
        tk.Label(frame_pacientes, text=texto_label).grid(row=i, column=0, sticky="e", padx=10, pady=5)
        caja_texto = tk.Entry(frame_pacientes, width=40)
        caja_texto.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        entradas[nombre_variable] = caja_texto

    columnas = ("id_paciente", "nombre", "apellido", "documento", "telefono")
    tree_pacientes = ttk.Treeview(frame_pacientes, columns=columnas, show="headings", height=8)

    for col in columnas:
        tree_pacientes.heading(col, text=col)
        tree_pacientes.column(col, width=120, anchor="center")

    tree_pacientes.grid(row=len(campos)+2, column=0, columnspan=2, padx=20, pady=20)

    btn_guardar = tk.Button(frame_pacientes, text="💾 Guardar Paciente", command=lambda: guardar_paciente(entradas, tree_pacientes))
    btn_guardar.grid(row=len(campos)+1, column=0, columnspan=2, pady=20)

    cargar_pacientes(tree_pacientes)

    ######################################################################################

    #pestaña para agregar médicos
    tk.Label(frame_medicos, text="Registro de Medicos   ", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
    entradas_medicos = {}
    campos_medicos = [
        ("Nombre *", "nombre"),
        ("Apellido *", "apellido"),
        ("Documento *", "documento"),
        ("Teléfono *", "telefono"),
        ("Correo", "correo")
    ]
    for i, (lbl, var) in enumerate(campos_medicos, start=1):
        tk.Label(frame_medicos, text=lbl).grid(row=i, column=0, sticky="e", padx=10, pady=5)
        caja = tk.Entry(frame_medicos, width=40)
        caja.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        entradas_medicos[var] = caja

        tk.Label(frame_medicos, text="Especialidad *").grid(row=len(campos_medicos)+1, column=0, sticky="e", padx=10, pady=5)

        lista_esp_bd = cargar_especialidades()
        nombres_especialidades = [esp[1] for esp in lista_esp_bd]

        combo_especialidad = ttk.Combobox(frame_medicos, values=nombres_especialidades, state="readonly", width=37)
        combo_especialidad.grid(row=len(campos_medicos)+1, column=1, padx=10, pady=5, sticky="w")

        btn_guardar_medico = tk.Button(frame_medicos, text="👨‍⚕️ Guardar Médico", command=lambda: guardar_medico(entradas_medicos, combo_especialidad, lista_esp_bd, None))
        btn_guardar_medico.grid(row=len(campos_medicos)+2, column=0, columnspan=2, pady=20) 

    ventana.mainloop()

if __name__ == "__main__":
    inicar_app()
    