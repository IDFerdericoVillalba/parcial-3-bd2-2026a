import tkinter as tk
from tkinter import messagebox, filedialog
from fpdf import FPDF
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


#generar pdf de la consulta seleccionada en el historial
def exportar_pdf(tree_historial, combo_paciente):
    """Toma la fila seleccionada en el historial y genera un PDF clínico profesional."""
    # 1. Verificar si el usuario seleccionó una fila en la tabla
    seleccion = tree_historial.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Por favor, selecciona una consulta de la tabla para exportarla a PDF.")
        return

    # 2. Extraer los datos de la fila seleccionada
    valores = tree_historial.item(seleccion[0], 'values')
    fecha, medico, diagnostico, observaciones, tratamiento = valores
    paciente_completo = combo_paciente.get()

    # 3. Abrir cuadro de diálogo para elegir dónde guardar el PDF
    nombre_sugerido = f"Consulta_{fecha}_{paciente_completo.split(' - ')[0].replace(' ', '_')}"
    ruta_archivo = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")],
        title="Guardar Reporte Clínico",
        initialfile=nombre_sugerido
    )

    if not ruta_archivo:
        return  # Si el usuario cancela la ventana de guardado

    try:
        # 4. Construcción estética del PDF
        pdf = FPDF()
        pdf.add_page()
        
        # --- ENCABEZADO ESTILO MÉDICO (Azul corporativo) ---
        pdf.set_fill_color(43, 87, 154)  # Color azul moderno #2B579A
        pdf.rect(0, 0, 210, 38, 'F')
        
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(255, 255, 255) # Texto blanco
        pdf.cell(0, 10, "SISTEMA DE GESTIÓN DE CONSULTAS MÉDICAS", ln=True, align="C")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 5, "Reporte Oficial de Consulta Clínica - Historial del Paciente", ln=True, align="C")
        
        pdf.ln(25) # Espacio después del bloque azul
        pdf.set_text_color(0, 0, 0) # Retornar texto a negro
        
        # --- SECCIÓN 1: DATOS GENERALES ---
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(43, 87, 154)
        pdf.cell(0, 8, "1. DATOS GENERALES DE ATENCIÓN", ln=True)
        pdf.set_draw_color(43, 87, 154)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Línea divisoria elegante
        pdf.ln(4)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(40, 6, "Paciente:", 0)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, str(paciente_completo), ln=True)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(40, 6, "Médico Tratante:", 0)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, str(medico), ln=True)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(40, 6, "Fecha de la Cita:", 0)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, str(fecha), ln=True)
        
        pdf.ln(8)
        
        # --- SECCIÓN 2: EVALUACIÓN CLÍNICA ---
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(43, 87, 154)
        pdf.cell(0, 8, "2. VALORACIÓN Y DIAGNÓSTICO", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, "Diagnóstico Médico Emitido:", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, str(diagnostico))
        pdf.ln(3)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, "Observaciones de la consulta:", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, str(observaciones))
        
        pdf.ln(8)
        
        # --- SECCIÓN 3: TRATAMIENTO Y FORMULACIÓN ---
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(43, 87, 154)
        pdf.cell(0, 8, "3. FORMULACIÓN MÉDICA (TRATAMIENTO)", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        
        # Recuadro destacado para la receta médica
        pdf.set_fill_color(245, 247, 250) # Fondo gris muy claro
        pdf.set_draw_color(200, 200, 200) # Borde gris suave
        
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(180, 40, 40) # Rojo corporativo clínico para el medicamento
        
        # Guardamos la posición para dibujar el rectángulo detrás del texto
        pos_y_inicial = pdf.get_y()
        pdf.multi_cell(0, 6, f" Medicamento / Indicaciones:\n {str(tratamiento)}", border=1, fill=True)
        
        # --- PIE DE PÁGINA (FIRMA) ---
        pdf.ln(35)
        pdf.set_text_color(0, 0, 0)
        pdf.set_draw_color(100, 100, 100)
        pdf.line(60, pdf.get_y(), 150, pdf.get_y()) # Línea para firmar
        pdf.set_font("Helvetica", "I", 9)
        pdf.cell(0, 6, f"Firma Digitalizada del Médico: {medico}", ln=True, align="C")
        
        # 5. Generar archivo final
        pdf.output(ruta_archivo)
        messagebox.showinfo("Éxito", "¡El resumen de la consulta se exportó a PDF correctamente!")
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el archivo PDF: {e}")