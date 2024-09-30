/* Lily Kendall
   Exam 1
   9/30/24
*/



-- Question 1

SELECT DISTINCT name, course_id, title
FROM (takes NATURAL JOIN course) NATURAL JOIN (SELECT ID, name FROM student) as S
WHERE lower(dept_name) like 'comp%sci%'
ORDER BY name;


-- Question 2

SELECT building, sum(capacity) AS total
FROM classroom
GROUP BY building
HAVING sum(capacity) >= 50
ORDER BY total DESC;

-- Question 3

SELECT course.course_id, course.title, course.dept_name
FROM course
WHERE course_id NOT IN (SELECT course_id FROM prereq)
ORDER BY dept_name, course_id;
