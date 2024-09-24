select name, ID, salary as oldsalary, salary*1.02 as newsalary
from instructor
where salary < 50000
order by name;

-- write a query that returns the course IDs that all the computer science majors have taken
select distinct course_id
from takes, student
where takes.id = student.id and lower(dept_name) ~ 'comp.*sci.*';


-- write a query that returns all of the course IDs that the computer science majors have taken
select distinct course_id
from takes
where id in (select id from student where lower(dept_name) like 'comp.%sci.%')
order by random()
limit 10;

select ID
from student
where lower(dept_name) like 'Comp.%Sci.%';