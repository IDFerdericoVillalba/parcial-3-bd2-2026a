import tkinter as tk
from tkinter import messagebox
from conexiones import conectar_bd


def obtener_historial_paciente(combo_paciente, tree, lista_pacientes):
    pac_sel = combo_paciente.get()
    if not pac_sel:
        messagebox.showwarning("Advertencia", "Selecciona un paciente para ver su historial.")
        return
    id_paciente = None
    for p in lista_pacientes:
        if f"{p[1]} {p[2]} - {p[3]}" == pac_sel:
            id_paciente = p[0]
            break
    for item in tree.get_children():
        tree.delete(item)

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                SELECT c.fecha, CONCAT(m.nombre, ' ', m.apellido) as medico, 
                       con.diagnostico, con.observaciones, t.medicamento
                FROM citas c
                JOIN medicos m ON c.id_medico = m.id_medico
                JOIN consultas con ON c.id_cita = con.id_cita
                LEFT JOIN tratamientos t ON con.id_consulta = t.id_consulta
                WHERE c.id_paciente = %s AND c.estado = 'atendida'
                ORDER BY c.fecha DESC
            """
            cursor.execute(sql, (id_paciente,))
            registros = cursor.fetchall()
            if not registros:
                messagebox.showinfo("Información", "Este paciente aún no tiene consultas registradas.")
                
            for fila in registros:
                tree.insert("", tk.END, values=fila)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el historial: {e}")
        finally:
            conexion.close()