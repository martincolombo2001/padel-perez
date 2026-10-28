import psycopg2

conexion = psycopg2.connect(dbname="padel_db", user="postgres", password="Luciano7#", host="localhost", port="5432")
cursor = conexion.cursor()

# Borramos las tablas de prueba viejas
cursor.execute("DROP TABLE IF EXISTS partidos_liga CASCADE")
cursor.execute("DROP TABLE IF EXISTS equipos_liga CASCADE")

# Creamos la tabla de equipos con los jugadores individualizados
cursor.execute('''
    CREATE TABLE equipos_liga (
        id SERIAL PRIMARY KEY,
        rama VARCHAR(50),
        categoria VARCHAR(50),
        j1_nombre VARCHAR(50),
        j1_apellido VARCHAR(50),
        j2_nombre VARCHAR(50),
        j2_apellido VARCHAR(50),
        puntos INTEGER DEFAULT 0,
        pj INTEGER DEFAULT 0
    )
''')

# Creamos la tabla de partidos vinculada inteligentemente a los equipos
cursor.execute('''
    CREATE TABLE partidos_liga (
        id SERIAL PRIMARY KEY,
        rama VARCHAR(50),
        categoria VARCHAR(50),
        fase VARCHAR(50),
        equipo1_id INTEGER REFERENCES equipos_liga(id) ON DELETE CASCADE,
        equipo2_id INTEGER REFERENCES equipos_liga(id) ON DELETE CASCADE,
        resultado VARCHAR(100) DEFAULT 'Pendiente'
    )
''')

conexion.commit()
conexion.close()
print("¡Motor actualizado! Jugadores individualizados correctamente.")