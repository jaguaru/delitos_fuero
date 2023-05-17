'''
    modulo principal para ejecutar todo el proceso
'''
import sys
# para poder importar el modulo create_database
sys.path.append('../database')
# para poder importar el modulo queries
sys.path.append('../query')

from create_database import conn_db, create_table
from queries import read_xlsx_file, change_date_format, save_txt_file
from queries import read_txt_file, insert_data, show_table


#--------------------------------------------------------------------------------------------------
# en caso de que el archivo sea ejecutado directamente
if __name__ == '__main__':
    print('---- Iniciando insercion de datos!')

    # llamando a funcion para crear/conectar la base de datos
    conn = conn_db()

    # asigando el parametro de nombre de tabla y llamando a la funcion crear tabla
    TABLE_NAME = 'delitos'
    create = create_table(conn, TABLE_NAME)

    # llamando a funcion para leer el archivo xlsx
    file_xlsx = read_xlsx_file()

    # llamando a funcion para obtener la fecha actual
    fecha_actual = change_date_format()

    # llamando a funcion para guardar el archivo txt
    save_txt = save_txt_file(file_xlsx, fecha_actual)

    # llamando a funcion que retorna una lista de tuplas
    read_file = read_txt_file(fecha_actual)

    # asigando el parametro de nombre de tabla y llamando a la funcion para insertar datos
    data_insert = insert_data(conn, TABLE_NAME, read_file)

    #### llamando a funcion para mostrar los datos guardados
    table = show_table(conn, TABLE_NAME)

    print('---- Finalizando insercion de datos!')
