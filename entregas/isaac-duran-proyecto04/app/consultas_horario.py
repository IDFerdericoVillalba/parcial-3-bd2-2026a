import tkinter as tk
from tkinter import messagebox
from conexiones import conectar_bd
 

def guardar_horario(entradas, listbox_dia, combo_medico, lista_medicos, tree_horarios):
    medico_seleccionado = combo_medico.get()
    hora_inicio = entradas['hora_inicio'].get()
    hora_fin = entradas['hora_fin'].get()
    indices_dias = listbox_dia.curselection()

    if not medico_seleccionado or not indices_dias or not hora_inicio or not hora_fin:
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

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """INSERT INTO horarios (id_medico, dia_semana, hora_inicio, hora_fin) 
                     VALUES (%s, %s, %s, %s)"""
            
            dias_guardados = []
            for indice in indices_dias:
                dia_texto = listbox_dia.get(indice)
                dia_num = dias_map.get(dia_texto)
                cursor.execute(sql, (id_medico, dia_num, hora_inicio, hora_fin))
                dias_guardados.append(dia_texto)
            
            conexion.commit()
            
            dias_str = ", ".join(dias_guardados)
            messagebox.showinfo("Éxito", f"Horario guardado para {medico_seleccionado} los días: {dias_str} de {hora_inicio} a {hora_fin}")

            combo_medico.set('')
            listbox_dia.selection_clear(0, tk.END)
            entradas['hora_inicio'].delete(0, tk.END)
            entradas['hora_fin'].delete(0, tk.END)

            cargar_tabla_horarios(tree_horarios)

        except Exception as e:
            conexion.rollback()
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


def cargar_tabla_horarios(tree):
    for item in tree.get_children():
        tree.delete(item)
        
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                SELECT 
                    CONCAT(m.nombre, ' ', m.apellido) as medico,
                    GROUP_CONCAT(
                        CASE h.dia_semana 
                            WHEN 1 THEN 'Lun' WHEN 2 THEN 'Mar' WHEN 3 THEN 'Mié' 
                            WHEN 4 THEN 'Jue' WHEN 5 THEN 'Vie' WHEN 6 THEN 'Sáb' WHEN 7 THEN 'Dom' 
                        END 
                        ORDER BY h.dia_semana SEPARATOR ', '
                    ) as dias,
                    h.hora_inicio, 
                    h.hora_fin
                FROM horarios h
                JOIN medicos m ON h.id_medico = m.id_medico
                GROUP BY m.id_medico, h.hora_inicio, h.hora_fin
            """
            cursor.execute(sql)
            registros = cursor.fetchall()
            
            for fila in registros:
                tree.insert("", tk.END, values=fila)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar horarios: {e}")
        finally:
            conexion.close()