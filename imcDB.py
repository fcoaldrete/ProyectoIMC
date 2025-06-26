import sqlite3

DB_NAME = "imc.db"

def crear_tabla():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personas_imc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            estatura REAL NOT NULL,
            peso REAL NOT NULL,
            imc REAL NOT NULL,
            clasificacion TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

def insertar(datos: dict) -> int:
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    sql = '''
        INSERT INTO personas_imc (nombre, edad, estatura, peso, imc, clasificacion)
        VALUES (:nombre, :edad, :estatura, :peso, :imc, :clasificacion)
    '''
    cursor.execute(sql, datos)
    conexion.commit()
    filas = cursor.rowcount
    conexion.close()
    return filas

def consultar() -> list:
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, edad, estatura, peso, imc, clasificacion FROM personas_imc")
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

# Crear la tabla al cargar el módulo
crear_tabla()
