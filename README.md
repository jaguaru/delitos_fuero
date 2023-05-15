Delitos del fuero comun - Prueba Tecnica ETL
==============================================================


Descargar Repositorio:
----------------------

    $ git clone https://github.com/jaguaru/delitos_fuero.git


Configuracion del entorno virtual:
----------------------------------

Abrir el directorio delitos_fuero

    $ cd delitos_fuero-main

Crear el directorio para el entorno virtual
    
    $ mkdir vserver

Crear el entorno virtual
    
    $ virtualenv -p python3 vserver

Activar el entorno virtual

    $ source vserver/bin/activate

Entorno virtual activado
    
    (vserver) $


Ejecutar el script para la extracción y carga de datos
--------------------------------

Abrir el directorio app/

    (vserver) $ cd app

Instalar la paqueteria

    (vserver) $ pip install -r requirements.txt

Abrir la carpeta script/
    
    (vserver) $ cd script

Ejecutar el script data_script.py

    (vserver) $ python3 data_script.py

Respuesta del script ejecutado

    $---- Iniciando insercion de datos!
    $.......  Base de datos creada!
    $**** Exception! - Error:  no such table: delitos
    $.......  Tabla eliminada!
    $.......  Tabla creada!
    $----------------------------------------------
    $  ----  ----  Se leyeron todos los datos!
    $----------------------------------------------
    $----------------------------------------------
    $  ----  Guardando info!
    $----------------------------------------------
    $----------------------------------------------
    $  ----   Se guardo el archivo txt!
    $----------------------------------------------
    $---- Se agregaron todas las transacciones!
    $---- Finalizando insercion de datos!


Ejecutar Pylint
--------------------------------

Abrimos la carpeta script

    (vserver) $ cd script

Ejecutamos pylint en el script data_script.py

    (vserver) $ pylint data_script.py

Respuesta de pylint

    $************* Module data_script
    $data_script.py:8:0: C0301: Line too long (109/100) (line-too-long)
    $data_script.py:11:0: C0301: Line too long (102/100) (line-too-long)
    $data_script.py:26:0: C0303: Trailing whitespace (trailing-whitespace)
    $data_script.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    $data_script.py:7:0: E0401: Unable to import 'create_database' (import-error)
    $data_script.py:7:0: C0413: Import "from create_database import conn_db, create_table" should be placed at the top of the module (wrong-import-position)
    $data_script.py:8:0: E0401: Unable to import 'queries' (import-error)
    $data_script.py:8:0: C0413: Import "from queries import read_xlsx_file, change_date_format, save_txt_file, read_txt_file, insert_data, $show_table" should be placed at the top of the module (wrong-import-position)
    $data_script.py:20:4: C0103: Constant name "table_name" doesn't conform to UPPER_CASE naming style (invalid-name)

    $------------------------------------------------------------------
    $Your code has been rated at 0.00/10 (previous run: 1.05/10, -1.05)
