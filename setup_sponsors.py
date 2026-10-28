import psycopg2

conexion = psycopg2.connect(dbname="padel_db", user="postgres", password="Luciano7#", host="localhost", port="5432")
cursor = conexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sponsors (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100),
        imagen VARCHAR(255)
    )
''')

conexion.commit()
conexion.close()
print("¡Tabla de sponsors creada con éxito!")