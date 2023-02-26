import psycopg2
from configparser import ConfigParser
from psycopg2 import sql
from typing import Dict


class GeodataDB:
    def __init__(self):
        self.conn_info = self.load_conn_info('database.ini')

        # connect to engine to create database
        self.initial_connect = f"user={self.conn_info['user']} password={self.conn_info['password']}"
        self.conn = psycopg2.connect(self.initial_connect)
        self.cur = self.conn.cursor()
        self.create_db()

    def connect(self):
        self.conn = psycopg2.connect(**self.conn_info)
        self.cur = self.conn.cursor()
        return self.cur

    def query(self, query):
        self.cur.execute(query)

    def close(self):
        self.cur.close()
        self.conn.close()

    def load_conn_info(self, ini_filename: str) -> Dict[str, str]:
        parser = ConfigParser()
        parser.read(ini_filename)
        conn_info = {param[0]: param[1] for param in parser.items('postgresql')}
        return conn_info

    def create_db(self) -> None:
        # create database requires autocommit so temporarily turn this on
        self.conn.autocommit = True
        sql_query = f"CREATE DATABASE {self.conn_info['database']}"

        try:
            self.cur.execute(sql_query)
        except Exception as e:
            print(f'{type(e).__name__}: {e}')
            print(f'Query: {self.cur.query}')
            self.cur.close()
        else:
            self.conn.autocommit = False

    def create_table(self, table_name: str) -> None:
        sql_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                GRID_POINTS int,
                GEOMETRY float,
                DEPTH float          
            )
        """
        try:
            self.cur.execute(sql.SQL(sql_query).format(table_name=sql.Identifier(table_name), ))
        except Exception as e:
            print(f'{type(e).__name__}: {e}')
            print(f'Query: {self.cur.query}')
            self.conn.rollback()
            self.cur.close()
        else:
            self.conn.commit()
