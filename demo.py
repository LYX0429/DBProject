import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

"# DB Project"


@st.cache
def get_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


@st.cache
def query_db(sql: str):
    # print(f"Running query_db(): {sql}")

    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df


"## Read tables"

sql_all_table_names = "SELECT relname FROM pg_class WHERE relkind='r' AND relname !~ '^(pg_|sql_)';"
try:
    all_table_names = query_db(sql_all_table_names)["relname"].tolist()
    table_name = st.selectbox("Choose a table", all_table_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if table_name:
    f"Display the table"

    sql_table = f"SELECT * FROM {table_name};"
    try:
        df = query_db(sql_table)
        st.dataframe(df)
    except:
        st.write(
            "Sorry! Something went wrong with your query, please try again."
        )

"## Courses Information"

sql = f"""
    SELECT concat(concat(concat(concat(M.id, ', '), M.name), ', '), S.name) as id
    FROM Major M, School S
    WHERE M.school_id = S.id
    ORDER BY M.id ASC;"""
try:
    majors = query_db(sql)["id"].tolist()
    major_chosen = st.selectbox("Choose a major", majors).split(", ")[0]
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if major_chosen:
    course_number_input = st.text_input("Enter course number")
    if course_number_input:
        # try:
        sql = f"""
            SELECT C.id, C.course_number, C.course_name, C.section, C.term, C.year, P.name AS professor, M.name AS major
            , Count(CS.student_ssn) as num_of_students
            FROM  professor P, Major M, course C LEFT OUTER JOIN course_students CS on C.id = CS.course_id
            WHERE C.course_number = '{course_number_input}' 
            AND C.major_id = '{major_chosen}'
            AND M.id = C.major_id
            AND P.ssn = C.professor_ssn
            GROUP BY (C.id, C.course_number, C.course_name, C.section, C.term, C.year, P.name, M.name)
            ORDER BY id ASC;"""
        result_1 = query_db(sql)
        st.dataframe(result_1)
        # except:
        #     st.write("Sorry! Something went wrong with your query, please try again.")

"## Get students whose grade above X in a specific course"

id_or_number = st.selectbox("Choose searching method", ("Course ID", "Course Number"))
method = 0
if id_or_number == "Course ID":
    method = 0
else:
    method = 1
course_id_input = st.text_input("Enter course information")
grade_input = st.text_input("Enter grade filter", '90')
grade_trigger= True
try:
    grade_input = int(grade_input)
    grade_trigger = True
except:
    st.write("Please enter 0~100.")
    grade_trigger = False

if course_id_input and grade_trigger:
    try:
        if method == 0:
            sql = f"""
                SELECT S.ssn, S.name, CS.grade, C.id as course_id, C.course_number as course_number, C.section, 
                C.term, C.year
                FROM Student S, course_students CS, Course C
                WHERE S.ssn = CS.student_ssn
                AND C.id = CS.course_id
                AND C.id = '{course_id_input}' 
                AND CS.grade >= {grade_input}
                ORDER BY grade DESC, ssn ASC;"""
        elif method == 1:
            sql = f"""
                SELECT S.ssn, S.name, CS.grade, C.id as course_id, C.course_number as course_number, C.section, 
                C.term, C.year
                FROM Student S, course_students CS, Course C
                WHERE S.ssn = CS.student_ssn
                AND C.id = CS.course_id
                AND C.course_number = '{course_id_input}' 
                AND CS.grade >= {grade_input}
                ORDER BY grade DESC, ssn ASC;"""
        result_2 = query_db(sql)
        st.dataframe(result_2)
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")

"## Get students total credits in specific term"

student_name_input = st.text_input("Enter student name")
year_chosen = st.selectbox("Choose a year", ['2020', '2021', '2022'])
term_chosen = st.selectbox("Choose a semester", ['Fall', 'Spring'])
if student_name_input:
    try:
        sql = f"""
            SELECT S.ssn, S.name, sum(C.credits) credits
            FROM Student S, course_students CS, Course C
            WHERE S.ssn = CS.student_ssn
            AND C.id = CS.course_id
            AND S.name LIKE UPPER('%{student_name_input}%')
            AND C.year = '{year_chosen}'
            AND C.term = UPPER('{term_chosen}')
            GROUP BY S.ssn
            ORDER BY S.ssn ASC, S.name ASC; """
        result_3 = query_db(sql)
        st.dataframe(result_3)
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")


"## Count the total number of A students get from a professor"

sql = f"""
    SELECT concat(concat(P.ssn, ', '), P.name) as id
    FROM professor P
    ORDER BY P.ssn ASC;"""
try:
    professors = query_db(sql)["id"].tolist()
    professor_chosen = st.selectbox("Choose a professor", professors).split(", ")[0]
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if professor_chosen:
    # try:
    sql = f"""
        SELECT S.ssn, S.name, Count(CS) as nums
        FROM Student S JOIN course_students CS ON S.ssn = CS.student_ssn
        WHERE CS.course_id = any (
            SELECT C.id 
            FROM Course C
            WHERE professor_ssn = '{professor_chosen}')
        AND CS.grade > 90
        GROUP BY (S.ssn, S.name)
        ORDER BY nums DESC, ssn ASC; """
    result_4 = query_db(sql)
    st.dataframe(result_4)
    # except:
    #     st.write("Sorry! Something went wrong with your query, please try again.")


"## Get students who have job and take a least one course in current semester"

year_chosen2 = st.selectbox("Choose a year", ['2022'])
term_chosen2 = st.selectbox("Choose a semester", ['Fall'])
try:
    sql = f"""
        SELECT S.ssn, S.name, SW.position, SW.type
        FROM Student S, course_students CS, Course C, student_work SW
        WHERE S.ssn = CS.student_ssn
        AND C.id = CS.course_id
        AND C.year = '{year_chosen2}'
        AND C.term = UPPER('{term_chosen2}')
        AND S.work_id = SW.id
        ORDER BY S.ssn ASC, S.name ASC; """
    result_5 = query_db(sql)
    st.dataframe(result_5)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

#
# "## Query orders"
#
# sql_order_ids = "SELECT order_id FROM orders;"
# try:
#     order_ids = query_db(sql_order_ids)["order_id"].tolist()
#     order_id = st.selectbox("Choose an order", order_ids)
# except:
#     st.write("Sorry! Something went wrong with your query, please try again.")
#
# if order_id:
#     sql_order = f"""
#         SELECT C.name, O.order_date
#         FROM orders as O, customers as C
#         WHERE O.order_id = {order_id}
#         AND O.customer_id = C.id;"""
#
#     try:
#         customer_info = query_db(sql_order).loc[0]
#         customer_name, order_date = (
#             customer_info["name"],
#             customer_info["order_date"],
#         )
#         st.write(f"This order is placed by {customer_name} on {order_date}.")
#     except:
#         st.write(
#             "Sorry! Something went wrong with your query, please try again."
#         )
