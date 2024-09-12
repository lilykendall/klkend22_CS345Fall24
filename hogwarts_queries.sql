select 
	id
from 
	students 
where 
	first = 'Harry' and last = 'Potter';

-- What are the course numbers of courses that harry has taken

Select
	coursenum
From
	enrollments
Where
	id = (
		select 
			id
		from 
			students 
		where 
			first = 'Harry' and last = 'Potter');

-- list all the course numbers that have had enrollments
select 
	coursenum
from
	enrollments;

-- list students by last names
select
	last, first, id
from
	students
order by
	last;

-- list all the course numbers who have titles that start with Intro
select
	coursenum, title
from
	courses
where
	title ~ 'Intro*' -- regular expression 
order by
	coursenum;

-- count the number of rows in the enrollments table
-- count is an example of an aggregate function
select count(*) from enrollments;

-- multiple table queries
-- cross join (computing teh cross product of the tables and filtering)
select	
	*
from
	students, enrollments
where
	students.id = enrollments.id;

-- table variables
select
	last, first, S.id, coursenum, semester, year
from
	students S, enrollments E
where
	S.id = E.id
order by
	last;

-- include the course title in the report
select
	last, first, S.id, C.coursenum, title, semester, year
from
	students S, enrollments E, courses C
where
	S.id = E.id and C.coursenum = E.coursenum
order by
	last;

-- because the attribute names match that we are joining on, this is also
-- called a natural inner join

create table if not exists R (
	x int not null,
	primary key (x) 
);
insert into R values (1), (2), (3), (4);

-- compute the cross product
select 
	r1.x as a, r2.x as b
from 
	R r1, R r2;

-- compute the cross product, but remove duplicates such that (a, a) is not listed
select 
	r1.x as a, r2.x as b
from 
	R r1, R r2
where
	r1.x <> r2.x;

-- union, union of two sets
-- union all will keep duplicates
-- intersect, keep rows that are in common between two sets
-- union and intersect are not primitive
