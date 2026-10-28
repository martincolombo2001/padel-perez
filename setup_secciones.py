import psycopg2

conexion = psycopg2.connect(
    dbname="padel_db",
    user="postgres",
    password="Luciano7#", # <-- TU CLAVE ACÁ
    host="localhost",
    port="5432"
)
cursor = conexion.cursor()

# Tabla para los Rankings
cursor.execute('''
    CREATE TABLE IF NOT EXISTS rankings (
        id SERIAL PRIMARY KEY,
        jugador VARCHAR(100) NOT NULL,
        categoria VARCHAR(50) NOT NULL,
        puntos INTEGER NOT NULL
    )
''')

# Tabla para la Tienda (Kiosco / Accesorios)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tienda (
        id SERIAL PRIMARY KEY,
        producto VARCHAR(100) NOT NULL,
        descripcion VARCHAR(200),
        precio VARCHAR(50) NOT NULL
    )
''')

conexion.commit()
conexion.close()
print("¡Nuevas estructuras listas! Tablas 'rankings' y 'tienda' creadas en la base de datos.")