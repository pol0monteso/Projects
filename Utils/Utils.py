import re
import numpy as np
from Classes.ClassControls import *


def indent(elem, level=0):
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def forceCondition(cond, binding):
    # Crear un diccionario de reemplazos
    """replacements = {
        '.#PV=="CAL"': '2<1',
        '.#PV=="BAD"': '3<1',
        '.AFLS<>': '1=1',
        '.AFLS=="AFL"': '4<1',
        '.AFLS==""': '2==2',
        '.AOFS=="AOF"': '5<1',
        '.AOFS==""': '1==1',
        '.ALRM=="ANS+"': '7<1',
        '.ALRM<>"ANS+"': '7<1',
        '.ALRM=="ANS-"': '8<1',
        '.ALRM<>"ANS-"': '8<1',
        '.ALRM=="CNF"': '9<1',
        '.ALRM<>"CNF"': '2==2',
        '.ALRM=="DV+"': '10<1',
        '.ALRM<>"DV+"': '2==2',
        '.ALRM=="DV-"': '2==2',
        '.ALRM<>"DV-"': '2==2',
        '.ALRM=="IOP"': '12<1',
        '.ALRM<>"IOP"': '3==3',
        '.ALRM=="IOP+"': '13<1',
        '.ALRM=="IOP-"': '14<1',
        '.ALRM=="OOP"': '15<1',
        '.ALRM<>"OOP"': '3==3',
        '.ALRM=="MHI"': '17<1',
        '.ALRM<>"MHI"': '3==3',
        '.ALRM=="MLO"': '18<1',
        '.ALRM<>"MLO"': '3==3',
        '.ALRM=="VEL+"': '19<1',
        '.ALRM=="VEL-"': '20<1',
        '.ALRM=="PERR"': '21<1',
        '.ALRM=="HHH"': '22<1',
        '.ALRM=="LLL"': '23<1',
        '.ALRM=="LTRP"': '24<1',
        '.ALRM=="HTRP"': '25<1',
        '.ALRM==""': '26<1',
        '.ALRM=="FLT"': '27<1',
        '.BPSW==0': '2==2',
        '.BPSW==1': '28<1',
        '.BPSW==2': '29<1',
        '.BPSW==3': '30<1',
        '.BPSW==4': '31<1',
        '.FAULT=="DirtyOptics"': '32<1',
        '.FAULT=="BlockBeam"': '33<1',
        '.FAULT=="DeviceFault"': '34<1',
        '.FAULT=="BitFault"': '35<1',
        '.HTRR==1': '36<1',
        '.HTRR==0': '2==2',
        '.LTRR==1': '37<1',
        '.LTRR==0': '2==2',
        '.HHH==1': '38<1',
        '.HHH==0': '2==2',
        '.LLL==1': '39<1',
        '.LLL==0': '2==2',
        '.OPMK==': '40<1',
        '.SHDN==0': '1=1',
        '.SHDN<>0': '1>2',
        '""': '2<1',
        '.MODE=="MAN IMAN"': '40<1',
        '.MODE=="AUT IMAN"': '40<1'
    }"""
    replacements = {
        '.#PV=="CAL"': '2<1',
        '.#PV=="BAD"': '2<1',
        '.AFLS<>': '1==1',
        '.AFLS=="AFL"': '2<1',
        '.AFLS==""': '1==1',
        '.AOFS=="AOF"': '2<1',
        '.AOFS==""': '1==1',
        '.ALRM=="ANS+"': '2<1',
        '.ALRM<>"ANS+"': '2<1',
        '.ALRM=="ANS-"': '2<1',
        '.ALRM<>"ANS-"': '2<1',
        '.ALRM=="CNF"': '2<1',
        '.ALRM<>"CNF"': '1==1',
        '.ALRM=="DV+"': '2<1',
        '.ALRM<>"DV+"': '1==1',
        '.ALRM=="DV-"': '1==1',
        '.ALRM<>"DV-"': '1==1',
        '.ALRM=="IOP"': '2<1',
        '.ALRM<>"IOP"': '1==1',
        '.ALRM=="IOP+"': '2<1',
        '.ALRM=="IOP-"': '2<1',
        '.ALRM=="OOP"': '2<1',
        '.ALRM<>"OOP"': '1==1',
        '.ALRM=="MHI"': '2<1',
        '.ALRM<>"MHI"': '1==1',
        '.ALRM=="MLO"': '2<1',
        '.ALRM<>"MLO"': '1==1',
        '.ALRM=="VEL+"': '2<1',
        '.ALRM=="VEL-"': '2<1',
        '.ALRM=="PERR"': '2<1',
        '.ALRM=="HHH"': '2<1',
        '.ALRM=="LLL"': '2<1',
        '.ALRM=="LTRP"': '2<1',
        '.ALRM=="HTRP"': '2<1',
        '.ALRM==""': '2<1',
        '.ALRM=="FLT"': '2<1',
        '.BPSW==0': '1==1',
        '.BPSW==1': '2<1',
        '.BPSW==2': '2<1',
        '.BPSW==3': '2<1',
        '.BPSW==4': '2<1',
        '.FAULT=="DirtyOptics"': '2<1',
        '.FAULT=="BlockBeam"': '2<1',
        '.FAULT=="DeviceFault"': '2<1',
        '.FAULT=="BitFault"': '2<1',
        '.HTRR==1': '2<1',
        '.HTRR==0': '1==1',
        '.LTRR==1': '2<1',
        '.LTRR==0': '1==1',
        '.HHH==1': '2<1',
        '.HHH==0': '1==1',
        '.LLL==1': '2<1',
        '.LLL==0': '1==1',
        '.OPMK==': '2<1',
        '.SHDN==0': '1==1',
        '.SHDN<>0': '2<1',
        '""': '2<1',
        '.MODE=="MAN IMAN"': '2<1',
        '.MODE=="AUT IMAN"': '2<1'
    }
    if str("." + binding.GenericName + "==0") in cond.Expression:
        pattern_equals = re.escape('$') + r'[^\$]*' + re.escape(binding.GenericName) + re.escape('==0')
        cond.Expression = re.sub(pattern_equals, '1==1', cond.Expression)
    if str("." + binding.GenericName + "<>0") in cond.Expression:
        pattern_not_equals = re.escape('$') + r'[^\$]*' + re.escape(binding.GenericName) + re.escape('<>0')
        cond.Expression = re.sub(pattern_not_equals, '2<1', cond.Expression)
    expression = cond.Expression

    # Reemplazos directos usando el diccionario
    for key, value in replacements.items():
        expression = expression.replace(str(binding.GenericName + key), value)

    # Manejo de patrones generales

    # Manejo de casos especiales
    special_cases = {
        '.ALRM=="NR"': '1==1',
        '.ALRM<>"NR"': '2<1'
    }

    for key, value in special_cases.items():
        expression = expression.replace(str(binding.GenericName + key), value)

    # Asignar la expresión modificada
    cond.Expression = expression
    if '""' in cond.Expression:
        cond.Expression = "False"


