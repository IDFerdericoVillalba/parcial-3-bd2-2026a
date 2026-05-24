import tkinter as tk
from tkinter import ttk, messagebox
from conexiones import conectar_bd
from consultas import cargar_pacientes, guardar_paciente, cargar_especialidades, guardar_medico


################################################################
################################################################


def inicar_app():

    #ventana principal
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión - Consulta Médico")
    ventana.geometry("900x700")

    #controlador de pestañas
    notebook = ttk.Notebook(ventana)
    notebook.pack(expand=True, fill='both', padx=10, pady=10)

    #frames para cada pestaña
    frame_pacientes = ttk.Frame(notebook)
    frame_medicos = ttk.Frame(notebook)
    frame_citas = ttk.Frame(notebook)

    #agrager frames al notebook
    notebook.add(frame_pacientes, text="👨‍⚕️ Gestion de Pacientes")
    notebook.add(frame_medicos, text="⚕️ Gestion de Médicos")
    notebook.add(frame_citas, text="📅 Gestion de Citas")

    #pestaña para agregar pacientes
    tk.Label(frame_pacientes, text="Registro de nuevo paciente", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
    entradas = {}
    campos = [
        ("Nombre *", "nombre"),
        ("Apellido *", "apellido"),
        ("Documento *", "documento"),
        ("Fecha de Nacimiento (YYYY-MM-DD) *", "fecha_nacimiento"),
        ("Teléfono *", "telefono"),
        ("Correo", "correo"),
        ("Dirección", "direccion")
    ]
    for i, (texto_label, nombre_variable) in enumerate(campos, start=1):    
        tk.Label(frame_pacientes, text=texto_label).grid(row=i, column=0, sticky="e", padx=10, pady=5)
        caja_texto = tk.Entry(frame_pacientes, width=40)
        caja_texto.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        entradas[nombre_variable] = caja_texto

    columnas = ("id_paciente", "nombre", "apellido", "documento", "telefono")
    tree_pacientes = ttk.Treeview(frame_pacientes, columns=columnas, show="headings", height=8)

    for col in columnas:
        tree_pacientes.heading(col, text=col)
        tree_pacientes.column(col, width=120, anchor="center")

    tree_pacientes.grid(row=len(campos)+2, column=0, columnspan=2, padx=20, pady=20)

    btn_guardar = tk.Button(frame_pacientes, text="💾 Guardar Paciente", command=lambda: guardar_paciente(entradas, tree_pacientes))
    btn_guardar.grid(row=len(campos)+1, column=0, columnspan=2, pady=20)

    cargar_pacientes(tree_pacientes)

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

    ventana.mainloop()

if __name__ == "__main__":
    inicar_app()
    