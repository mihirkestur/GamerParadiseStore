import pandas as pd
def get_col_names(cursor, table_name):
    command = f"""SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"""
    cursor.execute(command)
    return cursor.fetchall()

def select_from_table(cursor, table_name, value = "*", where=""):
    command = f"""select {value} from {table_name} {where}"""
    cursor.execute(command)
    return pd.DataFrame(cursor.fetchall(), columns=get_col_names(cursor, table_name))

def insert_into_table(cursor, table_name, column_names,  values, key_value):
   # fname, lname, email, phone, addr = values
    command = f"""insert into {table_name} {column_names} values {values} returning {key_value}"""
    cursor.execute(command)
    return cursor.fetchall()[0][0]

def delete_entry_from_table(cursor, table_name, id, key):
    command = f"""delete from {table_name} where {id} = {key}"""
    try:
        cursor.execute(command)
    except Exception as e:
        return e
    return "Deleted Successfully"

def execute_any_command(cursor, command):
    command = f"""{command}"""
    cursor.execute(command)
    op = cursor.fetchall()
    op = [tuple(str(item) for item in t) for t in op]
    return pd.DataFrame(op)