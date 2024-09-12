/*
students(first, last, preferred, id)
				 --
courses(coursenum, title)
	---------
enrollment(id, coursenum, semester, year)
	   --  ---------  --------  ----
*/

CREATE TABLE IF NOT EXISTS students(
	first TEXT NOT NULL,
	preferred TEXT,
	last TEXT NOT NULL,
	id TEXT NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS courses(
	coursenum TEXT NOT NULL,
	title TEXT NOT NULL,
	PRIMARY KEY (COURSENUM)
);

CREATE TABLE IF NOT EXISTS enrollments (
	id TEXT NOT NULL,
	coursenum TEXT NOT NULL,
	semester TEXT NOT NULL,
	year INT NOT NULL,
	PRIMARY KEY (id, coursenum, semester, year),
	FOREIGN KEY (id) REFERENCES students(id),
	FOREIGN KEY (coursenum) REFERENCES courses(coursenum)
);

insert into students values ('Harry', 'Harold', 'Potter', '1');
insert into students values ('Hermione', 'Hermit', 'Granger', '2');
insert into students values ('Ron', 'Ronald', 'Weasley', '3');
insert into courses values ('P140', 'Intro to Potions');
insert into courses values ('DA101', 'Intro to Dark Arts');
insert into courses values ('HB100', 'Intro to Herbology');
insert into enrollments values ('1', 'DA101', 'Fall', 2010);
insert into enrollments values ('1', 'P140', 'Fall', 2010);
insert into enrollments values ('2', 'P140', 'Fall', 2011);
insert into enrollments values ('3', 'P140', 'Fall', 2011);
insert into enrollments values ('3', 'P140', 'Fall', 2012);
