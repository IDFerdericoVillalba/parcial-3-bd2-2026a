import tkinter as tk
from tkinter import ttk, messagebox
from conexiones import conectar_bd

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


def cargar_tabla_medicos(tree):
    for item in tree.get_children():
        tree.delete(item)
        
    conexion = conectar_bd()
    medicos = []
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_medico, nombre, apellido FROM medicos")
            medicos = cursor.fetchall()
            
            for fila in medicos:
                tree.insert("", tk.END, values=fila)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar médicos en la tabla: {e}")
        finally:
            conexion.close()
    return medicos


def guardar_medico(entradas, listbox_esp, lista_especialidades, tree):
    nombre = entradas['nombre'].get()
    apellido = entradas['apellido'].get()
    documento = entradas['documento'].get()
    telefono = entradas['telefono'].get()
    correo = entradas['correo'].get()

    indices_seleccionados = listbox_esp.curselection()

    if not nombre or not apellido or not documento or not telefono or not indices_seleccionados:
        messagebox.showerror("Advertencia", "Los campos con * son obligatorios")
        return
    
    ids_especialidades_elegidas = []
    for indice in indices_seleccionados:
        nombre_esp_selecionada = listbox_esp.get(indice)
        for esp in lista_especialidades:
            if esp[1] == nombre_esp_selecionada:
                ids_especialidades_elegidas.append(esp[0])
                break

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()

            sql = """INSERT INTO medicos (nombre, apellido, documento, telefono, correo) 
            VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (nombre, apellido, documento, telefono, correo))

            id_medico_nuevo = cursor.lastrowid

            sql_relacion = """INSERT INTO medico_especialidad (id_medico, id_especialidad) VALUES (%s, %s)"""
            for id_esp in ids_especialidades_elegidas:
                cursor.execute(sql_relacion, (id_medico_nuevo, id_esp))

            conexion.commit()
            messagebox.showinfo("Éxito", f"Dr/Dra {apellido} guardado con su especialidad con {len(ids_especialidades_elegidas)} especialidad(es).") 

            for key in entradas:
                entradas[key].delete(0, tk.END)

            listbox_esp.selection_clear(0, tk.END)
            cargar_tabla_medicos(tree)

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el médico: {e}")
        finally:
            conexion.close()

