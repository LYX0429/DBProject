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
        level varchar(32) not null,
        type varchar(32) not null,
        primary key (level, type)
);

create table Student_Work(
        position varchar(32) primary key,
        type varchar(32),
        location varchar(32)
);

create table Professor (
        ssn integer primary key,
        name varchar(32) not null,
        dob date,
        highest_degree_level varchar(32),
        highest_degree_type varchar(32),
        foreign key (highest_degree_level, highest_degree_type) references Degree(level, type)
);

create table School(
        name varchar(32) primary key,
        dean_ssn integer unique,
        foreign key (dean_ssn) references Professor(ssn)
);

create table Major(
        name varchar(32) primary key,
        school varchar(32) not null,
        foreign key (school) references School(name)
);

create table Student(
        ssn integer primary key,
        name varchar(32) not null,
        year integer not null,
        dob date,
        graduated bool,
        major varchar(32),
        degree_level varchar(32) not null,
        degree_type varchar(32) not null,
        work varchar(32),
        foreign key (major) references Major(name),
        foreign key (degree_level, degree_type) references Degree(level, type),
        foreign key (work) references Student_Work(position)
);

create table Non_diploma_student(
        ssn integer primary key,
        name varchar(32) not null,
        work varchar(32),
        foreign key (work) references Student_Work(position)
);

create table Course(
        course_number integer,
        course_name varchar(32) not null,
        section varchar(32) not null,
        term varchar(32) not null,
        professor_ssn integer not null,
        major varchar(32) not null,
        primary key (course_number, section, term),
        foreign key (professor_ssn) references Professor(ssn),
        foreign key (major) references Major(name)
);

create table course_students(
        student_ssn integer not null,
        course_number integer not null,
        section varchar(32) not null,
        term varchar(32) not null,
        grade integer,
        primary key (student_ssn, course_number, section, term),
        foreign key (student_ssn) references Student(ssn),
        foreign key (course_number, section, term) references Course(course_number, section, term)
);

create table course_non_students(
        student_ssn integer not null,
        course_number integer not null,
        section varchar(32) not null,
        term varchar(32) not null,
        grade integer,
        primary key (student_ssn, course_number, section, term),
        foreign key (student_ssn) references Non_diploma_student(ssn),
        foreign key (course_number, section, term) references Course(course_number, section, term)
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