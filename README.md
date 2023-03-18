# Technical_Challenge_ML
Desafío técnico Mercado Libre

## Dependencias

* [Flask](https://flask.palletsprojects.com/en/2.2.x/)
* [requests](https://requests.readthedocs.io/en/latest/)
* [PyMongo](https://pymongo.readthedocs.io/en/stable/)

## Instalación [Linux]

Luego de clonar el repositorio, ubiquese en la carpeta del proyecto y cree un entorno virtual:

```
python3 -m venv venv
```

Una vez creado, active el entorno virtual:

```
. venv/bin/activate
```

Posteriormente, instale las dependencias:

```
pip install -e .
```

Para la base de datos, la imagen local se puede descargar en el [enlace](https://drive.google.com/file/d/1AAlm0bbjqFVKPjjhxfBb75kgEEB1ilGO/view?usp=sharing)


## Configuración del proyecto


El proyecto posee un archivo de configuración, para cambiar parámetros en su ejecución. Este archivo se encuentra en la ruta:

    app/config/config.ini
    
y su estructura es la siguiente:

    [reader]
    format=csv
    delimiter=,
    encoding=utf-8-sig
    newline=

    [file]
    filename=app/main/files/test.csv

    [processing]
    main_threads=1
    main_queue_size=2
    child_threads=2
    child_queue_size=4

    [database]
    connection_string=mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=MLChallengePython+0.0.1

El archivo está dividido por secciones, las cuales configuran una parte específica del proceso. 

* La sección `reader` configura la lectura del archivo, cambiando variables como el formato, el delimitador, el encoding, etc.
* La sección `file` especifica el nombre del archivo para su lectura.
* La sección `processing` especifica los hilos y el tamaño de la cola de procesos que se ejecutan
* La sección `database` contiene la string de conexión a la base de datos.

Es posible alterar el flujo y personalizarlo como se desee añadiendo más variables que se deseen en este archivo de configuración.

## Ejecución [Linux]


Cuando haya concluido el proceso de instalación y configuración, puede correr la aplicación con el comando:

```
flask --app app/main run --debug
```

La aplicación corre en el puerto 5000.


## Descripción del proyecto

### Estructura del directorio

    Technical_Challenge_ML
    ├── app                           
    |   ├── config                    # Archivos de configuración, Scripts de configuración de la aplicación
    |   ├── data                      # Scripts relacionados con modificación de datos.
    |   ├── database                  # Scripts relacionados con configuración de base de datos.
    |   ├── files                     # Folder de archivos para la lectura de data.
    |   ├── process                   # Scripts relacionados con procesamiento de data
    |   ├── services                  # Servicios de mercado libre
    |   ├── __init__.py               # Punto de entrada de la aplicación.
    |── README.md
    |── setup.py
    |── .gitignore

### Descripción del flujo

La aplicación implementa un servidor de Flask, donde se expone un endpoint para iniciar el proceso. Idealmente, el archivo debería ser subido por este endpoint mediante un dialogo de carga, utilizando un stream de datos para guardar el archivo en el disco o en la nube y posteriormente leerlo, sin embargo por motivos de tiempo no alcancé a realizar la modificación, y actualmente el archivo se está leyendo desde el disco (específicamente, la carpeta files).

Al realizar la petición

    curl --location 'http://127.0.0.1:5000/process_file'
    
Se encola el procesamiento de un archivo según el archivo de configuración, utilizando la variable `filename` para ubicar el archivo.

### Procesamiento de la data

El programa implementa un orquestador, el cual ejecuta tareas de lectura de archivo, consultas HTTP y escritura en base de datos de manera asíncrona para no bloquear el API. Una vez inicia la aplicación, se crea una cola de "Procesos principales", la cual está determinada por las variables `main_threads` y `main_queue_size`, donde `main_threads` determina el número de workers o hilos que van a estar trabajando en los procesos, y `main_queue_size` determina el número de procesos en simultaneo que pueden existir en ejecución al mismo tiempo. Todos los procesos que se encolen que superen el número de procesos en simultaneo, se encolarán para ejecutarse posteriormente una vez se libere espacio en la cola. La cola de "Procesos principales" se encarga de la lectura del archivo, la transformación de los datos para la ejecución de peticiones, y la creación de subprocesos para consultar las APIs de Mercado Libre.

Existe tambien una cola de "Procesos secundarios", que es administrada y ejecutada por los procesos de la primera cola. Es decir, si se están ejecutando 2 "Procesos Principales" (lectura de 2 archivos) simultaneamente, existirá para cada uno; una cola de "Procesos secundarios". Las variables que configuran dicha cola son `child_threads` y `child_queue_size`, y se comportan de la misma manera que la cola de "Procesos principales". Esta cola está encargada de consultar con la data suministrada por el proceso principal las APIs de Mercado Libre, la construcción del objeto a guardar en base de datos, y la escritura en la misma.

Un semáforo se encarga de limitar el proceso principal dependiendo de la cola secundaria. Una vez hay espacio disponible para iniciar otro proceso, se realiza la lectura de líneas del archivo hasta completar 20 o hasta encontrar un cambio en el `site` del archivo. La decisión de 20 líneas fue tomada con base en la documentación de mercado libre, donde se puede consultar el endpoint `/items?ids=id1,id2,...,id20` para un máximo de 20 ids en simultaneo para el mismo `site`.

Por lo tanto, la cola principal lee hasta 20 líneas o un cambio de `site`, construye el objeto para iniciar el procesamiento, y encola en la cola secundaria un nuevo proceso para trabajar las 20 líneas leídas. La cola secundaria consulta el APIs de `items`, y con la respuesta consulta la información requerida de las APIs `currencies`, `users` y `categories`, construye el objeto y lo guarda en la Base de datos.

Las colas están implementadas por la clase `Executor`, la cual se encuentra dentro de `app/main/process/executor.py`. Esta clase implementa los módulos `ThreadPoolExecutor` y `Semaphore` para cumplir con el comportamiento deseado.

### Servicios de Mercado Libre

Se estructuró un modelo de servicios utilizando un archivo json de configuración adicional llamado `map_url.json` (Ubicado en `/app/main/config`). Este archivo está encargado de plantear definiciones de los endpoints de Mercado Libre, de manera de que agregar un endpoint o modificarlo sea fácil y transparente. El modelo implementa la interfaz `Service`, la cual posee dos métodos para redefinir:

* `load_map_url` permite leer el archivo de configuración desde el scope principal del api, el cual se carga al lanzar el servidor. La idea del método es que pueda mapear las configuraciones realizadas en el archivo y definir el comportamiento y los atributos del servicio.

* `run` ejecuta la petición HTTP definida en el servicio, obteniendo la correspondiente respuesta según las configuraciones realizadas desde el `map_url.json`

La estructura del `map_url.json` es la siguiente:

    [
        {
            "name": "items",
            "url": "https://api.mercadolibre.com/items",
            "method": "GET",
            "attributes": "id,category_id,currency_id,seller_id,price,start_time"
        },
        {
            "name": "categories",
            "url": "https://api.mercadolibre.com/categories",
            "method": "GET",
            "attributes": "name"
        },
        {
            "name": "currencies",
            "url": "https://api.mercadolibre.com/currencies",
            "method": "GET",
            "attributes": "description"
        },
        {
            "name": "users",
            "url": "https://api.mercadolibre.com/users",
            "method": "GET",
            "attributes": "nickname"
        }
    ]
    
* El parámetro `name` determina el nombre del servicio. Este nombre se utiliza para identificar cada elemento del archivo y registrarlo como servicio posteriormente.
* `url` indica la ruta del servicio que se quiere consultar.
* `method` indica el método de la petición que se desea realizar.
* `attributes` es un componente adicionado basado en la documentación del API de mercado libre. En esta, se pueden configurar los valores que se desea obtener de cada una de las APIs en la respuesta, enviandolo como query param en la solicitud. Para este Factory, se requiere que el campo `attributes` esté definido, sin embargo es posible mutar la interfaz para definir servicios de manera que el parámetro no sea mandatorio y se pueda obtener la petición sin este filtro.

Cada uno de estos registros tiene un componente (dentro de la carpeta `app/main/services`) el cual implementa los métodos de la interfaz, de manera que se acomoden al formato especificado en la documentación de Mercado Libre. Se pueden incluir tantos servicios como se desee, adicionando el código de implementación junto con el correspondiente registro en `map_url.json`.


## Base de datos

Para el registro en MongoDB, se uso pyMongo como servicio de conexión. No se usó a mayores rasgos algún ORM o algoritmo, simplemente se ajustó la estructura de la colección para almacenar documentos conteniendo la información pedida. El programa tampoco tiene métodos de consulta o edición, sin embargo se pueden implementar fácilmente dentro del folder `database`.

La estructura de la base de datos quedó de la siguiente manera:

    ml_challenge_python               # Base de datos
    ├── ml-challenge-python           # Colección      
    
La estructura de los documentos, es la siguiente:

    {
        _id: ObjectId("6415156939cb67ed766cbdd3"),
        site: 'MLA',
        id: '742439189',
        price: 999,
        start_time: '2018-08-11T01:28:43.000Z',
        name: 'Otros',
        description: 'Peso argentino',
        nickname: 'MAXX2018',
        item_id_error: null,
        currency_id_error: null,
        category_id_error: null,
        seller_id_error: null
    },

Se agregaron flags de errores para las consultas a las APIs de Mercado Libre, de manera que si la petición falla se pueda identificar los documentos para los cuales falló. `db['ml-challenge-python'].find(item_id_error: true)` encuentra los documentos que fallaron por la consulta al API de items, e igualmente para las demás llaves, sin embargo al ser solicitudes dependientes de la existencia del item en el api, no se registraron campos con error en las otras consultas.

Para el registro de elementos, se agregó un índice en el campo `id`:

    db['ml-challenge-python'].createIndex( { "id": 1 }, { unique: true } )
    
Este índice se agregó de manera manual en la base de datos, y si no se agrega es posible que haya duplicidad de los ids para los archivos.

## Oportunidades de mejora

* Evidentemente falta un requerimiento y es la lectura del archivo por endpoint. Inclusive, hace falta una manera sencilla de controlar los nombres de archivo en local, dado que de momento están "quemados" en el archivo de configuración y no se pueden cambiar en runtime.

* Si bien el sistema de procesos es funcional, no se tiene un control real sobre el mismo. Falta la implementación de una colección en base de datos que permita mantener el seguimiento, junto con una implementación que permita el control de los mismos, para poder dar datos reales de estadísticas de tiempos de ejecución, optimización, etc.

* El api de endpoints se puede refinar para tener un mejor comportamiento.

* Se uso la librería requests, la cual no tiene capacidades asíncronas en las solicitudes. Si bien esto se resolvió mediante la ejecución de los subprocesos en paralelo, se puede migrar a otra librería que permita la funcionalidad asíncrona en las solicitudes.

* Se puede mostrar el resultado de los procesos en un dashboard desde frontend.

## Conclusiones finales

Espero cualquier realimentación que me puedan brindar, y si se requiere algo adicional, quedo pendiente. Muchas gracias por la oportunidad.

Juan David Alvarez Cano