def filtrar_y_separar(cadena):
    # Separar la cadena por espacios
    partes = cadena.split()
    # Filtrar y quedarse solo con las partes que contienen comillas
    partes_con_comillas = [parte for parte in partes if '"' in parte]

    # Separar cada parte que contenga comillas por '==' o '<>'
    resultado = []
    for parte in partes_con_comillas:
        # Separar por '==' o '<>'
        separado = re.split(r'(==|<>)', parte)
        # Filtrar los elementos separados que no tienen comillas y no son '==' o '<>'
        for s in separado:
            s = s.strip()
            if '"' not in s and s not in ['==', '<>']:
                resultado.append(s)

    return resultado

"""def filtrar_y_separar(cadena):
    # Separar la cadena por espacios
    partes = cadena.split()
    # Filtrar y quedarse solo con las partes que contienen comillas
    partes_con_comillas = [parte for parte in partes if '"' in parte]

    # Separar cada parte que contenga comillas por '==' o '<>'
    resultado = []
    for parte in partes_con_comillas:
        # Separar por '==' o '<>'
        separado = re.split(r'(==|<>)', parte)
        # Filtrar los elementos separados que no tienen comillas y no son '==' o '<>'
        for s in separado:
            s = s.strip()
            if '"' not in s and s not in ['==', '<>']:
                resultado.append(s)


    return resultado"""


def sanitZero(rt):
    elements = rt.split(',')
    if elements is not None:
        for i, val in enumerate(elements):
            if (float(elements[i]) < 1 and float(elements[i])) > 0 or (-1 < float(elements[i]) < 0):
                elements[i] = 0
        missatge = (
            "{0},{1},{2},{3},{4},{5}".format(str(elements[0]), str(elements[1]), str(elements[2]),
                                             str(elements[3]), str(elements[4]), str(elements[5])))
        return missatge


