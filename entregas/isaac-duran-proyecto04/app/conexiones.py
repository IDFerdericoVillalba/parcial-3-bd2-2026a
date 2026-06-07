import mysql.connector
from mysql.connector import Error

def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="TU HOST",  #tu servidor
            user="TU USUARIO", #tu usario 
            passwd="TU CONTRASEÑA", #tu contraseña
            database="TU BASE DE DATOS" #tu base de datos
        )

        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion
        
    except Error as e:
        print(f"Error al conectar a MySQL {e}")
        return None


#solo para probar si funcioma la conexion con la base de datos
if __name__ == "__main__":
    conexion_prueba = conectar_bd()
    if conexion_prueba:
        conexion_prueba.close()
        print("Conexión cerrada")