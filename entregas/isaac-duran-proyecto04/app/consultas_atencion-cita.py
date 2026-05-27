import tkinter as tk
from tkinter import ttk, messagebox
from conexiones import conectar_bd

def obtener_citas_pendieentes():
    conexion = conectar_bd()
    citas = []
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """SELECT c.id_cita, c.fecha, c.hora, p.nombre, p.apellido, c.motivo
            FROM citas c
            JOIN  paciente p ON c.id_paciente = p.id_paciente
            WHERE c.estado = 'programada'"""
            cursor.execute(sql)
            citas = cursor.fetchall()
        finally:
            conexion.close()
    return citas


def registrar_consulta_medica(combo_cita, ent_diag, ent_obs, ent_med, lista_citas):
    cita_sel = combo_cita.get()
    diagnostico = ent_diag.get()
    observaciones = ent_obs.get()
    medicamento = ent_med.get()

    if not cita_sel or not diagnostico or not medicamento:
        messagebox.showwarning("Advertencia", "Selecciona la cita y completa diagnóstico y medicamento.")
        return
    
    id_cita = None
    for c in lista_citas:
        texto_combo = f"ID: {c[0]} - {c[1]} {c[2]} - PACIENTE: {c[3]} {c[4]}"
        if texto_combo == cita_sel:
            id_cita = c[0]
            break   

    conexion = conectar_bd()
    if conexion:
        try:
            conexion.autocommit = False
            cursor = conexion.cursor()

            # 1. Insertar consulta 
            sql_consulta = """INSERT INTO consultas (id_cita, diagnostico, observaciones,)
            VALUES (%s, %s, %s)"""
            cursor.execute(sql_consulta, (id_cita, diagnostico, observaciones))
            id_consulta_nueva = cursor.lastrowid

            # 2. Insertar el tratamiento
            sql_tratamiento = """INSERT INTO tratamientos (id_consulta, medicamento) VALUES (%s, %s)"""
            cursor.execute(sql_tratamiento, (id_consulta_nueva, medicamento))

            # 3. Actualizar estado de la cita a 'atendida'
            sql_update_cita = "UPDATE citas SET estado = 'atendida' WHERE id_cita = %s"
            cursor.execute(sql_update_cita, (id_cita,))

            conexion.commit()
            messagebox.showinfo("Éxito", "Consulta médica registrada y cita actualizada a 'atendida'.")

            #limpiar campos
            combo_cita.set('')
            ent_diag.delete(0, tk.END)
            ent_obs.delete(0, tk.END)
            ent_med.delete(0, tk.END)
        
        except Exception as e:
            conexion.rollback()
            messagebox.showerror("Error", f"Error en la transaccion: {e}")
        finally:
            conexion.autocommit = True
            conexion.close()

            

