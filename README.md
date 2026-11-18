# Gestión de Datos de Países en Python

**Trabajo Práctico Integrador — Programación 1**  
**Carrera:** Tecnicatura Universitaria en Programación a Distancia.

Aplicación de consola que permite gestionar países mediante listas, diccionarios, funciones y archivos CSV. Incluye una opción para importar datos desde la API del Banco Mundial.

Este README documenta el funcionamiento de `TPI_Programacion.py` y organiza los requisitos de la consigna. Los enlaces y datos académicos señalados como pendientes deben completarse antes de entregar.

## Índice

1. [Objetivo](#1-objetivo)
2. [Integrantes y participación](#2-integrantes-y-participación)
3. [Requisitos y ejecución](#3-requisitos-y-ejecución)
4. [Archivos y datos](#4-archivos-y-datos)
5. [Opciones del menú](#5-opciones-del-menú)
6. [Ejemplos de entradas y salidas](#6-ejemplos-de-entradas-y-salidas)
7. [Integración con la API del Banco Mundial](#7-integración-con-la-api-del-banco-mundial)
8. [Validaciones y errores](#8-validaciones-y-errores)
9. [Conceptos y organización del código](#9-conceptos-y-organización-del-código)
10. [Esquema de operaciones](#10-esquema-de-operaciones)
11. [Decisiones técnicas y conclusiones](#11-decisiones-técnicas-y-conclusiones)
12. [Entregables y enlaces obligatorios](#12-entregables-y-enlaces-obligatorios)
13. [Bibliografía y webgrafía](#13-bibliografía-y-webgrafía)

## 1. Objetivo

Gestionar información de países, realizar consultas y obtener indicadores básicos aplicando los contenidos de Programación 1:

- Listas y diccionarios para representar los registros.
- Funciones con responsabilidades diferenciadas.
- Condicionales y ciclos para controlar el menú y procesar los datos.
- Lectura y escritura de CSV.
- Búsquedas, filtros, ordenamientos y estadísticas.
- Validaciones y manejo de errores previstos.

La API complementa el proyecto como fuente de datos. La aplicación mantiene la lectura desde CSV solicitada por la consigna.

## 2. Integrantes y participación

| Integrante | Legajo | Distribución propuesta, a confirmar |
|---|---|---|
| Franco Martinez | 55215 | Carga y guardado CSV, estructura de datos y sincronización con la API. |
| Leandro Ortuvia | 676767 | Búsquedas, filtros y ordenamientos. |
| Arón Petersen | 55246 | Estadísticas, revisión de validaciones y documentación. |
| Los tres integrantes | — | Revisión del programa completo, conclusiones y presentación del video. |


**Datos académicos por completar:**

- Institución: UTN Sede Mendoza
- Comisión: 3
- Docente: Cintia Rigoni | Ramiro Hualpa

## 3. Requisitos y ejecución

- Python 3.6 o superior, compatible con la sintaxis utilizada. Se recomienda una versión vigente de Python 3.
- Una terminal o consola.
- Conexión a Internet únicamente para la opción de sincronización.
- No se requieren paquetes externos: todas las bibliotecas importadas pertenecen a Python.

Abrir la terminal en la carpeta donde está el programa y ejecutar:

```bash
python TPI_Programacion.py
```

Según la instalación, también puede utilizarse:

```bash
python3 TPI_Programacion.py
```

En Windows:

```bash
py TPI_Programacion.py
```

Al comenzar, se intenta cargar `datos/paises.csv`. Luego aparece el menú. Ingresar el número de una opción y seguir las indicaciones.

La opción **0** termina la ejecución.

### Primera ejecución

Si ya se cuenta con el CSV, colocarlo en la carpeta `datos`, dentro de la carpeta del programa.

Si no existe, hay dos alternativas:

1. Crear `datos/paises.csv` con el encabezado y registros válidos del apartado siguiente.
2. Ejecutar el programa y elegir **10** para descargar los datos iniciales. Confirmar con `s`; esta operación crea la carpeta y el CSV si no existen.

Un archivo ausente genera un aviso inicial. La sincronización puede realizarse desde el menú para obtener una nueva carga.

Para la entrega académica, el dataset base debe incluirse en el repositorio: no debe dependerse de la primera descarga del evaluador.

## 4. Archivos y datos

Estructura de entrega sugerida:

```text
proyecto/
├── TPI_Programacion.py
├── README.md
├── informe.pdf                 # Incorporar y verificar la versión final
└── datos/
    ├── paises.csv              # Incluir el dataset base en el repositorio
    └── paises_fuente.json      # Generado al sincronizar con la API
```

`informe.pdf` es el nombre propuesto para el documento académico; el programa no lo genera.

El JSON de procedencia se genera con la sincronización y no es obligatorio para leer un CSV manual.

### Formato del CSV

| Campo | Tipo en memoria | Regla |
|---|---|---|
| `nombre` | `str` | Texto no vacío y sin duplicados normalizados. |
| `poblacion` | `int` | Entero mayor o igual a 0. |
| `superficie` | `int` | Entero mayor o igual a 1, expresado en km². |
| `continente` | `str` | Un continente admitido por el programa. |

El encabezado debe tener exactamente estas columnas, en este orden:

```csv
nombre,poblacion,superficie,continente
```

Ejemplo reproducido de la consigna:

```csv
nombre,poblacion,superficie,continente
Argentina,45376763,2780400,América
Japón,125800000,377975,Asia
Brasil,213993437,8515767,América
Alemania,83149300,357022,Europa
```

Guardar el archivo en UTF-8. La lectura también acepta UTF-8 con BOM.

Los números del CSV se escriben sin separadores de miles.

Los continentes admitidos son:

- África.
- América.
- Asia.
- Europa.
- Oceanía.
- Antártida.

El programa no establece una cantidad fija de países: depende del CSV o de los registros que pueda procesar en la descarga.

Las altas y actualizaciones se guardan automáticamente. Para escribir se utiliza un archivo temporal y luego se reemplaza el CSV original. Este temporal no es una copia de seguridad histórica.

## 5. Opciones del menú

| Opción | Operación | Comportamiento |
|---|---|---|
| 1 | Agregar país | Solicita los cuatro campos, valida y guarda el registro. |
| 2 | Actualizar país | Busca por nombre completo y cambia población y superficie. |
| 3 | Buscar por nombre | Permite elegir coincidencia exacta o parcial. |
| 4 | Filtrar por continente | Devuelve los países del continente ingresado. |
| 5 | Filtrar por población | Solicita mínimo y máximo inclusivos. |
| 6 | Filtrar por superficie | Solicita mínimo y máximo inclusivos, en km². |
| 7 | Ordenar | Permite seleccionar nombre, población o superficie y ambos sentidos. |
| 8 | Mostrar estadísticas | Presenta extremos de población, promedios y conteos por continente. |
| 9 | Listar todos | Muestra la tabla de países cargados. |
| 10 | Sincronizar con API | Solicita confirmación y reemplaza los datos locales por la descarga procesada. |
| 0 | Salir | Finaliza el programa. |

Las búsquedas y comparaciones de nombres ignoran mayúsculas, tildes y espacios externos.

Actualizar requiere el nombre completo. Los filtros y ordenamientos no modifican el contenido del CSV.

## 6. Ejemplos de entradas y salidas

**Condición de estos ejemplos:** comenzar con los cuatro registros del apartado 4.

Los resultados cambian si se agregan, actualizan o sincronizan países. Las salidas de búsqueda, continente y estadísticas se comprobaron con el código adjunto y ese CSV de ejemplo.

### Búsqueda exacta

Entradas:

```text
Opción: 3
Nombre o fragmento: japon
1. Exacta / 2. Parcial: 1
```

Salida:

```text
Nombre                          Población   Superficie km²  Continente
Japón                         125,800,000          377,975  Asia
```

Para una búsqueda parcial, elegir el modo `2`. Con `ar` se encuentra Argentina dentro de esta muestra.

Si se ingresa `zzzz`, se muestra:

```text
No se encontraron países.
```

### Filtro por continente

Entradas:

```text
Opción: 4
Continente: america
```

Salida:

```text
Nombre                          Población   Superficie km²  Continente
Argentina                      45,376,763        2,780,400  América
Brasil                        213,993,437        8,515,767  América
```

### Filtros por rangos

- Opción **5**, mínimo `50000000` y máximo `150000000`: devuelve Japón y Alemania en el orden de la muestra.
- Opción **6**, mínimo `1` y máximo `400000`: devuelve Japón y Alemania por su superficie.

Los dos extremos se incluyen. Ingresar un máximo inferior al mínimo produce un mensaje de rango inválido.

### Ordenamiento

Elegir **7**, campo **1** —nombre— y sentido **1** —ascendente—.

El orden resultante es:

```text
Alemania
Argentina
Brasil
Japón
```

Con campo **2** —población— y sentido **2** —descendente—, el orden es:

```text
Brasil
Japón
Alemania
Argentina
```

### Estadísticas

Elegir **8** con el CSV de cuatro países, antes de modificarlo.

Los indicadores son:

```text
Mayor población: Brasil (213,993,437)
Menor población: Argentina (45,376,763)
Promedio de población: 117,079,875.00 habitantes
Promedio de superficie: 3,007,791.00 km²
```

El conteo por continente es:

| Continente | Cantidad |
|---|---|
| América | 2 |
| Asia | 1 |
| Europa | 1 |

Las comas separan miles y el punto indica decimales en la presentación numérica.

### Alta y actualización

Ejemplo de carga manual para demostrar el flujo. Sus valores no se presentan como datos actuales verificados:

```text
Opción: 1
Nombre del país: Chile
Población: 19000000
Superficie en km²: 756102
Continente: América
Operación realizada y guardada correctamente.
```

Después, con la opción **2**, ingresar:

```text
Nombre del país: Chile
Nueva población: 19500000
Nueva superficie en km²: 756102
```

Buscarlo con la opción **3** para comprobar el cambio.

Si Chile ya está cargado, la opción 1 rechaza el duplicado; en ese caso corresponde actualizarlo.

## 7. Integración con la API del Banco Mundial

La integración está dentro de **`TPI_Programacion.py`** y se activa con la opción **10**.

El proceso es el siguiente:

1. `_consultar_json_wb()` envía una petición HTTP GET con `urllib.request` y lee el JSON. Configura un tiempo de espera de 15 segundos por solicitud.
2. `importar_desde_world_bank()` consulta el catálogo de países en español y los indicadores `SP.POP.TOTL` —población— y `AG.SRF.TOTL.K2` —superficie—.
3. Se crean diccionarios por código de país para relacionar los datos recibidos.
4. Se omiten agregados identificados con región `NA` y registros sin datos utilizables.
5. Se asigna el continente mediante `REGION_A_CONTINENTE` y `EXCEPCIONES_CONTINENTE`.
6. Se redondean los valores numéricos con `round()`, se validan los registros y se guarda el nuevo CSV.
7. Se escribe `paises_fuente.json` y se actualiza la lista utilizada por el menú.

La consulta solicita los últimos valores no vacíos mediante `mrnev=1`.

**No fija un año común para todos los países e indicadores.** El campo `anio` del JSON registra el año de ejecución de la importación, no necesariamente el período de los datos.

El JSON también guarda la fuente y la huella SHA-256 del CSV.

Al iniciar, `mostrar_procedencia()` compara esa huella y avisa si el archivo fue modificado desde la última sincronización. La huella permite detectar cambios; no comprueba la exactitud estadística de los datos.

### Alcance de esta implementación

- Cada consulta solicita `per_page=400`; el código no recorre páginas adicionales. La descarga no garantiza un inventario mundial completo ni una cantidad fija de registros.
- Las regiones de la API se convierten a continentes con reglas locales y excepciones. Esa clasificación es una decisión del proyecto.
- Excluir agregados no equivale a verificar que todos los registros restantes sean países soberanos: el catálogo también puede contener economías o territorios.
- No se conserva el año individual de cada observación ni el valor anterior al redondeo.
- Si no se procesa ningún registro válido, se informa un error. Los registros descartados individualmente no se enumeran al usuario.

**La sincronización reemplaza el CSV y la lista actual, incluidas las altas o modificaciones manuales. Solicita confirmación, pero no crea respaldos automáticos. Copiar el CSV antes de confirmar.**

El programa puede seguir usándose sin Internet una vez que dispone de un CSV válido.

## 8. Validaciones y errores

- No se admiten campos vacíos ni nombres duplicados después de normalizarlos.
- Se exigen población entera no negativa y superficie entera positiva.
- Se validan continente, opciones del menú y rangos.
- Las entradas vacías o los números mal escritos se vuelven a solicitar cuando corresponden a las funciones de lectura.
- Una búsqueda o filtro sin coincidencias muestra un mensaje y permite continuar.
- El CSV debe contener el encabezado exacto.
- Se avisan filas incorrectas, duplicados, problemas de lectura y errores de comillas detectados por el lector.
- Si existen avisos de carga, pueden consultarse los registros recuperados, pero se bloquean altas y actualizaciones para evitar sobrescribir una lectura parcial.
- Corregir el CSV y reiniciar, o sincronizar con la API aceptando el reemplazo, permite obtener una nueva carga válida.
- Se informan errores de conexión previstos.
- El menú contempla fin de entrada y `Ctrl+C` durante su ejecución.

Ejemplos de mensajes:

```text
Error: opción inválida.
Error: el campo no puede estar vacío.
Error: ingrese un entero mayor o igual a 0.
Error: Ya existe un país con ese nombre.
```

Para una lista vacía, las estadísticas muestran:

```text
No hay países para calcular estadísticas.
```

## 9. Conceptos y organización del código

| Concepto solicitado | Aplicación en el programa |
|---|---|
| Listas | La variable `paises` reúne los registros; las consultas devuelven listas de resultados. |
| Diccionarios | Cada país relaciona las claves `nombre`, `poblacion`, `superficie` y `continente` con sus valores. También se usan para indicadores de la API y conteos. |
| Funciones | Separan lectura, validación, consultas, presentación y guardado. |
| Condicionales | `if` y `elif` seleccionan acciones y controlan opciones, límites y errores. |
| Estructuras repetitivas | `while` mantiene el menú y repite entradas; `for` recorre países y datos descargados. |
| Ordenamientos | `sorted()` genera una lista nueva; `key` elige el campo y `reverse` el sentido. |
| Estadísticas básicas | `min`, `max`, `sum` y `len` permiten obtener extremos y promedios; un diccionario acumula cantidades por continente. |
| Archivos CSV | `csv.DictReader` interpreta filas por encabezado y `csv.DictWriter` guarda los cuatro campos. |

El promedio se calcula como:

```text
promedio = suma de los valores / cantidad de países
```

Se evita dividir por cero.

Si varios países empatan en mayor o menor población, se muestran todos sus nombres.

Las estadísticas corresponden a la lista completa, no al último filtro mostrado.

### Funciones principales

| Responsabilidad | Funciones |
|---|---|
| Validación y comparación | `normalizar`, `continente_valido`, `validar_pais`. |
| Archivos y procedencia | `cargar_paises`, `guardar_paises`, `mostrar_procedencia`. |
| API | `_consultar_json_wb`, `importar_desde_world_bank`. |
| Altas y cambios | `agregar_pais`, `actualizar_pais`, `persistir_cambio`. |
| Consultas | `buscar_paises`, `filtrar_continente`, `filtrar_rango`, `ordenar_paises`. |
| Estadísticas y salida | `calcular_estadisticas`, `mostrar_estadisticas`, `mostrar_paises`. |
| Entradas y coordinación | `leer_texto`, `leer_entero`, `leer_opcion`, `ejecutar_opcion`, `main`. |

## 10. Esquema de operaciones

```text
INICIO
  |
  v
Leer CSV y validar registros
  |
  +--> Mostrar avisos y procedencia
  |    Si hubo avisos: bloquear altas y actualizaciones
  v
MENÚ <---------------------------------------------------+
  +-- 1 Agregar --> Validar --> Guardar CSV ---------------+
  +-- 2 Actualizar --> Buscar exacto --> Guardar CSV ------+
  +-- 3 Buscar --> Exacta/parcial --> Mostrar -------------+
  +-- 4/5/6 Filtrar --> Continente/rango --> Mostrar -------+
  +-- 7 Ordenar --> Campo/sentido --> Mostrar -------------+
  +-- 8 Estadísticas --> Calcular o avisar lista vacía -----+
  +-- 9 Listar --> Mostrar tabla -------------------------+
  +-- 10 Sincronizar --> Confirmar                        |
  |       +-- No --> Volver ------------------------------+
  |       +-- Sí --> API --> Validar y clasificar          |
  |                    --> Guardar CSV y JSON             |
  |                    --> Reemplazar lista --------------+
  +-- Error previsto --> Informar y continuar ------------+
  +-- 0 Salir --> FIN
```

Este esquema describe el código existente. Para cumplir el apartado académico, debe incorporarse también al informe PDF con sus explicaciones.

## 11. Decisiones técnicas y conclusiones

### Decisiones de implementación

- Un único archivo Python organiza la aplicación mediante funciones.
- La ruta del CSV se calcula desde `__file__`, por lo que no depende de la carpeta desde la que se abre la terminal.
- Las comparaciones normalizan texto, mientras que la presentación conserva el nombre guardado.
- Las altas y actualizaciones se preparan en una copia de los diccionarios; la lista principal se confirma después de guardar.
- La escritura CSV utiliza un temporal antes del reemplazo.
- La sincronización escribe después los metadatos: no existe una transacción conjunta con recuperación automática de ambos archivos.
- Las bibliotecas estándar evitan una instalación adicional de dependencias.

### Dificultades técnicas abordadas

El código contempla la conversión de texto a enteros, diferencias de tildes al buscar, datos vacíos o duplicados, CSV parcialmente recuperables y consultas sin resultados.

La API agrega la necesidad de unir información por códigos y adaptar regiones a continentes.

Estas soluciones pueden explicarse en el informe. Las experiencias personales y la distribución real del trabajo deben redactarlas o confirmarlas los integrantes.

### Reflexión grupal propuesta para revisión

Este trabajo permite conectar los temas de la materia dentro de una misma aplicación. La organización en funciones ayuda a seguir el recorrido de los datos y entender qué hace cada parte.

También muestra que validar entradas y cuidar el guardado es tan necesario como obtener una consulta correcta. La incorporación de una API requiere revisar qué significan los datos recibidos y qué limitaciones tienen antes de utilizarlos.

## 12. Entregables y enlaces obligatorios

### Repositorio y README

Repositorio indicado durante el desarrollo:

https://github.com/Frames2424/TPI-Programaci-n-1-2026/tree/main



## 13. Bibliografía y webgrafía

- Consigna suministrada: `Consigna_TPI_Prog-1.docx.pdf`, cuatro páginas. Fuente de requisitos y del CSV utilizado en los ejemplos.
- Código de referencia: `TPI_Programacion.py`. Fuente de la descripción del funcionamiento.
- [Python: estructuras de datos](https://docs.python.org/es/3/tutorial/datastructures.html).
- [Python: control de flujo y funciones](https://docs.python.org/es/3/tutorial/controlflow.html).
- [Python: ordenamientos](https://docs.python.org/es/3/howto/sorting.html).
- [Python: funciones incorporadas](https://docs.python.org/es/3/library/functions.html).
- [Python: módulo csv](https://docs.python.org/es/3/library/csv.html).
- [Python: urllib.request](https://docs.python.org/es/3/library/urllib.request.html).
- [Python: módulo json](https://docs.python.org/es/3/library/json.html).
- [Banco Mundial: documentación de la API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation).
- [Banco Mundial: población total](https://data.worldbank.org/indicator/SP.POP.TOTL).
- [Banco Mundial: superficie en km²](https://data.worldbank.org/indicator/AG.SRF.TOTL.K2).