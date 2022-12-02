--students who get A in 6001
SELECT S.name 
	FROM Student S JOIN course_students C ON S.ssn = C.ssn 
	WHERE C.course_number = '6001' AND C.grade > 90
	UNION 
	SELECT N.name FROM Non_diploma_student N JOIN course_non_students NC ON N.ssn = NC.ssn 
		WHERE NC.course_number = '6001' AND NC.grade > 90;

--students and courses who have more than two courses in FALL 2022
SELECT S.name, count(C.course_number) count_course
	FROM Students S 
	JOIN course_students C ON S.ssn = C.ssn 
	HAVING count(C.course_number) >= 2
	GROUP BY S.name; 

--CS students who's taking 6003
SELECT S.ssn, S.name 
	FROM Students S JOIN course_students C ON S.ssn = C.ssn 
	WHERE C.course_number = '6003'
	INTERSECT 
	SELECT ssn, name FROM Students WHERE major = 'CS';


--EE students who's taking KLOUD(000020)'s class and get an A(grade > 90), 
SELECT S.ssn, S.name, S.major, C.grade
	FROM Students S JOIN course_students C ON S.ssn = C.ssn
	WHERE C.course_number = any (SELECT C.course_number, C.course_name 
		FROM Course 
		WHERE professor_ssn = '000020')
		AND C.grade > 90 
		AND S.major = 'EE';
	
	

--Students who's working in OGS and get A in all courses in FALL 2022
SELECT S.name, S.ssn 
	FROM Student S 
	WHERE S.work = any (SELECT position FROM Student_Work WHERE location = 'OGS')
	AND S.ssn = any(SELECT ssn FROM course_students C WHERE grade > 90 AND term = 'FALL 2022')
	


