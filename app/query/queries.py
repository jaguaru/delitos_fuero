####--------------------------------------------------------------------------------------------------
####    modulo para las funciones de leer xlsx, guardar y leer txt, guardar en base de datos,
####--------------------------------------------------------------------------------------------------
import sys
#### para poder importar el modulo create_database
sys.path.append('../database')

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
            tuple_values = ( 
                             anio := int(anio), 
                             fuente := str(fuente), 
                             cve_ent := int(cve_ent), 
                             entidad_federativa := str(entidad_federativa), 
                             delitos_fuero_comun := int(delitos_fuero_comun)
                            )
            
            #### agregando las tuplas a la lista
            apnd_datos.append(tuple_values)

    print('----------------------------------------------')
    print('  ----  ----  Se leyeron todos los datos!')
    print('----------------------------------------------')
    
    return apnd_datos

####--------------------------------------------------------------------------------------------------
#### funcion para leer el archivo txt y guardar los datos como tuplas en formato de texto
def save_txt_file(apnd_datos, formato_fecha):

    nombre_archivo = '/queries_' + formato_fecha + '.txt'
    directorio = '../docs' + str(nombre_archivo)

    try:
        print('----------------------------------------------')
        print('  ----  Guardando info!')
        print('----------------------------------------------')
        #### se crea el archivo en modo de escritura, si el archivo existe se sobrescribe
        with open(directorio, 'w', encoding='utf-8') as txt_file:
             #### creando el archivo txt para guardar las consultas
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
#### funcion para leer el archivo txt y retornar una tupla con los datos
def read_txt_file(formato_fecha):

    nombre_archivo = '/queries_' + formato_fecha + '.txt'
    directorio = '../docs' + str(nombre_archivo)

    #### abrir el archivo de texto y leer linea por linea
    with open(directorio) as txt_file:
         read_lines = txt_file.readlines()
    
    #### crear una variable de lista
    apnd_list = []
    #### leer las tuplas con un ciclo for
    for data in read_lines:
        #### convertir cada linea de texto en una tupla
        tupla = eval(data)
        #### agregar cada linea a la lista
        apnd_list.append(tupla)

    return apnd_list

####--------------------------------------------------------------------------------------------------
#### funcion con transaccion para guardar la informacion obtenida del archivo xlsx
def insert_data(conn_db, table_name, data_list):

    value = None

    try:
        #### abriendo el cursor para conectar a la base de datos
        conn_cursor = conn_db.cursor()

        #### iniciar la transaccion
        conn_cursor.execute('BEGIN')

        #### consulta para insertar en la tabla
        insert_query = 'INSERT INTO ' + table_name + ' (anio, fuente, cve_ent, entidad_federativa, delitos_fuero_comun) VALUES (?, ?, ?, ?, ?)'
        #### reasignacion de variable para almacenar la lista de tuplas
        insert_values = data_list

        for data in data_list:
            #### ejecutando la consulta con los valores
            conn_cursor.execute(insert_query, data)

            #### guardar todas las transacciones si todas son exitosas
            conn_cursor.execute('COMMIT')
        
        print('---- Se agregaron todas las transacciones!')
        value = True

    except:
        #### hacer rollback con las transacciones si ocurre algun error
        conn_cursor.execute('ROLLBACK')
        print('---- No se pudieron agregar las transacciones!')
        value = False

    return value

####--------------------------------------------------------------------------------------------------
#### en caso de que el archivo sea ejecutado directamente
if __name__ == '__main__':
    print('---- Iniciando insercion de datos!')

    #### llamando a funcion para crear/conectar la base de datos
    conn = conn_db()

    #### llamando a funcion para leer el archivo xlsx
    file_xlsx = read_xlsx_file()
    
    #### llamando a funcion para obtener la fecha actual
    fecha_actual = change_date_format()

    #### llamando a funcion para guardar el archivo txt
    save_txt = save_txt_file(file_xlsx, fecha_actual)

    #### llamando a funcion que retorna una lista de tuplas
    read_file = read_txt_file(fecha_actual)

    #### asigando el parametro de nombre de tabla y llamando a la funcion para insertar datos
    table_name = 'delitos'
    data_insert = insert_data(conn, table_name, read_file)

    #### llamando a funcion para mostrar la informacion guardada en la base de datos
    table_show = show_table(conn, table_name)
    print('---- table_show ', table_show)

    print('---- Finalizando insercion de datos!')