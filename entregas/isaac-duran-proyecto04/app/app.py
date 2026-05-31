import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
from tkcalendar import DateEntry
##################################################################
from consultas_paciente import cargar_pacientes, guardar_paciente
from consultas_medico import cargar_especialidades, cargar_medicos, guardar_medico
from consultas_horario import guardar_horario
from consultas_cita import obtener_pacientes_combo, agendar_cita, obtener_citas_programadas, ejecutar_cancelacion_cita
from consultas_atencionCita import obtener_citas_pendientes, registrar_consulta_medica
from historial import obtener_historial_paciente, exportar_pdf


################################################################
################################################################


def inicar_app():

    #ventana principal
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión - Consulta Médico")
    ventana.geometry("900x700")

    #tema nuevo para el aplicativo
    sv_ttk.set_theme("light")
    estilo = ttk.Style()
    estilo.configure(".", font=("segoe UI", 10))
    estilo.configure("Treeview.Heading", font=("segoe UI", 10, "bold"))

    #controlador de pestañas
    notebook = ttk.Notebook(ventana)
    notebook.pack(expand=True, fill='both', padx=10, pady=10)

    #frames para cada pestaña
    frame_pacientes = ttk.Frame(notebook)
    frame_medicos = ttk.Frame(notebook)
    frame_horarios = ttk.Frame(notebook)
    frame_citas = ttk.Frame(notebook)
    frame_consultas = ttk.Frame(notebook)
    frame_historial = ttk.Frame(notebook)

    #agrager frames al notebook
    notebook.add(frame_pacientes, text="👨‍⚕️ Gestion de Pacientes")
    notebook.add(frame_medicos, text="⚕️ Gestion de Médicos")
    notebook.add(frame_horarios, text="⏰ Gestion de Horarios")
    notebook.add(frame_citas, text="📅 Gestion de Citas")
    notebook.add(frame_consultas, text="🩺 Atender Citas")
    notebook.add(frame_historial, text="📋 Historial Clínico")


    # =========================================================
    # 1. DISEÑO DE GESTIÓN DE PACIENTES (REDISEÑO MODERNO)
    # =========================================================
    frame_pacientes.columnconfigure(0, weight=1) # Para que todo se centre bonito

    # Contenedor 1: Formulario agrupado en una caja suave
    lf_form_pacientes = ttk.LabelFrame(frame_pacientes, text=" 📋 Formulario de Registro de Paciente ", padding=(20, 15))
    lf_form_pacientes.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Columna Izquierda (Datos Básicos)
    ttk.Label(lf_form_pacientes, text="Nombre *").grid(row=0, column=0, padx=10, pady=8, sticky="e")
    ent_pac_nombre = ttk.Entry(lf_form_pacientes, width=35)
    ent_pac_nombre.grid(row=0, column=1, padx=10, pady=8, sticky="w")

    ttk.Label(lf_form_pacientes, text="Apellido *").grid(row=1, column=0, padx=10, pady=8, sticky="e")
    ent_pac_apellido = ttk.Entry(lf_form_pacientes, width=35)
    ent_pac_apellido.grid(row=1, column=1, padx=10, pady=8, sticky="w")

    ttk.Label(lf_form_pacientes, text="Documento *").grid(row=2, column=0, padx=10, pady=8, sticky="e")
    ent_pac_doc = ttk.Entry(lf_form_pacientes, width=35)
    ent_pac_doc.grid(row=2, column=1, padx=10, pady=8, sticky="w")

    # Reemplazamos la fecha de nacimiento manual por el Calendario
    ttk.Label(lf_form_pacientes, text="Fecha Nacimiento *").grid(row=3, column=0, padx=10, pady=8, sticky="e")
    ent_pac_fecha = DateEntry(lf_form_pacientes, width=33, background='#2B579A', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    ent_pac_fecha.grid(row=3, column=1, padx=10, pady=8, sticky="w")

    # Columna Derecha (Datos de Contacto)
    ttk.Label(lf_form_pacientes, text="Teléfono *").grid(row=0, column=2, padx=20, pady=8, sticky="e")
    ent_pac_tel = ttk.Entry(lf_form_pacientes, width=35)
    ent_pac_tel.grid(row=0, column=3, padx=10, pady=8, sticky="w")

    ttk.Label(lf_form_pacientes, text="Correo Electrónico").grid(row=1, column=2, padx=20, pady=8, sticky="e")
    ent_pac_correo = ttk.Entry(lf_form_pacientes, width=35)
    ent_pac_correo.grid(row=1, column=3, padx=10, pady=8, sticky="w")

    ttk.Label(lf_form_pacientes, text="Dirección Residencia").grid(row=2, column=2, padx=20, pady=8, sticky="e")
    ent_pac_dir = ttk.Entry(lf_form_pacientes, width=35)
    ent_pac_dir.grid(row=2, column=3, padx=10, pady=8, sticky="w")

    entradas_paciente = {
        'nombre': ent_pac_nombre,
        'apellido': ent_pac_apellido,
        'documento': ent_pac_doc,
        'fecha_nacimiento': ent_pac_fecha,
        'telefono': ent_pac_tel,
        'correo': ent_pac_correo,
        'direccion': ent_pac_dir
    }

    # Botón Principal (Usamos el estilo Accent para que resalte en azul)
    btn_guardar_pac = ttk.Button(lf_form_pacientes, text="💾 Guardar Nuevo Paciente", style="Accent.TButton",
                                 command=lambda: guardar_paciente(entradas_paciente, tree_pacientes))
    btn_guardar_pac.grid(row=4, column=0, columnspan=4, pady=25)

    # Contenedor 2: Tabla de Resultados
    lf_tabla_pacientes = ttk.LabelFrame(frame_pacientes, text=" 👥 Directorio de Pacientes ", padding=(10, 10))
    lf_tabla_pacientes.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

    columnas_pac = ("ID", "Nombre", "Apellido", "Documento", "Teléfono")
    tree_pacientes = ttk.Treeview(lf_tabla_pacientes, columns=columnas_pac, show="headings", height=7)

    anchos_pac = [50, 180, 180, 120, 120]
    for col, ancho in zip(columnas_pac, anchos_pac):
        tree_pacientes.heading(col, text=col)
        tree_pacientes.column(col, width=ancho, anchor="center")

    tree_pacientes.pack(fill="both", expand=True, padx=10, pady=10)

    cargar_pacientes(tree_pacientes)
######################################################################################
######################################################################################

    #pestaña para agregar médicos
    tk.Label(frame_medicos, text="Registro de Medicos   ", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
    entradas_medicos = {}
    campos_medicos = [
        ("Nombre *", "nombre"),
        ("Apellido *", "apellido"),
        ("Documento *", "documento"),
        ("Teléfono *", "telefono"),
        ("Correo", "correo")
    ]
    for i, (lbl, var) in enumerate(campos_medicos, start=1):
        tk.Label(frame_medicos, text=lbl).grid(row=i, column=0, sticky="e", padx=10, pady=5)
        caja = tk.Entry(frame_medicos, width=40)
        caja.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        entradas_medicos[var] = caja

        tk.Label(frame_medicos, text="Especialidad *").grid(row=len(campos_medicos)+1, column=0, sticky="e", padx=10, pady=5)

        lista_esp_bd = cargar_especialidades()
        nombres_especialidades = [esp[1] for esp in lista_esp_bd]

        combo_especialidad = ttk.Combobox(frame_medicos, values=nombres_especialidades, state="readonly", width=37)
        combo_especialidad.grid(row=len(campos_medicos)+1, column=1, padx=10, pady=5, sticky="w")

        btn_guardar_medico = tk.Button(frame_medicos, text="👨‍⚕️ Guardar Médico", command=lambda: guardar_medico(entradas_medicos, combo_especialidad, lista_esp_bd, None))
        btn_guardar_medico.grid(row=len(campos_medicos)+2, column=0, columnspan=2, pady=20) 


##################################################################################################################       
##################################################################################################################


    #pestaña para agregar horarios
    #-----Medicos
    tk.Label(frame_horarios, text="Configurar Horario Medico", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
    tk.Label(frame_horarios, text="Médico *").grid(row=1, column=0, sticky="e", padx=10, pady=5)
    lista_medicos_bd = cargar_medicos()
    nombres_medicos = [f"{med[1]} {med[2]}" for med in lista_medicos_bd]
    combo_horario_medico = ttk.Combobox(frame_horarios, values=nombres_medicos, state="readonly", width=37)
    combo_horario_medico.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    #-----Dias
    tk.Label(frame_horarios, text="Día de la semana *").grid(row=2, column=0, sticky="e", padx=10, pady=5)
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    combo_dia = ttk.Combobox(frame_horarios, values=dias_semana, state="readonly", width=37)
    combo_dia.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    #-----Horas
    entradas_horarios = {}
    tk.Label(frame_horarios, text="Hora Inicio (HH:MM) *").grid(row=3, column=0, sticky="e", padx=10, pady=5)
    entradas_horarios['hora_inicio'] = ttk.Entry(frame_horarios, width=40)
    entradas_horarios['hora_inicio'].grid(row=3, column=1, padx=10, pady=5, sticky="w")

    tk.Label(frame_horarios, text="Hora Fin (HH:MM) *").grid(row=4, column=0, sticky="e", padx=10, pady=5)
    entradas_horarios['hora_fin'] = ttk.Entry(frame_horarios, width=40)
    entradas_horarios['hora_fin'].grid(row=4, column=1, padx=10, pady=5, sticky="w")

    #-----Boton Guardar
    btn_guardar_horario = tk.Button(frame_horarios, text="⏰ Guardar Horario", command=lambda: guardar_horario(entradas_horarios, combo_horario_medico, combo_dia, lista_medicos_bd))
    btn_guardar_horario.grid(row=5, column=0, columnspan=2, pady=20)


######################################################################################################################
######################################################################################################################

    #pestaña para gestionar citas
    tk.Label(frame_citas, text="Agendar Nueva Cita", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    # Cargar datos para los combos
    lista_pac_bd = obtener_pacientes_combo()
    lista_med_bd = cargar_medicos()
    
    nombres_pac = [f"{p[1]} {p[2]} - {p[3]}" for p in lista_pac_bd] # Nombre + Apellido - Documento
    nombres_med = [f"{m[1]} {m[2]}" for m in lista_med_bd]

    # Combobox Paciente
    tk.Label(frame_citas, text="Paciente *").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    combo_cita_pac = ttk.Combobox(frame_citas, values=nombres_pac, state="readonly", width=40)
    combo_cita_pac.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Combobox Médico
    tk.Label(frame_citas, text="Médico *").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    combo_cita_med = ttk.Combobox(frame_citas, values=nombres_med, state="readonly", width=40)
    combo_cita_med.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    # Entradas de Texto (Fecha, Hora, Motivo)
    tk.Label(frame_citas, text="Seleccionar Fecha:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    ent_fecha = DateEntry(frame_citas, width=19, background='darkblue',
        foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    ent_fecha.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    
    tk.Label(frame_citas, text="Hora (HH:MM) *").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    ent_cita_hora = ttk.Entry(frame_citas, width=43)
    ent_cita_hora.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    tk.Label(frame_citas, text="Motivo de consulta *").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    ent_cita_motivo = ttk.Entry(frame_citas, width=43)
    ent_cita_motivo.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    # Botón Agendar
    btn_agendar = ttk.Button(frame_citas, text="📅 Agendar Cita", 
                             command=lambda: agendar_cita(combo_cita_pac, combo_cita_med, ent_fecha, ent_cita_hora, ent_cita_motivo, lista_pac_bd, lista_med_bd))
    btn_agendar.grid(row=6, column=0, columnspan=2, pady=20)

    #Boton Cancelar Cita
    btn_agendar.grid(row=6, column=0, columnspan=2, pady=15)
    
    # --- Sección Diferenciadora: Cancelación de Citas ---
    ttk.Separator(frame_citas, orient='horizontal').grid(row=7, column=0, columnspan=3, sticky='ew', pady=15)
    
    tk.Label(frame_citas, text="🚫 Cancelar una Cita Programada", font=("Arial", 11, "bold")).grid(row=8, column=0, columnspan=2, pady=5, sticky="w", padx=10)

    tk.Label(frame_citas, text="Seleccionar Cita:").grid(row=9, column=0, padx=10, pady=5, sticky="e")
    combo_cancelar_cita = ttk.Combobox(frame_citas, state="readonly", width=55)
    combo_cancelar_cita.grid(row=9, column=1, padx=10, pady=5, sticky="w")

    lista_citas_cancelar = []

    def refrescar_combo_cancelaciones():
        nonlocal lista_citas_cancelar
        lista_citas_cancelar = obtener_citas_programadas()
        textos_citas = [f"ID: {c[0]} | {c[1]} - {c[2]} | Paciente: {c[3]} {c[4]}" for c in lista_citas_cancelar]
        combo_cancelar_cita['values'] = textos_citas

    ttk.Button(frame_citas, text="🔄 Actualizar", command=refrescar_combo_cancelaciones).grid(row=9, column=2, padx=5)
    
    # Llamamos a la función para que cargue las citas existentes al abrir la app

    refrescar_combo_cancelaciones()

    btn_cancelar = ttk.Button(frame_citas, text="❌ Cancelar Cita", 
        command=lambda: [ejecutar_cancelacion_cita(combo_cancelar_cita, lista_citas_cancelar), refrescar_combo_cancelaciones()])
    btn_cancelar.grid(row=10, column=0, columnspan=2, pady=10)



######################################################################################################################
######################################################################################################################

    #pestaña para registrar atención médica (consultas)
    tk.Label(frame_consultas, text="Registrar Atención Médica", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
    tk.Label(frame_consultas, text="Seleccionar Cita *").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    
    combo_consultas_cita = ttk.Combobox(frame_consultas, state="readonly", width=55)
    combo_consultas_cita.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    
    lista_citas_pendientes = []

    def refrescar_citas():
        nonlocal lista_citas_pendientes
        lista_citas_pendientes = obtener_citas_pendientes()
        nombres_citas = [f"ID: {c[0]} | {c[1]} {c[2]} - Paciente: {c[3]} {c[4]}" for c in lista_citas_pendientes]
        combo_consultas_cita['values'] = nombres_citas
    
    ttk.Button(frame_consultas, text="🔄 Recargar Citas", command=refrescar_citas).grid(row=1, column=2, padx=5)
    refrescar_citas()

    # Entradas para la consulta
    tk.Label(frame_consultas, text="Diagnóstico *").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    ent_diag = ttk.Entry(frame_consultas, width=58)
    ent_diag.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    tk.Label(frame_consultas, text="Observaciones").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    ent_obs = ttk.Entry(frame_consultas, width=58)
    ent_obs.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    tk.Label(frame_consultas, text="Medicamento/Tratamiento *").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    ent_med = ttk.Entry(frame_consultas, width=58)
    ent_med.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    # Botón Guarda
    btn_guardar_consulta = ttk.Button(frame_consultas, text="🩺 Guardar Consulta", 
            command=lambda: registrar_consulta_medica(combo_consultas_cita, ent_diag, ent_obs, ent_med, lista_citas_pendientes))
    btn_guardar_consulta.grid(row=5, column=0, columnspan=2, pady=20)


##############################################################################################################
##############################################################################################################

    #pestaña para mostrar historial clínico del paciente
    tk.Label(frame_historial, text="Historial Clínico del Paciente", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame_historial, text="Buscar Paciente:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    combo_historial_pac = ttk.Combobox(frame_historial, values=nombres_pac, state="readonly", width=50)
    combo_historial_pac.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    columnas_hist = ("Fecha", "Médico", "Diagnóstico", "Observaciones", "Tratamiento")
    tree_historial = ttk.Treeview(frame_historial, columns=columnas_hist, show="headings", height=10)
    
    anchos = [90, 150, 200, 150, 150]
    for col, ancho in zip(columnas_hist, anchos):tree_historial.heading(col, text=col)
    tree_historial.column(col, width=ancho, anchor="center")
        
    tree_historial.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    btn_buscar_hist = ttk.Button(frame_historial, text="🔍 Ver Historial", 
                command=lambda: obtener_historial_paciente(combo_historial_pac, tree_historial, lista_pac_bd))
    btn_buscar_hist.grid(row=2, column=0, columnspan=2, pady=10)

    tree_historial.grid(row=3, column=0, columnspan=2, padx=20, pady=20)
    # Botón para exportar a PDF la consulta seleccionada de la tabla (Elemento diferenciador)
    btn_exportar_pdf = ttk.Button(frame_historial, text="🖨️ Exportar Consulta a PDF", 
                                  command=lambda: exportar_pdf(tree_historial, combo_historial_pac))
    btn_exportar_pdf.grid(row=4, column=0, columnspan=2, pady=5)


    ventana.mainloop()
if __name__ == "__main__":
    inicar_app()
    