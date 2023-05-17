'''
    modulo para las funciones de leer xlsx, guardar y leer txt,
    guardar en base de datos
'''
import sys
import ast
from datetime import date, datetime
import pandas as pd

# para poder importar el modulo create_database
sys.path.append('../database')

from create_database import conn_db, show_table


#---------------------------------------------------------
# funcion para cambiar el formato de fecha
def change_date_format():
    '''Funcion para cambiar formato de fecha'''
    # obteniendo la fecha actual en formato 2023-05-04
    fecha_actual = str(date.today())
    # asignando los formatos de entrada y salida
    formato_entrada = "%Y-%m-%d"
    formato_salida = "%B %dth, %Y"
    # creando la fecha-objeto
    fecha_objeto = datetime.strptime(fecha_actual, formato_entrada)
    # cambiar el formato de la fecha-objeto a May 4th, 2023
    fecha_convertida = fecha_objeto.strftime(formato_salida)
    return fecha_convertida

#---------------------------------------------------------
# funcion para leer el archivo xlsx
def read_xlsx_file():
    '''Funcion para leer el archivo de excel'''
    # declaracion de variables con el nombre del archivo,
    # nombre de la hoja y directorio del archivo
    nombre_archivo = '/delitos_fuero_comun.xlsx'
    archivo = '../docs' + str(nombre_archivo)
    sheet_name = 'delitos_fuero_comun'

    # funcion para leer los datos del archivo y crear el dataframe
    data_frame = pd.read_excel(archivo, sheet_name=sheet_name)

    # obteniendo el numero de filas del archivo
    num_rows = int(data_frame.shape[0])

    # declaracion de variable para guardar una lista de tuplas
    apnd_datos = []

    # nombres de las columnas del archivo de excel:
    # (AÑO, Fuente, CVE_ENT, Entidad_Federativa, Delitos_fuero_comun)

    # recorriendo todas las filas del archivo con un ciclo for
    for index in range(num_rows):
    #for index, row in df.iterrows():

        # leyendo el contenido de las celdas con el nombre de cada columna
        # limpiando los espacios al inicio y al final de cada celda con la funcion "strip()"
        anio = str(data_frame.loc[index, 'AÑO']).strip()
        fuente = str(data_frame.loc[index, 'Fuente']).strip()
        cve_ent = str(data_frame.loc[index, 'CVE_ENT']).strip()
        entidad_federativa = str(data_frame.loc[index, 'Entidad_Federativa']).strip()
        delitos_fuero_comun = str(data_frame.loc[index, 'Delitos_fuero_comun']).strip()

        # filtrando con un condicional if los delitos que sean mayores a 100
        if int(delitos_fuero_comun) > 100:

            # creando una lista de tuplas con los datos
            tuple_values = (int(anio),
                             str(fuente),
                             int(cve_ent),
                             str(entidad_federativa),
                             int(delitos_fuero_comun))

            #### agregando las tuplas a la lista
            apnd_datos.append(tuple_values)

    print('----------------------------------------------')
    print('  ----  ----  Se leyeron todos los datos!')
    print('----------------------------------------------')

    return apnd_datos

#---------------------------------------------------------
# funcion para leer el archivo txt y guardar los datos como tuplas en formato de texto
def save_txt_file(apnd_datos, formato_fecha):
    '''Funcion para leer el archivo txt y guardar en tuplas'''

    nombre_archivo = '/queries_' + formato_fecha + '.txt'
    directorio = '../docs' + str(nombre_archivo)

    try:
        print('----------------------------------------------')
        print('  ----  Guardando info!')
        print('----------------------------------------------')
        # se crea el archivo en modo de escritura, si el archivo existe se sobrescribe
        with open(directorio, 'w', encoding='utf-8') as txt_file:
            # creando el archivo txt para guardar las consultas
            for data in apnd_datos:
                txt_file.write(str(data) + '\n')

        message = 'Se guardo el archivo txt!'
        print('----------------------------------------------')
        print('  ----  ', message)
        print('----------------------------------------------')

    except:
        message = 'No se pudo guardar el archivo txt!'
        print('----------------------------------------------')
        print('  ----  ', message)
        print('----------------------------------------------')

    return message

#---------------------------------------------------------
# funcion para leer el archivo txt y retornar una tupla con los datos
def read_txt_file(formato_fecha):
    '''Funcion para leer archivo txt y retornar tupla'''

    nombre_archivo = '/queries_' + formato_fecha + '.txt'
    directorio = '../docs' + str(nombre_archivo)

    # abrir el archivo de texto y leer linea por linea
    with open(directorio, encoding='utf-8') as txt_file:
        read_lines = txt_file.readlines()

    # crear una variable de lista
    apnd_list = []
    # leer las tuplas con un ciclo for
    for data in read_lines:
        # convertir cada linea de texto en una tupla
        #tupla = eval(data)
        tupla = ast.literal_eval(data)
        # agregar cada linea a la lista
        apnd_list.append(tupla)

    return apnd_list

#---------------------------------------------------------
# funcion con transaccion para guardar la informacion obtenida del archivo xlsx
def insert_data(conn_db, table_name, data_list):
    '''Funcion para guardar en base de datos mediante transacciones'''

    value = None

    try:
        # abriendo el cursor para conectar a la base de datos
        conn_cursor = conn_db.cursor()

        # iniciar la transaccion
        conn_cursor.execute('BEGIN TRANSACTION')

        # consulta para insertar en la tabla
        insert_query = f'''INSERT INTO {table_name}
                                        (anio,
                                        fuente,
                                        cve_ent,
                                        entidad_federativa,
                                        delitos_fuero_comun)
                                        VALUES (?, ?, ?, ?, ?)'''
        # reasignacion de variable para almacenar la lista de tuplas
        insert_values = data_list

        for data in insert_values:
            # ejecutando la consulta con los valores
            conn_cursor.execute(insert_query, data)

        # guardar todas las transacciones, si todas son exitosas
        conn_cursor.execute('COMMIT')

        print('---- Se agregaron todas las transacciones!')
        value = True

    except:
        # hacer rollback con las transacciones si ocurre algun error
        conn_cursor.execute('ROLLBACK')
        print('---- No se pudieron agregar las transacciones!')
        value = False

    return value

#---------------------------------------------------------
# en caso de que el archivo sea ejecutado directamente
if __name__ == '__main__':
    print('---- Iniciando insercion de datos!')

    # llamando a funcion para crear/conectar la base de datos
    conn = conn_db()

    # llamando a funcion para leer el archivo xlsx
    file_xlsx = read_xlsx_file()

    # llamando a funcion para obtener la fecha actual
    ACTUAL_DATE = change_date_format()

    # llamando a funcion para guardar el archivo txt
    SAVE_TXT = save_txt_file(file_xlsx, ACTUAL_DATE)

    # llamando a funcion que retorna una lista de tuplas
    read_file = read_txt_file(ACTUAL_DATE)

    # asigando el parametro de nombre de tabla y llamando a la funcion para insertar datos
    TABLE_NAME = 'delitos'
    data_insert = insert_data(conn, TABLE_NAME, read_file)

    # llamando a funcion para mostrar la informacion guardada en la base de datos
    table_show = show_table(conn, TABLE_NAME)
    print('---- table_show ', table_show)

    print('---- Finalizando insercion de datos!')
