Delitos del fuero comun - Prueba Tecnica ETL
==============================================================


Descargar Repositorio:
----------------------

    $ git clone https://github.com/jaguaru/delitos_fuero.git


Configuracion del entorno virtual:
----------------------------------

Abrir el directorio kubernetes

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
    
    $ cd delitos_fuero

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
