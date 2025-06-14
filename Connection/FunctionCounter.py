"""import xml.etree.ElementTree as ET
import os
directorio = (r"C:\Emulation\HMIscreensYOKOGAWA")

callWindow = 0
for archivo in os.listdir(directorio):
    if archivo.startswith('PRO-') and archivo.endswith('.xaml'):

        point = archivo.find('.')
        ruta_archivo = os.path.join(directorio, archivo)
        tree1 = ET.parse(ruta_archivo)
        root1 = tree1.getroot()

        for child in root1:
            tag = child.tag
            if tag.endswith("TouchTarget") or tag.endswith("PushButton"):
                for funct in child.findall(
                        './/{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.FunctionLink.Control;assembly'
                        '=Yokogawa.IA.iPCS.Platform.View.Graphic.FunctionLink.Control'
                        '}FunctionLinkControlCommandParameter'):
                    print(funct.attrib.get("FunctionAndParameter", "") +  "              " + str(archivo[:point]))





import json
import pyodbc
import os
import pandas as pd

def load_units_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Crear un diccionario donde la clave es el nombre del tag y el valor es la unidad
    units = {tag_name: tag_info['Unit'] for tag_name, tag_info in data.items()}
    return units

def generate_units_json():
    # Ruta de los archivos .mdb
    path = r'C:\Emulation\HMIscreensYOKOGAWA\Source'

    # Archivos .mdb que comienzan con 'FCS'
    files = [f for f in os.listdir(path) if f.endswith('.mdb') and f.startswith('FCS')]

    # Diccionario para almacenar los resultados
    results_dict = {}

    for file in files:
        # Conectar a la base de datos
        conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + os.path.join(path, file)
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Ejecutar la consulta
        """"query =" '''
        SELECT ElemName, UnitID
        FROM ElemTbl
        WHERE WindowName LIKE 'PRO%';
        '''"""
        query = '''
                SELECT ElemName, UnitID
                FROM ElemTbl;
                '''
        cursor.execute(query)

        # Obtener los resultados y agregarlos al diccionario
        for row in cursor.fetchall():
            elem_name = row.ElemName
            unit_id = row.UnitID
            if elem_name not in results_dict:
                results_dict[elem_name] = {'UnitID': unit_id, 'Unit': None}  # Inicializar sin unidad

        # Cerrar la conexión
        cursor.close()
        conn.close()

    # Leer la tabla UnitTbl del archivo PjtRef.mdb
    pjt_ref_file = 'PjtRef.mdb'
    pjt_ref_path = os.path.join(path, pjt_ref_file)
    conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + pjt_ref_path
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Ejecutar la consulta para obtener UnitID y Unit
    query = '''
    SELECT UnitID, Unit
    FROM UnitTbl;
    '''
    cursor.execute(query)

    # Crear un DataFrame con la tabla UnitTbl
    unit_tbl_df = pd.DataFrame.from_records(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

    # Cerrar la conexión
    cursor.close()
    conn.close()

    # Actualizar el diccionario con las unidades
    for _, row in unit_tbl_df.iterrows():
        unit_id = row['UnitID']
        unit = row['Unit']
        for tag, info in results_dict.items():
            if info['UnitID'] == unit_id:
                info['Unit'] = unit

    # Eliminar las entradas con unidad None o "(None)"
    results_dict = {tag: info for tag, info in results_dict.items() if info['Unit'] not in [None, "(None)"]}

    # Guardar el diccionario en un archivo JSON
    json_file_path = r'C:\Emulation\HMIscreensYOKOGAWA\Source\results_with_units.json'
    with open(json_file_path, 'w') as f:
        json.dump(results_dict, f, indent=4)

    print("Diccionario guardado en 'results_with_units.json'")

    # Cargar y mostrar los resultados
    units = load_units_from_json(json_file_path)
    return units

# Llama a esta función para generar el archivo JSON y mostrar los resultados
units = generate_units_json()
print("Unidades cargadas desde el archivo JSON:")
for tag, unit in units.items():
    print(f"Tag: {tag}, Unidad: {unit}")"""

import json
import pyodbc
import os
import pandas as pd

def load_units_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Crear un diccionario donde la clave es el nombre del tag y el valor es un diccionario con la unidad, SH y SL
    units = {tag_name: {'Unit': tag_info['Unit'], 'SH': tag_info.get('SH'), 'SL': tag_info.get('SL'), 'Comment': tag_info.get('Comment')} for tag_name, tag_info in data.items()}
    return units