def string_to_matrix(s):
    # Convertimos la cadena a una lista de enteros
    lst = list(map(int, s.split(',')))

    # Aseguramos que la lista tiene al menos 4 elementos para formar una matriz 2x2
    if len(lst) < 4:
        raise ValueError("La longitud de la lista debe ser al menos 4 para formar una matriz 2x2")

    # Seleccionamos los primeros 4 elementos
    sub_lst = lst[:4]

    # Convertimos la lista a un array numpy y lo redimensionamos a 2x2
    matrix = np.array(sub_lst).reshape(2, 2)
    return matrix


"""def string_to_matrix(s):

    rows = s.strip().split(',')
    return np.array([list(map(float, row.split())) for row in rows])"""


def matrix_to_string(matrix):
    # Aseguramos que la matriz tiene las dimensiones correctas 3x2

    # Convertimos la matriz en una lista plana de enteros
    lst = matrix.flatten().tolist()

    # Convertimos la lista de enteros en una cadena separada por comas
    s = ','.join(map(str, lst))
    s = s + ",0,0"

    return s

def FlipRotationMode(value):
    mode_map = {
        '-1,0,0,1,0,0': "FH",
        '1,0,0,-1,0,0': "FV",
        '0,1,-1,0,0,0': "RL",
        '-1,0,0,-1,0,0': "RD",
        '0,-1,1,0,0,0': "RLLL",
        '0,-1,-1,0,0,0': "RR",
        '1,0,0,1,0,0': "Identity",
        '0,1,1,0,0,0': "RL+"
    }
    return mode_map.get(value, "Unknown")  # Default to "Unknown" if value is not fou


def orderByZIndex(object_list):
    return sorted(object_list, key=lambda object1: int(object1.ZIndex))

def calculateTransHelper(rt_value, cl, l, ct, t, rect):
    """mode_map = {
        "FH": lambda: (float(l) - float(cl), float(t) + float(ct)),
        "RLLL": lambda: (float(l) + float(ct), float(t) - float(cl)),
        "RD": lambda: (float(l) - float(cl), float(t) - float(ct)),
        "RR": lambda: (float(l) - float(ct), float(t) - float(cl)),
        "Identity": lambda: (float(l) + float(cl), float(t) + float(ct)),
        "RL+": lambda: (float(l) - float(ct), float(t) + float(cl)),
        "RL": lambda: (float(l) + float(cl), float(t) + float(ct))
    }"""
    mode_map = {
        "FH": lambda: (float(l) - float(cl), float(t) + float(ct)),
        "RLLL": lambda: (float(l) - float(ct), float(t) + float(cl)),
        "RD": lambda: (float(l) - float(cl), float(t) - float(ct)),
        "RR": lambda: (float(l) - float(ct), float(t) - float(cl)),
        "Identity": lambda: (float(l) + float(cl), float(t) + float(ct)),
        "RL+": lambda: (float(l) - float(ct), float(t) + float(cl)),
        "RL": lambda: (float(l) - float(ct), float(t) + float(cl)), #float(l) + float(cl), float(t) + float(ct)
        "FV": lambda: (float(l) + float(cl), float(t) - float(ct)) #float(t) + float(ct))
    }

    mode = FlipRotationMode(rt_value)
    if mode in mode_map:
        rect.X, rect.Y = mode_map[mode]()


def FlipRotationMode2(value):
    mode_map = {
        '-1,0,0,1,0,0': "FH",
        '1,0,0,-1,0,0': "FV",
        '0,1,-1,0,0,0': "RL",
        '-1,0,0,-1,0,0': "RD",
        '0,-1,1,0,0,0': "RLLL",
        '0,-1,-1,0,0,0': "RR",
        '1,0,0,1,0,0': "Identity",
        '0,1,1,0,0,0': "RL+"
    }
    return mode_map.get(value, "Unknown")  # Default to "Unknown" if value is not fou


