import tkinter as tk
from tkinter import ttk, messagebox
from conexiones import conectar_bd


def obtener_pacientes_combo():
    """Trae la lista de pacientes para el desplegable de citas."""
    conexion = conectar_bd()
    pacientes = []
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_paciente, nombre, apellido, documento FROM pacientes")
            pacientes = cursor.fetchall()
        finally:
            conexion.close()
    return pacientes

def agendar_cita(combo_pac, combo_med, ent_fecha, ent_hora, ent_motivo, lista_pac, lista_med):
    """Valida conflictos (RF5) y guarda la cita (RF4)"""
    pac_sel = combo_pac.get()
    med_sel = combo_med.get()
    fecha = ent_fecha.get()
    hora = ent_hora.get()
    motivo = ent_motivo.get()

    if not pac_sel or not med_sel or not fecha or not hora or not motivo:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        return

    # 1. Obtener IDs buscando en las listas
    id_pac = None
    for p in lista_pac:
        if f"{p[1]} {p[2]} - {p[3]}" == pac_sel:
            id_pac = p[0]
            break

    id_med = None
    for m in lista_med:
        if f"{m[1]} {m[2]}" == med_sel:
            id_med = m[0]
            break

    # 2. Conectar a BD para validar y guardar
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()

            # --- RF5: VALIDACIÓN DE CONFLICTOS ---
            # A) ¿El médico ya está ocupado a esa hora y fecha?
            sql_val_med = "SELECT COUNT(*) FROM citas WHERE id_medico = %s AND fecha = %s AND hora = %s AND estado != 'cancelada'"
            cursor.execute(sql_val_med, (id_med, fecha, hora))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Conflicto de Horario", "❌ El MÉDICO ya tiene una cita asignada en esa fecha y hora.")
                return

            # B) ¿El paciente ya tiene una cita a esa hora y fecha?
            sql_val_pac = "SELECT COUNT(*) FROM citas WHERE id_paciente = %s AND fecha = %s AND hora = %s AND estado != 'cancelada'"
            cursor.execute(sql_val_pac, (id_pac, fecha, hora))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Conflicto de Horario", "❌ El PACIENTE ya tiene una cita asignada en esa fecha y hora.")
                return

            # --- RF4: INSERTAR LA CITA ---
            # Si pasamos las validaciones, hacemos el INSERT. Por defecto el estado será 'programada'.
            sql_insert = """INSERT INTO citas (id_paciente, id_medico, fecha, hora, motivo, estado) 
                            VALUES (%s, %s, %s, %s, %s, 'programada')"""
            cursor.execute(sql_insert, (id_pac, id_med, fecha, hora, motivo))
            conexion.commit()

            messagebox.showinfo("Éxito", "📅 Cita agendada correctamente.")
            
            # Limpiar campos
            combo_pac.set('')
            combo_med.set('')
            ent_fecha.delete(0, tk.END)
            ent_hora.delete(0, tk.END)
            ent_motivo.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error de BD", f"Error al agendar: {e}")
        finally:
            conexion.close()
            

def obtener_citas_programadas():
    conexion = conectar_bd()
    citas = []
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                SELECT c.id_cita, c.fecha, c.hora, p.nombre, p.apellido 
                FROM citas c
                JOIN pacientes p ON c.id_paciente = p.id_paciente
                WHERE c.estado = 'programada'
            """
            cursor.execute(sql)
            citas = cursor.fetchall()
        finally:
            conexion.close()
    return citas

def ejecutar_cancelacion_cita(combo_cancelar, lista_citas):
    cita_sel = combo_cancelar.get()
    if not cita_sel:
        messagebox.showwarning("Advertencia", "Selecciona una cita para cancelar.")
        return

    # Extraer el ID de la cita
    id_cita = None
    for c in lista_citas:
        texto_match = f"ID: {c[0]} | {c[1]} - {c[2]} | Paciente: {c[3]} {c[4]}"
        if texto_match == cita_sel:
            id_cita = c[0]
            break

    seguro = messagebox.askyesno("Confirmar", "¿Está seguro de que desea cancelar esta cita?")
    if not seguro:
        return

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "UPDATE citas SET estado = 'cancelada' WHERE id_cita = %s"
            cursor.execute(sql, (id_cita,))
            conexion.commit()
            messagebox.showinfo("Éxito", "La cita ha sido cancelada correctamente.")
            combo_cancelar.set('')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cancelar la cita: {e}")
        finally:
            conexion.close()