def generate_units_json():
    # Ruta de los archivos .mdb
    path = r'C:\Emulation\HMIscreensYOKOGAWA\Source'

    # Archivos .mdb que comienzan con 'FCS'
    files = [f for f in os.listdir(path) if f.endswith('.mdb') and f.startswith('FCS')]

    # Diccionario para almacenar los resultados
    results_dict = {}

    for file in files:
        # Conectar a la base de datos
        conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + os.path.join(path, file)
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Ejecutar la consulta incluyendo SH y SL
        query = '''
                SELECT ElemName, UnitID, SH, SL, Comment
                FROM ElemTbl;
                '''
        cursor.execute(query)

        # Obtener los resultados y agregarlos al diccionario
        for row in cursor.fetchall():
            elem_name = row.ElemName
            unit_id = row.UnitID
            sh_value = row.SH
            sl_value = row.SL
            comment_value = row.Comment
            if elem_name not in results_dict:
                results_dict[elem_name] = {'UnitID': unit_id, 'Unit': None, 'SH': sh_value, 'SL': sl_value, 'Comment': comment_value}  # Inicializar sin unidad y añadir SH y SL

        # Cerrar la conexión
        cursor.close()
        conn.close()

    # Leer la tabla UnitTbl del archivo PjtRef.mdb
    pjt_ref_file = 'PjtRef.mdb'
    pjt_ref_path = os.path.join(path, pjt_ref_file)
    conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + pjt_ref_path
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Ejecutar la consulta para obtener UnitID y Unit
    query = '''
    SELECT UnitID, Unit
    FROM UnitTbl;
    '''
    cursor.execute(query)

    # Crear un DataFrame con la tabla UnitTbl
    unit_tbl_df = pd.DataFrame.from_records(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

    # Cerrar la conexión
    cursor.close()
    conn.close()

    # Actualizar el diccionario con las unidades
    for _, row in unit_tbl_df.iterrows():
        unit_id = row['UnitID']
        unit = row['Unit']
        for tag, info in results_dict.items():
            if info['UnitID'] == unit_id:
                info['Unit'] = unit

    # Eliminar las entradas con unidad None o "(None)"
    """results_dict = {tag: info for tag, info in results_dict.items() if info['Unit'] not in [None, "(None)"]}"""

    # Guardar el diccionario en un archivo JSON
    json_file_path = r'C:\Emulation\HMIscreensYOKOGAWA\Source\results_with_units.json'
    with open(json_file_path, 'w') as f:
        json.dump(results_dict, f, indent=4)

    print("Diccionario guardado en 'results_with_units.json'")

    # Cargar y mostrar los resultados
    units = load_units_from_json(json_file_path)
    return units

# Llama a esta función para generar el archivo JSON y mostrar los resultados
units = generate_units_json()
print("Unidades cargadas desde el archivo JSON:")

# Imprimir cada unidad, SH y SL
for tag, info in units.items():
    print(f"Tag: {tag}, Unidad: {info['Unit']}, SH: {info['SH']}, SL: {info['SL']}")
"""import json
import pyodbc
import os
import pandas as pd


def load_units_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Crear un diccionario donde la clave es el nombre del tag y el valor es un diccionario con la unidad, SH, SL, y Comment
    units = {tag_name: {'Unit': tag_info['Unit'], 'SH': tag_info.get('SH'), 'SL': tag_info.get('SL'),
                        'Comment': tag_info.get('Comment')} for tag_name, tag_info in data.items()}
    return units


def generate_units_json():
    # Ruta de los archivos .mdb
    path = r'C:\Emulation\HMIscreensYOKOGAWA\Source'

    # Archivos .mdb que comienzan con 'FCS' o 'SCS'
    files = [f for f in os.listdir(path) if f.endswith('.mdb') and (f.startswith('FCS'))]

    # Diccionario para almacenar los resultados
    results_dict = {}

    for file in files:
        # Conectar a la base de datos
        conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + os.path.join(path, file)
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        query = '''
                SELECT ElemName, UnitID, SH, SL, Comment
                FROM ElemTbl;
                '''
        cursor.execute(query)

        for row in cursor.fetchall():
            elem_name = row.ElemName
            unit_id = row.UnitID if pd.notna(row.UnitID) else 1
            sh_value = row.SH if pd.notna(row.SH) else None  # Asignar None si SH es nulo
            sl_value = row.SL if pd.notna(row.SL) else None  # Asignar None si SL es nulo
            comment_value = row.Comment if pd.notna(row.Comment) else ''  # Asignar cadena vacía si Comment es nulo

            # Depurar para verificar los datos extraídos
            print(
                f"Procesando tag: {elem_name}, UnitID: {unit_id}, SH: {sh_value}, SL: {sl_value}, Comment: {comment_value}")

            if elem_name not in results_dict:
                results_dict[elem_name] = {
                    'UnitID': unit_id,
                    'Unit': None,
                    'SH': sh_value,
                    'SL': sl_value,
                    'Comment': comment_value
                }

        cursor.close()
        conn.close()

    # Leer la tabla UnitTbl del archivo PjtRef.mdb
    pjt_ref_file = 'PjtRef.mdb'
    pjt_ref_path = os.path.join(path, pjt_ref_file)
    conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + pjt_ref_path
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    query = '''
    SELECT UnitID, Unit
    FROM UnitTbl;
    '''
    cursor.execute(query)

    unit_tbl_df = pd.DataFrame.from_records(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

    cursor.close()
    conn.close()

    # Actualizar el diccionario con las unidades
    for _, row in unit_tbl_df.iterrows():
        unit_id = row['UnitID']
        unit = row['Unit']
        for tag, info in results_dict.items():
            if info['UnitID'] == unit_id:
                info['Unit'] = unit

    # Filtrar los resultados eliminando entradas con unidad None o "(None)"

    # Guardar el diccionario en un archivo JSON
    json_file_path = r'C:\Emulation\HMIscreensYOKOGAWA\Source\results_with_units.json'
    try:
        with open(json_file_path, 'w') as f:
            json.dump(results_dict, f, indent=4)
        print(f"Diccionario guardado en '{json_file_path}'")
    except Exception as e:
        print(f"Error al guardar el archivo JSON: {e}")

    units = load_units_from_json(json_file_path)
    return units


# Llamar a la función para generar el JSON
units = generate_units_json()

print("Unidades cargadas desde el archivo JSON:")
for tag, info in units.items():
    print(f"Tag: {tag}, Unidad: {info['Unit']}, SH: {info['SH']}, SL: {info['SL']}, Comment: {info['Comment']}")"""
