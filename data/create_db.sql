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
		grade varchar(32),
        primary key (course_number, section, term),
        foreign key (professor_ssn) references Professor(ssn),
        foreign key (major) references Major(name)
);

create table course_students(
        student_ssn integer not null,
        course_number integer not null,
        section varchar(32) not null,
        term varchar(32) not null,
        primary key (student_ssn, course_number, section, term),
        foreign key (student_ssn) references Student(ssn),
        foreign key (course_number, section, term) references Course(course_number, section, term)
);

create table course_non_students(
        student_ssn integer not null,
        course_number integer not null,
        section varchar(32) not null,
        term varchar(32) not null,
        primary key (student_ssn, course_number, section, term),
        foreign key (student_ssn) references Non_diploma_student(ssn),
        foreign key (course_number, section, term) references Course(course_number, section, term)
);

