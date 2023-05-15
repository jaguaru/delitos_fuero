####--------------------------------------------------------------------------------------------------
####    modulo para crear/conectar a la base de datos y crear la tabla
####--------------------------------------------------------------------------------------------------
import sqlite3


####--------------------------------------------------------------------------------------------------
#### funcion para crear la base de datos y hacer la conexion
def conn_db():

    conn = None

    try:
        #### creando la base de datos y el objeto de conexion
        conn = sqlite3.connect('../database/data_crimes.db')
        message = '.......  Base de datos creada!'
        print(message)

    except:
        #### excepcion en caso de error, se asigna "None" a la variable conn y se envia mensaje
        conn = None
        message = '.......  No se pudo crear la base de datos!'
        print(message)
    
    return conn

####--------------------------------------------------------------------------------------------------
#### funcion para ver el contenido de una tabla
def show_table(conn, table_name):

    result = None

    try:
        #### abriendo el cursor para conectar a la base de datos
        cursor = conn.cursor()
        #### creando la consulta con el nombre de la tabla
        query = 'SELECT * FROM ' + str(table_name)
        #### ejecutando y llamando todos los resultados de la consulta
        cursor.execute(query)
        result = cursor.fetchall()
    
    #### obteniendo la excepcion y guardandola en la variable "error"
    except sqlite3.OperationalError as error:
        result = None
        #### enviando un mensaje con el error
        print('**** Exception! - Error: ', error)

    return result

####--------------------------------------------------------------------------------------------------
#### funcion para checar si la tabla existe, si existe el resultado es True de lo contrario envia False
def check_table_exist(conn, table_name):

    value = None

    try:
        #### abriendo el cursor para conectar a la base de datos
        cursor = conn.cursor()
        #### creando la consulta con el nombre de la tabla
        query = 'SELECT * FROM ' + str(table_name)

        #### ejecutando y llamando una fila de la consulta
        cursor.execute(query)
        #### asignando a una variable el resultado de la consulta
        result = cursor.fetchone()        
:
        #### verificar si la tabla existe, esta vacia o tiene datos
        if result:
            value = True
            print('.......  La tabla existe y tiene datos!')
        
        if not result:
            value = False
            print('.......  La tabla existe y esta vacia!')

    
    #### obteniendo la excepcion y guardandola en la variable "error"
    except sqlite3.OperationalError as error:
        #### retorna el valor None si hay una excepcion
        value = None
        #### enviando un mensaje con el error
        print('**** Exception! - Error: ', error)

    return value

####--------------------------------------------------------------------------------------------------
#### funcion para crear la tabla
def create_table(conn, table_name):

    #### nombres de las columnas del archivo de excel:
    #### (AÑO, Fuente, CVE_ENT, Entidad_Federativa, Delitos_fuero_comun)

    table_name = str(table_name)

    try:
        #### abriendo el cursor para conectar a la base de datos
        cursor = conn.cursor()

        #### llamar a funcion "check_table_exist" la tabla "delitos"
        table_exist = check_table_exist(conn, table_name)
        
        #### si la table no tiene datos se elimina
        if not table_exist:
            #### eliminar la base de datos "delitos", si existe
            query = 'DROP TABLE IF EXISTS ' + table_name
            #### ejecutando la consulta
            cursor.execute(query)

            message = '.......  Tabla eliminada!'
            print(message)

            #### crear la tabla "delitos", con los tipos de datos correspondientes
            query = 'CREATE TABLE ' + table_name + ' ' + '''
                                (id INTEGER PRIMARY KEY,
                                anio INTEGER,
                                fuente TEXT,
                                cve_ent INTEGER,
                                entidad_federativa TEXT,
                                delitos_fuero_comun INTEGER)'''
            cursor.execute(query)
            message = '.......  Tabla creada!'
            print(message)
        
        #### guardar los cambios con un "commit"
        conn.commit()
            
        #### retorna el valor True si la tabla de crea de forma exitosa
        value = True

    except sqlite3.OperationalError as error:
        #### retorna el valor None si hay una excepcion
        value = None
        #### enviando un mensaje con el error
        print('**** Exception! - Error: ', error)

    return value


####--------------------------------------------------------------------------------------------------
#### en caso de que el archivo sea ejecutado directamente
if __name__ == '__main__':
    print('---- Iniciando creacion de base de datos!')
    #### llamando a la funcion para crear/conectar la base de datos
    conn = conn_db()
    #### asigando el parametro de nombre de tabla y llamando a la funcion crear tabla
    table_name = 'delitos'
    create = create_table(conn, table_name)
    print('---- Finalizando creacion de base de datos!')

