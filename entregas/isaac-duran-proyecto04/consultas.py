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


############################################################################################################################
############################################################################################################################


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