####--------------------------------------------------------------------------------------------------
####    modulo para las funciones de leer xlsx, guardar y leer txt, guardar en base de datos,
####--------------------------------------------------------------------------------------------------
import sys
sys.path.append('../database')

#import sqlite3
import pandas as pd
import json

from datetime import date
from create_database import conn_db, show_table


####--------------------------------------------------------------------------------------------------
#### funcion para cambiar el formato de fecha
def change_date_format():
    #### obteniendo la fecha actual en formato 2023-05-04
    fecha_actual = date.today()
    #### cambiar el formato de la fecha a  May 4th, 2023
    formato_fecha = str(fecha_actual.strftime("%B %d, %Y"))
    return formato_fecha


####--------------------------------------------------------------------------------------------------
#### funcion para leer el archivo xlsx
def read_xlsx_file():

    #### declaracion de variables con el nombre del archivo, nombre de la hoja y directorio del archivo
    nombre_archivo = '/delitos_fuero_comun.xlsx'
    #archivo = '/home/muzen/Test Vacantes Trabajos/PCD Systems/Test/delitos_fuero/app/doc' + str(nombre_archivo)
    archivo = '../docs' + str(nombre_archivo)
    sheet_name = 'delitos_fuero_comun'

    #### funcion para leer los datos del archivo y crear el dataframe
    df = pd.read_excel(archivo, sheet_name=sheet_name)
    
    #### obteniendo el numero de filas del archivo
    num_rows = int(df.shape[0])
    
    #### declaracion de variable para guardar una lista de tuplas
    apnd_datos = []

    #### nombres de las columnas del archivo de excel:
    #### (AÑO, Fuente, CVE_ENT, Entidad_Federativa, Delitos_fuero_comun)

    #### recorriendo todas las filas del archivo con un ciclo for
    for index in range(num_rows):
        
        #### leyendo el contenido de las celdas con el nombre de cada columna
        #### limpiando los espacios al inicio y al final de cada celda con la funcion "strip()"
        anio = str(df.loc[index, 'AÑO']).strip()
        fuente = str(df.loc[index, 'Fuente']).strip()
        cve_ent = str(df.loc[index, 'CVE_ENT']).strip()
        entidad_federativa = str(df.loc[index, 'Entidad_Federativa']).strip()
        delitos_fuero_comun = str(df.loc[index, 'Delitos_fuero_comun']).strip()
        
        #### filtrando con un condicional if los delitos que sean mayores a 100
        if int(delitos_fuero_comun) > 100:

            #### creando una lista de tuplas con los datos
            #########convert_dict(anio, fuente, cve_ent, entidad_federativa, delitos_fuero_comun)
            #dict_values = {
            #               'anio': int(anio), 
            #               'fuente': str(fuente), 
            #               'cve_ent': int(cve_ent), 
            #               'entidad_federativa': str(entidad_federativa), 
            #               'delitos_fuero_comun': int(delitos_fuero_comun)
            #              }

            #### creando una lista de tuplas con los datos
            #########convert_tuple(anio, fuente, cve_ent, entidad_federativa, delitos_fuero_comun)
            tuple_values = ( 
                             anio := int(anio), 
                             fuente := str(fuente), 
                             cve_ent := int(cve_ent), 
                             entidad_federativa := str(entidad_federativa), 
                             delitos_fuero_comun := int(delitos_fuero_comun)
                            )
            
            #### agregando las tuplas a la lista
            #apnd_datos.append(dict_values)
            apnd_datos.append(tuple_values)

    print('----------------------------------------------')
    print('  ----  ----  Se leyeron todos los datos!')
    print('----------------------------------------------')
    
    return apnd_datos

####--------------------------------------------------------------------------------------------------
#### funcion para leer el archivo txt
def save_txt_file(apnd_datos, formato_fecha):

    nombre_archivo = '/queries_' + formato_fecha + '.txt'

    #directorio = '/home/muzen/Test Vacantes Trabajos/PCD Systems/Test/delitos_fuero/app/docs' + str(nombre_archivo)
    directorio = '../docs' + str(nombre_archivo)


    try:
        print('----------------------------------------------')
        print('  ----  Guardando info!')
        print('----------------------------------------------')
        #### se crea el archivo en modo de escritura, si el archivo existe se sobrescribe
        #### creando el archivo txt para guardar las consultas
        with open(directorio, 'w', encoding='utf-8') as txt_file:
             for data in apnd_datos:
                 txt_file.write(str(data) + "\n")
        
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

