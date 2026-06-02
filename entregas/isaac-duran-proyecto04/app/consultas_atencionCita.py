import tkinter as tk
from tkinter import ttk, messagebox
from conexiones import conectar_bd

def obtener_citas_pendientes():
    """Trae las citas en estado 'programada' para atenderlas."""
    conexion = conectar_bd()
    citas = []
    if conexion:
        try:
            cursor = conexion.cursor()
            # CAMBIO: Usamos 'citas' y 'pacientes' en plural
            sql = """
                SELECT c.id_cita, c.fecha, c.hora, p.nombre, p.apellido, c.motivo 
                FROM citas c
                JOIN pacientes p ON c.id_paciente = p.id_paciente
                WHERE c.estado = 'programada'
            """
            cursor.execute(sql)
            citas = cursor.fetchall()
        finally:
            conexion.close()
    return citas

def registrar_consulta_medica(combo_cita, ent_diag, ent_obs, ent_med, lista_citas):
    """Guarda la consulta, el tratamiento y actualiza la cita (RF6)"""
    cita_sel = combo_cita.get()
    diagnostico = ent_diag.get()
    observaciones = ent_obs.get()
    medicamento = ent_med.get()

    if not cita_sel or not diagnostico or not medicamento:
        messagebox.showwarning("Advertencia", "Selecciona la cita y llena diagnóstico y medicamento.")
        return

    id_cita = None
    for c in lista_citas:
        texto_combo = f"ID: {c[0]} | {c[1]} - {c[2]} | Paciente: {c[3]} {c[4]}"
        if texto_combo == cita_sel:
            id_cita = c[0]
            break

    conexion = conectar_bd()
    if conexion:
        try:
            conexion.autocommit = False
            cursor = conexion.cursor()

            # CAMBIO 1: Insertar en 'consultas' (Plural)
            sql_consulta = "INSERT INTO consultas (id_cita, diagnostico, observaciones) VALUES (%s, %s, %s)"
            cursor.execute(sql_consulta, (id_cita, diagnostico, observaciones))
            id_consulta_nueva = cursor.lastrowid

            # CAMBIO 2: Insertar en 'tratamientos' (Plural)
            sql_tratamiento = "INSERT INTO tratamientos (id_consulta, medicamento) VALUES (%s, %s)"
            cursor.execute(sql_tratamiento, (id_consulta_nueva, medicamento))

            # CAMBIO 3: Actualizar 'citas' (Plural)
            sql_update_cita = "UPDATE citas SET estado = 'atendida' WHERE id_cita = %s"
            cursor.execute(sql_update_cita, (id_cita,))

            conexion.commit()
            messagebox.showinfo("Éxito", "Consulta registrada y cita actualizada a 'atendida'.")
            
            combo_cita.set('')
            ent_diag.delete(0, tk.END)
            ent_obs.delete(0, tk.END)
            ent_med.delete(0, tk.END)

        except Exception as e:
            conexion.rollback()
            messagebox.showerror("Error", f"Error en la transacción: {e}")
        finally:
            conexion.autocommit = True
            conexion.close()
            

