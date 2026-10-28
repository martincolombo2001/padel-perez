import psycopg2

conexion = psycopg2.connect(
    dbname="padel_db",
    user="postgres",
    password="Luciano7#", # <-- Tu clave acá
    host="localhost",
    port="5432"
)
cursor = conexion.cursor()

# Agregamos la nueva columna para los premios
cursor.execute("ALTER TABLE torneos ADD COLUMN premios VARCHAR(200) DEFAULT 'A confirmar';")

conexion.commit()
conexion.close()
print("¡Columna 'premios' agregada con éxito a la base de datos!")