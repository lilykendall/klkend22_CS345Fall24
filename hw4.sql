
DROP TABLE IF EXISTS gpa;
CREATE TABLE gpa (
    grade varchar(2),
    num_grade float
);

INSERT INTO gpa VALUES ('A+', 4.0);
INSERT INTO gpa VALUES ('A ', 3.7);
INSERT INTO gpa VALUES ('A-', 3.4);
INSERT INTO gpa VALUES ('B+', 3.1);
INSERT INTO gpa VALUES ('B ', 2.8);
INSERT INTO gpa VALUES ('B-', 2.5);
INSERT INTO gpa VALUES ('C+', 2.2);
INSERT INTO gpa VALUES ('C ', 1.9);
INSERT INTO gpa VALUES ('C-', 1.6);
INSERT INTO gpa VALUES ('D+', 1.3);
INSERT INTO gpa VALUES ('D ', 1.0);
INSERT INTO gpa VALUES ('F ', 0.0);

CREATE VIEW knutson_grades AS (
    SELECT ID, grade, credits, num_grade
    FROM takes NATURAL JOIN gpa NATURAL JOIN course
    WHERE takes.course_id = course.course_id AND
          ID = (SELECT ID FROM student WHERE name = 'Knutson')
);

SELECT student.ID, student.name, student.dept_name, CAST(SUM(credits * num_grade) / SUM(credits) AS DECIMAL(10, 3)) AS gpa
FROM knutson_grades, student
WHERE knutson_grades.ID = student.ID
GROUP BY student.ID;
