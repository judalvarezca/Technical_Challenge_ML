# Exámen teórico

## Procesos, hilos y corrutinas.

* Un caso en el que usarías procesos para resolver un problema y por qué.
Un ejemplo sería procesar una gran cantidad de datos, o un archivo muy grande. Los procesos tienen su propio stack de memoria, por lo que independizar el hilo general (por ejemplo, una API REST) del procesamiento del archivo será ideal para garantizar que el API funcione sin demoras independientemente del proceso, si no se satura la máquina.

* Un caso en el que usarías threads para resolver un problema y por qué.
Lo usaría para una tarea bloqueante que requiera poco espacio en memoria, dado que el hilo corre en el mismo espacio de memoria que la aplicación. Por ejemplo, realizar una serie de consultas a un API en secuencia (una dependiente de la otra).

* Un caso en el que usarías corrutinas y por qué.
Las usaría en un endpoint o un servicio que tenga muy alta concurrencia, de manera que puedan iniciar suspender y resumirlas dependiendo de la prioridad que requiera la aplicación. Por ejemplo, un gran numero de peticiones para web-scrapping


## Optimización de recursos del sistema operativo

Si tuvieras 1000000 de elementos y tuvieras que consultar para cada uno de ellos información en una API HTTP, ¿Cómo lo harías? Explicar

Para realizar la consulta, crearía corrutinas que permitan consultar de manera asíncrona cada elemento en el API. El uso de corrutinas permitirá lanzar peticiones sin esperar a que haya una respuesta previa. También, implementaría un limitador, de manera que pueda controlar el tiempo que transcurre entre la ejecución de una petición y otra, y finalmente un Semáforo que limite el número de peticiones que están activas. Esto permitirá que el sistema no se sobrecargue y tener un control de la ejecución de las solicitudes, mientras se optimiza la cantidad que se realizan y los tiempos muertos entre respuestas.


## Análisis de complejidad

* Dados 4 algoritmos A, B, C y D que cumplen la misma funcionalidad, con complejidades O(n^2), O(n^3), O(2^n) y O(n log n), respectivamente, ¿Cuál de los algoritmos favorecerías y cuál descartarías en principio? Explicar por qué.

Inicialmente descartaría el O(2^n), ya que es el que más operaciones requiere para ejecutar el proceso a mayor cantidad de datos, y por lo tanto el menos eficiente. Sin embargo, el O(n log n) puede ser más lento para cuando n tiene valores pequeños (n<100), por lo que en este caso sería preferible las otras soluciones.

* Asume que dispones de dos bases de datos para utilizar en diferentes problemas a resolver. La primera llamada AlfaDB tiene una complejidad de O(1) en consulta y O(n^2) en escritura. La segunda llamada BetaDB que tiene una complejidad de O(log n) tanto para consulta, como para escritura. ¿Describe en forma sucinta, qué casos de uso podrías atacar con cada una?

Usaría AlphaDB para casos donde se requiera lectura constante de la data, pero no se muten los datos con frecuencia. Usaría BetaDB para aplicaciones donde se deba guardar y mutar la data constantemente.