"""def calculateTransHelper2(rt_value, cl, l, ct, t):
    mode_map = {
        "FH": lambda: (float(l) - float(cl), float(t) + float(ct)),
        "RLLL": lambda: (float(l) + float(ct), float(t) - float(cl)),
        "RD": lambda: (float(l) - float(cl), float(t) - float(ct)),
        "RR": lambda: (float(l) - float(ct), float(t) - float(cl)),
        "Identity": lambda: (float(l) + float(cl), float(t) + float(ct)),
        "RL+": lambda: (float(l) - float(ct), float(t) + float(cl)),
        "RL": lambda: (float(l) + float(cl), float(t) + float(ct))
        #"RL": lambda: (float(l) - float(ct), float(t) + float(cl))
    }

    mode = FlipRotationMode2(rt_value)
    if mode in mode_map:
        return mode_map[mode]()
"""

""""FH": lambda: (float(l) - float(cl), float(t) + float(ct)),
        "RLLL": lambda: (float(l) - float(ct), float(t) - float(cl)),
        "RD": lambda: (float(l) - float(cl), float(t) - float(ct)),
        "RR": lambda: (float(l) - float(ct), float(t) - float(cl)),
        "Identity": lambda: (float(l) + float(cl), float(t) + float(ct)),
        "RL+": lambda: (float(l) - float(ct), float(t) + float(cl)),
        "RL": lambda: (float(l) + float(cl), float(t) + float(ct))"""


def check_alarm(units, tag, alarm, screen):
    # Verificar si el tag está en las unidades
    if tag in units:
        tag_info = units[tag]  # Obtener la información del tag

        # Extraer los valores de las alarmas y límites
        hh = tag_info.get('HH')
        sh = tag_info.get('SH')
        ll = tag_info.get('LL')
        sl = tag_info.get('SL')
        li = tag_info.get('LO')
        hi = tag_info.get('HI')

        # Inicializar una lista para almacenar resultados
        result = []

        # Comparar el tipo de alarma solicitado con los valores y crear objetos
        if alarm == "LL" and ll != sl:
            tag1 = Tag.default()
            tag1.Name = f"{tag}.ALMPVLL"
            tag1.HysysVar = f"0@@1@@IIS.Saw{tag1.Name}"
            alarm_obj = Alarm.default()
            alarm_obj.Name = tag1.Name
            alarm_obj.Tag = tag1.ID
            alarm_obj.Screen = screen
            result = [tag1, alarm_obj]

        elif alarm == "HH" and hh != sh:
            tag1 = Tag.default()
            tag1.Name = f"{tag}.ALMPVHH"
            tag1.HysysVar = f"0@@1@@IIS.Saw{tag1.Name}"
            alarm_obj = Alarm.default()
            alarm_obj.Name = tag1.Name
            alarm_obj.Tag = tag1.ID
            alarm_obj.Screen = screen
            result = [tag1, alarm_obj]

        elif alarm == "HI" and hi != sh:
            tag1 = Tag.default()
            tag1.Name = f"{tag}.ALMPVHI"
            tag1.HysysVar = f"0@@1@@IIS.Saw{tag1.Name}"
            alarm_obj = Alarm.default()
            alarm_obj.Name = tag1.Name
            alarm_obj.Tag = tag1.ID
            alarm_obj.Screen = screen
            result = [tag1, alarm_obj]

        elif alarm == "L0" and li != sl:
            tag1 = Tag.default()
            tag1.Name = f"{tag}.ALMPVL0"
            tag1.HysysVar = f"0@@1@@IIS.Saw{tag1.Name}"
            alarm_obj = Alarm.default()
            alarm_obj.Name = tag1.Name
            alarm_obj.Tag = tag1.ID
            alarm_obj.Screen = screen
            result = [tag1, alarm_obj]

        # Devolver la lista de resultados (vacía si no se cumple ninguna condición)
        return result

    # Si no se encuentra el tag, devolver una lista vacía
    return []


def calculateTransHelper2(rt_value, cl, l, ct, t):
    mode_map = {
        "FH": lambda: (float(l) - float(cl), float(t) + float(ct)),
        "RLLL": lambda: (float(l) - float(ct), float(t) + float(cl)),
        "RD": lambda: (float(l) + float(cl), float(t) - float(ct)),
        "RR": lambda: (float(l) - float(ct), float(t) - float(cl)),
        "Identity": lambda: (float(l) + float(cl), float(t) + float(ct)),
        "RL+": lambda: (float(l) - float(ct), float(t) + float(cl)),
        "RL": lambda: (float(l) + float(cl), float(t) + float(ct))
    }

    mode = FlipRotationMode2(rt_value)
    if mode in mode_map:
        return mode_map[mode]()
    return mode_map["Identity"]()

