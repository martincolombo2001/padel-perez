import psycopg2

conexion = psycopg2.connect(dbname="padel_db", user="postgres", password="Luciano7#", host="localhost", port="5432")
cursor = conexion.cursor()

# Borramos la tabla vieja de tienda
cursor.execute("DROP TABLE IF EXISTS tienda")

# Creamos la nueva súper tabla con foto, categoría y talle
cursor.execute('''
    CREATE TABLE tienda (
        id SERIAL PRIMARY KEY,
        categoria VARCHAR(50),  -- 'Padel' o 'Indumentaria'
        genero VARCHAR(50),     -- 'Caballeros', 'Damas' o 'Unisex'
        producto VARCHAR(100),
        talle VARCHAR(50),
        precio VARCHAR(50),
        imagen VARCHAR(255)     -- Acá guardamos el nombre de la foto
    )
''')

conexion.commit()
conexion.close()
print("¡Base de datos de la Tienda actualizada con éxito para subir fotos y talles!")