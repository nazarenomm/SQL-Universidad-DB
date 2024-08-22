CREATE DATABASE Universidad;

USE Universidad;

CREATE TABLE Profesor (
	profesor_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    apellido VARCHAR(50) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    documento INT NOT NULL #podria ser clave semantica
);

CREATE TABLE Ayudante (
	ayudante_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    apellido VARCHAR(50) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    documento INT NOT NULL #podria ser clave semantica
);


CREATE TABLE Carrera (
    carrera_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_carrera VARCHAR(50) NOT NULL
);


CREATE TABLE Materia (
    materia_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    carrera_id INT NOT NULL,
    nombre_materia VARCHAR(50) NOT NULL,
    FOREIGN KEY (carrera_id) REFERENCES Carrera(carrera_id)
);



CREATE TABLE Curso (
	curso_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    materia_id INT NOT NULL,
    profesor_id INT NOT NULL,
    ayudante_id INT NOT NULL, 
    año INT NOT NULL,
    numero_cuatrimestre TINYINT NOT NULL,
    FOREIGN KEY (profesor_id) REFERENCES Profesor(profesor_id),
    FOREIGN KEY (ayudante_id) REFERENCES Ayudante(ayudante_id),
    FOREIGN KEY (materia_id) REFERENCES Materia(materia_id)
);


CREATE TABLE Sede (
    sede_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_sede VARCHAR(50) NOT NULL
);



CREATE TABLE Alumno (
    alumno_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    sede_id INT NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    documento INT NOT NULL,
    FOREIGN KEY (sede_id) REFERENCES Sede(sede_id)
);



CREATE TABLE Matriculaciones (
    matriculacion_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    curso_id INT NOT NULL,
    nota_final INT,
    FOREIGN KEY (alumno_id) references Alumno(alumno_id),
    FOREIGN KEY (curso_id) references Curso(curso_id)
);




CREATE TABLE Tipo_evaluacion (
tipo_evaluacion_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
tipo_evaluacion VARCHAR(50) NOT NULL
);


CREATE TABLE Evaluacion (
evaluacion_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
matriculacion_id INT NOT NULL,
tipo_evaluacion_id INT NOT NULL,
nota int,
FOREIGN KEY (matriculacion_id) REFERENCES Matriculaciones(matriculacion_id),
FOREIGN KEY (tipo_evaluacion_id) REFERENCES Tipo_evaluacion(tipo_evaluacion_id)
);

