/*
 Lily Kendall
Database HW3
Due 9/25/24
 */

 -- Part 1: problems

-- 3.11: Write the following queries in SQL, using the university schema.

-- a: Find the ID and name of each student who has taken at least one Comp.
-- Sci. course; make sure there are no duplicate names in the result.

SELECT DISTINCT student.ID, student.name
FROM student, takes
WHERE student.ID = takes.ID
  AND takes.course_id in (SELECT course_id FROM course WHERE dept_name LIKE 'Comp.%Sci.%');

-- b: Find the ID and name of each student who has not taken any course
-- oﬀered before 2017.

-- in 2017, there are no rows
SELECT student.ID, student.name
FROM student
WHERE student.ID NOT IN (
    SELECT takes.ID
    FROM takes
    WHERE takes.year < 2017);

-- checking 2005
SELECT student.ID, student.name
FROM student
WHERE student.ID NOT IN (
    SELECT takes.ID
    FROM takes
    WHERE takes.year < 2005);


-- c: For each department, find the maximum salary of instructors in that department.
-- You may assume that every department has at least one instructor.

SELECT dept_name, max(salary)
FROM instructor
GROUP BY dept_name;

-- d: Find the lowest, across all departments, of the per-department maximum
-- salary computed by the preceding query.

SELECT min(salary)
FROM (
         SELECT max(salary) AS salary
         FROM instructor
         GROUP BY dept_name
     ) AS max_salaries;


-- 3.12: Write the SQL statements using the university schema to perform the following
-- operations:

-- a: Create a new course “CS-001”, titled “Weekly Seminar”, with 0 credits.

INSERT INTO course
VALUES ('001', 'Weekly Seminar', 'Comp. Sci.', 0);
-- this query produces an error because in the DDL, there is a check that credits is > 0.
-- this is a constraint, so no course is allowed to have 0 or fewer credits.
-- to fix this issue you could change the check to allow 0 credits or get rid of the check or change the number
-- credits the course has (which I will do below).

INSERT INTO course
VALUES ('001', 'Weekly Seminar', 'Comp. Sci.', 3);

-- b: Create a section of this course in Fall 2017, with sec id of 1, and with the
-- location of this section not yet specified.

INSERT INTO section (course_id, sec_id, semester, year)
VALUES ('001','1', 'Fall', 2017);


-- c: Enroll every student in the Comp. Sci. department in the above section.
INSERT INTO takes (id, course_id, sec_id, semester, year)
VALUES (
        (SELECT ID from student where dept_name = 'Comp. Sci.'),
        '001',
        '1',
        'Fall',
        2017
       );

--FOR ID IN (SELECT ID from student where dept_name = 'Comp. Sci.')


-- d: Delete enrollments in the above section where the student’s ID is 12345.

-- e: Delete the course CS-001. What will happen if you run this delete
-- statement without first deleting oﬀerings (sections) of this course?

-- f: Delete all takes tuples corresponding to any section of any course with
-- the word “advanced” as a part of the title; ignore case when matching the
-- word with the title.


-- 3.24: Using the university schema, write an SQL query to find the name and ID of
-- those Accounting students advised by an instructor in the Physics department.

SELECT student.ID, student.name
FROM student, (
    SELECT advisor.i_id, advisor.s_id
    FROM advisor, instructor
    WHERE advisor.i_id = instructor.id AND instructor.dept_name = 'Physics'
) as p_advisors
WHERE student.ID = p_advisors.s_id and student.dept_name = 'Accounting';


-- 3.25: Using the university schema, write an SQL query to find the names of those
-- departments whose budget is higher than that of Philosophy. List them in alphabetic order.
-- because there is no philosophy department, I am choosing the accounting department instead.

SELECT dept_name
FROM department
WHERE budget > (SELECT budget FROM department WHERE dept_name = 'Accounting')
ORDER BY dept_name;

-- 3.26: Using the university schema, use SQL to do the following: For each student who
-- has retaken a course at least twice (i.e., the student has taken the course at least
-- three times), show the course ID and the student’s ID.
-- Please display your results in order of course ID and do not display duplicate
-- rows.

SELECT course_id, ID
FROM (
         SELECT count(*) as retakes, course_id, ID
         FROM takes
         GROUP BY ID, course_id
     ) as total_retakes
WHERE retakes >= 3
ORDER BY course_id;


-- 3.27: Using the university schema, write an SQL query to find the IDs of those stu-
-- dents who have retaken at least three distinct courses at least once (i.e, the
-- student has taken the course at least two times).
SELECT ID, dist_retakes
FROM (SELECT ID, count(*) as dist_retakes
      FROM (SELECT count(*) as retakes, course_id, ID
            FROM takes
            GROUP BY ID, course_id) as total_retakes
      WHERE retakes >= 2
      GROUP BY ID) as student_retakes
WHERE dist_retakes > 2

