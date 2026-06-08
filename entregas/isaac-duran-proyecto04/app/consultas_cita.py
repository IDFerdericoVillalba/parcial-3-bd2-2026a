import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
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
    """Valida conflictos (RF5), horarios del médico y guarda la cita (RF4)"""
    pac_sel = combo_pac.get()
    med_sel = combo_med.get()
    fecha = ent_fecha.get()
    hora = ent_hora.get()
    motivo = ent_motivo.get()

    if not pac_sel or not med_sel or not fecha or not hora or not motivo:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        return
    try:
        datetime.strptime(hora, "%H:%M")
    except ValueError:
        messagebox.showerror("Error de Formato", "Por favor, ingresa la hora exactamente en formato HH:MM (por ejemplo: 08:30 o 14:00).")
        return

    # 1. Obtener IDs utilizando diccionarios de mapeo (Búsqueda O(1))
    mapa_pacientes = {f"{p[1]} {p[2]} - {p[3]}": p[0] for p in lista_pac}
    id_pac = mapa_pacientes.get(pac_sel)
    mapa_medicos = {f"{m[1]} {m[2]}": m[0] for m in lista_med}
    id_med = mapa_medicos.get(med_sel)

    # Validación extra de seguridad
    if not id_pac or not id_med:
        messagebox.showerror("Error Interno", "No se pudo recuperar el ID del paciente o médico seleccionado.")
        return

    # En Python, Monday=0, Sunday=6. En nuestra BD: Lunes=1, Domingo=7.
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        dia_semana_solicitado = fecha_obj.weekday() + 1 
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha incorrecto. Use AAAA-MM-DD")
        return

    # 2. Conectar a BD para validar y guardar
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql_val_horario = """
                SELECT COUNT(*) FROM horarios 
                WHERE id_medico = %s 
                  AND dia_semana = %s 
                  AND hora_inicio <= %s 
                  AND hora_fin >= %s
            """
            cursor.execute(sql_val_horario, (id_med, dia_semana_solicitado, hora, hora))
            if cursor.fetchone()[0] == 0:
                messagebox.showerror("Fuera de Horario", "❌ El médico seleccionado NO atiende en ese día de la semana o la hora indicada está fuera de su turno.")
                return

            # --- RF5: VALIDACIÓN DE CONFLICTOS DE CRUCE ---
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
            sql_insert = """INSERT INTO citas (id_paciente, id_medico, fecha, hora, motivo, estado) 
                            VALUES (%s, %s, %s, %s, %s, 'programada')"""
            cursor.execute(sql_insert, (id_pac, id_med, fecha, hora, motivo))
            conexion.commit()

            messagebox.showinfo("Éxito", "📅 Cita agendada correctamente.")
            
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

    # Extraer el ID de la cita usando mapeo seguro
    mapa_citas = {f"ID: {c[0]} | {c[1]} - {c[2]} | Paciente: {c[3]} {c[4]}": c[0] for c in lista_citas}
    id_cita = mapa_citas.get(cita_sel)

    if not id_cita:
        messagebox.showerror("Error", "No se pudo identificar la cita seleccionada.")
        return
    
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


def obtener_especialidades_medico(id_medico):
    conexion = conectar_bd()
    especialidades = []
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                SELECT e.nombre 
                FROM especialidades e
                JOIN medico_especialidad me ON e.id_especialidad = me.id_especialidad
                WHERE me.id_medico = %s
            """
            cursor.execute(sql, (id_medico,))
            resultados = cursor.fetchall()
            especialidades = [fila[0] for fila in resultados] 
        finally:
            conexion.close()
    return especialidades


def obtener_horarios_medico_texto(id_medico):
    """Devuelve un texto formateado con los días y horas de atención de un médico."""
    conexion = conectar_bd()
    horarios_texto = []
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                SELECT 
                    GROUP_CONCAT(
                        CASE dia_semana 
                            WHEN 1 THEN 'Lun' WHEN 2 THEN 'Mar' WHEN 3 THEN 'Mié' 
                            WHEN 4 THEN 'Jue' WHEN 5 THEN 'Vie' WHEN 6 THEN 'Sáb' WHEN 7 THEN 'Dom' 
                        END 
                        ORDER BY dia_semana SEPARATOR ', '
                    ) as dias,
                    hora_inicio, 
                    hora_fin
                FROM horarios
                WHERE id_medico = %s
                GROUP BY hora_inicio, hora_fin
            """
            cursor.execute(sql, (id_medico,))
            resultados = cursor.fetchall()
            
            for fila in resultados:
                horarios_texto.append(f"{fila[0]} ({fila[1]} a {fila[2]})")
        finally:
            conexion.close()
            
    return " | ".join(horarios_texto) if horarios_texto else "Sin horario asignado"


