# ==============================================================================
# PROYECTO DATALAB - ENTREGA 1: EXPLORADOR DE SPOTIFY
# Programación de Computadores - Universidad Nacional de Colombia
# ==============================================================================

def split_linea_csv(linea):
    """
    Función auxiliar: separa los campos de una línea de CSV respetando
    las comillas dobles (ej: "J Balvin, Pharrell Williams") sin librerías externas.
    """
    campos = []
    campo_actual = []
    dentro_de_comillas = False
    
    for caracter in linea:
        if caracter == '"':
            dentro_de_comillas = not dentro_de_comillas
        elif caracter == ',' and not dentro_de_comillas:
            campos.append("".join(campo_actual).strip())
            campo_actual = []
        else:
            campo_actual.append(caracter)
            
    campos.append("".join(campo_actual).strip())
    return campos


# ------------------------------------------------------------------------------
# FUNCIÓN 1: Carga y procesamiento del dataset
# Requisito: Cargar con open(), recorrer con bucles y procesar campos.
# ------------------------------------------------------------------------------
def cargar_datos(nombre_archivo):
    """
    Lee el archivo CSV de 50 filas usando open() y la función auxiliar.
    Convierte 'rank' y 'streams' a números (float/int).
    """
    datos = []
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()
        
        # Saltamos la primera línea (cabecera: title,rank,date,artist,url,region,chart,trend,streams)
        for i in range(1, len(lineas)):
            linea = lineas[i].strip()
            if linea:  # Omitir líneas vacías
                columna = split_linea_csv(linea)
                
                # Verificamos que la línea tenga las 9 columnas
                if len(columna) >= 9:
                    title = columna[0]
                    rank = int(columna[1])
                    date = columna[2]
                    artist = columna[3]
                    url = columna[4]
                    region = columna[5]
                    chart = columna[6]
                    trend = columna[7]
                    streams = float(columna[8])
                    
                    fila = [title, rank, date, artist, url, region, chart, trend, streams]
                    datos.append(fila)
                
    return datos


# ------------------------------------------------------------------------------
# FUNCIÓN 2: Funcionalidad Obligatoria 1 - Búsqueda por texto
# Requisito: Mostrar coincidencias y contar el total encontrado.
# ------------------------------------------------------------------------------
def buscar_registros(datos, termino_busqueda):
    """
    Busca coincidencias de texto en el título, artista, región o tendencia (trend).
    """
    termino = termino_busqueda.lower()
    coincidencias = []
    
    for fila in datos:
        title = fila[0].lower()
        artist = fila[3].lower()
        region = fila[5].lower()
        trend = fila[7].lower()
        
        if termino in title or termino in artist or termino in region or termino in trend:
            coincidencias.append(fila)
            
    print(f"\n--- Resultados para la búsqueda: '{termino_busqueda}' ---")
    if len(coincidencias) > 0:
        for reg in coincidencias:
            print(f"Puesto #{reg[1]} | Canción: {reg[0]} | Artista: {reg[3]} | Países: {reg[5]} | Streams: {int(reg[8]):,}")
    else:
        print("No se encontraron registros que coincidan con la búsqueda.")
        
    print(f"Se encontraron {len(coincidencias)} registros.")
    return len(coincidencias)


# ------------------------------------------------------------------------------
# FUNCIÓN 3: Funcionalidad Obligatoria 2 - Estadísticas Básicas
# Requisito: Máximo, mínimo y promedio usando bucles y acumuladores.
# ------------------------------------------------------------------------------
def calcular_estadisticas(datos, indice_columna, nombre_campo):
    """
    Calcula el valor máximo, mínimo y promedio de 'rank' o 'streams' sin funciones integradas.
    """
    if len(datos) == 0:
        print("No hay datos cargados.")
        return None

    # Inicializamos acumuladores con el primer registro
    primer_valor = datos[0][indice_columna]
    maximo = primer_valor
    minimo = primer_valor
    suma_total = 0.0
    cantidad = 0

    for fila in datos:
        valor = fila[indice_columna]
        suma_total = suma_total + valor
        cantidad = cantidad + 1
        
        if valor > maximo:
            maximo = valor
        if valor < minimo:
            minimo = valor

    promedio = suma_total / cantidad

    print(f"\n--- Estadísticas para el campo '{nombre_campo}' ---")
    print(f"Máximo: {maximo:,.2f}")
    print(f"Mínimo: {minimo:,.2f}")
    print(f"Promedio: {promedio:,.2f}")
    
    return {"maximo": maximo, "minimo": minimo, "promedio": promedio}


