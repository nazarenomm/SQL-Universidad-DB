import pandas as pd
import random
import faker
import mysql.connector

# Creamos una instancia de Faker
fake = faker.Faker("es_AR")

# Datos de conexión a la base de datos
host = ""
user = "grupo1"
password = "" # Hay contraseña pero no la mostramos
database = "Universidad"
port = 3306

# Conectar a MySQL
try:
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )
    cursor = conn.cursor()
    print("Conexión exitosa a la base de datos.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)
    
    
#%%
# Funciones para generar datos aleatorios
def generar_profesores(n):
    datos = []
    for _ in range(n):
        datos.append([fake.last_name(), fake.first_name(), fake.random_int(min=10000000, max=39999999)])
    return pd.DataFrame(datos, columns=['apellido', 'nombre', 'documento'])

def generar_ayudantes(n):
    datos = []
    for _ in range(n):
        datos.append([fake.last_name(), fake.first_name(), fake.random_int(min=35000000, max=50999999)])
    return pd.DataFrame(datos, columns=['apellido', 'nombre', 'documento'])

def generar_sedes():
    sedes = ['Economia y Negocios', 'Ciencia y Tecnología', 'Arte', 'Politica', 'Sociales']
    datos = {'nombre_sede': sedes}
    return pd.DataFrame(datos)

def generar_alumnos(n, sedes, carrera_por_sede):
    datos = []
    for _ in range(n):
        sede = random.choice(sedes)
        carreras = carrera_por_sede[sede]
        carrera = random.choice(carreras)
        datos.append([sede, fake.last_name(), fake.first_name(), fake.random_int(min=10000000, max=50999999), carrera])
    return pd.DataFrame(datos, columns=['sede_id', 'apellido', 'nombre', 'documento', 'carrera']) # deberia ser carrera id

# Diccionario de carreras y materias con nuevas carreras asignadas a sedes específicas
dicc_carreras_materias = {
    "Economia y Negocios": {
        "Lic. en Administración": ["Contabilidad", "Economía", "Finanzas", "Marketing"],
        "Lic. en Economía": ["Microeconomía", "Macroeconomía", "Econometría", "Historia Económica"],
        "Lic. en Comercio Internacional": ["Logística", "Negocios Internacionales", "Economía Internacional", "Marketing Internacional"]
    },
    "Ciencia y Tecnología": {
        "Lic. Ciencia de Datos": ["Programación 1", "Análisis 1", "Probabilidad y Estadística", "Algoritmos 1"],
        "Lic. en Matemáticas": ["Análisis 1", "Álgebra Lineal", "Geometría Analítica"],
        "Ing. en Sistemas": ["Programación 1", "Bases de Datos", "Redes"],
        "Ing. en Electrónica": ["Circuitos Eléctricos", "Electrónica Digital", "Telecomunicaciones", "Microcontroladores"],
        "Lic. en Biotecnología": ["Biología Molecular", "Genética", "Microbiología", "Bioinformática"]
    },
    "Arte": {
        "Lic. en Artes Visuales": ["Dibujo", "Pintura", "Escultura", "Historia del Arte"],
        "Lic. en Música": ["Teoría Musical", "Composición", "Instrumento", "Historia de la Música"],
        "Lic. en Teatro": ["Actuación", "Dirección Teatral", "Historia del Teatro", "Escenografía"]
    },
    "Politica": {
        "Lic. en Ciencias Políticas": ["Teoría Política", "Relaciones Internacionales", "Política Comparada", "Sistemas Políticos"],
        "Lic. en Relaciones Internacionales": ["Derecho Internacional", "Economía Política Internacional", "Organizaciones Internacionales", "Política Exterior"],
        "Lic. en Estudios Globales": ["Globalización", "Economía Global", "Cultura Global", "Derechos Humanos"]
    },
    "Sociales": {
        "Lic. en Sociología": ["Teoría Sociológica", "Métodos de Investigación", "Estructura Social", "Sociología Urbana"],
        "Lic. en Psicología": ["Psicología General", "Psicopatología", "Psicología Social", "Neurociencia"],
        "Lic. en Trabajo Social": ["Intervención Social", "Políticas Públicas", "Desarrollo Comunitario", "Derechos Humanos"]
    }
}

# Generar datos para cada tabla
df_profesores = generar_profesores(100)
df_ayudantes = generar_ayudantes(100)
df_sedes = generar_sedes()
#print(f"sedes\n : {df_sedes}")

#%%

# Insertar datos en las tablas correspondientes
def insertar_datos(tabla, df):
    cols = ", ".join([str(i) for i in df.columns.tolist()])
    placeholders = ", ".join(["%s"] * len(df.columns))
    sql = f"INSERT INTO {tabla} ({cols}) VALUES ({placeholders})"
    for _, row in df.iterrows():
        cursor.execute(sql, tuple(row))

insertar_datos('Profesor', df_profesores)
insertar_datos('Ayudante', df_ayudantes)
insertar_datos('Sede', df_sedes)

#%%

# Obtener los IDs generados
cursor.execute("SELECT sede_id FROM Sede")
sede_ids = [row[0] for row in cursor.fetchall()]

# Asignar carreras a cada sede asegurando que todas las sedes tengan al menos una carrera
carrera_por_sede = {sede: [] for sede in sede_ids}
for sede, carreras in zip(sede_ids, dicc_carreras_materias.keys()):
    carrera_por_sede[sede].extend(list(dicc_carreras_materias[carreras].keys()))

# Generar alumnos y asignar una carrera basada en la sede
df_alumnos = generar_alumnos(1000, sede_ids, carrera_por_sede)
#print(f"alumnos : {df_alumnos}")

# Insertar alumnos
insertar_datos('Alumno', df_alumnos[['sede_id', 'apellido', 'nombre', 'documento']])

# Obtener IDs generados para alumnos
cursor.execute("SELECT alumno_id FROM Alumno")
alumno_ids = [row[0] for row in cursor.fetchall()]

#%%

# Insertar carreras
carreras_data = []
for carreras in dicc_carreras_materias.values():
    for carrera in carreras:
        carreras_data.append([carrera])
df_carreras = pd.DataFrame(carreras_data, columns=['nombre_carrera'])
insertar_datos('Carrera', df_carreras)

# Obtener IDs generados para carreras
cursor.execute("SELECT carrera_id, nombre_carrera FROM Carrera")
carrera_id_map = {row[1]: row[0] for row in cursor.fetchall()}

# Insertar materias
materias_data = []
for carreras in dicc_carreras_materias.values():
    for carrera, materias in carreras.items():
        carrera_id = carrera_id_map[carrera]
        for materia in materias:
            materias_data.append([carrera_id, materia])
df_materias = pd.DataFrame(materias_data, columns=['carrera_id', 'nombre_materia'])
insertar_datos('Materia', df_materias)

# Obtener IDs generados para materias
cursor.execute("SELECT materia_id, nombre_materia FROM Materia")
materia_id_map = {row[1]: row[0] for row in cursor.fetchall()}
#print(f"map:\n{materia_id_map}")

# Obtener IDs generados para profesores y ayudantes
cursor.execute("SELECT profesor_id FROM Profesor")
profesor_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT ayudante_id FROM Ayudante")
ayudante_ids = [row[0] for row in cursor.fetchall()]

#%%

# Generar y asignar cursos asegurando IDs válidos
df_cursos = pd.DataFrame([(materia_id_map[materia], random.choice(profesor_ids), random.choice(ayudante_ids), random.choice([2022, 2023, 2024]), random.choice([1, 2])) for materia in materia_id_map], columns=['materia_id', 'profesor_id', 'ayudante_id', 'año', 'numero_cuatrimestre'])
insertar_datos('Curso', df_cursos)

# Obtener IDs generados para cursos
cursor.execute("SELECT curso_id, materia_id FROM Curso")
cursos = cursor.fetchall()
curso_ids = [row[0] for row in cursos]
materia_ids = [row[1] for row in cursos]

# Generar y asignar matriculaciones
matriculaciones_data = []
for i, alumno_id in enumerate(alumno_ids):
    carrera = df_alumnos.iloc[i]['carrera']
    sede_id = df_alumnos.iloc[i]['sede_id']
    sede = df_sedes.iloc[sede_id - 1]["nombre_sede"]
    carrera_id = carrera_id_map[carrera]
    materias = [materia_id_map[materia] for materia in dicc_carreras_materias[sede][carrera]]
    for materia_id in materias:
        curso_id = random.choice([curso_id for curso_id, materia in cursos if materia == materia_id])
        matriculaciones_data.append([alumno_id, curso_id, random.randint(1, 10)])
df_matriculaciones = pd.DataFrame(matriculaciones_data, columns=['alumno_id', 'curso_id', 'nota_final'])
insertar_datos('Matriculaciones', df_matriculaciones)

#%%

# Insertar tipos de evaluación
tipos_evaluacion = ["Parcial", "TP", "Laboratorio"]
df_tipos_evaluacion = pd.DataFrame(tipos_evaluacion, columns=['tipo_evaluacion'])
insertar_datos('Tipo_evaluacion', df_tipos_evaluacion)

# Obtener IDs generados para tipos de evaluación
cursor.execute("SELECT tipo_evaluacion_id, tipo_evaluacion FROM Tipo_evaluacion")
tipo_evaluacion_map = {row[1]: row[0] for row in cursor.fetchall()}

#%%
# Insertar evaluaciones
evaluaciones_data = []
for curso in df_matriculaciones['curso_id'].unique():
    alumnos_curso = df_matriculaciones[df_matriculaciones['curso_id'] == curso]
    for _ in range(5):
        tipo_evaluacion_id = tipo_evaluacion_map[random.choice(tipos_evaluacion)]
        for idx, alumno in alumnos_curso.iterrows():
            nota = fake.random_int(min=1, max=10)
            evaluaciones_data.append([idx+1, tipo_evaluacion_id, nota])
df_evaluaciones = pd.DataFrame(evaluaciones_data, columns=['matriculacion_id', 'tipo_evaluacion_id', 'nota'])
insertar_datos('Evaluacion', df_evaluaciones)

#%%
# Confirmar cambios y cerrar conexión
conn.commit()
cursor.close()
conn.close()