def modificar_cita(combo_modificar, ent_fecha, ent_hora, lista_citas):
    """Actualiza la fecha y hora de una cita programada, validando conflictos."""
    cita_sel = combo_modificar.get()
    nueva_fecha = ent_fecha.get()
    nueva_hora = ent_hora.get()

    if not cita_sel or not nueva_fecha or not nueva_hora:
        messagebox.showwarning("Advertencia", "Selecciona una cita y define la nueva fecha y hora.")
        return
    try:
        datetime.strptime(nueva_hora, "%H:%M")
    except ValueError:
        messagebox.showerror("Error de Formato", "Por favor, ingresa la nueva hora exactamente en formato HH:MM (por ejemplo: 08:30 o 14:00).")
        return

    # Extraer el ID de la cita usando mapeo seguro
    mapa_citas = {f"ID: {c[0]} | {c[1]} - {c[2]} | Paciente: {c[3]} {c[4]}": c[0] for c in lista_citas}
    id_cita = mapa_citas.get(cita_sel)
    
    if not id_cita:
        messagebox.showerror("Error", "No se pudo identificar la cita seleccionada.")
        return

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # 2. Buscar qué médico y paciente están en esta cita para hacer las validaciones
            cursor.execute("SELECT id_medico, id_paciente FROM citas WHERE id_cita = %s", (id_cita,))
            resultado = cursor.fetchone()
            id_med = resultado[0]
            id_pac = resultado[1]

            # 3. Validar qué día de la semana es la nueva fecha
            try:
                fecha_obj = datetime.strptime(nueva_fecha, "%Y-%m-%d")
                dia_semana_solicitado = fecha_obj.weekday() + 1 
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha incorrecto.")
                return

            # 4. Validar si el médico trabaja en ese nuevo horario
            sql_val_horario = """
                SELECT COUNT(*) FROM horarios 
                WHERE id_medico = %s AND dia_semana = %s AND hora_inicio <= %s AND hora_fin >= %s
            """
            cursor.execute(sql_val_horario, (id_med, dia_semana_solicitado, nueva_hora, nueva_hora))
            if cursor.fetchone()[0] == 0:
                messagebox.showerror("Fuera de Horario", "❌ El médico NO atiende en ese día o la nueva hora está fuera de su turno.")
                return

            # 5. Validar que el médico no tenga OTRA cita distinta a la misma hora
            sql_val_med = "SELECT COUNT(*) FROM citas WHERE id_medico = %s AND fecha = %s AND hora = %s AND estado != 'cancelada' AND id_cita != %s"
            cursor.execute(sql_val_med, (id_med, nueva_fecha, nueva_hora, id_cita))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Conflicto", "❌ El MÉDICO ya tiene OTRA cita asignada en esa nueva fecha y hora.")
                return

            # 6. Validar que el paciente no tenga OTRA cita en esa misma fecha y hora
            sql_val_pac = "SELECT COUNT(*) FROM citas WHERE id_paciente = %s AND fecha = %s AND hora = %s AND estado != 'cancelada' AND id_cita != %s"
            cursor.execute(sql_val_pac, (id_pac, nueva_fecha, nueva_hora, id_cita))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Conflicto", "❌ El PACIENTE ya tiene OTRA cita asignada en esa nueva fecha y hora.")
                return

            # 7. Hacer el UPDATE
            cursor.execute("UPDATE citas SET fecha = %s, hora = %s WHERE id_cita = %s", (nueva_fecha, nueva_hora, id_cita))
            conexion.commit()
            
            messagebox.showinfo("Éxito", "🔄 Cita reprogramada correctamente.")
            combo_modificar.set('')
            ent_fecha.config(state="normal")
            ent_fecha.delete(0, tk.END)
            ent_fecha.config(state="readonly")
            ent_hora.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar la cita: {e}")
        finally:
            conexion.close()


def ejecutar_no_asistio_cita(combo_cita, lista_citas):
    """Marca una cita programada como 'no_asistio' en la base de datos."""
    cita_sel = combo_cita.get()
    if not cita_sel:
        messagebox.showwarning("Advertencia", "Selecciona una cita de la lista.")
        return

    # Extraer el ID de la cita usando mapeo seguro
    mapa_citas = {f"ID: {c[0]} | {c[1]} - {c[2]} | Paciente: {c[3]} {c[4]}": c[0] for c in lista_citas}
    id_cita = mapa_citas.get(cita_sel)
    
    if not id_cita:
        messagebox.showerror("Error", "No se pudo identificar la cita seleccionada.")
        return

    seguro = messagebox.askyesno("Confirmar Inasistencia", "¿Está seguro de marcar que el paciente NO ASISTIÓ a esta cita?")
    if not seguro:
        return

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "UPDATE citas SET estado = 'no_asistio' WHERE id_cita = %s"
            cursor.execute(sql, (id_cita,))
            conexion.commit()
            messagebox.showinfo("Éxito", "La cita ha sido marcada como 'No Asistió'.")
            combo_cita.set('')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la cita: {e}")
        finally:
            conexion.close()

