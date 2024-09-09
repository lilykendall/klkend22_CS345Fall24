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
