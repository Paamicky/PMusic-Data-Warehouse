import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries, create_table_queries, drop_table_queries


## this function loads data from S3 bucket into the staging area
def load_staging_tables(cur, conn):
    """
    :
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

## inserting data from staging area into the facts and dimension table
def insert_tables(cur, conn):
    """
    :
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    :
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    print("Connection complete")
    cur = conn.cursor()
    print("Cursor Connection complete")
    
    
    load_staging_tables(cur, conn)
    print("staging done")
    
    insert_tables(cur, conn)
    print("Done")
    
    
    conn.close()


if __name__ == "__main__":
    """
    :
    """
    main()