import pyodbc
import os
import pandas as pd


def load_units(path):
    # Ruta de los archivos .mdb
    #path = r'C:\Emulation\HMIscreensYOKOGAWA\Source'

    # Archivos .mdb que comienzan con 'FCS' o 'SCS'
    files = [f for f in os.listdir(path) if (f.endswith('.mdb') or f.endswith('.accdb')) and (f.startswith('FCS') or f.startswith('SCS'))]

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
                results_dict[elem_name] = {
                    'UnitID': unit_id,
                    'Unit': None,
                    'SH': sh_value,
                    'SL': sl_value,
                    'Comment': comment_value
                }

        # Cerrar la conexión
        cursor.close()
        conn.close()

    # Leer la tabla UnitTbl del archivo PjtRef.mdb
    """pjt_ref_file = 'PjtRef.accdb'
    #pjt_ref_file = 'PjtRef.mdb'
    pjt_ref_path = os.path.join(path, pjt_ref_file)
    conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + pjt_ref_path
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()"""
    accdb_file = 'PjtRef.accdb'
    mdb_file = 'PjtRef.mdb'

    # Verificar cuál archivo existe
    if os.path.exists(os.path.join(path, accdb_file)):
        pjt_ref_file = accdb_file
    elif os.path.exists(os.path.join(path, mdb_file)):
        pjt_ref_file = mdb_file
    else:
        raise FileNotFoundError("No se encontró ni 'PjtRef.accdb' ni 'PjtRef.mdb'.")

    # Crear la conexión
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

    # Retornar el diccionario de resultados
    return results_dict


def load_csv_data(csv_file_path):
    try:
        # Leer el archivo CSV
        df = pd.read_csv(csv_file_path, skiprows=3, header=None)

        # Diccionario para almacenar los datos del CSV
        csv_data = {}

        # Iterar por cada fila del DataFrame
        for index, row in df.iterrows():
            if len(row) >= 236:  # Asegúrate de que hay al menos 236 columnas
                name = row[1]  # Columna B
                block = row[2]
                hh = row[131]  # Columna EB
                ll = row[137]  # Columna EH
                ph = row[217]  # Columna HJ
                pl = row[235]  # Columna IB
                ml = row[141]
                mh = row[140]
                ophi = row[204]
                oplo = row[205]
                msh = row[144]
                msl = row[145]
                pv = row[292]
                """p = row[207]
                sv = row[455]
                i = row[237]
                mv = row[163]
                vl = row[516]
                d = row[67]
                dl = row[63]
                gw = row[130]
                svh = row[457]
                db = row[68]
                svl = row[458]
                cb = row[68]
                ck = row[69]"""


                if pd.notna(name):
                    csv_data[name] = {
                        'HH': hh,
                        'LL': ll,
                        'PH': ph,
                        'PL': pl,
                        'MH': mh,
                        'ML': ml,
                        'Block': block,
                        'OPHI': ophi,
                        'OPLO': oplo,
                        'MSH': msh,
                        'MSL': msl,
                        'PV': pv
                    }

        return csv_data

    except Exception as e:
        print(f"Error al procesar el archivo {csv_file_path}: {e}")
        return {}


def generate_csv_data(csv_directory):
    csv_data = {}
    for file in os.listdir(csv_directory):
        if file.endswith('.csv'):
            csv_file_path = os.path.join(csv_directory, file)
            file_data = load_csv_data(csv_file_path)
            csv_data.update(file_data)

    return csv_data

def load_connect_mapping(path):
    # Archivos .mdb que comienzan con 'FCS' o 'SCS'
    files = [f for f in os.listdir(path) if (f.endswith('.mdb') or f.endswith('.accdb')) and (f.startswith('FCS') or f.startswith('SCS'))]

    connect_dict = {}

    for file in files:
        # Conexión a la base de datos
        conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + os.path.join(path, file)
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        try:
            # Consulta a ConnectTbl incluyendo FromItemName
            query = '''
                    SELECT FromTagName, ToTagName, FromItemName
                    FROM ConnectTbl;
                    '''
            cursor.execute(query)

            for row in cursor.fetchall():
                from_tag = row.FromTagName
                to_tag = row.ToTagName
                from_item = row.FromItemName

                # Filtrar solo si FromItemName contiene 'OUT'
                if from_item and 'OUT' in from_item.upper():
                    if to_tag and not str(to_tag).startswith('%'):
                        connect_dict[from_tag] = to_tag

        except Exception as e:
            print(f"Error leyendo ConnectTbl en {file}: {e}")

        cursor.close()
        conn.close()

    return connect_dict

