import tkinter as tk
from tkinter import ttk, messagebox
from conexiones import conectar_bd

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

            sql_relacion = """INSERT INTO medico_especialidad (id_medico, id_especialidad) VALUES (%s, %s)"""
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


################################################################################################################
################################################################################################################


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

########################################################################################################################
########################################################################################################################


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