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
    SELECT concat(concat(concat(concat(M.id, ' '), S.name), ' '), M.name) as id
    FROM Major M, School S
    WHERE M.school_id = S.id
    ORDER BY M.id ASC;"""
try:
    majors = query_db(sql)["id"].tolist()
    major_chosen = st.selectbox("Choose a major", majors).split(" ")[0]
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if major_chosen:
    course_number_input = st.text_input("Enter course number")
    if course_number_input:
        try:
            sql = f"""
                SELECT C.id, C.course_number, C.course_name, C.section, C.term, C.year, P.name AS professor, M.name AS major
                FROM course C, professor P, Major M
                WHERE C.course_number = '{course_number_input}' 
                AND C.major_id = '{major_chosen}'
                AND M.id = C.major_id
                AND P.ssn = C.professor_ssn
                ORDER BY C.id ASC;"""
            result_1 = query_db(sql)
            st.dataframe(result_1)
        except:
            st.write("Sorry! Something went wrong with your query, please try again.")

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
                UNION 
                SELECT S.ssn, S.name, CS.grade, C.id as course_id, C.course_number as course_number, C.section, 
                C.term, C.year
                FROM Non_diploma_student S, course_students CS, Course C
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
                UNION 
                SELECT S.ssn, S.name, CS.grade, C.id as course_id, C.course_number as course_number, C.section, 
                C.term, C.year
                FROM Non_diploma_student S, course_students CS, Course C
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
if student_name_input:
    try:
        sql = f"""
            SELECT S.ssn, S.name, sum(C.credits) credits
            FROM Student S, course_students CS, Course C
            WHERE S.ssn = CS.student_ssn
            AND C.id = CS.course_id
            AND S.name LIKE '%{student_name_input}%'
            GROUP BY S.ssn
            ORDER BY S.ssn ASC, S.name ASC; """
        result_3 = query_db(sql)
        st.dataframe(result_3)
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
