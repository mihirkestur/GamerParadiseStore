import pandas as pd
def get_col_names(cursor, table_name):
    command = f"""SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"""
    cursor.execute(command)
    return cursor.fetchall()

def select_from_table(cursor, table_name, value = "*"):
    command = f"""select {value} from {table_name}"""
    cursor.execute(command)
    return pd.DataFrame(cursor.fetchall(), columns=get_col_names(cursor, table_name))

def insert_into_table(cursor, table_name, values):
    pass

def execute_any_command(cursor, command):
    command = f"""{command}"""
    cursor.execute(command)
    return cursor.fetchall()