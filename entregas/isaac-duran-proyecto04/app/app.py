import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
from tkcalendar import DateEntry
##################################################################
from consultas_paciente import cargar_pacientes, guardar_paciente
from consultas_medico import cargar_especialidades, cargar_tabla_medicos, guardar_medico
from consultas_horario import guardar_horario, cargar_medicos, cargar_tabla_horarios
from consultas_cita import obtener_especialidades_medico, obtener_pacientes_combo, agendar_cita, obtener_citas_programadas, ejecutar_cancelacion_cita, obtener_pacientes_combo
from consultas_atencionCita import obtener_citas_pendientes, registrar_consulta_medica
from historial import obtener_historial_paciente, exportar_pdf

################################################################–
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


    # ==========================================================================================================================
    # 1. DISEÑO DE GESTIÓN DE PACIENTES (REDISEÑO MODERNO)
    # ==========================================================================================================================
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


    # =================================================================================================================
    # 2. DISEÑO DE GESTIÓN DE MÉDICOS (REDISEÑO MULTI-ESPECIALIDAD)
    # =================================================================================================================
    frame_medicos.columnconfigure(0, weight=1)
    # Contenedor 1: Formulario agrupado
    lf_form_medicos = ttk.LabelFrame(frame_medicos, text=" 📋 Formulario de Registro de Médico ", padding=(20, 15))
    lf_form_medicos.grid(row=0, column=0, padx=20, pady=15, sticky="nsew")

    # Columna Izquierda (Datos Personales)
    ttk.Label(lf_form_medicos, text="Nombre *").grid(row=0, column=0, padx=10, pady=6, sticky="e")
    ent_med_nombre = ttk.Entry(lf_form_medicos, width=30)
    ent_med_nombre.grid(row=0, column=1, padx=10, pady=6, sticky="w")

    ttk.Label(lf_form_medicos, text="Apellido *").grid(row=1, column=0, padx=10, pady=6, sticky="e")
    ent_med_apellido = ttk.Entry(lf_form_medicos, width=30)
    ent_med_apellido.grid(row=1, column=1, padx=10, pady=6, sticky="w")

    ttk.Label(lf_form_medicos, text="Documento *").grid(row=2, column=0, padx=10, pady=6, sticky="e")
    ent_med_doc = ttk.Entry(lf_form_medicos, width=30)
    ent_med_doc.grid(row=2, column=1, padx=10, pady=6, sticky="w")

    ttk.Label(lf_form_medicos, text="Teléfono *").grid(row=3, column=0, padx=10, pady=6, sticky="e")
    ent_med_tel = ttk.Entry(lf_form_medicos, width=30)
    ent_med_tel.grid(row=3, column=1, padx=10, pady=6, sticky="w")

    ttk.Label(lf_form_medicos, text="Correo Electrónico").grid(row=4, column=0, padx=10, pady=6, sticky="e")
    ent_med_correo = ttk.Entry(lf_form_medicos, width=30)
    ent_med_correo.grid(row=4, column=1, padx=10, pady=6, sticky="w")

    # Columna Derecha: Selección de Especialidades Múltiples
    ttk.Label(lf_form_medicos, text="Seleccione Especialidad(es)").grid(row=0, column=2, padx=15, pady=5, sticky="ne")
    
    # Frame interno para juntar el listbox con su scrollbar
    frame_listbox = ttk.Frame(lf_form_medicos)
    frame_listbox.grid(row=0, column=3, rowspan=4, padx=10, pady=5, sticky="nw")

    # Listbox con selectmode="multiple" para permitir selección múltiple
    listbox_especialidades = tk.Listbox(frame_listbox, height=6, width=32, selectmode="multiple", exportselection=0)
    scrollbar_esp = ttk.Scrollbar(frame_listbox, orient="vertical", command=listbox_especialidades.yview)
    listbox_especialidades.configure(yscrollcommand=scrollbar_esp.set)
    
    listbox_especialidades.pack(side="left", fill="y")
    scrollbar_esp.pack(side="right", fill="y")

    # Cargar las especialidades de la BD dentro del Listbox
    lista_esp_bd = cargar_especialidades()
    for esp in lista_esp_bd:
        listbox_especialidades.insert(tk.END, esp[1])

    entradas_medico = {
        'nombre': ent_med_nombre,
        'apellido': ent_med_apellido,
        'documento': ent_med_doc,
        'telefono': ent_med_tel,
        'correo': ent_med_correo
    }

    # Botón Principal
    btn_guardar_med = ttk.Button(lf_form_medicos, text="💾 Guardar Nuevo Médico", style="Accent.TButton",
                                 command=lambda: guardar_medico(entradas_medico, listbox_especialidades, lista_esp_bd, tree_medicos))
    btn_guardar_med.grid(row=5, column=0, columnspan=4, pady=15)

    # Contenedor 2: Tabla de Médicos Registrados
    lf_tabla_medicos = ttk.LabelFrame(frame_medicos, text=" 👥 Personal Médico Registrado ", padding=(10, 10))
    lf_tabla_medicos.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

    columnas_med = ("ID", "Nombre", "Apellido")
    tree_medicos = ttk.Treeview(lf_tabla_medicos, columns=columnas_med, show="headings", height=6)

    for col in columnas_med:
        tree_medicos.heading(col, text=col)
        tree_medicos.column(col, width=200, anchor="center")

    tree_medicos.pack(fill="both", expand=True, padx=10, pady=5)
    cargar_tabla_medicos(tree_medicos)


