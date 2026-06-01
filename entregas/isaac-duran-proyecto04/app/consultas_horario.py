import tkinter as tk
from tkinter import ttk, messagebox
from conexiones import conectar_bd

def guardar_horario(entradas, combo_medico, combo_dia, lista_medicos):
    medico_seleccionado = combo_medico.get()
    dia_texto= combo_dia.get()
    hora_inicio = entradas['hora_inicio'].get()
    hora_fin = entradas['hora_fin'].get()

    if not medico_seleccionado or not dia_texto or not hora_inicio or not hora_fin:
        messagebox.showerror("Advertencia", "Todos los campos son obligatorios")
        return
    
    id_medico = None
    for med in lista_medicos:
        nombre_completo = f"{med[1]} {med[2]}"
        if nombre_completo == medico_seleccionado:
            id_medico = med[0]
            break

    dias_map = {
        "Lunes": 1, "Martes": 2, "Miércoles": 3, "Jueves": 4, "Viernes": 5, "Sábado": 6, "Domingo": 7
    }
    dia_num = dias_map.get(dia_texto)

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """INSERT INTO horarios (id_medico, dia_semana, hora_inicio, hora_fin) 
            VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (id_medico, dia_num, hora_inicio, hora_fin))
            conexion.commit()
            messagebox.showinfo("Éxito", f"Horario guardado para {medico_seleccionado} el día {dia_texto} de {hora_inicio} a {hora_fin}")

            combo_medico.set('')
            combo_dia.set('')
            entradas['hora_inicio'].delete(0, tk.END)
            entradas['hora_fin'].delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el horario: {e}")
        finally:
            conexion.close()

def cargar_medicos():
    conexion = conectar_bd()
    medicos = []
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_medico, nombre, apellido FROM medicos")
            medicos = cursor.fetchall()
        finally:
            conexion.close()
    return medicos