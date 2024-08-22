DELIMITER //

DROP FUNCTION IF EXISTS promedio_alumno_curso //

CREATE FUNCTION promedio_alumno_curso(alumno_id_ INT, curso_id_ INT)
    RETURNS DECIMAL(10, 2)
    DETERMINISTIC
BEGIN
    DECLARE nota_promedio DECIMAL(10, 2);

    SELECT AVG(e.nota) INTO nota_promedio
    FROM Evaluacion e
    JOIN Matriculaciones m ON e.matriculacion_id = m.matriculacion_id
    WHERE m.alumno_id = alumno_id_
      AND m.curso_id = curso_id_;

    RETURN nota_promedio;
END //

DELIMITER ;


DELIMITER //

DROP PROCEDURE IF EXISTS actualizar_nota_final_alumno_curso //

CREATE PROCEDURE actualizar_nota_final_alumno_curso(IN curso_id_ INT, IN alumno_id_ INT)
BEGIN
    DECLARE promedio DECIMAL(10, 2);

    -- Calcular el promedio del alumno en el curso usando la función
    SET promedio = promedio_alumno_curso(alumno_id_, curso_id_);

    -- Actualizar la nota final del alumno en la tabla Matriculaciones
    UPDATE Matriculaciones
    SET nota_final = promedio
    WHERE curso_id = curso_id_ AND alumno_id = alumno_id_;
END //

DELIMITER ;


DELIMITER //

DROP TRIGGER IF EXISTS after_evaluacion_insert //

CREATE TRIGGER after_evaluacion_insert
AFTER INSERT ON Evaluacion
FOR EACH ROW
BEGIN
    DECLARE curso_id_ INT;
    DECLARE alumno_id_ INT;

    -- Obtener el curso_id y alumno_id del matriculacion_id
    SELECT m.curso_id, m.alumno_id INTO curso_id_, alumno_id_
    FROM Matriculaciones m
    WHERE m.matriculacion_id = NEW.matriculacion_id;

    -- Llamar al stored procedure para actualizar la nota final del alumno en el curso
    CALL actualizar_nota_final_alumno_curso(curso_id_, alumno_id_);
END //

DELIMITER ;

