import psycopg2
from configparser import ConfigParser

@st.cache
def get_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


db_info = get_config()
conn = psycopg2.connect(**db_info)
cur = conn.cursor()
cur.close()
conn.close()