import psycopg2

try:
    # ATENCIÓN: Cambiá 'tu_contraseña' por la clave que inventaste al instalar PostgreSQL
    conexion = psycopg2.connect(
        dbname="padel_db",
        user="postgres",
        password="Luciano7#",
        host="localhost",
        port="5432"
    )
    cursor = conexion.cursor()

    # Creamos la tabla 'torneos' con sus columnas específicas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS torneos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            categorias VARCHAR(50) NOT NULL,
            fecha VARCHAR(100) NOT NULL,
            precio VARCHAR(50) NOT NULL
        )
    ''')
    
    conexion.commit() # Confirmamos los cambios
    print("¡Los cimientos están listos! Tabla 'torneos' creada con éxito.")

except Exception as e:
    print(f"Hubo un error al conectar: {e}")

finally:
    if 'conexion' in locals():
        cursor.close()
        conexion.close()
