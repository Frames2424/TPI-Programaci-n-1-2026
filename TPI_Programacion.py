"""TPI Programación 1: gestión de países con listas, diccionarios, CSV y API World Bank."""
import csv
import hashlib
import json
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / 'datos' / 'paises.csv'
CAMPOS = ['nombre', 'poblacion', 'superficie', 'continente']
CONTINENTES = ['África', 'América', 'Asia', 'Europa', 'Oceanía', 'Antártida']

REGION_A_CONTINENTE = {
    'LCN': 'América',  
    'NAC': 'América',  
    'ECS': 'Europa',   
    'EAS': 'Asia',     
    'SAS': 'Asia',     
    'MEA': 'Asia',     
    'SSF': 'África',   
}

EXCEPCIONES_CONTINENTE = {
    'AUS': 'Oceanía', 'NZL': 'Oceanía', 'FJI': 'Oceanía', 'PNG': 'Oceanía',
    'SLB': 'Oceanía', 'VUT': 'Oceanía', 'WSM': 'Oceanía', 'TON': 'Oceanía',
    'KIR': 'Oceanía', 'FSM': 'Oceanía', 'MHL': 'Oceanía', 'PLW': 'Oceanía',
    'NRU': 'Oceanía', 'TUV': 'Oceanía',
    'DZA': 'África', 'EGY': 'África', 'LBY': 'África', 'MAR': 'África',
    'TUN': 'África', 'DJI': 'África',
    'KAZ': 'Asia', 'KGZ': 'Asia', 'TJK': 'Asia', 'TKM': 'Asia', 'UZB': 'Asia',
    'ARM': 'Asia', 'AZE': 'Asia', 'GEO': 'Asia', 'TUR': 'Asia',
}


def normalizar(texto):
    """Compara texto sin distinguir mayúsculas, tildes ni espacios externos."""
    texto = unicodedata.normalize('NFD', texto.strip().casefold())
    return ''.join(letra for letra in texto if not unicodedata.combining(letra))


def continente_valido(texto):
    """Devuelve la escritura canónica del continente o informa el error."""
    for continente in CONTINENTES:
        if normalizar(texto) == normalizar(continente):
            return continente
    raise ValueError('Continente inválido. Use: ' + ', '.join(CONTINENTES))


def validar_pais(fila):
    """Valida un registro completo y convierte sus campos numéricos a enteros."""
    if set(fila) != set(CAMPOS):
        raise ValueError('Se requieren exactamente cuatro columnas.')
    if any(not isinstance(fila[campo], str) or not fila[campo].strip()
           for campo in CAMPOS):
        raise ValueError('No se permiten campos vacíos ni columnas faltantes.')
    pais = {campo: fila[campo].strip() for campo in CAMPOS}
    for campo in ['poblacion', 'superficie']:
        try:
            pais[campo] = int(pais[campo])
        except ValueError:
            raise ValueError(f'{campo.capitalize()} debe ser un entero.') from None
        minimo = 0 if campo == 'poblacion' else 1
        if pais[campo] < minimo:
            raise ValueError(f'{campo.capitalize()} debe ser mayor o igual a {minimo}.')
    pais['continente'] = continente_valido(pais['continente'])
    return pais


