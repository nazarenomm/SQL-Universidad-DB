use Universidad;

#A : Profesor
#B : Curso
#C : Matric

#6. Realizar consultas para la obtención de datos de la siguiente forma:
#a. A partir de un dato contenido en A conseguir uno de C 
#b. A partir de un dato contenido en C conseguir uno de B 
#c. A partir de un dato contenido en C conseguir uno de A 

# Profesores con mas alumnos
SELECT p.apellido, p.nombre, 
	   COUNT(m.alumno_id) AS num_alumnos
FROM Profesor p
LEFT JOIN Curso ON p.profesor_id = Curso.profesor_id
LEFT JOIN Matriculaciones m 
ON Curso.curso_id = m.curso_id
GROUP BY p.profesor_id
ORDER BY num_alumnos DESC;

# Cuatrimestres con mas alumnos
SELECT c.año, c.numero_cuatrimestre, 
	COUNT(m.alumno_id) AS num_alumnos
FROM Curso c
JOIN Matriculaciones m ON c.curso_id = m.curso_id
GROUP BY c.año, c.numero_cuatrimestre
ORDER BY num_alumnos DESC;

# Profesores del alumno de id = 10
SELECT p.nombre, p.apellido 
FROM Matriculaciones m
LEFT JOIN Curso c 
ON m.curso_id = c.curso_id
LEFT JOIN Profesor p 
ON c.profesor_id = p.profesor_id
WHERE m.alumno_id = 10;

#Cantidad de alumnos en cada tipo de evaluacion

SELECT 
    te.tipo_evaluacion,
    COUNT(DISTINCT ma.alumno_id) AS cantidad_alumnos
FROM 
    Evaluacion e
JOIN 
    Matriculaciones ma ON e.matriculacion_id = ma.matriculacion_id
JOIN 
    Tipo_evaluacion te ON e.tipo_evaluacion_id = te.tipo_evaluacion_id
GROUP BY 
    te.tipo_evaluacion
ORDER BY 
    cantidad_alumnos DESC;

#Materia con mayor cantidad de alumnos

SELECT 
    m.nombre_materia,
    COUNT(ma.alumno_id) AS cantidad_alumnos
FROM 
    Matriculaciones ma
JOIN 
    Curso c ON ma.curso_id = c.curso_id
JOIN 
    Materia m ON c.materia_id = m.materia_id
GROUP BY 
    m.materia_id, m.nombre_materia
ORDER BY 
    cantidad_alumnos DESC
LIMIT 1;


#Alumnos por sede

SELECT 
    s.nombre_sede,
    COUNT(a.alumno_id) AS cantidad_alumnos
FROM 
    Sede s
JOIN 
    Alumno a ON s.sede_id = a.sede_id
GROUP BY 
    s.sede_id, s.nombre_sede
ORDER BY 
    cantidad_alumnos DESC;
    
    
#Obtener nombre y apellido del alumno y su sede

SELECT Alumno.nombre, Alumno.apellido, Sede.nombre_sede
FROM Alumno
JOIN Sede ON Alumno.sede_id = Sede.sede_id;



#Insertar codigo a una tabla

-- Insertar un nuevo elemento en la tabla Materia
INSERT INTO Materia (carrera_id, nombre_materia) 
VALUES (1, 'Mecanica de fluidos');


# Function y SP

# Utilizamos la función promedio_alumno_curso() para encontrar los promedios más altos por curso
SELECT a.apellido, a.nombre, c.curso_id, mat.nombre_materia, 
promedio_alumno_curso(a.alumno_id, c.curso_id) AS nota_promedio
FROM Alumno a 
LEFT JOIN Matriculaciones m on a.alumno_id = m.alumno_id
LEFT JOIN Curso c ON m.curso_id = c.curso_id
LEFT JOIN Materia mat ON c.materia_id = mat.materia_id
ORDER BY nota_promedio DESC;

# Trabajamos con el Curso con ID 10
UPDATE Matriculaciones SET nota_final = NULL WHERE curso_id = 10;
SELECT * FROM Matriculaciones WHERE curso_id = 10;

# Un llamado al Stored Procedure nos permite actualizar la nota de todos los estudiantes del curso
CALL actualizar_nota_final_alumno_curso(10, 40);
SELECT * FROM Matriculaciones WHERE curso_id = 10;


# Trigger

# Veamos las notas promedio del alumno con ID 2
SELECT m.matriculacion_id, m.alumno_id, a.apellido, a.nombre, m.nota_final FROM Matriculaciones m 
LEFT JOIN Alumno a ON m.alumno_id = a.alumno_id
WHERE m.alumno_id = 2;

# Agregamos una evaluación y observamos que la nota final se ha actualizado automáticamente
INSERT INTO Evaluacion (matriculacion_id, tipo_evaluacion_id, nota)
VALUES (4, 1, 100);

