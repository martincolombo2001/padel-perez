import psycopg2

conexion = psycopg2.connect(
    dbname="padel_db",
    user="postgres",
    password="Luciano7#", # <-- TU CLAVE ACÁ
    host="localhost",
    port="5432"
)
cursor = conexion.cursor()

# 1. Tabla para los Equipos (Las Parejas)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS equipos_liga (
        id SERIAL PRIMARY KEY,
        rama VARCHAR(50),      -- Para saber si es 'Caballeros' o 'Damas'
        categoria VARCHAR(50), -- Para separar '5ta', '6ta' o '7ma'
        pareja VARCHAR(100),   -- Ej: 'Colombo / Rossi'
        puntos INTEGER DEFAULT 0,
        pj INTEGER DEFAULT 0   -- Partidos Jugados
    )
''')

# 2. Tabla para los Partidos (Fixture y Resultados)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS partidos_liga (
        id SERIAL PRIMARY KEY,
        rama VARCHAR(50),
        categoria VARCHAR(50),
        fase VARCHAR(50),      -- Ej: 'Fecha 1', 'Fecha 2', 'Semifinal'
        equipo1 VARCHAR(100),
        equipo2 VARCHAR(100),
        resultado VARCHAR(100) DEFAULT 'Pendiente' -- Se actualiza cuando juegan
    )
''')

conexion.commit()
conexion.close()
print("¡Motor de Ligas instalado! Tablas 'equipos_liga' y 'partidos_liga' listas.")