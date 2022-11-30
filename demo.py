import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

"# Demo: Streamlit + Postgres"


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

"## Query Students"

sql_student_names = "SELECT name FROM student;"
try:
    student_names = query_db(sql_student_names)["name"].tolist()
    student_name = st.selectbox("Choose a student", student_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if student_name:
    sql_student = f"SELECT * FROM student WHERE name = '{student_name}';"
    try:
        student_info = query_db(sql_student).loc[0]
        c_age, c_city, c_state = (
            student_info["ssn"],
            student_info["year"],
            student_info["major"],
        )
        st.write(
            f"{student_name} is a {year} of {major} whose ssn is {ssn}."
        )
    except:
        st.write(
            "Sorry! Something went wrong with your query, please try again."
        )
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
