import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import psycopg2
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="mq4nofbd",
    api_key="742332246719442",
    api_secret="G_tkal-OerfFrlKccxvuYs6Q4Sg"
)

app = Flask(__name__)
app.secret_key = 'padelperez2026'

def obtener_conexion():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL)
    else:
        return psycopg2.connect(dbname="padel_db", user="postgres", password="Luciano7#", host="localhost", port="5432")

@app.route('/')
def inicio():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, categorias, fecha, precio, premios FROM torneos ORDER BY id DESC")
    torneos_guardados = cursor.fetchall()
    cursor.execute("SELECT id, nombre, imagen FROM sponsors ORDER BY id ASC")
    sponsors_guardados = cursor.fetchall()
    conexion.close()
    return render_template('index.html', torneos=torneos_guardados, sponsors=sponsors_guardados)

@app.route('/ligas')
def pagina_ligas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT nombre, apellido, SUM(puntos) as total_puntos, categoria
        FROM (
            SELECT j1_nombre as nombre, j1_apellido as apellido, puntos, rama, categoria FROM equipos_liga
            UNION ALL
            SELECT j2_nombre as nombre, j2_apellido as apellido, puntos, rama, categoria FROM equipos_liga
        ) as jugadores
        WHERE rama = 'Caballeros' AND nombre != ''
        GROUP BY nombre, apellido, categoria
        ORDER BY categoria, total_puntos DESC
    """)
    ranking_caballeros = cursor.fetchall()
    cursor.execute("""
        SELECT nombre, apellido, SUM(puntos) as total_puntos, categoria
        FROM (
            SELECT j1_nombre as nombre, j1_apellido as apellido, puntos, rama, categoria FROM equipos_liga
            UNION ALL
            SELECT j2_nombre as nombre, j2_apellido as apellido, puntos, rama, categoria FROM equipos_liga
        ) as jugadores
        WHERE rama = 'Damas' AND nombre != ''
        GROUP BY nombre, apellido, categoria
        ORDER BY categoria, total_puntos DESC
    """)
    ranking_damas = cursor.fetchall()
    conexion.close()
    return render_template('ligas.html', ranking_cab=ranking_caballeros, ranking_dam=ranking_damas)

@app.route('/tienda')
def pagina_tienda():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, categoria, genero, producto, talle, precio, imagen FROM tienda ORDER BY id DESC")
    tienda_guardada = cursor.fetchall()
    conexion.close()
    return render_template('tienda.html', tienda=tienda_guardada)

@app.route('/reglamento')
def pagina_reglamento():
    return render_template('reglamento.html')

@app.route('/caballeros')
def liga_caballeros():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT categoria, j1_nombre, j1_apellido, j2_nombre, j2_apellido, puntos, pj FROM equipos_liga WHERE rama = 'Caballeros' ORDER BY categoria, puntos DESC")
    equipos_guardados = cursor.fetchall()
    cursor.execute("""
        SELECT p.categoria, p.fase, 
               e1.j1_nombre, e1.j1_apellido, e1.j2_nombre, e1.j2_apellido,
               e2.j1_nombre, e2.j1_apellido, e2.j2_nombre, e2.j2_apellido,
               p.resultado 
        FROM partidos_liga p
        JOIN equipos_liga e1 ON p.equipo1_id = e1.id
        JOIN equipos_liga e2 ON p.equipo2_id = e2.id
        WHERE p.rama = 'Caballeros' ORDER BY p.id DESC
    """)
    partidos_guardados = cursor.fetchall()
    conexion.close()
    return render_template('liga_detalle.html', titulo="Liga Caballeros", equipos=equipos_guardados, partidos=partidos_guardados)

@app.route('/damas')
def liga_damas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT categoria, j1_nombre, j1_apellido, j2_nombre, j2_apellido, puntos, pj FROM equipos_liga WHERE rama = 'Damas' ORDER BY categoria, puntos DESC")
    equipos_guardados = cursor.fetchall()
    cursor.execute("""
        SELECT p.categoria, p.fase, 
               e1.j1_nombre, e1.j1_apellido, e1.j2_nombre, e1.j2_apellido,
               e2.j1_nombre, e2.j1_apellido, e2.j2_nombre, e2.j2_apellido,
               p.resultado 
        FROM partidos_liga p
        JOIN equipos_liga e1 ON p.equipo1_id = e1.id
        JOIN equipos_liga e2 ON p.equipo2_id = e2.id
        WHERE p.rama = 'Damas' ORDER BY p.id DESC
    """)
    partidos_guardados = cursor.fetchall()
    conexion.close()
    return render_template('liga_detalle.html', titulo="Liga Damas", equipos=equipos_guardados, partidos=partidos_guardados)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        if usuario == 'tincho' and clave == 'padel2026':
            session['admin_logueado'] = True
            return redirect(url_for('panel_admin'))
        else:
            error = 'Credenciales incorrectas'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('admin_logueado', None)
    return redirect(url_for('inicio'))

@app.route('/admin', methods=['GET', 'POST'])
def panel_admin():
    if not session.get('admin_logueado'):
        return redirect(url_for('login'))
        
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if request.method == 'POST':
        accion = request.form.get('accion')

        if accion == 'nuevo_torneo':
            cursor.execute("INSERT INTO torneos (nombre, categorias, fecha, precio, premios) VALUES (%s, %s, %s, %s, %s)",
                (request.form.get('nombre', ''), request.form.get('categorias', ''), request.form.get('fecha', ''), request.form.get('precio', ''), request.form.get('premios', '')))
        
        elif accion == 'nuevo_producto':
            categoria = request.form.get('categoria', '')
            genero = request.form.get('genero', '')
            producto = request.form.get('producto', '')
            talle = request.form.get('talle', '')
            precio_prod = request.form.get('precio_prod', '')
            foto = request.files.get('imagen')
            
            url_foto = 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg' # Imagen por defecto
            if foto and foto.filename != '':
                respuesta = cloudinary.uploader.upload(foto)
                url_foto = respuesta.get('secure_url')
                
            cursor.execute("INSERT INTO tienda (categoria, genero, producto, talle, precio, imagen) VALUES (%s, %s, %s, %s, %s, %s)",
                (categoria, genero, producto, talle, precio_prod, url_foto))
        
        elif accion == 'nuevo_equipo':
            cursor.execute("INSERT INTO equipos_liga (rama, categoria, j1_nombre, j1_apellido, j2_nombre, j2_apellido) VALUES (%s, %s, %s, %s, %s, %s)",
                (request.form.get('rama', ''), request.form.get('categoria', ''), request.form.get('j1_nombre', ''), request.form.get('j1_apellido', ''), request.form.get('j2_nombre', ''), request.form.get('j2_apellido', '')))
        
        elif accion == 'nuevo_partido':
            cursor.execute("INSERT INTO partidos_liga (rama, categoria, fase, equipo1_id, equipo2_id) VALUES (%s, %s, %s, %s, %s)",
                (request.form.get('rama', ''), request.form.get('categoria', ''), request.form.get('fase', ''), request.form.get('equipo1', ''), request.form.get('equipo2', '')))

        elif accion == 'nuevo_sponsor':
            nombre = request.form.get('nombre', '')
            foto = request.files.get('imagen')
            
            url_foto = 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg' # Imagen por defecto
            if foto and foto.filename != '':
                respuesta = cloudinary.uploader.upload(foto)
                url_foto = respuesta.get('secure_url')
                
            cursor.execute("INSERT INTO sponsors (nombre, imagen) VALUES (%s, %s)", (nombre, url_foto))

        conexion.commit()
        return redirect(url_for('panel_admin'))

    cursor.execute("SELECT id, nombre, fecha FROM torneos ORDER BY id DESC")
    torneos_guardados = cursor.fetchall()
    cursor.execute("SELECT id, categoria, genero, producto, talle, precio, imagen FROM tienda ORDER BY id DESC")
    tienda_guardada = cursor.fetchall()
    cursor.execute("SELECT id, rama, categoria, j1_nombre, j1_apellido, j2_nombre, j2_apellido, puntos, pj FROM equipos_liga ORDER BY rama, categoria")
    equipos_guardados = cursor.fetchall()
    cursor.execute("SELECT id, nombre, imagen FROM sponsors ORDER BY id ASC")
    sponsors_guardados = cursor.fetchall()
    cursor.execute("""
        SELECT p.id, p.rama, p.categoria, p.fase, 
               e1.j1_apellido, e1.j2_apellido, 
               e2.j1_apellido, e2.j2_apellido, 
               p.resultado 
        FROM partidos_liga p
        JOIN equipos_liga e1 ON p.equipo1_id = e1.id
        JOIN equipos_liga e2 ON p.equipo2_id = e2.id
        ORDER BY p.id DESC
    """)
    partidos_guardados = cursor.fetchall()
    conexion.close()
    return render_template('admin.html', torneos=torneos_guardados, tienda=tienda_guardada, equipos=equipos_guardados, partidos=partidos_guardados, sponsors=sponsors_guardados)

@app.route('/actualizar_resultado', methods=['POST'])
def actualizar_resultado():
    id_partido = request.form.get('id_partido')
    ganador = request.form.get('ganador')
    cant_sets = request.form.get('cant_sets')
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT equipo1_id, equipo2_id, resultado FROM partidos_liga WHERE id = %s", (id_partido,))
    partido = cursor.fetchone()
    if partido and partido[2] == 'Pendiente':
        e1_id = partido[0]
        e2_id = partido[1]
        cursor.execute("UPDATE partidos_liga SET resultado = %s WHERE id = %s", (request.form.get('resultado_texto', ''), id_partido))
        pts_eq1, pts_eq2 = 0, 0
        if ganador == 'equipo1':
            pts_eq1 = 3
            pts_eq2 = 1 if cant_sets == '3' else 0
        elif ganador == 'equipo2':
            pts_eq2 = 3
            pts_eq1 = 1 if cant_sets == '3' else 0
        elif ganador == 'empate':
            pts_eq1 = 1
            pts_eq2 = 1
        cursor.execute("UPDATE equipos_liga SET puntos = puntos + %s, pj = pj + 1 WHERE id = %s", (pts_eq1, e1_id))
        cursor.execute("UPDATE equipos_liga SET puntos = puntos + %s, pj = pj + 1 WHERE id = %s", (pts_eq2, e2_id))
    conexion.commit()
    conexion.close()
    return redirect(url_for('panel_admin'))

@app.route('/generar_semis', methods=['POST'])
def generar_semis():
    rama = request.form.get('rama')
    categoria = request.form.get('categoria')
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM equipos_liga WHERE rama = %s AND categoria = %s ORDER BY puntos DESC LIMIT 4", (rama, categoria))
    top4 = cursor.fetchall()
    if len(top4) >= 4:
        cursor.execute("INSERT INTO partidos_liga (rama, categoria, fase, equipo1_id, equipo2_id) VALUES (%s, %s, 'Semifinal 1', %s, %s)", (rama, categoria, top4[0][0], top4[3][0]))
        cursor.execute("INSERT INTO partidos_liga (rama, categoria, fase, equipo1_id, equipo2_id) VALUES (%s, %s, 'Semifinal 2', %s, %s)", (rama, categoria, top4[1][0], top4[2][0]))
    conexion.commit()
    conexion.close()
    return redirect(url_for('panel_admin'))

@app.route('/eliminar/<int:id_torneo>')
def eliminar_torneo(id_torneo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM torneos WHERE id = %s", (id_torneo,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('panel_admin'))

@app.route('/eliminar_producto/<int:id_producto>')
def eliminar_producto(id_producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM tienda WHERE id = %s", (id_producto,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('panel_admin'))

@app.route('/eliminar_equipo/<int:id_equipo>')
def eliminar_equipo(id_equipo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM equipos_liga WHERE id = %s", (id_equipo,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('panel_admin'))

@app.route('/eliminar_partido/<int:id_partido>')
def eliminar_partido(id_partido):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM partidos_liga WHERE id = %s", (id_partido,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('panel_admin'))

@app.route('/eliminar_sponsor/<int:id_sponsor>')
def eliminar_sponsor(id_sponsor):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM sponsors WHERE id = %s", (id_sponsor,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('panel_admin'))

def inicializar_base_datos():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS torneos (id SERIAL PRIMARY KEY, nombre VARCHAR(100), categorias VARCHAR(100), fecha VARCHAR(100), precio VARCHAR(100), premios VARCHAR(100))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS rankings (id SERIAL PRIMARY KEY, jugador VARCHAR(100), categoria VARCHAR(50), puntos INTEGER)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS tienda (id SERIAL PRIMARY KEY, categoria VARCHAR(50), genero VARCHAR(50), producto VARCHAR(100), talle VARCHAR(50), precio VARCHAR(50), imagen VARCHAR(255))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS equipos_liga (id SERIAL PRIMARY KEY, rama VARCHAR(50), categoria VARCHAR(50), j1_nombre VARCHAR(50), j1_apellido VARCHAR(50), j2_nombre VARCHAR(50), j2_apellido VARCHAR(50), puntos INTEGER DEFAULT 0, pj INTEGER DEFAULT 0)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS partidos_liga (id SERIAL PRIMARY KEY, rama VARCHAR(50), categoria VARCHAR(50), fase VARCHAR(50), equipo1_id INTEGER REFERENCES equipos_liga(id) ON DELETE CASCADE, equipo2_id INTEGER REFERENCES equipos_liga(id) ON DELETE CASCADE, resultado VARCHAR(100) DEFAULT 'Pendiente')''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS sponsors (id SERIAL PRIMARY KEY, nombre VARCHAR(100), imagen VARCHAR(255))''')
        conexion.commit()
        conexion.close()
    except Exception as e:
        print("Aviso de conexión a base de datos:", e)

inicializar_base_datos()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)