import pymysql
import pandas as pd
import numpy as np
from pymysql import IntegrityError


class PyMySqlClient:

    def __init__(self, usr="", pswd="", hst="", db=""):

        if(not usr or not pswd or not hst):
            self.conn = None
            raise Exception('''
                            Unable to form connection with missing information - 
                            Usage: PyToSql(username, password, hostname)
                            ''')
            return 
        self._username = usr
        self._password = pswd
        self._hostname = hst
        self._database = db
        

    def get_table_info(self, table):
        conn = self._get_connection()
        cursor = conn.cursor()

        query = f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'"
        cursor.execute(query)
        res = cursor.fetchall()
        conn.close()
        return res

    def get_tables(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s"
        res = self.run_query(sql, [self._database])
        conn.close()
        return res
    
    def _get_connection(self):
        conn = pymysql.connect(
            user=self._username,
            password=self._password,
            host=self._hostname,
            db=self._database,
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn

    
    def run_query(self, sql, args, fetch=True):
        """
        Runs a query. The SQL contains "%s" placeholders for parameters for the query. If fetch is true, return the
        result set.
        :param sql: An SQL string with "%s" please holders for parameters.
        :param args: A list of values to insert into the query for the parameters.
        :param fetch: If true, return the result set.
        :return: The result set or the number of rows affected.
        """

        result = None
        conn = self._get_connection()
        cursor = conn.cursor()
        result = cursor.execute(sql, args)
        if fetch:
            result = cursor.fetchall()
        conn.close()
        
        return result

    def database_exists(self):
        """
        Check if a database exists.
        :param database_name: Name of the database.
        :return: True if the database exists, False otherwise.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES LIKE %s", (self._database))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    # There may be some security considerations here
    def insert_row_table(self, table_name, row_dict):
        """
        Insert a dictionary into a table.
        :param table_name: Name of the table.
        :param row_dict: A dictionary of column names and values.
        :return: 1 of the insert occurred and 0 otherwise.
        """

        columns = []
        placeholders = []
        values = []
        for col, val in row_dict.items():
            if val is not None and (not isinstance(val, str) or len(val) > 0):
                columns.append(col)
                placeholders.append("%s")
                values.append(val)
        sql = f"INSERT INTO {self._database}.{table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        try:
            self.run_query(sql, values, fetch=False)
        except IntegrityError as e:
            print("THERE WAS AN INTEGRITY ERROR", e)
            return 0
        return 1

    def retrieve(self, table_name, field_list = [], query_dict = {}):
        """
        Maps a query on a resource collection to an SQL statement and returns the result.

        :param table_name: Name of the table.
        :param field_list: List of columns to return.
        :param query_dict: Dictionary of name, value pairs to form a where clause.
        :return: The result set as a list of dictionaries.
        """

        # Ensure field_list is not empty
        if not field_list:
            field_list = ['*']

        # Build the SELECT statement
        sql = "SELECT " + ", ".join(field_list) + f" FROM {self._database}.{table_name}"
        args = []

        # Build the WHERE clause if query_dict is provided
        if query_dict:
            where_clauses = []
            for col, val in query_dict.items():
                where_clauses.append(f"{col} = %s")
                args.append(val)
            sql += " WHERE " + " AND ".join(where_clauses)

        return self.run_query(sql, args)

    def build_where_clause_pk(self, table_name:str, vals:dict):
        """
        builds where clause for any kind of query. returns both
        values for pk in a list + where clause itself
        

        Parameters:
        - table_name: Name of the table to update.
        - vals: Dictionary where keys with values are held
        """
        pks = self.get_primary_keys(table_name)
        where_clause = ""
        pk_vals = []
        for pk in pks:
            key = pk['COLUMN_NAME']
            where_clause += f"{key}=%s AND"
            pk_vals.append(str(vals[key]))
        
        where_clause = where_clause[:len(where_clause)-len(" AND")]
        return (pk_vals, where_clause)

    def update_entry(self, table_name, update_values, old_values):
        """
        Update rows in a given table with new values.

        Parameters:
        - db_config: Dictionary containing database connection parameters.
        - table_name: Name of the table to update.
        - update_values: Dictionary where keys are column names and values are the new values to set.
        - old_values: Dictionary where keys are column names to match and values are the old values.

        """
    
        # Construct the SET clause of the UPDATE statement
        set_clause = ""
        upd_list = []
        for key, value in update_values.items():
            if(len(str(value)) == 0):
                value = None
            if(str(value) != str(old_values[key])):
                set_clause += f"{key}=%s, "
                if(value != None):
                    value = str(value)
                upd_list.append(value)

        set_clause = set_clause[:len(set_clause)-len(", ")] + " WHERE"

        # Construct the WHERE clause based on old_values
        pk_vals, where_clause = self.build_where_clause_pk(table_name, old_values)

        # Combine update_values and old_values for execution
        combined_values = upd_list + pk_vals
            
        # Construct the full UPDATE statement
        sql = f"UPDATE {table_name} SET {set_clause} {where_clause}"
        print(sql)
        print(combined_values)
        
        try:
            self.run_query(sql, combined_values, fetch=False)
        except Exception as e:
            raise Exception("update query failed", e)

    def get_primary_keys(self, table_name):
        """
        Retrieve primary key columns for a specific table in the specified database.

        Parameters:
        - database_name: Name of the database to inspect.
        - table_name: Name of the table to retrieve primary keys for.
        """
        sql_query = """
        SELECT KCU.COLUMN_NAME, C.DATA_TYPE
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KCU
            JOIN INFORMATION_SCHEMA.COLUMNS AS C ON KCU.TABLE_SCHEMA = C.TABLE_SCHEMA
                AND KCU.TABLE_NAME = C.TABLE_NAME
                AND KCU.COLUMN_NAME = C.COLUMN_NAME
            WHERE KCU.CONSTRAINT_SCHEMA = %s 
              AND KCU.TABLE_NAME = %s 
              AND KCU.CONSTRAINT_NAME = 'PRIMARY'
            ORDER BY KCU.ORDINAL_POSITION;
            """
        
        return self.run_query(sql_query, [self._database, table_name])
    
    def delete_row(self, table_name, condition):
        """
        Deletes a row from a specified table based on a condition.

        Parameters:
        - table_name: Name of the table from which to delete the row.
        - condition: A dictionary specifying the column-value pairs that identify the row to delete.
                     For example, {'id': 123} deletes the row where the id column equals 123.
        """
        pk_vals, where_clause = self.build_where_clause_pk(table_name, condition)

        sql_query = f"DELETE FROM {table_name} WHERE {where_clause}"

        try:
            self.run_query(sql_query, pk_vals, fetch=False)
        except Exception as e:
            raise Exception("delete query failed", e)
    
    def change_db(self, database):
        self._database = database

    def get_db(self):
        return self._database