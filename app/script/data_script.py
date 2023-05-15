import sys
sys.path.append('../database')
sys.path.append('../query')

from create_database import conn_db, create_table
from queries import read_xlsx_file, change_date_format, save_txt_file, read_txt_file, insert_data, show_table


####--------------------------------------------------------------------------------------------------
#### en caso de que el archivo sea ejecutado directamente
if __name__ == '__main__':
    print('---- Iniciando insercion de datos!')

    #### llamando a funcion para crear/conectar la base de datos
    conn = conn_db()

    #### asigando el parametro de nombre de tabla y llamando a la funcion crear tabla
    table_name = 'delitos'
    create = create_table(conn, table_name)

    #### llamando a funcion para leer el archivo xlsx
    file_xlsx = read_xlsx_file()
    ##print('---- file_xlsx ', file_xlsx)
    
    #### llamando a funcion para obtener la fecha actual
    fecha_actual = change_date_format()

    #### llamando a funcion para guardar el archivo txt
    save_txt = save_txt_file(file_xlsx, fecha_actual)
    #print('---- save_txt ', save_txt)

    #### llamando a funcion que retorna una lista de tuplas
    read_file = read_txt_file(fecha_actual)
    #print('---- read_file ', read_file)

    #### asigando el parametro de nombre de tabla y llamando a la funcion para insertar datos
    data_insert = insert_data(conn, table_name, read_file)
    #print('---- data_insert ', data_insert)

    #### llamando a funcion para mostrar los datos guardados
    table = show_table(conn, table_name)
    #print('---- table_show ', table)

    print('---- Finalizando insercion de datos!')
