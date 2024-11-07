import openpyxl


def leer_y_modificar_excel(archivo_excel):
    # Cargar el archivo de Excel
    libro = openpyxl.load_workbook(archivo_excel)
    hoja = libro.active  # Usamos la hoja activa

    # Crear el diccionario
    diccionario = {}

    # Iterar sobre todas las filas y columnas de la hoja (empezando desde la segunda fila si hay cabecera)
    for fila in hoja.iter_rows(min_row=2):  # Recorremos cada fila desde la segunda
        clave = fila[0].value  # Columna 0 (clave)
        valor_col_6 = fila[6].value  # Columna 6
        valor_col_8 = fila[8].value  # Columna 8

        # Sumar 1 a cada columna que contenga un número

        # Asegurarnos de que la clave no sea None y convertirla a cadena
        if clave:
            clave_str = str(clave)  # Convertir la clave a cadena

            # Verificar si la clave contiene .HH, .HI, .LL, .LO
            if any(sufijo in clave_str for sufijo in ['.HH', '.HI', '.LL', '.LO']):
                diccionario[clave_str] = (valor_col_6, valor_col_8)

    # Guardar los cambios en el archivo Excel
    #libro.save(archivo_excel)

    return diccionario


"""# Ejemplo de uso
archivo_excel = r'C:\Emulation\HMIscreensYOKOGAWA\Source\CAMSAlm-CENTUM.xlsx'
diccionario_resultante = leer_y_modificar_excel(archivo_excel)
r celda in fila:
            if isinstance(celda.value, (int, float)):  # Si es número (int o float)
                celda.value += 1
# Imprimir el diccionario resultante
for clave, valores in diccionario_resultante.items():
    print(f"{clave}: {valores}")"""