def _consultar_json_wb(url):
    """Realiza una petición GET a la API del Banco Mundial y parsea el JSON."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Python-TPI-Paises/1.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        datos = json.loads(resp.read().decode('utf-8'))
    if not isinstance(datos, list) or len(datos) < 2:
        raise ValueError('Respuesta inesperada de la API del Banco Mundial.')
    return datos[1]


def importar_desde_world_bank(ruta):
    """Descarga países, población y superficie desde la API del Banco Mundial."""
    print('Conectando con la API del Banco Mundial (esto puede demorar unos segundos)...')
    try:
        paises_raw = _consultar_json_wb(
            'https://api.worldbank.org/v2/es/country?format=json&per_page=400'
        )
        pop_raw = _consultar_json_wb(
            'https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&mrnev=1&per_page=400'
        )
        sup_raw = _consultar_json_wb(
            'https://api.worldbank.org/v2/country/all/indicator/AG.SRF.TOTL.K2?format=json&mrnev=1&per_page=400'
        )
    except (urllib.error.URLError, TimeoutError, ValueError) as error:
        raise ValueError(f'Error al conectar con el Banco Mundial: {error}') from None

    poblaciones = {
        item['countryiso3code']: item['value']
        for item in pop_raw if item.get('value') is not None
    }
    superficies = {
        item['countryiso3code']: item['value']
        for item in sup_raw if item.get('value') is not None
    }

    nuevos_paises = []
    for item in paises_raw:
        region_id = item.get('region', {}).get('id')
        if region_id == 'NA':
            continue

        iso3 = item.get('id')
        nombre = item.get('name', '').strip()
        pop = poblaciones.get(iso3)
        sup = superficies.get(iso3)

        if not nombre or pop is None or sup is None or sup < 1:
            continue

        continente = EXCEPCIONES_CONTINENTE.get(iso3) or REGION_A_CONTINENTE.get(region_id)
        if not continente:
            continue

        try:
            pais = validar_pais({
                'nombre': nombre,
                'poblacion': str(round(pop)),
                'superficie': str(round(sup)),
                'continente': continente,
            })
            if not buscar_paises(nuevos_paises, pais['nombre'], exacta=True):
                nuevos_paises.append(pais)
        except ValueError:
            continue

    if not nuevos_paises:
        raise ValueError('No se pudieron procesar países válidos desde la API.')

    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    guardar_paises(nuevos_paises, ruta)

    metadatos = ruta.with_name(ruta.stem + '_fuente.json')
    info_fuente = {
        'fuente': 'Banco Mundial API v2',
        'anio': datetime.now().year,
        'csv_sha256': hashlib.sha256(ruta.read_bytes()).hexdigest(),
    }
    metadatos.write_text(json.dumps(info_fuente, indent=2), encoding='utf-8')

    return nuevos_paises


def cargar_paises(ruta):
    """Lee CSV UTF-8: conserva filas válidas y devuelve avisos por las inválidas."""
    paises, avisos = [], []
    try:
        with open(ruta, encoding='utf-8-sig', newline='') as archivo:
            lector = csv.DictReader(archivo, strict=True)
            if lector.fieldnames != CAMPOS:
                return [], ['Encabezado inválido: se espera ' + ','.join(CAMPOS)]
            try:
                for fila in lector:
                    try:
                        pais = validar_pais(fila)
                        if buscar_paises(paises, pais['nombre'], exacta=True):
                            raise ValueError('Nombre de país duplicado.')
                        paises.append(pais)
                    except ValueError as error:
                        avisos.append(f'Línea {lector.line_num}: {error}')
            except csv.Error as error:
                avisos.append(f'CSV mal formado cerca de línea {lector.line_num}: {error}. '
                              'Se detuvo la lectura; se conservan registros anteriores.')
    except (OSError, UnicodeError) as error:
        avisos.append(f'No se pudo leer el archivo: {error}')
    return paises, avisos


def guardar_paises(paises, ruta):
    """Guarda primero en un temporal para evitar sobrescribir un CSV incompleto."""
    ruta = Path(ruta)
    temporal = ruta.with_name(ruta.name + '.tmp')
    try:
        with open(temporal, 'w', encoding='utf-8', newline='') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows(paises)
        temporal.replace(ruta)
    finally:
        if temporal.exists():
            temporal.unlink()


def buscar_paises(paises, nombre, exacta=False):
    """Busca por nombre completo o por una parte del nombre."""
    buscado = normalizar(nombre)
    if not buscado:
        raise ValueError('La búsqueda no puede estar vacía.')
    if exacta:
        return [p for p in paises if normalizar(p['nombre']) == buscado]
    return [p for p in paises if buscado in normalizar(p['nombre'])]


def agregar_pais(paises, fila):
    """Agrega un país validado, siempre que su nombre no esté registrado."""
    pais = validar_pais(fila)
    if buscar_paises(paises, pais['nombre'], exacta=True):
        raise ValueError('Ya existe un país con ese nombre.')
    paises.append(pais)


def actualizar_pais(paises, nombre, poblacion, superficie):
    """Actualiza únicamente población y superficie de una coincidencia exacta."""
    encontrados = buscar_paises(paises, nombre, exacta=True)
    if not encontrados:
        raise ValueError('No se encontró el país.')
    pais = encontrados[0]
    nuevo = validar_pais({**pais, 'poblacion': str(poblacion),
                         'superficie': str(superficie)})
    pais.update(nuevo)


def filtrar_continente(paises, continente):
    """Selecciona los países del continente indicado."""
    continente = continente_valido(continente)
    return [p for p in paises if p['continente'] == continente]


def filtrar_rango(paises, campo, minimo, maximo):
    """Aplica un rango inclusivo de población o superficie."""
    if campo not in ['poblacion', 'superficie']:
        raise ValueError('Campo de filtro inválido.')
    piso = 0 if campo == 'poblacion' else 1
    if minimo < piso or maximo < minimo:
        raise ValueError('Rango inválido: revise mínimo y máximo.')
    return [p for p in paises if minimo <= p[campo] <= maximo]


def ordenar_paises(paises, campo, descendente=False):
    """Devuelve una lista ordenada sin modificar el orden de el orden original."""
    if campo not in ['nombre', 'poblacion', 'superficie']:
        raise ValueError('Campo de ordenamiento inválido.')
    if campo == 'nombre':
        return sorted(paises, key=lambda p: normalizar(p['nombre']), reverse=descendente)
    return sorted(paises, key=lambda p: p[campo], reverse=descendente)


def calcular_estadisticas(paises):
    """Calcula extremos, promedios y conteos; contempla el dataset vacío y empates."""
    if not paises:
        return None
    mayor = max(p['poblacion'] for p in paises)
    menor = min(p['poblacion'] for p in paises)
    cantidades = {}
    for pais in paises:
        continente = pais['continente']
        cantidades[continente] = cantidades.get(continente, 0) + 1
    return {
        'mayor': [p['nombre'] for p in paises if p['poblacion'] == mayor],
        'menor': [p['nombre'] for p in paises if p['poblacion'] == menor],
        'poblacion_mayor': mayor, 'poblacion_menor': menor,
        'promedio_poblacion': sum(p['poblacion'] for p in paises) / len(paises),
        'promedio_superficie': sum(p['superficie'] for p in paises) / len(paises),
        'por_continente': cantidades,
    }


def leer_texto(mensaje):
    """Repite la entrada hasta obtener un texto no vacío."""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print('Error: el campo no puede estar vacío.')


def leer_entero(mensaje, minimo=0):
    """Solicita un entero con límite inferior y recupera errores de escritura."""
    while True:
        try:
            numero = int(input(mensaje))
            if numero < minimo:
                raise ValueError
            return numero
        except ValueError:
            print(f'Error: ingrese un entero mayor o igual a {minimo}.')


def leer_opcion(mensaje, opciones):
    """Controla que la opción pertenezca al menú ofrecido."""
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones:
            return opcion
        print('Error: opción inválida.')


def mostrar_paises(paises):
    """Muestra una tabla y comunica explícitamente si no hubo resultados."""
    if not paises:
        print('No se encontraron países.')
        return
    print(f"{'Nombre':25} {'Población':>15} {'Superficie km²':>16}  Continente")
    for pais in paises:
        print(f"{pais['nombre']:25} {pais['poblacion']:>15,} "
              f"{pais['superficie']:>16,}  {pais['continente']}")


def mostrar_estadisticas(paises):
    """Presenta los indicadores calculados con unidades y dos decimales."""
    datos = calcular_estadisticas(paises)
    if datos is None:
        print('No hay países para calcular estadísticas.')
        return
    print('Mayor población:', ', '.join(datos['mayor']), f"({datos['poblacion_mayor']:,})")
    print('Menor población:', ', '.join(datos['menor']), f"({datos['poblacion_menor']:,})")
    print(f"Promedio de población: {datos['promedio_poblacion']:,.2f} habitantes")
    print(f"Promedio de superficie: {datos['promedio_superficie']:,.2f} km²")
    for continente, cantidad in sorted(datos['por_continente'].items()):
        print(f'{continente}: {cantidad} países')


def persistir_cambio(paises, candidatos, ruta, permitir_guardado):
    """Confirma cambios en memoria solo si pudieron guardarse en disco."""
    if not permitir_guardado:
        raise ValueError('Edición bloqueada: corrija el CSV y reinicie para evitar perder filas.')
    guardar_paises(candidatos, ruta)
    paises[:] = candidatos
    print('Operación realizada y guardada correctamente.')


def ejecutar_opcion(opcion, paises, ruta, permitir_guardado):
    """Coordina las entradas de cada opción y delega el procesamiento."""
    if opcion in ['1', '2']:
        if not permitir_guardado:
            raise ValueError('Edición bloqueada: corrija los avisos del CSV y reinicie.')
        candidatos = [p.copy() for p in paises]
        nombre = leer_texto('Nombre del país: ')
        if opcion == '1':
            fila = {'nombre': nombre,
                    'poblacion': str(leer_entero('Población: ')),
                    'superficie': str(leer_entero('Superficie en km²: ', 1)),
                    'continente': leer_texto('Continente: ')}
            agregar_pais(candidatos, fila)
        else:
            if not buscar_paises(candidatos, nombre, exacta=True):
                raise ValueError('No se encontró el país.')
            poblacion = leer_entero('Nueva población: ')
            superficie = leer_entero('Nueva superficie en km²: ', 1)
            actualizar_pais(candidatos, nombre, poblacion, superficie)
        persistir_cambio(paises, candidatos, ruta, permitir_guardado)
    elif opcion == '3':
        nombre = leer_texto('Nombre o fragmento: ')
        modo = leer_opcion('1. Exacta / 2. Parcial: ', ['1', '2'])
        mostrar_paises(buscar_paises(paises, nombre, modo == '1'))
    elif opcion == '4':
        mostrar_paises(filtrar_continente(paises, leer_texto('Continente: ')))
    elif opcion in ['5', '6']:
        campo = 'poblacion' if opcion == '5' else 'superficie'
        piso = 0 if campo == 'poblacion' else 1
        minimo = leer_entero('Mínimo inclusive: ', piso)
        maximo = leer_entero('Máximo inclusive: ', piso)
        mostrar_paises(filtrar_rango(paises, campo, minimo, maximo))
    elif opcion == '7':
        campos = {'1': 'nombre', '2': 'poblacion', '3': 'superficie'}
        campo = campos[leer_opcion('1. Nombre / 2. Población / 3. Superficie: ', campos)]
        orden = leer_opcion('1. Ascendente / 2. Descendente: ', ['1', '2'])
        mostrar_paises(ordenar_paises(paises, campo, orden == '2'))
    elif opcion == '8':
        mostrar_estadisticas(paises)
    elif opcion == '9':
        mostrar_paises(paises)
    elif opcion == '10':
        confirmar = leer_opcion('Esto reemplazará los datos locales con los del Banco Mundial. ¿Continuar? (s/n): ', ['s', 'n', 'S', 'N'])
        if confirmar.lower() == 's':
            nuevos = importar_desde_world_bank(ruta)
            paises[:] = nuevos
            print(f'¡Listo! Se descargaron y guardaron {len(paises)} países desde la API.')
            return True
    return permitir_guardado


def mostrar_procedencia(ruta):
    """Informa la fuente y detecta cambios manuales posteriores a la importación."""
    ruta = Path(ruta)
    metadatos = ruta.with_name(ruta.stem + '_fuente.json')
    if not metadatos.exists():
        return
    try:
        datos = json.loads(metadatos.read_text(encoding='utf-8'))
        if not isinstance(datos, dict):
            raise ValueError('Metadatos inválidos.')
        if hashlib.sha256(ruta.read_bytes()).hexdigest() == datos.get('csv_sha256'):
            print(f"Fuente: Banco Mundial, año {datos.get('anio')}. "
                  'Continentes asignados por el proyecto.')
        else:
            print('El CSV tiene cambios posteriores a la importación del Banco Mundial; '
                  'consulte los metadatos para conocer la versión importada.')
    except (OSError, ValueError):
        print('Aviso: no se pudo verificar la procedencia; se usará el CSV disponible.')


def main():
    """Carga los datos y mantiene el menú activo hasta elegir salir."""
    paises, avisos = cargar_paises(ARCHIVO)
    for aviso in avisos:
        print('Aviso:', aviso)
    permitir_guardado = not avisos
    print(f'Se cargaron {len(paises)} países.')
    mostrar_procedencia(ARCHIVO)
    try:
        while True:
            print('\nGESTIÓN DE PAÍSES\n1. Agregar país\n2. Actualizar población y superficie'
                  '\n3. Buscar por nombre\n4. Filtrar por continente'
                  '\n5. Filtrar por población\n6. Filtrar por superficie'
                  '\n7. Ordenar\n8. Estadísticas\n9. Listar todos'
                  '\n10. Sincronizar con API del Banco Mundial\n0. Salir')
            opcion = leer_opcion('Opción: ', [str(n) for n in range(11)])
            if opcion == '0':
                print('Hasta luego.')
                break
            try:
                permitir_guardado = ejecutar_opcion(opcion, paises, ARCHIVO, permitir_guardado)
            except (ValueError, OSError) as error:
                print(f'Error: {error}')
    except (EOFError, KeyboardInterrupt):
        print('\nEntrada interrumpida. Los cambios confirmados ya están guardados.')


if __name__ == '__main__':
    main()