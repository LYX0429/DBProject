Drop table course_non_students;
Drop table course_students;
Drop table Course;
Drop table Non_diploma_student;
Drop table Student;
Drop table Major;
Drop table School;
Drop table Professor;
Drop table Student_Work;
Drop table Degree;

create table Degree(
        id integer primary key,
        name varchar(32),
        level varchar(32),
        type varchar(32)
);

create table Student_Work(
        id integer primary key,
        position varchar(32),
        type varchar(32),
        location varchar(32)
);

create table Professor (
        ssn integer primary key,
        name varchar(32) not null,
        dob date,
        degree_id integer,
        foreign key (degree_id) references Degree(id)
);

create table School(
        id integer primary key,
        name varchar(32) not null,
        dean_ssn integer unique not null,
        foreign key (dean_ssn) references Professor(ssn)
);

create table Major(
        id integer primary key,
        name varchar(32) not null,
        school_id integer not null,
        foreign key (school_id) references School(id)
);

create table Student(
        ssn integer primary key,
        name varchar(64) not null,
        year integer not null,
        dob date,
        graduated bool,
        major_id integer not null,
        degree_id integer not null,
        work_id integer,
        foreign key (major_id) references Major(id),
        foreign key (degree_id) references Degree(id),
        foreign key (work_id) references Student_Work(id)
);

create table Non_diploma_student(
        ssn integer primary key,
        name varchar(64) not null,
        work_id integer,
        foreign key (work_id) references Student_Work(id)
);

create table Course(
        id integer primary key,
        course_number integer not null,
        course_name varchar(32) not null,
        section varchar(32) not null,
        term varchar(32) not null,
        year varchar(32) not null,
        professor_ssn integer not null,
        major_id integer not null,
        foreign key (professor_ssn) references Professor(ssn),
        foreign key (major_id) references Major(id)
);

create table course_students(
        student_ssn integer not null,
        course_id integer not null,
        grade integer,
        primary key (student_ssn, course_id),
        foreign key (student_ssn) references Student(ssn),
        foreign key (course_id) references Course(id)
);

create table course_non_students(
        student_ssn integer not null,
        course_id integer not null,
        grade integer,
        primary key (student_ssn, course_id),
        foreign key (student_ssn) references Non_diploma_student(ssn),
        foreign key (course_id) references Course(id)
);

COPY Degree
FROM 'D:\DBProject\data\csv\Degree.csv'
DELIMITER ','
CSV HEADER;

COPY Student_Work
FROM 'D:\DBProject\data\csv\Student_Work.csv'
DELIMITER ','
CSV HEADER;

COPY Professor
FROM 'D:\DBProject\data\csv\Professor.csv'
DELIMITER ','
CSV HEADER;

COPY School
FROM 'D:\DBProject\data\csv\School.csv'
DELIMITER ','
CSV HEADER;

COPY Major
FROM 'D:\DBProject\data\csv\Major.csv'
DELIMITER ','
CSV HEADER;

COPY Student
FROM 'D:\DBProject\data\csv\Student.csv'
DELIMITER ','
CSV HEADER;

COPY Non_diploma_student
FROM 'D:\DBProject\data\csv\Non_diploma_student.csv'
DELIMITER ','
CSV HEADER;

COPY Course
FROM 'D:\DBProject\data\csv\Course.csv'
DELIMITER ','
CSV HEADER;

COPY course_students
FROM 'D:\DBProject\data\csv\course_students.csv'
DELIMITER ','
CSV HEADER;

COPY course_non_students
FROM 'D:\DBProject\data\csv\course_non_students.csv'
DELIMITER ','
CSV HEADER;