# ==========================================================================================================================
# 3. DISEÑO DE GESTIÓN DE HORARIOS (ASIGNACIÓN DE HORARIOS A MÉDICOS)
# ==========================================================================================================================   
    frame_horarios.columnconfigure(0, weight=1)

    # --- CONTENEDOR 1: FORMULARIO ---
    lf_form_horarios = ttk.LabelFrame(frame_horarios, text=" ⏰ Asignar Horario a Médico ", padding=(20, 15))
    lf_form_horarios.grid(row=0, column=0, padx=20, pady=15, sticky="nsew")

    lista_medicos_bd = cargar_medicos()
    nombres_medicos = [f"{med[1]} {med[2]}" for med in lista_medicos_bd]

    def actualizar_combo_horarios_medicos():
        # RECTIFICACIÓN: Llamamos directo a la BD, no al Treeview de otra pestaña
        lista_medicos_bd.clear()
        lista_medicos_bd.extend(cargar_medicos())
        nombres_med_actualizados = [f"{m[1]} {m[2]}" for m in lista_medicos_bd]
        combo_horario_medico['values'] = nombres_med_actualizados

    # Fila 0: Médico
    ttk.Label(lf_form_horarios, text="Médico *").grid(row=0, column=0, sticky="e", padx=10, pady=8)
    combo_horario_medico = ttk.Combobox(lf_form_horarios, values=nombres_medicos, postcommand=actualizar_combo_horarios_medicos, state="readonly", width=37)
    combo_horario_medico.grid(row=0, column=1, padx=10, pady=8, sticky="w")

    # Fila 1: Días de la semana (Listbox Múltiple)
    ttk.Label(lf_form_horarios, text="Días de la semana *\n(Clic para elegir varios)").grid(row=1, column=0, sticky="ne", padx=10, pady=8)
    
    frame_dias = ttk.Frame(lf_form_horarios)
    frame_dias.grid(row=1, column=1, padx=10, pady=8, sticky="w")
    listbox_dias = tk.Listbox(frame_dias, height=4, width=39, selectmode="multiple", exportselection=0)
    scrollbar_dias = ttk.Scrollbar(frame_dias, orient="vertical", command=listbox_dias.yview)
    listbox_dias.configure(yscrollcommand=scrollbar_dias.set)
    listbox_dias.pack(side="left", fill="y")
    scrollbar_dias.pack(side="right", fill="y")

    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for dia in dias_semana:
        listbox_dias.insert(tk.END, dia)

    # Filas 2 y 3: Horas
    entradas_horarios = {}
    ttk.Label(lf_form_horarios, text="Hora Inicio (HH:MM) *").grid(row=2, column=0, sticky="e", padx=10, pady=8)
    entradas_horarios['hora_inicio'] = ttk.Entry(lf_form_horarios, width=40)
    entradas_horarios['hora_inicio'].grid(row=2, column=1, padx=10, pady=8, sticky="w")

    ttk.Label(lf_form_horarios, text="Hora Fin (HH:MM) *").grid(row=3, column=0, sticky="e", padx=10, pady=8)
    entradas_horarios['hora_fin'] = ttk.Entry(lf_form_horarios, width=40)
    entradas_horarios['hora_fin'].grid(row=3, column=1, padx=10, pady=8, sticky="w")

    # --- CONTENEDOR 2: TABLA DE HORARIOS ---
    lf_tabla_horarios = ttk.LabelFrame(frame_horarios, text=" 📅 Horarios Registrados ", padding=(10, 10))
    lf_tabla_horarios.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

    columnas_hor = ("Médico", "Días de Atención", "Inicio", "Fin")
    tree_horarios = ttk.Treeview(lf_tabla_horarios, columns=columnas_hor, show="headings", height=6)

    anchos_hor = [150, 200, 80, 80]
    for col, ancho in zip(columnas_hor, anchos_hor):
        tree_horarios.heading(col, text=col)
        tree_horarios.column(col, width=ancho, anchor="center")

    tree_horarios.pack(fill="both", expand=True, padx=10, pady=5)

    # Fila 4: Botón Guardar (Ahora con estilo Accent azul)
    btn_guardar_horario = ttk.Button(lf_form_horarios, text="⏰ Guardar Horario", style="Accent.TButton",
                                    command=lambda: guardar_horario(entradas_horarios, listbox_dias, combo_horario_medico, lista_medicos_bd, tree_horarios))
    btn_guardar_horario.grid(row=4, column=0, columnspan=2, pady=15)

    # Cargar datos en la tabla al inicio
    from consultas_horario import cargar_tabla_horarios 
    cargar_tabla_horarios(tree_horarios)


