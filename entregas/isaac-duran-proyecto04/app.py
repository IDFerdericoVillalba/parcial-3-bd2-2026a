import tkinter as tk
from tkinter import ttk, messagebox
from conexiones import conectar_bd

def guaradar_paciente(entradas):
    nombre = entradas['nombre'].get()
    apelido = entradas['apellido'].get()
    docuemnto = entradas['documento'].get()
    fecha_nacimiento = entradas['fecha_nacimiento'].get()
    telefono = entradas['telefono'].get()
    correo = entradas['correo'].get()
    direccion = entradas['direccion'].get()


    #validar que todos los campos de paciente no esten vacios
    if not (nombre and apelido and docuemnto and fecha_nacimiento and telefono and correo and direccion):
        tk.messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    
    conecxion = conectar_bd()
    if conecxion:
        try:
            cursor = conecxion.cursor()
            sql = """INSERT INTO pacientes (nombre, apellido, documento, fecha_nacimiento, telefono, correo, direccion) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            valores = (nombre, apelido, docuemnto, fecha_nacimiento, telefono, correo, direccion)

            cursor.execute(sql, valores)
            conecxion.commit()

            messagebox.showinfo("Éxito", f"Paciente {nombre} guardado correctamente")

            for key in entradas:
                entradas[key].delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el paciente: {e}")
        finally:
            conecxion.close()
    else:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")


################################################################


def inicar_app():

    #ventana principal
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión - Consulta Médico")
    ventana.geometry("800x400")

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

    #Formulario para agregar pacientes
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
    btn_guardar = tk.Button(frame_pacientes, text="💾 Guardar Paciente", command=lambda: guaradar_paciente(entradas))
    btn_guardar.grid(row=len(campos)+1, column=0, columnspan=2, pady=20)


    ventana.mainloop()

if __name__ == "__main__":
    inicar_app()
    