####--------------------------------------------------------------------------------------------------
#### funcion para leer el archivo txt
def read_txt_file(formato_fecha):

    nombre_archivo = '/queries_' + formato_fecha + '.txt'

    #directorio = '/home/muzen/Test Vacantes Trabajos/PCD Systems/Test/delitos_fuero/app/docs' + str(nombre_archivo)
    directorio = '../docs' + str(nombre_archivo)

    with open(directorio) as txt_file:
         read_lines = txt_file.readlines()
    
    apnd_list = []
    for data in read_lines:
        tupla = eval(data)
        apnd_list.append(tupla)
    #print('---- type(apnd_list) ', type(apnd_list))

    return apnd_list

####--------------------------------------------------------------------------------------------------
#### funcion con transaccion para guardar la informacion obtenida del archivo xlsx
def insert_data(conn_db, table_name, data_list):

    value = None

    #data_list = [(2018, 'INEGI Censo Nacional de Gobierno Seguridad Pública y Sistema Penitenciario Estatales 2019. SNIEG', 27, 'Tabasco', 6892), (2018, 'INEGI Censo Nacional de Gobierno Seguridad Pública y Sistema Penitenciario Estatales 2019. SNIEG', 28, 'Tamaulipas', 2408), (2018, 'INEGI Censo Nacional de Gobierno Seguridad Pública y Sistema Penitenciario Estatales 2019. SNIEG', 29, 'Tlaxcala', 7277), (2018, 'INEGI Censo Nacional de Gobierno Seguridad Pública y Sistema Penitenciario Estatales 2019. SNIEG', 30, 'Veracruz', 22381), (2018, 'INEGI Censo Nacional de Gobierno Seguridad Pública y Sistema Penitenciario Estatales 2019. SNIEG', 31, 'Yucatán', 59643), (2018, 'INEGI Censo Nacional de Gobierno Seguridad Pública y Sistema Penitenciario Estatales 2019. SNIEG', 32, 'Zacatecas', 645)]
    #print(' -- type(conn_db) ', type(conn_db))
    #print('---- leyendo los datos del archivo -- data_list ', data_list)

    try:
        #### abriendo el cursor para conectar a la base de datos
        conn_cursor = conn_db.cursor()

        #### iniciar la transaccion
        conn_cursor.execute('BEGIN')

        ####with conn_cursor:
        # crear la consulta para insertar en la tabla
        #cursor.execute("INSERT INTO table_name (column1, column2) VALUES (?, ?)", (value1, value2))
        insert_query = 'INSERT INTO ' + table_name + ' (anio, fuente, cve_ent, entidad_federativa, delitos_fuero_comun) VALUES (?, ?, ?, ?, ?)'
        #print('---- insert_query ', insert_query)
        #values = ('2020', 'INEGI asdfasdfasdfasdf', '1', 'Aguascalientes', '234')
        insert_values = data_list
        for data in data_list:
        #conn_cursor.executemany(insert_query, insert_values)
            conn_cursor.execute(insert_query, data)

            #### guardar todas las transacciones si todas son exitosas
            conn_cursor.execute('COMMIT')
        
        print('---- Se agregaron todas las transacciones!')
        value = True

    except:
        #### hacer rollback con las transacciones si ocurre algun error
        conn.execute('ROLLBACK')
        print('---- No se pudieron agregar las transacciones!')
        value = False

    #finally:
        #### cerrando el cursor y la conexion a base de datos
    #    conn_cursor.close()
    #    conn_db.close()
    
    return value

####--------------------------------------------------------------------------------------------------
#### en caso de que el archivo sea ejecutado directamente
if __name__ == '__main__':
    print('---- Iniciando insercion de datos!')

    #### llamando a funcion para crear/conectar la base de datos
    conn = conn_db()

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
    table_name = 'delitos'
    data_insert = insert_data(conn, table_name, read_file)
    #print('---- data_insert ', data_insert)

    #### llamando a funcion para mostrar la informacion guardada en la base de datos
    table_show = show_table(conn, table_name)
    print('---- table_show ', table_show)

    #### asigando el parametro de nombre de tabla y llamando a la funcion para insertar datos
    #table_name = 'delitos'
    #insert = insert_data(conn, table_name)
    print('---- Finalizando insercion de datos!')