# ==========================================================================================================================
# 4. DISEÑO DE GESTIÓN DE CITAS (AGENDAR Y CANCELAR CITAS)
# ==========================================================================================================================
    frame_citas.columnconfigure(0, weight=1)

    # --- CONTENEDOR 1: AGENDAR CITA ---
    lf_form_citas = ttk.LabelFrame(frame_citas, text=" 📅 Formulario para Agendar Nueva Cita ", padding=(20, 15))
    lf_form_citas.grid(row=0, column=0, padx=20, pady=15, sticky="nsew")

    # Cargar datos iniciales
    lista_pac_bd = obtener_pacientes_combo()
    lista_med_bd = cargar_medicos()
    nombres_pac = [f"{p[1]} {p[2]} - {p[3]}" for p in lista_pac_bd] 
    nombres_med = [f"{m[1]} {m[2]}" for m in lista_med_bd]

    # Combobox Paciente
    def actualizar_pacientes_citas():
        lista_pac_bd.clear()
        lista_pac_bd.extend(obtener_pacientes_combo())
        combo_cita_pac['values'] = [f"{p[1]} {p[2]} - {p[3]}" for p in lista_pac_bd]

    ttk.Label(lf_form_citas, text="Paciente *").grid(row=0, column=0, padx=10, pady=8, sticky="e")
    combo_cita_pac = ttk.Combobox(lf_form_citas, postcommand=actualizar_pacientes_citas, values=nombres_pac, state="readonly", width=40)
    combo_cita_pac.grid(row=0, column=1, padx=10, pady=8, sticky="w")

    # Combobox Médico y Especialidad
    def actualizar_medicos_citas():
        lista_med_bd.clear()
        lista_med_bd.extend(cargar_medicos())
        combo_cita_med['values'] = [f"{m[1]} {m[2]}" for m in lista_med_bd]

    ttk.Label(lf_form_citas, text="Médico *").grid(row=1, column=0, padx=10, pady=8, sticky="e")
    combo_cita_med = ttk.Combobox(lf_form_citas, postcommand=actualizar_medicos_citas, values=nombres_med, state="readonly", width=40)
    combo_cita_med.grid(row=1, column=1, padx=10, pady=8, sticky="w")

    lbl_especialidades = tk.Label(lf_form_citas, text="Especialidad: (Seleccione un médico)", fg="gray", font=("Arial", 9, "italic"))
    lbl_especialidades.grid(row=1, column=2, padx=10, sticky="w")
    
    def mostrar_especialidades(event):
        med_sel = combo_cita_med.get()
        if not med_sel:
            lbl_especialidades.config(text="Especialidad: (Seleccione un médico)", fg="gray")
            return
        
        id_medico = None
        for m in lista_med_bd:
            if f"{m[1]} {m[2]}" == med_sel:
                id_medico = m[0]
                break
        
        if id_medico:
            especialidades = obtener_especialidades_medico(id_medico)
            texto_esp = ", ".join(especialidades) if especialidades else "General"
            lbl_especialidades.config(text=f"Especialidad(es): {texto_esp}", fg="#2B579A", font=("Arial", 9, "bold"))

    combo_cita_med.bind("<<ComboboxSelected>>", mostrar_especialidades)

    # Entradas de Fecha, Hora y Motivo
    ttk.Label(lf_form_citas, text="Seleccionar Fecha *").grid(row=2, column=0, padx=10, pady=8, sticky="e")
    ent_fecha = DateEntry(lf_form_citas, width=38, background='#2B579A', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    ent_fecha.grid(row=2, column=1, padx=10, pady=8, sticky="w")
    
    ttk.Label(lf_form_citas, text="Hora (HH:MM) *").grid(row=3, column=0, padx=10, pady=8, sticky="e")
    ent_cita_hora = ttk.Entry(lf_form_citas, width=43)
    ent_cita_hora.grid(row=3, column=1, padx=10, pady=8, sticky="w")

    ttk.Label(lf_form_citas, text="Motivo de consulta *").grid(row=4, column=0, padx=10, pady=8, sticky="e")
    ent_cita_motivo = ttk.Entry(lf_form_citas, width=43)
    ent_cita_motivo.grid(row=4, column=1, padx=10, pady=8, sticky="w")

    # Botón Agendar
    def ejecutar_agendar_seguro():
        pacientes_frescos = obtener_pacientes_combo()
        # RECTIFICACIÓN: Obtenemos datos directamente de BD, no del treeview
        medicos_frescos = cargar_medicos() 
        agendar_cita(combo_cita_pac, combo_cita_med, ent_fecha, ent_cita_hora, ent_cita_motivo, pacientes_frescos, medicos_frescos)

    btn_agendar = ttk.Button(lf_form_citas, text="📅 Agendar Cita", style="Accent.TButton", command=ejecutar_agendar_seguro)
    btn_agendar.grid(row=5, column=0, columnspan=3, pady=20)


    # --- CONTENEDOR 2: CANCELAR CITA ---
    lf_cancelar_citas = ttk.LabelFrame(frame_citas, text=" 🚫 Cancelar Cita Programada ", padding=(20, 15))
    lf_cancelar_citas.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

    def ejecutar_cancelar_seguro():
        citas_programadas_frescas = obtener_citas_programadas()
        ejecutar_cancelacion_cita(combo_cancelar_cita, citas_programadas_frescas)

    def actualizar_combo_cancelar_citas():
        global_citas_programadas_bd = obtener_citas_programadas()
        citas_formateadas = [f"ID: {c[0]} | {c[1]} - {c[2]} | Paciente: {c[3]} {c[4]}" for c in global_citas_programadas_bd]
        combo_cancelar_cita['values'] = citas_formateadas

    ttk.Label(lf_cancelar_citas, text="Seleccionar Cita:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    combo_cancelar_cita = ttk.Combobox(lf_cancelar_citas, state="readonly", postcommand=actualizar_combo_cancelar_citas, width=65)
    combo_cancelar_cita.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    btn_cancelar = ttk.Button(lf_cancelar_citas, text="❌ Cancelar Cita", command=ejecutar_cancelar_seguro)
    btn_cancelar.grid(row=1, column=0, columnspan=2, pady=10)


# ==========================================================================================================================
# 5. DISEÑO DE GESTIÓN DE CONSULTAS (REGISTRAR ATENCIÓN MÉDICA)
# ==========================================================================================================================
    frame_consultas.columnconfigure(0, weight=1)

    lf_form_consultas = ttk.LabelFrame(frame_consultas, text=" 🩺 Formulario de Registro de Atención Médica ", padding=(20, 25))
    lf_form_consultas.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def obtener_formato_cita(c):
        return f"ID: {c[0]} | {c[1]} - {c[2]} | Paciente: {c[3]} {c[4]}"
    
    def actualizar_combo_atender_citas():
        global_citas_pendientes_bd = obtener_citas_pendientes()
        citas_pendientes_formateadas = [obtener_formato_cita(c) for c in global_citas_pendientes_bd]
        combo_consultas_cita['values'] = citas_pendientes_formateadas
    
    ttk.Label(lf_form_consultas, text="Seleccionar Cita *").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    combo_consultas_cita = ttk.Combobox(lf_form_consultas, state="readonly", postcommand=actualizar_combo_atender_citas, width=65)
    combo_consultas_cita.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    ttk.Label(lf_form_consultas, text="Diagnóstico *").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    ent_diag = ttk.Entry(lf_form_consultas, width=68)
    ent_diag.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    ttk.Label(lf_form_consultas, text="Observaciones").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    ent_obs = ttk.Entry(lf_form_consultas, width=68)
    ent_obs.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    ttk.Label(lf_form_consultas, text="Medicamento/Tratamiento *").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    ent_med = ttk.Entry(lf_form_consultas, width=68)
    ent_med.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    # Función envoltorio para asegurar datos frescos al guardar
    def ejecutar_registro_consulta_seguro():
        citas_frescas = obtener_citas_pendientes()
        registrar_consulta_medica(combo_consultas_cita, ent_diag, ent_obs, ent_med, citas_frescas)

    btn_guardar_consulta = ttk.Button(lf_form_consultas, text="🩺 Guardar Registro Clínico", style="Accent.TButton", command=ejecutar_registro_consulta_seguro)
    btn_guardar_consulta.grid(row=4, column=0, columnspan=2, pady=30)


#==========================================================================================================================
# 6. PESTAÑA DE HISTORIAL CLÍNICO (CONSULTA Y EXPORTACIÓN A PDF)
#==========================================================================================================================
    tk.Label(frame_historial, text="Historial Clínico del Paciente", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    def actualizar_combo_historial():
        lista_pac_bd.clear()
        lista_pac_bd.extend(obtener_pacientes_combo())
        
        nombres_pac_actualizados = [f"{p[1]} {p[2]} - {p[3]}" for p in lista_pac_bd]
        combo_historial_pac['values'] = nombres_pac_actualizados

    tk.Label(frame_historial, text="Buscar Paciente:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    combo_historial_pac = ttk.Combobox(frame_historial, values=nombres_pac, state="readonly", width=50, postcommand=actualizar_combo_historial)
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
    combo_paciente_historial = ttk.Combobox(frame_historial, state="readonly")


    ventana.mainloop()
if __name__ == "__main__":
    inicar_app()
    