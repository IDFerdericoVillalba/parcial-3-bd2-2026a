import tkinter as tk
from tkinter import messagebox
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