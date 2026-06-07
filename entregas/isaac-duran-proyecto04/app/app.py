import tkinter as tk
from tkinter import ttk
import sv_ttk
from tkcalendar import Calendar
##################################################################
from consultas_paciente import cargar_pacientes, guardar_paciente
from consultas_medico import cargar_especialidades, cargar_tabla_medicos, guardar_medico
from consultas_horario import guardar_horario, cargar_medicos, cargar_tabla_horarios
from consultas_cita import obtener_especialidades_medico, obtener_pacientes_combo, agendar_cita, obtener_citas_programadas, ejecutar_cancelacion_cita, obtener_horarios_medico_texto, modificar_cita, ejecutar_no_asistio_cita
from consultas_atencionCita import obtener_citas_pendientes, registrar_consulta_medica
from historial import obtener_historial_paciente, exportar_pdf

################################################################–
################################################################


def iniciar_app():
    #ventana principal
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión - Consulta Médico")
    ventana.geometry("1024x768") # Tamaño base de respaldo
    
    # Intentar maximizar la ventana según el sistema operativo (Windows/Linux/Mac)
    try:
        ventana.state('zoomed') 
    except tk.TclError:
        ventana.attributes('-zoomed', True)

    #FUNCIÓN: SELECTOR DE FECHAS A PRUEBA DE BUGS
    def abrir_calendario_seguro(entry_widget):
        top = tk.Toplevel(ventana)
        top.title("Elegir Fecha")
        x = entry_widget.winfo_rootx()
        y = entry_widget.winfo_rooty() + 30
        top.geometry(f"+{x}+{y}")
        top.grab_set()
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd', background='#2B579A', foreground='white')
        cal.pack(padx=15, pady=10)
        
        def confirmar_fecha():
            entry_widget.config(state="normal")
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, cal.get_date())
            entry_widget.config(state="readonly")
            top.destroy()     
        ttk.Button(top, text="✔ Confirmar Fecha", style="Accent.TButton", command=confirmar_fecha).pack(pady=(0, 10))
    # -----------------------------------------------------------

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

    # Reemplazamos el DateEntry conflictivo por nuestro selector personalizado
    ttk.Label(lf_form_pacientes, text="Fecha Nacimiento *").grid(row=3, column=0, padx=10, pady=8, sticky="e")
    frame_cal_pac = ttk.Frame(lf_form_pacientes)
    frame_cal_pac.grid(row=3, column=1, padx=10, pady=8, sticky="w")
    ent_pac_fecha = ttk.Entry(frame_cal_pac, width=28, state="readonly")
    ent_pac_fecha.pack(side="left", padx=(0, 5))
    btn_cal_pac = ttk.Button(frame_cal_pac, text="📅", width=4, command=lambda: abrir_calendario_seguro(ent_pac_fecha))
    btn_cal_pac.pack(side="left")

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

    # Cargar las especialidades iniciales
    lista_esp_bd = cargar_especialidades()
    for esp in lista_esp_bd:
        listbox_especialidades.insert(tk.END, esp[1])

    def actualizar_especialidades_seguro(event=None):
        nuevas_esp = cargar_especialidades()
        
        if nuevas_esp != lista_esp_bd:
            # 1. Guardar lo que el usuario ya tenía seleccionado para no borrárselo
            selecciones_actuales = [listbox_especialidades.get(i) for i in listbox_especialidades.curselection()]
            
            # 2. Limpiar el cuadro y actualizar la lista en memoria
            listbox_especialidades.delete(0, tk.END)
            lista_esp_bd.clear()
            lista_esp_bd.extend(nuevas_esp)
            
            # 3. Volver a llenar el cuadro y restaurar las selecciones previas
            for i, esp in enumerate(lista_esp_bd):
                listbox_especialidades.insert(tk.END, esp[1])
                if esp[1] in selecciones_actuales:
                    listbox_especialidades.selection_set(i)
    # Refresco inteligente: Solo consultar la BD al entrar a la pestaña "Médicos"
    def al_cambiar_pestana(event):
        pestana_activa = notebook.tab(notebook.select(), "text")
        if "Gestion de Médicos" in pestana_activa:
            actualizar_especialidades_seguro()

    notebook.bind("<<NotebookTabChanged>>", al_cambiar_pestana)

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

    cargar_tabla_horarios(tree_horarios)


    # ==========================================================================================================================
    # 4. DISEÑO DE GESTIÓN DE CITAS (AGENDAR, MODIFICAR Y CANCELAR)
    # ==========================================================================================================================
    frame_citas.columnconfigure(0, weight=6) 
    frame_citas.columnconfigure(1, weight=5) 
    frame_citas.rowconfigure(0, weight=1)
    frame_citas.rowconfigure(1, weight=1)

    # --- PANEL IZQUIERDO: AGENDAR CITA ---
    lf_form_citas = ttk.LabelFrame(frame_citas, text=" 📅 Formulario para Agendar Nueva Cita ", padding=(20, 15))
    # rowspan=2 hace que este formulario ocupe toda la altura del lado izquierdo
    lf_form_citas.grid(row=0, column=0, rowspan=2, padx=(20, 10), pady=15, sticky="nsew")

    # Cargar datos iniciales
    lista_pac_bd = obtener_pacientes_combo()
    lista_med_bd = cargar_medicos()
    nombres_pac = [f"{p[1]} {p[2]} - {p[3]}" for p in lista_pac_bd] 
    nombres_med = [f"{m[1]} {m[2]}" for m in lista_med_bd]

    def actualizar_pacientes_citas():
        lista_pac_bd.clear()
        lista_pac_bd.extend(obtener_pacientes_combo())
        combo_cita_pac['values'] = [f"{p[1]} {p[2]} - {p[3]}" for p in lista_pac_bd]

    ttk.Label(lf_form_citas, text="Paciente *").grid(row=0, column=0, padx=10, pady=8, sticky="e")
    combo_cita_pac = ttk.Combobox(lf_form_citas, postcommand=actualizar_pacientes_citas, values=nombres_pac, state="readonly", width=40)
    combo_cita_pac.grid(row=0, column=1, padx=10, pady=8, sticky="w")

    def actualizar_medicos_citas():
        lista_med_bd.clear()
        lista_med_bd.extend(cargar_medicos())
        combo_cita_med['values'] = [f"{m[1]} {m[2]}" for m in lista_med_bd]

    ttk.Label(lf_form_citas, text="Médico *").grid(row=1, column=0, padx=10, pady=(8, 0), sticky="e")
    combo_cita_med = ttk.Combobox(lf_form_citas, postcommand=actualizar_medicos_citas, values=nombres_med, state="readonly", width=40)
    combo_cita_med.grid(row=1, column=1, padx=10, pady=(8, 0), sticky="w")

    # Tarjeta Informativa
    frame_info_medico = tk.Frame(lf_form_citas, bg="#F0F4F8", highlightbackground="#B0C4DE", highlightthickness=1)
    frame_info_medico.grid(row=2, column=1, padx=10, pady=(4, 10), sticky="w")

    lbl_icono_esp = tk.Label(frame_info_medico, text="⚕️ Especialidad:", bg="#F0F4F8", fg="#2B579A", font=("Arial", 9, "bold"))
    lbl_icono_esp.grid(row=0, column=0, padx=(8, 2), pady=(4, 2), sticky="w")
    lbl_especialidades = tk.Label(frame_info_medico, text="(Seleccione un médico)", bg="#F0F4F8", fg="#666666", font=("Arial", 9, "italic"))
    lbl_especialidades.grid(row=0, column=1, padx=(0, 8), pady=(4, 2), sticky="w")

    lbl_icono_hor = tk.Label(frame_info_medico, text="⏰ Horario:", bg="#F0F4F8", fg="#2B579A", font=("Arial", 9, "bold"))
    lbl_icono_hor.grid(row=1, column=0, padx=(8, 2), pady=(0, 4), sticky="w")
    lbl_horarios = tk.Label(frame_info_medico, text="(Seleccione un médico)", bg="#F0F4F8", fg="#666666", font=("Arial", 9, "italic"))
    lbl_horarios.grid(row=1, column=1, padx=(0, 8), pady=(0, 4), sticky="w")
    
    def mostrar_info_medico(event):
        med_sel = combo_cita_med.get()
        if not med_sel:
            lbl_especialidades.config(text="(Seleccione un médico)", fg="#666666", font=("Arial", 9, "italic"))
            lbl_horarios.config(text="(Seleccione un médico)", fg="#666666", font=("Arial", 9, "italic"))
            frame_info_medico.config(bg="#F0F4F8", highlightbackground="#B0C4DE")
            lbl_icono_esp.config(bg="#F0F4F8")
            lbl_especialidades.config(bg="#F0F4F8")
            lbl_icono_hor.config(bg="#F0F4F8")
            lbl_horarios.config(bg="#F0F4F8")
            return
        
        id_medico = None
        for m in lista_med_bd:
            if f"{m[1]} {m[2]}" == med_sel:
                id_medico = m[0]
                break
        
        if id_medico:
            especialidades = obtener_especialidades_medico(id_medico)
            texto_esp = " • ".join(especialidades) if especialidades else "Medicina General"
            texto_horario = obtener_horarios_medico_texto(id_medico)
            
            lbl_especialidades.config(text=texto_esp, fg="#004A99", font=("Arial", 9, "bold"))
            lbl_horarios.config(text=texto_horario, fg="#004A99", font=("Arial", 9, "bold"))
            frame_info_medico.config(bg="#E8F0FE", highlightbackground="#8DB6CD")
            lbl_icono_esp.config(bg="#E8F0FE")
            lbl_especialidades.config(bg="#E8F0FE")
            lbl_icono_hor.config(bg="#E8F0FE")
            lbl_horarios.config(bg="#E8F0FE")

    combo_cita_med.bind("<<ComboboxSelected>>", mostrar_info_medico)

    ttk.Label(lf_form_citas, text="Seleccionar Fecha *").grid(row=3, column=0, padx=10, pady=8, sticky="e")
    frame_cal_cita = ttk.Frame(lf_form_citas)
    frame_cal_cita.grid(row=3, column=1, padx=10, pady=8, sticky="w")
    ent_fecha = ttk.Entry(frame_cal_cita, width=35, state="readonly")
    ent_fecha.pack(side="left", padx=(0, 5))
    btn_cal_cita = ttk.Button(frame_cal_cita, text="📅", width=4, command=lambda: abrir_calendario_seguro(ent_fecha))
    btn_cal_cita.pack(side="left")
    
    ttk.Label(lf_form_citas, text="Hora (HH:MM) *").grid(row=4, column=0, padx=10, pady=8, sticky="e")
    ent_cita_hora = ttk.Entry(lf_form_citas, width=43)
    ent_cita_hora.grid(row=4, column=1, padx=10, pady=8, sticky="w")

    ttk.Label(lf_form_citas, text="Motivo de consulta *").grid(row=5, column=0, padx=10, pady=8, sticky="e")
    ent_cita_motivo = ttk.Entry(lf_form_citas, width=43)
    ent_cita_motivo.grid(row=5, column=1, padx=10, pady=8, sticky="w")

    def ejecutar_agendar_seguro():
        pacientes_frescos = obtener_pacientes_combo()
        medicos_frescos = cargar_medicos() 
        agendar_cita(combo_cita_pac, combo_cita_med, ent_fecha, ent_cita_hora, ent_cita_motivo, pacientes_frescos, medicos_frescos)

    btn_agendar = ttk.Button(lf_form_citas, text="📅 Agendar Cita", style="Accent.TButton", command=ejecutar_agendar_seguro)
    btn_agendar.grid(row=6, column=0, columnspan=2, pady=30)


    # --- PANEL DERECHO (ARRIBA): MODIFICAR CITA ---
    lf_modificar_citas = ttk.LabelFrame(frame_citas, text=" 🔄 Reprogramar Cita Existente ", padding=(20, 15))
    # Puesto en la columna 1, fila 0
    lf_modificar_citas.grid(row=0, column=1, padx=(10, 20), pady=(15, 5), sticky="nsew")

    def actualizar_combo_modificar_citas():
        global_citas_programadas_bd = obtener_citas_programadas()
        citas_formateadas = [f"ID: {c[0]} | {c[1]} - {c[2]} | Paciente: {c[3]} {c[4]}" for c in global_citas_programadas_bd]
        combo_mod_cita['values'] = citas_formateadas

    ttk.Label(lf_modificar_citas, text="Seleccionar Cita:").grid(row=0, column=0, padx=10, pady=8, sticky="e")
    combo_mod_cita = ttk.Combobox(lf_modificar_citas, state="readonly", postcommand=actualizar_combo_modificar_citas, width=45)
    combo_mod_cita.grid(row=0, column=1, padx=10, pady=8, sticky="w")

    ttk.Label(lf_modificar_citas, text="Nueva Fecha:").grid(row=1, column=0, padx=10, pady=8, sticky="e")
    frame_cal_mod = ttk.Frame(lf_modificar_citas)
    frame_cal_mod.grid(row=1, column=1, padx=10, pady=8, sticky="w")
    ent_mod_fecha = ttk.Entry(frame_cal_mod, width=38, state="readonly")
    ent_mod_fecha.pack(side="left", padx=(0, 5))
    ttk.Button(frame_cal_mod, text="📅", width=4, command=lambda: abrir_calendario_seguro(ent_mod_fecha)).pack(side="left")

    ttk.Label(lf_modificar_citas, text="Nueva Hora (HH:MM):").grid(row=2, column=0, padx=10, pady=8, sticky="e")
    ent_mod_hora = ttk.Entry(lf_modificar_citas, width=45)
    ent_mod_hora.grid(row=2, column=1, padx=10, pady=8, sticky="w")

    def ejecutar_modificar_seguro():
        citas_programadas_frescas = obtener_citas_programadas()
        modificar_cita(combo_mod_cita, ent_mod_fecha, ent_mod_hora, citas_programadas_frescas)

    btn_modificar = ttk.Button(lf_modificar_citas, text="🔄 Guardar Nueva Fecha", command=ejecutar_modificar_seguro)
    btn_modificar.grid(row=3, column=0, columnspan=2, pady=10)


    # --- PANEL DERECHO (ABAJO): GESTIONAR ESTADO DE LA CITA ---
    lf_gestionar_citas = ttk.LabelFrame(frame_citas, text=" 🚫 Cancelar o Marcar Inasistencia ", padding=(20, 15))
    lf_gestionar_citas.grid(row=1, column=1, padx=(10, 20), pady=(5, 15), sticky="nsew")

    def ejecutar_cancelar_seguro():
        citas_programadas_frescas = obtener_citas_programadas()
        ejecutar_cancelacion_cita(combo_gest_cita, citas_programadas_frescas)

    def ejecutar_no_asistio_seguro():
        citas_programadas_frescas = obtener_citas_programadas()
        ejecutar_no_asistio_cita(combo_gest_cita, citas_programadas_frescas)

    def actualizar_combo_gestionar_citas():
        global_citas_programadas_bd = obtener_citas_programadas()
        citas_formateadas = [f"ID: {c[0]} | {c[1]} - {c[2]} | Paciente: {c[3]} {c[4]}" for c in global_citas_programadas_bd]
        combo_gest_cita['values'] = citas_formateadas

    ttk.Label(lf_gestionar_citas, text="Seleccionar Cita:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    combo_gest_cita = ttk.Combobox(lf_gestionar_citas, state="readonly", postcommand=actualizar_combo_gestionar_citas, width=45)
    combo_gest_cita.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # Contenedor interno para poner los dos botones alineados
    frame_btns_estado = ttk.Frame(lf_gestionar_citas)
    frame_btns_estado.grid(row=1, column=0, columnspan=2, pady=10)
    btn_cancelar = ttk.Button(frame_btns_estado, text="❌ Cancelar Cita", command=ejecutar_cancelar_seguro)
    btn_cancelar.pack(side="left", padx=10)
    btn_no_asistio = ttk.Button(frame_btns_estado, text="⚠️ Paciente No Asistió", command=ejecutar_no_asistio_seguro)
    btn_no_asistio.pack(side="left", padx=10)


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


# ==========================================================================================================================
# 6. DISEÑO DE HISTORIAL CLÍNICO
# ==========================================================================================================================
    frame_historial.columnconfigure(0, weight=1)

    # --- CONTENEDOR 1: BUSCADOR ---
    lf_buscador_historial = ttk.LabelFrame(frame_historial, text=" 🔍 Buscar Historial de Paciente ", padding=(20, 15))
    lf_buscador_historial.grid(row=0, column=0, padx=20, pady=15, sticky="nsew")

    lista_pac_historial_bd = obtener_pacientes_combo()
    nombres_pac_historial = [f"{p[1]} {p[2]} - {p[3]}" for p in lista_pac_historial_bd]

    def actualizar_combo_historial_pac():
        lista_pac_historial_bd.clear()
        lista_pac_historial_bd.extend(obtener_pacientes_combo())
        combo_historial_pac['values'] = [f"{p[1]} {p[2]} - {p[3]}" for p in lista_pac_historial_bd]

    ttk.Label(lf_buscador_historial, text="Seleccionar Paciente *").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    combo_historial_pac = ttk.Combobox(lf_buscador_historial, state="readonly", postcommand=actualizar_combo_historial_pac, values=nombres_pac_historial, width=50)
    combo_historial_pac.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # RECTIFICACIÓN: Función segura para garantizar datos frescos al buscar
    def ejecutar_buscar_historial_seguro():
        pacientes_frescos = obtener_pacientes_combo()
        obtener_historial_paciente(combo_historial_pac, tree_historial, pacientes_frescos)

    btn_buscar_historial = ttk.Button(lf_buscador_historial, text="🔍 Buscar", style="Accent.TButton", command=ejecutar_buscar_historial_seguro)
    btn_buscar_historial.grid(row=0, column=2, padx=10, pady=10)


    # --- CONTENEDOR 2: RESULTADOS Y EXPORTACIÓN ---
    lf_resultados_historial = ttk.LabelFrame(frame_historial, text=" 📄 Registros Clínicos ", padding=(10, 10))
    lf_resultados_historial.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

    columnas_hist = ("Fecha", "Médico Tratante", "Diagnóstico Médico", "Observaciones", "Tratamiento / Medicamento")
    tree_historial = ttk.Treeview(lf_resultados_historial, columns=columnas_hist, show="headings", height=10)

    anchos_hist = [90, 150, 200, 200, 200]
    for col, ancho in zip(columnas_hist, anchos_hist):
        tree_historial.heading(col, text=col)
        tree_historial.column(col, width=ancho, anchor="center")

    tree_historial.pack(fill="both", expand=True, padx=10, pady=10)

    # Botón Exportar PDF (Queda debajo de la tabla)
    btn_exportar_pdf = ttk.Button(lf_resultados_historial, text="📄 Exportar Consulta a PDF", style="Accent.TButton", command=lambda: exportar_pdf(tree_historial, combo_historial_pac))
    btn_exportar_pdf.pack(pady=10)



    ventana.mainloop()
if __name__ == "__main__":
    iniciar_app()
    