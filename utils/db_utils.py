import psycopg2
import geopandas as gpd
from configparser import ConfigParser
from typing import Dict
from sqlalchemy import create_engine


class GeodataDB:
    def __init__(self):
        self.conn_info = self.load_conn_info('database.ini')
        try:
            self.conn = psycopg2.connect(**self.conn_info)
            self.cur = self.conn.cursor()
        except psycopg2.OperationalError as err:
            print(f"Database {self.conn_info['database']} does not exist, creating new database from info in "
                  f"database.ini")
            self.create_db()
            self.conn = psycopg2.connect(**self.conn_info)
            self.cur = self.conn.cursor()

    def connect(self):
        self.conn = psycopg2.connect(**self.conn_info)
        self.cur = self.conn.cursor()

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
        initial_connect = f"user={self.conn_info['user']} password={self.conn_info['password']}"
        self.conn = psycopg2.connect(initial_connect)
        self.cur = self.conn.cursor()

        # create database requires autocommit so temporarily turn this on
        self.conn.autocommit = True
        sql_query = f"CREATE DATABASE {self.conn_info['database']}"

        try:
            self.cur.execute(sql_query)
        except Exception as e:
            print(f'{type(e).__name__}: {e}')
            self.cur.close()
        else:
            self.conn.autocommit = False

    def dataframe_to_table(self, gdf: gpd.GeoDataFrame, table: str):
        connect = "postgresql+psycopg2://%s:%s@%s:5432/%s" % (
            self.conn_info['user'],
            self.conn_info['password'],
            self.conn_info['host'],
            self.conn_info['database']
        )
        engine = create_engine(connect)
        gdf.to_postgis(table, engine)