# ------------------------------------------------------------------------------
# FUNCIÓN 4: Funcionalidad Opcional - Filtrar por condición numérica
# Requisito: Mostrar registros donde un campo numérico supere un umbral.
# ------------------------------------------------------------------------------
def filtrar_por_condicion(datos, indice_columna, umbral, nombre_campo):
    """
    Filtra los registros cuyo valor de 'streams' supere un umbral o cuyo 'rank' sea superior/mejor.
    """
    filtrados = []
    for fila in datos:
        valor = fila[indice_columna]
        if valor > umbral:
            filtrados.append(fila)

    print(f"\n--- Canciones con {nombre_campo} mayor a {umbral:,.0f} ---")
    if len(filtrados) > 0:
        for reg in filtrados:
            print(f"Puesto #{reg[1]} | {reg[0]} - {reg[3]} | {nombre_campo}: {reg[indice_columna]:,.0f}")
    else:
        print("Ninguna canción cumple la condición.")

    print(f"Total de registros encontrados: {len(filtrados)}")
    return filtrados


# ------------------------------------------------------------------------------
# MENÚ INTERACTIVO DE CONSOLA
# ------------------------------------------------------------------------------
def menu():
    archivo = "spotify_pequeño.csv"
    
    try:
        datos = cargar_datos(archivo)
        print(f"Éxito: Se cargaron {len(datos)} canciones correctamente desde '{archivo}'.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'. Asegúrate de que esté en la misma carpeta que main.py.")
        return

    while True:
        print("\n==========================================")
        print("   DATALAB SPOTIFY - EXPLORADOR TOP 50    ")
        print("==========================================")
        print("1. Buscar registros por texto (Artista, Canción, Región o Tendencia)")
        print("2. Calcular estadísticas (Reproducciones/Streams o Ranking/Rank)")
        print("3. Filtrar canciones por un umbral numérico")
        print("4. Salir")
        
        opcion = input("Elija una opción (1-4): ").strip()

        if opcion == "1":
            termino = input("Ingrese el término a buscar (ej: Shakira, Chantaje, MOVE_UP, Argentina): ")
            buscar_registros(datos, termino)

        elif opcion == "2":
            print("\nCampos numéricos disponibles:")
            print("1. Reproducciones / Streams (Columna 8)")
            print("2. Posición en Top / Rank (Columna 1)")
            sub = input("Elija el campo (1 o 2): ").strip()
            
            if sub == "1":
                calcular_estadisticas(datos, 8, "Streams (Reproducciones)")
            elif sub == "2":
                calcular_estadisticas(datos, 1, "Rank (Posición)")
            else:
                print("Opción no válida.")

        elif opcion == "3":
            print("\nFiltrar por:")
            print("1. Reproducciones (Streams) mayores a un valor")
            print("2. Posición (Rank) mayor a un número")
            sub = input("Elija el campo (1 o 2): ").strip()
            
            if sub == "1":
                val = float(input("Mostrar canciones con reproducciones (Streams) mayores a: "))
                filtrar_por_condicion(datos, 8, val, "Streams")
            elif sub == "2":
                val = float(input("Mostrar canciones con Rank mayor a: "))
                filtrar_por_condicion(datos, 1, val, "Rank")
            else:
                print("Opción no válida.")

        elif opcion == "4":
            print("¡Gracias por usar DataLab Spotify! Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    menu()