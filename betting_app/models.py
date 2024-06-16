# Example model
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

from .utils import read_data_from_csv, model_input_ratio, transform_odds

class Database:
    def __init__(self, db_name, csv):
        self._db_name = db_name
        self._conn = None
        self._cur = None

        self.features, self.targets, _, _ = read_data_from_csv(csv)
    
    # @db_name.setter
    def _db_name(self, value):
        self._db_name = value
    
    # @db_name.getter
    def _db_name(self):
        return self._db_name
    
    def connect_db(self):
        import sqlite3
        self._conn = sqlite3.connect(self._db_name)
        self._cur = self._conn.cursor()

    def insert_bulk_data(self):
        import pandas as pd

        self.connect_db()

        self.features.to_sql('table_features', self._conn, if_exists='replace', index=False)
        self.targets.to_sql('table_targets', self._conn, if_exists='replace', index=False)

        self.commit_db()
        self.close_db()

    def commit_db(self):
        self._conn.commit()

    def close_db(self):
        self._conn.close()