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
FROM student, takes -- join the student and takes tables by ID
WHERE student.ID = takes.ID
  AND takes.course_id in (SELECT course_id FROM course WHERE dept_name LIKE 'Comp.%Sci.%'); -- get the course IDs that are in the Comp. Sci. department

-- b: Find the ID and name of each student who has not taken any course
-- oﬀered before 2017.

-- in 2017, there are no rows
SELECT student.ID, student.name
FROM student
WHERE student.ID NOT IN ( -- get the IDs of students who have taken a course before 2017, then get the students who are not in that query (set)
    SELECT takes.ID
    FROM takes
    WHERE takes.year < 2017);

-- checking 2005, this is the same code as above, but with 2005 instead of 2017
SELECT student.ID, student.name
FROM student
WHERE student.ID NOT IN (
    SELECT takes.ID
    FROM takes
    WHERE takes.year < 2005);


-- c: For each department, find the maximum salary of instructors in that department.
-- You may assume that every department has at least one instructor.

SELECT dept_name, max(salary) -- max salary in this case will return the max salary for each department because of the group by clause
FROM instructor
GROUP BY dept_name; -- group by department name to get the max salary for each department

-- d: Find the lowest, across all departments, of the per-department maximum
-- salary computed by the preceding query.

SELECT min(salary) -- taking the minimum of all max salaries from each department
FROM ( -- get the max salaries for each department (this is the same query as above)
         SELECT max(salary) AS salary
         FROM instructor
         GROUP BY dept_name
     ) AS max_salaries; -- to use a query in the FROM clause, it must be named


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

INSERT INTO section (course_id, sec_id, semester, year) -- only select the columns that there are values for
VALUES ('001','1', 'Fall', 2017); -- the location is not specified, so it is null and not specified here


-- c: Enroll every student in the Comp. Sci. department in the above section.

INSERT INTO takes (ID, course_id, sec_id, semester, year) -- only select the columns that there are values for
SELECT ID, '001', '1', 'Fall', 2017 -- using a query to get the IDs of students in the Comp. Sci. department
FROM student
WHERE dept_name = 'Comp. Sci.'; -- using the query to insert multiple rows


-- d: Delete enrollments in the above section where the student’s ID is 12345.

DELETE FROM takes
WHERE ID = '12345' AND course_id = '001' AND sec_id = '1' AND semester = 'Fall' AND year = 2017;

-- e: Delete the course CS-001. What will happen if you run this delete
-- statement without first deleting oﬀerings (sections) of this course?

DELETE FROM course
WHERE course_id = '001';
-- You have to delete the sections of the course first because the sections reference the course,
-- so there will be a foreign key error

-- f: Delete all takes tuples corresponding to any section of any course with
-- the word “advanced” as a part of the title; ignore case when matching the
-- word with the title.

DELETE FROM takes
WHERE course_id IN ( -- because the subquery is in the where clause, it does not need to be named
    SELECT course_id
    FROM course
    WHERE lower(title) LIKE '%advanced%'
    -- lower will ignore all capitals, the like clause will match any title that has advanced in it
    -- because we are allowing anything before and after advanced
);


-- 3.24: Using the university schema, write an SQL query to find the name and ID of
-- those Accounting students advised by an instructor in the Physics department.

SELECT student.ID, student.name
FROM student, ( -- joining the student table with the subquery that gets the advisors of physics students
    SELECT advisor.i_id, advisor.s_id
    FROM advisor, instructor -- joining the advisor table and instructor table to find department names
    WHERE advisor.i_id = instructor.id AND instructor.dept_name = 'Physics' -- find advisors in the physics department
) as p_advisors
WHERE student.ID = p_advisors.s_id and student.dept_name = 'Accounting';

-- 3.25: Using the university schema, write an SQL query to find the names of those
-- departments whose budget is higher than that of Philosophy. List them in alphabetic order.
-- because there is no philosophy department, I am choosing the accounting department instead.

SELECT dept_name
FROM department
WHERE budget > (SELECT budget FROM department WHERE dept_name = 'Accounting') -- subquery to get the budget of the accounting department
ORDER BY dept_name; -- order by department name to get the departments in alphabetical order

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
     ) as total_retakes -- get the total number of retakes for each student and course
WHERE retakes >= 3 -- only get the students who have retaken the course at least 3 times
ORDER BY course_id;


-- 3.27: Using the university schema, write an SQL query to find the IDs of those stu-
-- dents who have retaken at least three distinct courses at least once (i.e, the
-- student has taken the course at least two times).
SELECT ID, dist_retakes
FROM (SELECT ID, count(*) as dist_retakes -- count the number of distinct courses each student has retaken at least twice
      FROM (SELECT count(*) as retakes, course_id, ID -- count the number of times each student has taken each course
            FROM takes
            GROUP BY ID, course_id) as total_retakes -- total_retakes gets the number of times each student has taken each course
      WHERE retakes >= 2
      GROUP BY ID) as student_retakes -- student_retakes gets the number of distinct courses each student has retaken at least twice
WHERE dist_retakes > 2; -- find the students who have 3 or more distinct courses they have retaken at least twice