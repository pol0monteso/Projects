import math

from Classes import LogicClass
from Utils.NewPoint import getNewPoint
from Classes.ClassControls import *
import xml.etree.ElementTree as ET
from Classes.LogicClass import XPoint, Size, SweepDirection, GetArcCenterPoint
import re

from Utils.Utils import *


# Funciones utilitarias para reducir redundancias
def parse_size(child):
    size_components = child.attrib["Size"].split(',')
    return float(size_components[0]), float(size_components[1])


def parse_point(attr):
    return LogicClass.XPoint(*map(float, attr.split(',')))


"""def parse_render_transform(child, render_list):
    if render_list:
        if len(render_list) > 1:
            acc_matrix = np.array([[1, 0], [0, 1]])
            for render in render_list:
                render_matrix = string_to_matrix(sanitZero(render))
                acc_matrix = np.dot(acc_matrix, np.transpose(render_matrix))
            if "RenderTransform" in child.attrib and child.attrib["RenderTransform"] != "Identity":
                return sanitZero(matrix_to_string(np.dot(acc_matrix, np.transpose(string_to_matrix(sanitZero(child.attrib["RenderTransform"]))))))
            else:
                return sanitZero(matrix_to_string(acc_matrix))
        else:
            if "RenderTransform" in child.attrib and child.attrib["RenderTransform"] != "Identity":
                return sanitZero(matrix_to_string(np.dot(np.transpose(string_to_matrix(sanitZero(render_list[0]))), string_to_matrix(sanitZero(child.attrib["RenderTransform"])))))
            else:
                return sanitZero(render_list[0])
    else:
        if "RenderTransform" in child.attrib and child.attrib["RenderTransform"] != "Identity":
            return sanitZero(child.attrib["RenderTransform"])
        else:
            return "1,0,0,1,0,0"""

"""def parse_render_transform(child, render_list):
    if "Rotation" in child.attrib and child.attrib["Rotation"] != "0":
        rotation_degrees = float(child.attrib["Rotation"])

        # Convierte grados a radianes
        rotation_radians = math.radians(rotation_degrees)

        # Calcula los valores de coseno y seno en radianes
        cos_rotation = math.cos(rotation_radians)
        sin_rotation = math.sin(rotation_radians)
        rotation_matrix = string_to_matrix(sanitZero(f"{int(cos_rotation)},{int(sin_rotation)},{-int(sin_rotation)},{int(cos_rotation)},0,0"))
    else:
        rotation_matrix = np.array([[1, 0], [0, 1]])
    if render_list:
        if len(render_list) > 1:
            acc_matrix = np.array([[1, 0], [0, 1]])
            for render in render_list:
                render_matrix = string_to_matrix(sanitZero(render))
                acc_matrix = np.dot(acc_matrix, np.transpose(render_matrix))
            if "RenderTransform" in child.attrib and child.attrib["RenderTransform"] != "Identity":
                res = np.dot(acc_matrix, (string_to_matrix(sanitZero(child.attrib["RenderTransform"]))))
                return sanitZero(matrix_to_string(np.dot(rotation_matrix, res)))
            else:
                return sanitZero(matrix_to_string((np.dot(acc_matrix, rotation_matrix))))
        else:
            if "RenderTransform" in child.attrib and child.attrib["RenderTransform"] != "Identity":
                res = np.dot((string_to_matrix(sanitZero(render_list[0]))), string_to_matrix(sanitZero(child.attrib["RenderTransform"])))
                return sanitZero(matrix_to_string(np.dot(rotation_matrix, res)))
            else:
                return sanitZero(render_list[0])
    else:
        if "RenderTransform" in child.attrib and child.attrib["RenderTransform"] != "Identity":
            return sanitZero(child.attrib["RenderTransform"])
        else:
            return "1,0,0,1,0,0"""


def parse_render_transform(child, render_list):
    if "Rotation" in child.attrib and child.attrib["Rotation"] != "0":
        rotation_degrees = float(child.attrib["Rotation"])

        # Convierte grados a radianes
        rotation_radians = math.radians(rotation_degrees)

        # Calcula los valores de coseno y seno en radianes
        cos_rotation = math.cos(rotation_radians)
        sin_rotation = math.sin(rotation_radians)
        rotation_matrix = string_to_matrix(
            sanitZero(f"{int(cos_rotation)},{int(sin_rotation)},{-int(sin_rotation)},{int(cos_rotation)},0,0"))
        rotation_matrix = np.array([[1, 0], [0, 1]])
    else:
        rotation_matrix = np.array([[1, 0], [0, 1]])
    if "RenderTransform" in child.attrib and child.attrib["RenderTransform"] != "Identity":
        render_matrix = string_to_matrix(sanitZero(child.attrib["RenderTransform"]))
    else:
        render_matrix = np.array([[1, 0], [0, 1]])
    resultat = np.dot(rotation_matrix, render_matrix)
    if render_list:
        for render in render_list[::-1]:
            resultat = np.dot(resultat, string_to_matrix(sanitZero(render)))
    return matrix_to_string(resultat)


"""if rt == "Identity":
        return "1,0,0,1,0,0"
    if rt and "RenderTransform" not in child.attrib:
        # Convertir los valores a enteros cuando sea necesario
        elements = [0 if (-1 < float(e) < 0 or 0 < float(e) < 1) else int(1) for e in rt.split(',')]
        return "{},{},{},{},{},{}".format(*elements)
    if rt == "" and "RenderTransform" in child.attrib:
        return child.attrib["RenderTransform"]
    return rt"""

"""def parse_fill(fill):
    match = re.search(r'Color1=([#A-Fa-f0-9]+), Color2=([#A-Fa-f0-9]+)', fill)
    return match.group(1) if match else fill"""


def parse_fill(fill):
    match = re.search(r'Color1=([#A-Fa-f0-9a-zA-Z]+), Color2=([#A-Fa-f0-9a-zA-Z]+)', fill)
    return match.group(1) if match else fill


"""def set_common_attributes(obj, child, rt, ro, l, t, aux):
    attrs = {"Tag", "Stroke", "StrokeThickness", "Fill", "ShapeWidth", "ShapeHeight", "Canvas.Left", "Canvas.Top"}
    for attr in attrs:
        if attr in child.attrib:
            setattr(obj, attr.replace("Canvas.", ""), child.attrib[attr])

    obj.Fill = parse_fill(child.attrib["Fill"]) if "Fill" in child.attrib else obj.Fill
    obj.RenderTransform = parse_render_transform(rt, child)
    if aux and "Canvas.Left" in child.attrib and "Canvas.Top" in child.attrib:
        Utils.calculateTransHelper(obj.RenderTransform, child.attrib["Canvas.Left"], l, child.attrib["Canvas.Top"], t,
                                   obj)
    elif "Canvas.Left" in child.attrib and "Canvas.Top" in child.attrib:
        obj.X = float(child.attrib["Canvas.Left"]) + float(l)
        obj.Y = float(child.attrib["Canvas.Top"]) + float(t)
    obj.RenderTransformOrigin = ro"""


def set_common_attributes(obj, child, ro, l, t, aux, render_list, name, tuplas_report):
    attrs = {"Stroke", "StrokeThickness", "Fill", "ShapeWidth", "ShapeHeight", "Canvas.Left", "Canvas.Top",
             "Rotation", "Panel.ZIndex"}
    rt = 0
    for attr in attrs:
        if attr in child.attrib:
            if attr == "ShapeWidth":
                obj.Width = str(round(float(child.attrib[attr]), 1))
            elif attr == "ShapeHeight":
                obj.Height = str(round(float(child.attrib[attr]), 1))
            elif attr == "Stroke":
                if "Null" not in child.attrib[attr]:
                    obj.Stroke = child.attrib[attr]
                else:
                    obj.Stroke = "#00FF0000"
            else:
                setattr(obj, attr.replace("Canvas.", ""), child.attrib[attr])

    if "{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.Builder.Designer.Component;assembly=Yokogawa.IA.iPCS.Platform.View.Graphic.Builder.Designer}ComponentProperties.Name" in child.attrib:
        obj.ShapeName = child.attrib[
            "{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.Builder.Designer.Component;assembly=Yokogawa.IA.iPCS.Platform.View.Graphic.Builder.Designer}ComponentProperties.Name"]
    if "Fill" in child.attrib and "Null" not in child.attrib["Fill"]:
        obj.Fill = parse_fill(child.attrib["Fill"]) if "Fill" in child.attrib else obj.Fill
        other_color = "#00FFFFFF"
        if "Gradient" in child.attrib["Fill"]:
            nombre_obj = obj.ShapeName
            typeYoko = child.tag.split('}', 1)[1].strip()
            typeIIS = type(obj).__name__
            priority = 5
            description = ("The attribute of " + str(type(obj).__name__) + " is a gradient of the colours " + str(
                other_color) +
                           " and " + str(obj.Fill) + ". Colour " + str(obj.Fill) + " was chosen")
            tuplas_report.append([name, nombre_obj, typeYoko, typeIIS, priority, description])
    else:
        obj.Fill = "#00FF0000"
    obj.RenderTransform = parse_render_transform(child, render_list)

    if "RenderTransform" in child.attrib:
        if child.attrib["RenderTransform"] == "Identity" or sanitZero(child.attrib["RenderTransform"]) == "1,0,0,1,0,0":
            render = obj.RenderTransform
            rt = "1,0,0,1,0,0"
        else:
            render = sanitZero(child.attrib["RenderTransform"])
            rt = sanitZero(child.attrib["RenderTransform"])
    else:
        rt = "1,0,0,1,0,0"
        render = obj.RenderTransform
    if aux and "Canvas.Left" in child.attrib and "Canvas.Top" in child.attrib:
        if "RenderTransform" not in child.attrib:
            if len(render_list) == 1 and render_list[0] == "0,-1,1,0,0,0":
                obj.X = l + float(child.attrib["Canvas.Top"])
                obj.Y = t - float(child.attrib["Canvas.Left"])
            elif len(render_list) == 1 and render_list[0] == "0,1,1,0,0,0":
                obj.X = float(l) + float(child.attrib["Canvas.Top"])
                obj.Y = float(t) + float(child.attrib["Canvas.Left"])
            else:
                calculateTransHelper(render, child.attrib["Canvas.Left"], l, child.attrib["Canvas.Top"], t, obj)
        else:
            if render_list[-1] == "-1,0,0,-1,0,0" and rt == "0,1,-1,0,0,0":
                obj.X = float(l) - float(child.attrib["Canvas.Left"])
                obj.Y = float(t) - float(child.attrib["Canvas.Top"])
            elif render_list[-1] == "0,-1,1,0,0,0" and rt == "0,1,-1,0,0,0":
                obj.X = float(l) + float(child.attrib["Canvas.Top"])
                obj.Y = float(t) - float(child.attrib["Canvas.Left"])
            elif render_list[-1] == "0,1,-1,0,0,0" and rt == "1,0,0,-1,0,0":
                obj.X = float(l) - float(child.attrib["Canvas.Top"])
                obj.Y = float(t) - float(child.attrib["Canvas.Left"])  #POT SER QUE SIGUI (+) en lloc de (-)
            elif render_list[-1] == "0,1,-1,0,0,0" and rt == "-1,0,0,-1,0,0":
                obj.X = float(l) - float(child.attrib["Canvas.Top"])
                obj.Y = float(t) + float(child.attrib["Canvas.Left"])
            elif render_list[-1] == "0,1,1,0,0,0" and rt == "-1,0,0,-1,0,0":
                obj.X = float(l) + float(child.attrib["Canvas.Top"])
                obj.Y = float(t) + float(child.attrib["Canvas.Left"])
            elif render_list[-1] == "0,1,1,0,0,0" and rt == "1,0,0,-1,0,0":
                obj.X = float(l) + float(child.attrib["Canvas.Top"])
                obj.Y = float(t) + float(child.attrib["Canvas.Left"])
            elif render_list[-1] == "0,1,-1,0,0,0" and rt == "1,0,0,1,0,0":
                obj.X = float(l) - float(child.attrib["Canvas.Top"])  #+
                obj.Y = float(t) + float(child.attrib["Canvas.Left"])
            elif render_list[-1] == "-1,0,0,1,0,0" and rt == "0,1,1,0,0,0":
                obj.X = float(l) + float(child.attrib["Canvas.Left"])
                obj.Y = float(t) + float(child.attrib["Canvas.Top"])
            elif render_list[-1] == "-1,0,0,1,0,0" and rt == "0,1,-1,0,0,0":
                obj.X = float(l) - float(child.attrib["Canvas.Left"])
                obj.Y = float(t) + float(child.attrib["Canvas.Top"])
            elif render_list[-1] == "-1,0,0,1,0,0" and rt == "0,-1,-1,0,0,0":
                obj.X = float(l) - float(child.attrib["Canvas.Left"])
                obj.Y = float(t) + float(child.attrib["Canvas.Top"])
            elif render_list[-1] == "0,-1,1,0,0,0" and rt == "1,0,0,1,0,0":
                obj.X = float(l) - float(child.attrib["Canvas.Top"])
                obj.Y = float(t) - float(child.attrib["Canvas.Left"])
            elif render_list[-1] == "0,-1,1,0,0,0" and rt == "-1,0,0,1,0,0":
                obj.X = float(l) + float(child.attrib["Canvas.Top"])
                obj.Y = float(t) - float(child.attrib["Canvas.Left"])
            elif render_list[-1] == "0,-1,-1,0,0,0" and rt == "-1,0,0,1,0,0":
                obj.X = float(l) - float(child.attrib["Canvas.Top"])
                obj.Y = float(t) - float(child.attrib["Canvas.Left"])
            elif render_list[-1] == "-1,0,0,1,0,0" and rt == "1,0,0,-1,0,0":
                obj.X = float(l) - float(child.attrib["Canvas.Left"])
                obj.Y = float(t) + float(child.attrib["Canvas.Top"])
            elif render_list[-1] == "-1,0,0,1,0,0" and rt == "-1,0,0,-1,0,0":
                obj.X = float(l) - float(child.attrib["Canvas.Left"])
                obj.Y = float(t) + float(child.attrib["Canvas.Top"])
            elif render_list[-1] == "1,0,0,1,0,0" and rt == "1,0,0,-1,0,0":
                obj.X = float(l) + float(child.attrib["Canvas.Left"])
                obj.Y = float(t) + float(child.attrib["Canvas.Top"])
            elif render_list[-1] == "1,0,0,1,0,0" and len(render_list) == 1:
                obj.X = float(l) + float(child.attrib["Canvas.Left"])
                obj.Y = float(t) + float(child.attrib["Canvas.Top"])
            elif render_list[-1] == "0,1,1,0,0,0" and rt == "-1,0,0,1,0,0":
                obj.X = float(l) + float(child.attrib["Canvas.Top"])
                obj.Y = float(t) + float(child.attrib["Canvas.Left"])
            elif render_list[-1] == "0,1,1,0,0,0" and rt == "1,0,0,1,0,0":
                obj.X = float(l) + float(child.attrib["Canvas.Top"])
                obj.Y = float(t) + float(child.attrib["Canvas.Left"])
            elif render_list[-1] == "0,1,1,0,0,0" and rt == "1,0,0,-1,0,0":
                obj.X = float(l) + float(child.attrib["Canvas.Top"])
                obj.Y = float(t) + float(child.attrib["Canvas.Left"])
            elif render_list[-1] == "1,0,0,-1,0,0" and rt == "-1,0,0,1,0,0":
                obj.X = float(l) + float(child.attrib["Canvas.Left"])
                obj.Y = float(t) - float(child.attrib["Canvas.Top"])
            elif render_list[-1] == "1,0,0,-1,0,0" and rt == "-1,0,0,-1,0,0":
                obj.X = float(l) + float(child.attrib["Canvas.Left"])
                obj.Y = float(t) - float(child.attrib["Canvas.Top"])
            elif render_list[-1] == "0,1,-1,0,0,0":
                obj.X = float(l) - float(child.attrib["Canvas.Top"])  # +
                obj.Y = float(t) + float(child.attrib["Canvas.Left"])
            elif render_list[-1] == "0,1,1,0,0,0":
                obj.X = float(l) + float(child.attrib["Canvas.Top"])
                obj.Y = float(t) + float(child.attrib["Canvas.Left"])
            else:
                calculateTransHelper(render, child.attrib["Canvas.Left"], l, child.attrib["Canvas.Top"], t, obj)

    elif "Canvas.Left" in child.attrib and "Canvas.Top" in child.attrib:
        obj.X = float(child.attrib["Canvas.Left"]) + float(l)
        obj.Y = float(child.attrib["Canvas.Top"]) + float(t)

    if "RenderTransformOrigin" in child.attrib:
        obj.RenderTransformOrigin = child.attrib["RenderTransformOrigin"]
    else:
        obj.RenderTransformOrigin = ro


"""IDENTITY_TRANSFORM = "1,0,0,1,0,0"
NULL_COLOR = "#00FF0000"
"""
"""def set_common_attributes(obj, child, ro, l, t, aux, render_list, name, tuplas_report):
    attrs_mapping = {
        "ShapeWidth": lambda v: setattr(obj, "Width", str(round(float(v), 1))),
        "ShapeHeight": lambda v: setattr(obj, "Height", str(round(float(v), 1))),
        "Stroke": lambda v: setattr(obj, "Stroke", v if "Null" not in v else NULL_COLOR),
        "Fill": lambda v: setattr(obj, "Fill", parse_fill(v) if "Null" not in v else NULL_COLOR)
    }

    for attr, handler in attrs_mapping.items():
        if attr in child.attrib:
            handler(child.attrib[attr])

    for attr in {"Canvas.Left", "Canvas.Top", "Rotation", "Panel.ZIndex"}:
        if attr in child.attrib:
            setattr(obj, attr.replace("Canvas.", ""), child.attrib[attr])

    name_key = "{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.Builder.Designer.Component;assembly=Yokogawa.IA.iPCS.Platform.View.Graphic.Builder.Designer}ComponentProperties.Name"
    obj.ShapeName = child.attrib.get(name_key, "")

    if "Fill" in child.attrib and "Gradient" in child.attrib["Fill"]:
        other_color = "Transparent"
        nombre_obj = obj.ShapeName
        typeYoko = child.tag.split('}', 1)[1].strip()
        typeIIS = type(obj).__name__
        priority = 5
        description = f"The attribute of {typeIIS} is a gradient of the colours {other_color} and {obj.Fill}. Colour {obj.Fill} was chosen"
        tuplas_report.append([name, nombre_obj, typeYoko, typeIIS, priority, description])

    obj.RenderTransform = parse_render_transform(child, render_list)
    if child.attrib.get("RenderTransform") == "Identity":
        rt = sanitZero(IDENTITY_TRANSFORM)
    else:
        rt = sanitZero(child.attrib.get("RenderTransform", IDENTITY_TRANSFORM))
    render = obj.RenderTransform if rt == IDENTITY_TRANSFORM else rt

    if aux and "Canvas.Left" in child.attrib and "Canvas.Top" in child.attrib:
        calculate_position(obj, render_list, rt, render, child, l, t)
    elif "Canvas.Left" in child.attrib and "Canvas.Top" in child.attrib:
        obj.X = float(child.attrib["Canvas.Left"]) + float(l)
        obj.Y = float(child.attrib["Canvas.Top"]) + float(t)

    obj.RenderTransformOrigin = child.attrib.get("RenderTransformOrigin", ro)


def calculate_position(obj, render_list, rt, render, child, l, t):
    canvas_left = float(child.attrib["Canvas.Left"])
    canvas_top = float(child.attrib["Canvas.Top"])
    last_render = render_list[-1] if render_list else IDENTITY_TRANSFORM

    position_cases = {
        ("-1,0,0,-1,0,0", "0,1,-1,0,0,0"): lambda: (float(l) - canvas_left, float(t) - canvas_top),
        ("0,-1,1,0,0,0", "0,1,-1,0,0,0"): lambda: (float(l) + canvas_top, float(t) - canvas_left),
        ("0,1,-1,0,0,0", "1,0,0,-1,0,0"): lambda: (float(l) - canvas_top, float(t) - canvas_left),
        ("1,0,0,1,0,0", IDENTITY_TRANSFORM): lambda: (float(l) + canvas_left, float(t) + canvas_top),
    }

    if (last_render, rt) in position_cases:
        obj.X, obj.Y = position_cases[(last_render, rt)]()
    else:
        calculateTransHelper(render, canvas_left, l, canvas_top, t, obj)"""


def process_conditions(obj, child):
    for condition in child.findall('.//{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel'
                                   ';assembly=Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel}Condition'):
        colorChange = False
        cond = IISCondition.default()
        cond.Expression = re.sub(r'\b0\b', str("0,0"), condition.attrib.get("Expression", ""))
        cond.IISCondition = condition.attrib.get("Continuous", "")
        for action in condition:
            for typeA in action:
                if typeA.tag.endswith("ColorChange"):
                    if not colorChange:
                        colorChange = True
                        cond.ColorC1 = typeA.attrib.get("Color", "")
                        cond.ColorChangeType1 = typeA.attrib.get("ColorChangeType", "")
                        if typeA.attrib.get("ColorChangeType", "") == "ChangeAlarmSpecificColor":
                            cond.ColorChangeType1 = "NormalColorChange"
                        cond.PropertyNameCC1 = typeA.attrib.get("PropertyName", "")
                    else:
                        cond.ColorC2 = typeA.attrib.get("Color", "")
                        cond.ColorChangeType2 = typeA.attrib.get("ColorChangeType", "")
                        if typeA.attrib.get("ColorChangeType", "") == "ChangeAlarmSpecificColor":
                            cond.ColorChangeType2 = "NormalColorChange"
                        cond.PropertyNameCC2 = typeA.attrib.get("PropertyName", "")
                if typeA.tag.endswith("Set"):
                    if typeA.attrib.get("AttributeName") == "Visibility" and typeA.attrib.get("To"):
                        if type(obj) == Text or type(obj) == ProcessData or type(obj) == Level or type(obj) == Button:
                            cond.ColorC1 = "#00FFFFFF"
                            cond.ColorChangeType1 = "NormalColorChange"
                            cond.PropertyNameCC1 = "Background"
                            cond.ColorC2 = "#00FFFFFF"
                            cond.ColorChangeType2 = "NormalColorChange"
                            cond.PropertyNameCC2 = "Foreground"
                        elif type(obj) == Line or type(obj) == PolyLine or type(obj) == Arc:
                            cond.ColorC1 = "#00FFFFFF"
                            cond.ColorChangeType1 = "NormalColorChange"
                            cond.PropertyNameCC1 = "Stroke"
                        else:
                            cond.ColorC1 = "#00FFFFFF"
                            cond.ColorChangeType1 = "NormalColorChange"
                            cond.PropertyNameCC1 = "Stroke"
                            cond.ColorC2 = "#00FFFFFF"
                            cond.ColorChangeType2 = "NormalColorChange"
                            cond.PropertyNameCC2 = "Fill"

                if typeA.tag.endswith("Blinking"):
                    cond.PropertyNameBLK1 = typeA.attrib.get("PropertyName", "")
                    if "TypeBlinking" in typeA.attrib and (
                            typeA.attrib["TypeBlinking"] == "AlarmSpecificBlinking" or typeA.attrib[
                        "TypeBlinking"] == "Yes") and cond.PropertyNameBLK1 != "":
                        """cond.ColorB1 = "FindColor"
                        cond.BlinkingType1 = "Yes"
                        """
                        cond.ColorB1 = cond.ColorC1
                        cond.BlinkingType1 = "Yes"

                    obj.IISCondition.append(cond)


def process_bindings(obj, child):
    for binding in child.findall('.//{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.GenericName;assembly'
                                 '=Yokogawa.IA.iPCS.Platform.View.Graphic.GenericName}GNBinding'):
        bind = Binding.default()
        bind.GenericName = binding.attrib.get("GenericName", "")
        bind.Value = binding.attrib.get("Value", "")
        """ or "TagInventat_" + ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=5))"""
        obj.Binding.append(bind)


def read_tag_and_binding_DataCharacter(obj, child):
    bind = child.findall('.//{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.GenericName;assembly'
                         '=Yokogawa.IA.iPCS.Platform.View.Graphic.GenericName}GNBinding')
    GenericName = bind.attrib.get("Value", "")

    binding = child.find('.//{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel'
                         ';assembly=Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel}SimpleDataLink')
    Value = binding.attrib.get("Value", "")


def readText(child, l, t, rt, ro, aux, render_list, name, tuplas_report):
    text1 = Text.default()
    set_common_attributes(text1, child, ro, l, t, aux, render_list, name, tuplas_report)
    xml_data = ET.tostring(child, encoding='unicode')
    #pattern = r'</[^:]*:GenericNameComponent\.GenericName>(.*?)</[^:]*:Text>'
    #pattern = r'</[^>]+>(.*?)</[^:]+:Text>'
    pattern = r'</[^>]+>([^<]+)</[^:]+:Text>'
    matches = re.findall(pattern, xml_data, re.DOTALL)

    if matches:
        if matches[0].endswith('\n'):
            text1.Text = matches[0].replace('\n', "")
        else:
            text1.Text = matches[0]

    attrib = child.attrib
    text1.FontSize = attrib.get("FontSize", "")
    text1.FontFamily = attrib.get("FontFamily", "")
    if "Foreground" in child.attrib and "Null" not in child.attrib["Foreground"]:
        text1.Foreground = attrib.get("Foreground", "")
    else:
        text1.Foreground = "#00FF0000"
    if "Background" in child.attrib and "Null" not in child.attrib["Background"]:
        text1.Background = attrib.get("Background", "")
    else:
        text1.Background = "#00FF0000"
    """text1.Width = 1.133 * float(attrib.get("FontSize", ""))
    text1.Height = 2.4 * float(attrib.get("FontSize", ""))"""
    """if "TextAlignmen" in child.attrib and (child.attrib["TextAlignment"] == "center" or child.attrib["TextAlignmen"] == "CompactCenter"):
        text1.TextAlign = "Center"
    else:
        text1.TextAlign = "Center"""

    if "ScaleX" in attrib:
        text1.ScaleX = attrib["ScaleX"]
    if "ScaleY" in attrib:
        text1.ScaleY = attrib["ScaleY"]
    if "Canvas.Left" in attrib and "Canvas.Top" in attrib:
        x_offset = float(attrib["Canvas.Left"]) + float(l)
        y_offset = float(attrib["Canvas.Top"]) + float(t)
        text1.X = x_offset
        text1.Y = y_offset
    if "FontWeight" in attrib:
        text1.FontWeight = attrib["FontWeight"]

    process_bindings(text1, child)
    if "$" in text1.Text:
        for bind in text1.Binding:
            if bind.GenericName in text1.Text:
                text1.Text = text1.Text.replace(bind.GenericName, bind.Value)
    read_conditions_alarms(child, text1)
    """process_conditions(text1, child)"""
    """process_bindings(text1, child)"""

    return text1


"""for action in condition:
    for type in action:
        if type.tag.endswith("ColorChange"):
            if not colorChange:
                colorChange = True
                cond.ColorC1 = type.attrib.get("Color", "")
                cond.ColorChangeType1 = type.attrib.get("ColorChangeType", "")
                if type.attrib.get("ColorChangeType", "") == "ChangeAlarmSpecificColor":
                    cond.ColorChangeType1 = "NormalColorChange"
                cond.PropertyNameCC1 = type.attrib.get("PropertyName", "")
            else:
                cond.ColorC2 = type.attrib.get("Color", "")
                cond.ColorChangeType2 = type.attrib.get("ColorChangeType", "")
                if type.attrib.get("ColorChangeType", "") == "ChangeAlarmSpecificColor":
                    cond.ColorChangeType2 = "NormalColorChange"
                cond.PropertyNameCC2 = type.attrib.get("PropertyName", "")
        if type.tag.endswith("Blinking"):
            cond.PropertyNameBLK1 = type.attrib.get("PropertyName", "")
            if "TypeBlinking" in type.attrib and (
                    type.attrib["TypeBlinking"] == "AlarmSpecificBlinking" or type.attrib[
                "TypeBlinking"] == "Yes") and cond.PropertyNameBLK1 != "":
                cond.ColorB1 = "Red"
                cond.BlinkingType1 = "Yes"""


def read_conditions_alarms(child, obj):
    for condition in child.findall('.//{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel'
                                   ';assembly=Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel}Condition'):
        cond = IISCondition.default()
        cond.Expression = re.sub(r'\b0\b', str("0,0"), condition.attrib.get("Expression", ""))
        cond.IISCondition = condition.attrib.get("Continuous", "")
        write = False
        colorChange = False
        for action in condition:
            for type in action:
                if type.tag.endswith("ColorChange"):
                    if not colorChange:
                        cond.ColorC1 = type.attrib.get("Color", "")
                        cond.ColorChangeType1 = type.attrib.get("ColorChangeType", "")
                        if type.attrib.get("ColorChangeType", "") == "ChangeAlarmSpecificColor":
                            cond.ColorChangeType1 = "NormalColorChange"
                        cond.PropertyNameCC1 = type.attrib.get("PropertyName", "")
                        write = True
                    else:
                        cond.ColorC2 = type.attrib.get("Color", "")
                        cond.ColorChangeType2 = type.attrib.get("ColorChangeType", "")
                        if type.attrib.get("ColorChangeType", "") == "ChangeAlarmSpecificColor":
                            cond.ColorChangeType2 = "NormalColorChange"
                        cond.PropertyNameCC2 = type.attrib.get("PropertyName", "")
                        write = True
                if type.tag.endswith("Blinking"):
                    cond.PropertyNameBLK = type.attrib.get("PropertyName", "")
                    if "TypeBlinking" in type.attrib and (
                            type.attrib["TypeBlinking"] == "AlarmSpecificBlinking" or type.attrib[
                        "TypeBlinking"] == "Yes") and cond.PropertyNameBLK != "":
                        cond.ColorB = "Red"
                        cond.BlinkingType = "Yes"
                        write = True
                if type.tag.endswith("ReplaceText"):
                    text = type.attrib.get("Text", "")
                    if '$' not in text:
                        cond.Text = text
                    if '"' in text:
                        text = text.replace('"', "")
                    for bind in obj.Binding:
                        if bind.GenericName == text:
                            cond.Text = text
                    if '"' in cond.Text:
                        cond.Text = cond.Text.replace('"', "")
                    cond.ReplaceText = "True"
                    write = True
        if write:
            obj.IISCondition.append(cond)


def readDataCharacter(child, l, t, rt, ro, aux, render_list, name, tuplas_report):
    text1 = ProcessData.default()
    set_common_attributes(text1, child, ro, l, t, aux, render_list, name, tuplas_report)
    xml_data = ET.tostring(child, encoding='unicode')
    #pattern = r'</[^:]*:GenericNameComponent\.GenericName>(.*?)</[^:]*:Text>'
    #pattern = r'</[^>]+>(.*?)</[^:]+:Text>'
    pattern = r'</[^>]+>([^<]+)</[^:]+:Text>'
    matches = re.findall(pattern, xml_data, re.DOTALL)

    if matches:
        text1.Text = matches[0]

    attrib = child.attrib
    text1.FontSize = attrib.get("FontSize", "")
    text1.FontFamily = attrib.get("FontFamily", "")
    if "Foreground" in child.attrib and "Null" not in child.attrib["Foreground"]:
        text1.Foreground = attrib.get("Foreground", "")
    else:
        text1.Foreground = "#00FF0000"
    if "Background" in child.attrib and "Null" not in child.attrib["Background"]:
        text1.Background = attrib.get("Background", "")
    else:
        text1.Background = "#00FF0000"
    text1.Width = attrib.get("Width", "")
    text1.Height = attrib.get("Height", "")

    if "Alignment" in child.attrib and (
            child.attrib["Alignment"] == "center" or child.attrib["Alignment"] == "CompactCenter"):
        text1.TextAlign = "Center"
    else:
        text1.TextAlign = attrib.get("Alignment", "")

    if "Canvas.Left" in attrib and "Canvas.Top" in attrib:
        x_offset = float(attrib["Canvas.Left"]) + float(l)
        y_offset = float(attrib["Canvas.Top"]) + float(t)
        text1.X = x_offset
        text1.Y = y_offset
    data_char = DataChar.default()

    if "ShowEngineerUnit" in child.attrib:
        if child.attrib["ShowEngineerUnit"] == "Visible":
            text1.isVisibleUnits = True

    for bind in child.findall('.//{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.GenericName;assembly'
                              '=Yokogawa.IA.iPCS.Platform.View.Graphic.GenericName}GNBinding'):
        if text1.binding_dic:
            if bind.attrib.get("GenericName", "") not in text1.binding_dic:
                binding = Binding.default()
                text1.binding_dic[bind.attrib.get("GenericName", "")] = bind.attrib.get("Value", "")
                binding.GenericName = binding.Value = bind.attrib.get("Value", "")
                text1.Binding.append(binding)
            else:
                if text1.binding_dic[bind.attrib.get("GenericName", "")] == "":
                    binding = Binding.default()
                    text1.binding_dic[bind.attrib.get("GenericName", "")] = bind.attrib.get("Value", "")
                    binding.GenericName = binding.Value = bind.attrib.get("Value", "")
                    text1.Binding.append(binding)
        else:
            binding = Binding.default()
            text1.binding_dic[bind.attrib.get("GenericName", "")] = bind.attrib.get("Value", "")
            binding.GenericName = binding.Value = bind.attrib.get("Value", "")
            text1.Binding.append(binding)

    #data_char.GenericName = bind.attrib.get("Value", "")
    #binding = child.find('.//{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel'
    #';assembly=Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel}SimpleDataLink')
    #data_char.Value = binding.attrib.get("Value", "")
    #data_char.Value = binding.attrib.get("Value", "")

    for binding in child.findall('.//{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel'
                                 ';assembly=Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel}SimpleDataLink'):
        data_char.Value = binding.attrib.get("Value", "")

    content = data_char.Value
    data_list = content.split('.')
    if len(data_list) == 2:
        var_type = data_list[-1]
        if var_type != "PV" and var_type != "MV" and "@" not in content:
            if var_type in text1.binding_dic:
                data_char.Value = data_char.Value.replace(var_type, text1.binding_dic[var_type])
        else:
            if "@" in content:
                var_type = None
                target_value = None

                for key, value in text1.binding_dic.items():
                    if value in ["PV", "MV"]:
                        var_type = key
                        target_value = value
                        break

                if var_type:
                    data_char.Value = data_char.Value.replace(var_type, target_value)
    text1.dataChar = data_char
    process_conditions(text1, child)
    process_bindings(text1, child)

    return text1


def initRectangles(child, l, t, ro, aux, render_list, name, tuplas_report):
    rect1 = Rectangle.default()
    attrib = child.attrib
    set_common_attributes(rect1, child, ro, l, t, aux, render_list, name, tuplas_report)

    # Recolectar los bindings: { "$TAG": "65FC2", "$XYZ": "value", ... }
    bindings = {}
    for binding in child.findall(".//{*}GNBinding"):
        generic_name = binding.attrib.get("GenericName")
        value = binding.attrib.get("Value")
        if generic_name and value:
            bindings[generic_name] = value

    # Función para reemplazar placeholders en un string
    def replace_placeholders(s):
        for key, val in bindings.items():
            s = s.replace(key, val)
        return s

    # Set Fill color
    fill_attr = attrib.get("Fill", "")
    if "Fill" in attrib and "Null" not in fill_attr:
        fill = replace_placeholders(fill_attr)
        rect1.Fill = parse_fill(fill) if 'Gradient' in fill else fill
    else:
        rect1.Fill = "#00FF0000"

    rect1.RenderTransformOrigin = ro

    process_conditions(rect1, child)
    process_bindings(rect1, child)

    # Extraer AdvanceDataLink con valores reales sustituidos
    rect1.DataLinkInfo = []
    for dl_modifiers in child.findall(".//{*}DataLinkModifier"):
        for data_link in dl_modifiers.findall(".//{*}AdvanceDataLink"):
            info = {
                "HighLimit": replace_placeholders(data_link.attrib.get("HighLimit", "")),
                "LowLimit": replace_placeholders(data_link.attrib.get("LowLimit", "")),
                "PropertyName": replace_placeholders(data_link.attrib.get("PropertyName", "")),
                "Value": replace_placeholders(data_link.attrib.get("Value", "")),
                "TransformFrom": None,
                "TransformTo": None,
                "OffSet": None  # <--- Añadido
            }

            # TransformFrom
            tf = data_link.find(".//{*}AdvanceDataLink.TransformFrom/{*}Double")
            if tf is not None:
                info["TransformFrom"] = float(tf.text)

            # TransformTo
            tt = data_link.find(".//{*}AdvanceDataLink.TransformTo/{*}Double")
            if tt is not None:
                info["TransformTo"] = float(tt.text)

            # OffSet <--- Nuevo
            offset = data_link.find(".//{*}AdvanceDataLink.OffSet/{*}Double")
            if offset is not None:
                info["OffSet"] = float(offset.text)

            rect1.DataLinkInfo.append(info)

    return rect1


def initGroupComp(child, l, t, rt, ro, aux, tag_list, object_list, render_list, name, tuplas_report):
    """cl = float(child.attrib["Canvas.Left"]) + float(l)
    ct = float(child.attrib["Canvas.Top"]) + float(t)"""
    if "RenderTransform" in child.attrib:
        if child.attrib["RenderTransform"] == "Identity":
            child.attrib["RenderTransform"] = "1,0,0,1,0,0"
        cl = float(child.attrib["Canvas.Left"]) + float(l)
        ct = float(child.attrib["Canvas.Top"]) + float(t)
        render = sanitZero(child.attrib["RenderTransform"])
        """if render_list and render_list[0] == "0,1,1,0,0,0" and render == "1,0,0,1,0,0":
            cl = float(l) + float(child.attrib["Canvas.Top"])
            ct = float(t) + float(child.attrib["Canvas.Left"])"""
        if aux:
            cl, ct = calculateTransHelper2(render, float(child.attrib["Canvas.Left"]), l, float(child.attrib["Canvas"
                                                                                                             ".Top"]),
                                           t)

    else:
        cl = float(child.attrib["Canvas.Left"]) + float(l)
        ct = float(child.attrib["Canvas.Top"]) + float(t)

    if "RenderTransform" in child.attrib:
        if child.attrib["RenderTransform"] == "Identity":
            child.attrib["RenderTransform"] = "1,0,0,1,0,0"
        render_list.append(sanitZero(child.attrib["RenderTransform"]))
        ro = str(child.attrib["RenderTransformOrigin"])
        readRect_rec(child, cl, ct, rt, ro, True, tag_list, object_list, render_list, name, tuplas_report)
        render_list.pop()
        aux = False
    else:
        rt = ""
        ro = ""
        readRect_rec(child, cl, ct, rt, ro, aux, tag_list, object_list, render_list, name, tuplas_report)
        aux = False
        zindex = 0


"""def initGroupComp(child, l, t, rt, ro, aux, tag_list, object_list, render_list):
    if "RenderTransform" in child.attrib:
        if child.attrib["RenderTransform"] == "Identity":
            child.attrib["RenderTransform"] = "1,0,0,1,0,0"
        cl = float(child.attrib["Canvas.Left"])
        ct = float(child.attrib["Canvas.Top"]) + float(t)
        render = sanitZero(child.attrib["RenderTransform"])
        if aux:
            cl, ct = calculateTransHelper2(render, float(child.attrib["Canvas.Left"]), l, float(child.attrib["Canvas"
                                                                                                             ".Top"]), t)

    else:
        cl = float(child.attrib["Canvas.Left"]) + float(l)
        ct = float(child.attrib["Canvas.Top"]) + float(t)

    if "RenderTransform" in child.attrib:
        if child.attrib["RenderTransform"] == "Identity":
            child.attrib["RenderTransform"] = "1,0,0,1,0,0"
        render_list.append(child.attrib["RenderTransform"])
        ro = str(child.attrib["RenderTransformOrigin"])
        readRect_rec(child, cl, ct, rt, ro, True, tag_list, object_list, render_list)
        render_list.pop()
    else:
        rt = ""
        ro = ""
        readRect_rec(child, cl, ct, rt, ro, aux, tag_list, object_list, render_list)
"""


def initLine(child, l, t, ro, aux, render_list, name, tuplas_report):
    line = Line.default()
    line.ArrowStart = False
    line.ArrowEnd = False
    set_common_attributes(line, child, ro, l, t, aux, render_list, name, tuplas_report)
    line.Width = max(child.attrib["X1"], child.attrib["X2"])
    line.Height = max(child.attrib["Y1"], child.attrib["Y2"])
    point_1 = LogicClass.XPoint()
    point_2 = LogicClass.XPoint()
    point_1.X = float(child.attrib["X1"])
    point_1.Y = float(child.attrib["Y1"])
    point_2.X = float(child.attrib["X2"])
    point_2.Y = float(child.attrib["Y2"])
    """total = [point_1.X, point_1.Y, point_2.X, point_2.Y]"""
    total = [(point_1.X, point_1.Y), (point_2.X, point_2.Y)]
    line.Points.append(point_1)
    line.Points.append(point_2)

    if "ArrowEndStyle" in child.attrib:
        if child.attrib["ArrowEndStyle"] != "None":
            arrow1 = Arrow.default()
            arrow1.isVisible = True
            line.arrowEnd = arrow1
            line.ArrowEnd = True
            if total is not None:
                a, b = getNewPoint(total)
                line.Points[-1] = b
    if "ArrowStartStyle" in child.attrib:
        if child.attrib["ArrowStartStyle"] != "None":
            arrow2 = Arrow.default()
            arrow2.isVisible = True
            line.arrowStart = arrow2
            line.ArrowStart = True
            if total is not None:
                a, b = getNewPoint(total)
                line.Points[0] = a
    if "LineStyle" in child.attrib:
        line.LineStyle = "DASH"

    #set_common_attributes(line, child, ro, l, t, aux, render_list)
    process_conditions(line, child)
    process_bindings(line, child)
    return line


def init_polyline(child, l, t, ro, aux, render_list, name, tuplas_report):
    line = Line.default()
    line.ArrowStart = False
    line.ArrowEnd = False
    total = None
    set_common_attributes(line, child, ro, l, t, aux, render_list, name, tuplas_report)
    if "Points" in child.attrib:
        points = [tuple(map(float, pair.split(','))) for pair in child.attrib["Points"].split()]
        line.Width = max(x for x, y in points)
        line.Height = max(y for x, y in points)
        total = points
        line.Points.extend(XPoint(x, y) for x, y in points)
    if "ArrowEndStyle" in child.attrib:
        if child.attrib["ArrowEndStyle"] != "None":
            arrow1 = Arrow.default()
            arrow1.isVisible = True
            line.arrowEnd = arrow1
            line.ArrowEnd = True
            if total is not None:
                a, b = getNewPoint(total)
                line.Points[-1] = b
    if "ArrowStartStyle" in child.attrib:
        if child.attrib["ArrowStartStyle"] != "None":
            arrow2 = Arrow.default()
            arrow2.isVisible = True
            line.arrowStart = arrow2
            line.ArrowStart = True
            if total is not None:
                a, b = getNewPoint(total)
                line.Points[0] = a
    if "LineStyle" in child.attrib:
        line.LineStyle = "DASH"

    #set_common_attributes(line, child, ro, l, t, aux, render_list)
    process_conditions(line, child)
    process_bindings(line, child)
    return line


def init_level(child, l, t, ro, aux, render_list, name, tuplas_report):
    level = Level.default()
    set_common_attributes(level, child, ro, l, t, aux, render_list, name, tuplas_report)
    if "Foreground" in child.attrib:
        level.LevelFill1 = child.attrib["Foreground"]
    if "GrowthDirection" in child.attrib:
        if child.attrib["GrowthDirection"] == "Up":
            level.Orientation = "Vertical"
        elif child.attrib["GrowthDirection"] == "Right":
            level.Orientation = "Horizontal"
    level.Width = child.attrib["Width"]
    level.Height = child.attrib["Height"]
    if "BorderBrush" in child.attrib and "Null" not in child.attrib["BorderBrush"]:
        level.Stroke = child.attrib["BorderBrush"]
    else:
        level.Stroke = "Transparent"
    if "BorderThickness" in child.attrib:
        primer_numero = re.search(r'\d+', child.attrib["BorderThickness"])
        level.StrokeThickness = int(primer_numero.group()) if primer_numero else 1

    for bind in child.findall('.//{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.GenericName;assembly'
                              '=Yokogawa.IA.iPCS.Platform.View.Graphic.GenericName}GNBinding'):
        if level.binding_dic:
            if bind.attrib.get("GenericName", "") not in level.binding_dic:
                binding = Binding.default()
                level.binding_dic[bind.attrib.get("GenericName", "")] = bind.attrib.get("Value", "")
                binding.GenericName = binding.Value = bind.attrib.get("Value", "")
                level.Binding.append(binding)
            else:
                if level.binding_dic[bind.attrib.get("GenericName", "")] == "":
                    binding = Binding.default()
                    level.binding_dic[bind.attrib.get("GenericName", "")] = bind.attrib.get("Value", "")
                    binding.GenericName = binding.Value = bind.attrib.get("Value", "")
                    level.Binding.append(binding)
        else:
            binding = Binding.default()
            level.binding_dic[bind.attrib.get("GenericName", "")] = bind.attrib.get("Value", "")
            binding.GenericName = binding.Value = bind.attrib.get("Value", "")
            level.Binding.append(binding)
    data_char = DataChar.default()
    for datalink in child.findall('.//{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel'
                                  ';assembly=Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel}SimpleDataLink'):
        if "LowLimit" in datalink.attrib.get("AlternateValue", ""):
            if datalink.attrib.get("Value", "") == "":
                level.LevelValue1 = 0
            elif "SL" in datalink.attrib.get("Value", "") or "LO" in datalink.attrib.get("Value",
                                                                                         "") or "ML" in datalink.attrib.get(
                "Value", ""):
                level.LevelValue1 = datalink.attrib.get("Value", "")
        elif "HighLimit" in datalink.attrib.get("AlternateValue", ""):
            if datalink.attrib.get("Value", "") == "":
                level.LevelValue2 = 100
            elif "SH" in datalink.attrib.get("Value", "") or "HI" in datalink.attrib.get("Value",
                                                                                         "") or "MH" in datalink.attrib.get(
                "Value", ""):
                level.LevelValue2 = datalink.attrib.get("Value", "")
        elif datalink.attrib.get("Value", ""):
            data_char.GenericName = data_char.Value = datalink.attrib.get("Value", "")
            level.dataChar = data_char
    content = data_char.Value
    data_list = content.split('.')
    if len(data_list) == 2:
        var_type = data_list[-1]
        tag_type = data_list[0]
        if var_type != "PV" and var_type != "MV" and "@" not in content:
            if var_type in level.binding_dic and tag_type in level.binding_dic:
                data_char.Value = data_char.Value.replace(var_type, level.binding_dic[var_type])
                data_char.Value = data_char.Value.replace(tag_type, level.binding_dic[tag_type])
        else:
            if "@" in content:
                var_type = None
                target_value = None

                for key, value in level.binding_dic.items():
                    if value in ["PV", "MV"]:
                        var_type = key
                        target_value = value
                        break

                if var_type:
                    data_char.Value = data_char.Value.replace(var_type, target_value)
        """var_type = data_list[-1]
        if var_type != "PV" and var_type != "MV" and "@" not in content:
            if var_type in level.binding_dic:
                data_char.Value = data_char.Value.replace(var_type, level.binding_dic[var_type])
        else:
            if "@" in content:
                var_type = None
                target_value = None

                for key, value in level.binding_dic.items():
                    if value in ["PV", "MV"]:
                        var_type = key
                        target_value = value
                        break

                if var_type:
                    data_char.Value = data_char.Value.replace(var_type, target_value)"""
    process_conditions(level, child)
    process_bindings(level, child)
    return level


def readRect_rec(node, l, t, rt, ro, aux, tag_list, object_list, render_list, name, tuplas_report):
    for child in node:
        tag = child.tag
        if tag.endswith("IPCSRectangle"):
            rect1 = initRectangles(child, l, t, ro, aux, render_list, name, tuplas_report)
            update_tags_and_lists(rect1, None, tag_list, object_list)
        elif tag.endswith("IPCSSector"):
            sect1 = initSector(child, l, t, ro, aux, False, render_list, name, tuplas_report)
            update_tags_and_lists(sect1, None, tag_list, object_list)
        elif tag.endswith("IPCSArc"):
            arc1 = initSector(child, l, t, ro, aux, True, render_list, name, tuplas_report)
            update_tags_and_lists(arc1, None, tag_list, object_list)
        elif tag.endswith("IPCSEllipse") or tag.endswith("IPCSCircle"):
            elip = initEllipse(child, l, t, ro, aux, render_list, name, tuplas_report)
            update_tags_and_lists(elip, None, tag_list, object_list)
        elif tag.endswith("Text"):
            text = readText(child, l, t, rt, ro, aux, render_list, name, tuplas_report)
            text.ZIndex = child.attrib["Panel.ZIndex"]
            update_tags_and_lists(text, None, tag_list, object_list)
        elif tag.endswith("GroupComponent"):
            zindex = child.attrib["Panel.ZIndex"]
            initGroupComp(child, l, t, rt, ro, aux, tag_list, object_list, render_list, name, tuplas_report)
        elif tag.endswith("IPCSFillArea"):
            poly1 = initFillArea(child, l, t, ro, aux, render_list, name, tuplas_report)
            update_tags_and_lists(poly1, None, tag_list, object_list)
        elif tag.endswith("IPCSPolyLine"):
            line = init_polyline(child, l, t, ro, aux, render_list, name, tuplas_report)
            update_tags_and_lists(line, None, tag_list, object_list)
        elif tag.endswith("IPCSLine"):
            line = initLine(child, l, t, ro, aux, render_list, name, tuplas_report)
            update_tags_and_lists(line, None, tag_list, object_list)
        elif tag.endswith("ProcessDataCharacter"):
            text = readDataCharacter(child, l, t, rt, ro, aux, render_list, name, tuplas_report)
            update_tags_and_lists(text, None, tag_list, object_list)
            """elif tag.endswith("PenTool"):
                nombre_obj = child.attrib[("{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.Builder.Designer"
                                           ".Component;assembly=Yokogawa.IA.iPCS.Platform.View.Graphic.Builder"
                                           ".Designer}ComponentProperties.Name")]
                typeYoko = "IPCSPenTool"
                typeIIS = "None"
                priority = 10
                description = "Non-emulated Yokogawa object. IIS does not have PenTool object to add to the screen."
                tuplas_report.append([name, nombre_obj, typeYoko, typeIIS, priority, description])
            elif tag.endswith("Marker"):
                nombre_obj = child.attrib[("{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.Builder.Designer"
                                           ".Component;assembly=Yokogawa.IA.iPCS.Platform.View.Graphic.Builder"
                                           ".Designer}ComponentProperties.Name")]
                typeYoko = "IPCSMarker"
                typeIIS = "None"
                priority = 10
                description = "Non-emulated Yokogawa object. IIS does not have Marker object to add to the screen."
                tuplas_report.append([name, nombre_obj, typeYoko, typeIIS, priority, description])"""
        elif tag.endswith("PushButton"):
            button = readButton(child, l, t, ro, aux, render_list, name, tuplas_report)
            if button:
                process_bindings(button, child)
                process_conditions(button, child)
                for bind in button.Binding:
                    data_tag = button.DataTag
                    data = data_tag.split('.')
                    if bind.GenericName == data[0]:
                        button.DataTag = data_tag.replace(data[0], bind.Value)

                update_tags_and_lists(button, None, tag_list, object_list)
                """object_list.append(button)"""
        elif tag.endswith("ProcessDataBar"):
            level = init_level(child, l, t, ro, aux, render_list, name, tuplas_report)
            update_tags_and_lists(level, None, tag_list, object_list)
        elif tag.endswith("TouchTarget"):
            touch = readTouch(child, l, t, ro, aux, render_list, name, tuplas_report, tag_list)
            if touch:
                object_list.append(touch)
            """nombre_obj = child.attrib[("{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.Builder.Designer"
                                       ".Component;assembly=Yokogawa.IA.iPCS.Platform.View.Graphic.Builder"
                                       ".Designer}ComponentProperties.Name")]
            typeYoko = "TouchTarget"
            typeIIS = "None"
            priority = 10
            description = "Non-emulated Yokogawa object. IIS does not have TouchTarget object to add to the screen."
            tuplas_report.append([name, nombre_obj, typeYoko, typeIIS, priority, description])"""

    return tag_list, object_list, tuplas_report


def readButton(child, l, t, ro, aux, render_list, name, tuplas_report):
    button = Button.default()
    attrib = child.attrib
    set_common_attributes(button, child, ro, l, t, aux, render_list, name, tuplas_report)
    button.Height = attrib.get("Height", "")
    button.Width = attrib.get("Width", "")
    text = attrib.get("Text", "")
    button.Text = text
    """button.Text = attrib.get("Text", "")"""
    button.Foreground = attrib.get("Foreground", "")
    if "Background" in attrib:
        button.Background = parse_fill(attrib.get("Background"))
        #button.Background = attrib.get("Background")
    else:
        button.Background = "#00FFFFFF"
    button.FontFamily = attrib.get("FontFamily")
    if "FontWeight" in attrib and "Null" not in attrib["FontWeight"]:
        button.FontWeight = attrib.get("FontWeight")
    else:
        button.FontWeight = "Normal"
    button.FontSize = attrib.get("FontSize")
    for binding in child.findall('.//{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.GenericName;assembly'
                                 '=Yokogawa.IA.iPCS.Platform.View.Graphic.GenericName}GNBinding'):
        bind = Binding.default()
        bind.GenericName = binding.attrib.get("GenericName", "")
        bind.Value = binding.attrib.get("Value", "")
        if text == bind.GenericName:
            if '    ' in bind.Value:
                if bind.Value.startswith('    '):
                    bind.Value = bind.Value[4:]
                    button.Text = bind.Value.replace("    ", '\n')
            else:
                button.Text = bind.Value
        """ or "TagInventat_" + ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=5))"""
        for funct in child.findall(
                './/{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.FunctionLink.Control;assembly'
                '=Yokogawa.IA.iPCS.Platform.View.Graphic.FunctionLink.Control'
                '}FunctionLinkControlCommandParameter'):
            if "type=callWindow;target=graphic;parameter=" + str(bind.GenericName) in funct.attrib.get(
                    "FunctionAndParameter", ""):
                button.Screen = bind.Value
                button.FunctionType = "callWindow"
                return button
            elif "type=instrumentCommand;cmbDataType=ProcessData;" in funct.attrib.get(
                    "FunctionAndParameter", ""):
                input_str = funct.attrib.get("FunctionAndParameter", "")
                data_dict = dict(item.split("=") for item in input_str.split(";") if "=" in item)

                # Extraemos los valores de txtData y commandData
                txt_data = data_dict.get("txtData")
                command_data = data_dict.get("commandData")

                button.FunctionType = "instrumentCommand"
                button.DataTag = txt_data
                button.CommandData = command_data


def readTouch(child, l, t, ro, aux, render_list, name, tuplas_report, tag_list):
    touch = Touch.default()
    attrib = child.attrib

    """rect1.Width = attrib.get("ShapeWidth", "")
    rect1.Height = attrib.get("ShapeHeight", "")
    rect1.Tag = attrib.get("Tag", "")
    rect1.Stroke = attrib.get("Stroke", "")
    rect1.StrokeThickness = attrib.get("StrokeThickness", "")"""
    set_common_attributes(touch, child, ro, l, t, aux, render_list, name, tuplas_report)
    touch.Height = attrib.get("Height", "")
    touch.Width = attrib.get("Width", "")
    touch.Stroke = attrib.get("BorderBrush")
    if not touch.Stroke:
        touch.Stroke = "White"
    for binding in child.findall('.//{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.GenericName;assembly'
                                 '=Yokogawa.IA.iPCS.Platform.View.Graphic.GenericName}GNBinding'):
        bind = Binding.default()
        bind.GenericName = binding.attrib.get("GenericName", "")
        bind.Value = binding.attrib.get("Value", "")
        """ or "TagInventat_" + ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=5))"""
        for funct in child.findall(
                './/{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.FunctionLink.Control;assembly'
                '=Yokogawa.IA.iPCS.Platform.View.Graphic.FunctionLink.Control'
                '}FunctionLinkControlCommandParameter'):
            if "type=callWindow;target=graphic" in funct.attrib.get("FunctionAndParameter", ""):
                touch.Screen = bind.Value
                touch.FunctionType = "callWindow"
                return touch
            elif "type=instrumentCommand;cmbDataType=ProcessData;" in funct.attrib.get(
                    "FunctionAndParameter", ""):
                input_str = funct.attrib.get("FunctionAndParameter", "")
                data_dict = dict(item.split("=") for item in input_str.split(";") if "=" in item)

                # Extraemos los valores de txtData y commandData
                txt_data = data_dict.get("txtData")
                if "$_STATIONNAME" in txt_data:
                    tag1 = Tag.default()
                    tag1.ID = uuid.uuid4()
                    tag1.Name = txt_data
                    tag1.HysysVar = "0@@100@@IIS.Saw" + str(tag1.Name)
                    tag_list.append(tag1)

                command_data = data_dict.get("commandData")
                # Imprimimos los resultados
                """print("txtData:", txt_data)
                print("commandData:", command_data)"""
                touch.FunctionType = "instrumentCommand"
                touch.DataTag = txt_data
                touch.CommandData = command_data
                return touch
            elif "type=callWindow;target=faceplate;" in funct.attrib.get(
                    "FunctionAndParameter", ""):
                #TODO: read Tag and initialize faceplate PVI
                input_str = funct.attrib.get("FunctionAndParameter", "")
                data_dict = dict(item.split("=") for item in input_str.split(";") if "=" in item)
                tag_faceplate = data_dict.get("parameter")
                if bind.GenericName == tag_faceplate and bind.Value != "":
                    touch.Faceplate = bind.Value
                    return touch

def force_zindex(zindex_list, zindexGroup):
    sorted_list = sorted(zindex_list, key=lambda object1: int(object1.ZIndex))
    for index, obj in enumerate(sorted_list):
        obj.ZIndex = str(int(zindexGroup) + int(index))


"""def readTags(object):
    tag_list = []
    # Iterar sobre una copia de la lista original
    for cond in object.IISCondition[:]:
        removed = False
        for bind in object.Binding:
            if bind.Value != "":
                tag1 = Tag.default()
                if str(bind.GenericName) + ".MV" in cond.Expression:
                    if bind.Value is not None:
                        tag1.Name = str(bind.Value) + ".MV"
                    tag1.HysysVar = "@@@@" + str(tag1.Name)
                elif str(bind.GenericName) + ".PV" in cond.Expression:
                    if bind.Value is not None:
                        tag1.Name = str(bind.Value) + ".PV"
                    tag1.HysysVar = "@@@@" + str(tag1.Name)
                tag_list.append(tag1)
            else:
                object.IISCondition.remove(cond)
                break  # Salir del bucle interno si se elimina la condición
    return tag_list"""

#FER QUE AGAFI ELS TAGS CORRECTAMENT, NO AFEGIR TAGS REPETITS, CAMBIAR EL BINDING (GenericName=TAG.NAME / Value=Tag.Name)
"""def readTags(object):
    tag_list = []
    # Iterar sobre una copia de la lista original
    for cond in object.IISCondition[:]:
        removed = False
        for bind in object.Binding:
            cond.Expression = cond.Expression.replace(bind.GenericName, bind.Value)
        pattern = r'\b[\w-]+\.(?:PV|MV)[\w]*\b'
        match = re.search(pattern, cond.Expression)
        if match:
            for m in match.:
                tag1 = Tag.default()
                tag1.Name = m.group(0)
                tag1.HysysVar = "@@@@" + str(tag1.Name)
                if not any(tag.Name == tag1.Name for tag in tag_list):
                    tag_list.append(tag1)
                    print(match.group(0))


    return tag_list"""


def readTags(object):
    tag_list = []
    binding_dict = {}
    binding_list = object.Binding
    condition_list = object.IISCondition

    for cond in condition_list:
        if cond:
            for bind in binding_list:
                if bind:
                    if "$_STATIONNAME" not in bind.GenericName and bind.Value != "":
                        cond.Expression = cond.Expression.replace(bind.GenericName, bind.Value)
            if "$" in cond.Expression and "$_STATIONNAME" not in cond.Expression:
                cond.Expression = "1>2"
            if "$_STATIONNAME" in cond.Expression:
                pattern = r'\b[\w$-]*STATIONNAME[\w$-]*\.(?:PV|MV)[\w]*\b'
                matches = re.findall(pattern, cond.Expression)
                for match in matches:
                    tag1 = Tag.default()
                    tag1.Name = match
                    binding_dict[match] = match
                    tag1.HysysVar = "0@@100@@IIS.Saw" + str(tag1.Name)
                    if not any(tag.Name == tag1.Name for tag in tag_list):
                        tag_list.append(tag1)
            pattern = r'\b[\w-]+\.(?:PV|MV|MODE|CMOD|OMOD|#PV|ALRM|AOFS|AFLS)[\w]*\b'
            matches = re.findall(pattern, cond.Expression)
            for match in matches:
                if match != "_STATIONNAME.PV":
                    binding_dict[match] = match
                    tag1 = Tag.default()
                    tag1.Name = match
                    tag1.HysysVar = "0@@100@@IIS.Saw" + str(tag1.Name)
                    if not any(tag.Name == tag1.Name for tag in tag_list):
                        tag_list.append(tag1)
    object.Binding = []
    for key, value in binding_dict.items():
        bind = Binding.default()
        bind.GenericName = bind.Value = value
        object.Binding.append(bind)
    return tag_list


"""def readTags(object):
    tag_list = []
    conditions_to_remove = []

    # Iterar sobre una copia de la lista original
    for cond in object.IISCondition[:]:
        if cond:
            for bind in object.Binding:
                if bind.Value != "":
                    # Reemplazar el nombre genérico con el valor
                    expression = cond.Expression.replace(bind.GenericName, bind.Value)
                    if re.search(r'#PV[\w]*|#MV[\w]*', expression):  # Buscar patrones #PV o #MV con caracteres adicionales
                        conditions_to_remove.append(cond)
                        break  # Salir del bucle si encontramos #PV o #MV
                    else:
                        cond.Expression = expression

    for cond in object.IISCondition:
        if cond:
            if "$" in cond.Expression and "_STATIONNAME" not in cond.Expression:
                cond.Expression = "1>2"

    object.Binding.clear()

    # Eliminar las condiciones marcadas para eliminar
    for cond in conditions_to_remove:
        if cond:
            object.IISCondition.remove(cond)

    # Procesar los tags después de eliminar las condiciones
    for cond in object.IISCondition:
        # Expresión regular para buscar todas las coincidencias con .PV o .MV y caracteres adicionales
        #pattern = r'\b[\w-]+\.(?:PV|MV)[\w]*\b'
        if cond:
            pattern = r'\b[\w$-]*STATIONNAME[\w$-]*\.(?:PV|MV)[\w]*\b'
            matches = re.findall(pattern, cond.Expression)

            for match in matches:
                tag1 = Tag.default()
                tag1.Name = match
                tag1.HysysVar = "0@@100@@IIS.Saw" + str(tag1.Name)

                if not any(tag.Name == tag1.Name for tag in tag_list):
                    tag_list.append(tag1)
                    binding = Binding.default()
                    if ".PV" in tag1.Name:
                        part = tag1.Name.split('.')
                        binding.GenericName = part[0]
                    else:
                        part = tag1.Name.split('.')
                        binding.GenericName = part[0]
                    binding.Value = binding.GenericName
                    if not any(bindi.GenericName == binding.GenericName for bindi in object.Binding):
                        object.Binding.append(binding)

    if not object.Binding:
        for cond in object.IISCondition:
            if cond:
                pattern = r'\b([\w-]+)\.[\w]+\b'
                matches = re.findall(pattern, cond.Expression)

                for match in matches:
                    tag1 = Tag.default()
                    tag1.Name = match
                    tag1.HysysVar = "0@@100@@" + str(tag1.Name)

                    if not any(tag.Name == tag1.Name for tag in tag_list):
                        tag_list.append(tag1)
                        binding = Binding.default()
                        binding.GenericName = tag1.Name
                        binding.Value = tag1.Name
                        if not any(bindi.GenericName == binding.GenericName for bindi in object.Binding):
                            object.Binding.append(binding)

    return tag_list"""


def readConditions(node, rect):
    condition_namespace = '{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel;assembly=Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel}'

    for condition in node.findall(f'.//{condition_namespace}Condition'):
        cond = IISCondition.default()  # Assuming default() initializes an instance with default values
        cond.Expression = condition.attrib.get("Expression", "")

        var = condition.find(f'./{condition_namespace}ColorChange')
        if var is not None:
            cond.ColorChangeType = var.attrib.get("ColorChangeType", "")
            cond.Color = var.attrib.get("Color", "")
            cond.PropertyNameCC = var.attrib.get("PropertyNameCC", "")

        rect.IISCondition.append(cond)


def update_tags_and_lists(obj, obj_list, tag_list, object_list):
    tag_l = readTags(obj)
    for tag in tag_l:
        if tag.Name not in [t.Name for t in tag_list] and tag.Name != "":
            tag_list.append(tag)
    if obj_list is not None:
        obj_list.append(obj)
    object_list.append(obj)


def initSector(child, l, t, ro, aux, is_arc, render_list, name, tuplas_report):
    sect1 = Arc.default() if is_arc else Sector.default()
    if all(attr in child.attrib for attr in
           ["Size", "SweepDirection", "IsLargeArc", "StartPoint", "EndPoint", "RotationAngle"]):
        start_point = parse_point(child.attrib["StartPoint"])
        end_point = parse_point(child.attrib["EndPoint"])
        rotate_angle = float(child.attrib["RotationAngle"])
        width, height = parse_size(child)
        size = Size(width, height)
        sect1.Width = max(start_point.X, end_point.X, width)
        sect1.Height = max(start_point.Y, end_point.Y, height)
        is_large_arc = child.attrib["IsLargeArc"] != "False"
        sd = SweepDirection.Counterclockwise if child.attrib[
                                                    "SweepDirection"] == "Counterclockwise" else SweepDirection.Clockwise
        result = GetArcCenterPoint(start_point, end_point, int(rotate_angle), size, is_large_arc, sd)

        if result:
            center_point, angle_start_deg, angle_end_deg = result
            sect1.StartAngle = angle_start_deg
            sect1.EndAngle = angle_end_deg

    set_common_attributes(sect1, child, ro, l, t, aux, render_list, name, tuplas_report)
    process_conditions(sect1, child)
    process_bindings(sect1, child)

    return sect1


def initFillArea(child, l, t, ro, aux, render_list, name, tuplas_report):
    poly1 = Polygon.default()
    if "Points" in child.attrib:
        points = [tuple(map(float, pair.split(','))) for pair in child.attrib["Points"].split()]
        poly1.Width = max(x for x, y in points)
        poly1.Height = max(y for x, y in points)
        poly1.Points.extend(XPoint(x, y) for x, y in points)
    attrib = child.attrib
    set_common_attributes(poly1, child, ro, l, t, aux, render_list, name, tuplas_report)
    process_conditions(poly1, child)
    process_bindings(poly1, child)
    poly1.DataLinkInfo = []
    # Recolectar los bindings: { "$TAG": "65FC2", "$XYZ": "value", ... }
    bindings = {}
    for binding in child.findall(".//{*}GNBinding"):
        generic_name = binding.attrib.get("GenericName")
        value = binding.attrib.get("Value")
        if generic_name and value:
            bindings[generic_name] = value
    def replace_placeholders(s):
        for key, val in bindings.items():
            s = s.replace(key, val)
        return s

    # Set Fill color
    fill_attr = attrib.get("Fill", "")
    if "Fill" in attrib and "Null" not in fill_attr:
        fill = replace_placeholders(fill_attr)
        poly1.Fill = parse_fill(fill) if 'Gradient' in fill else fill
    else:
        poly1.Fill = "#00FF0000"
    for dl_modifiers in child.findall(".//{*}DataLinkModifier"):
        for data_link in dl_modifiers.findall(".//{*}AdvanceDataLink"):
            info = {
                "HighLimit": replace_placeholders(data_link.attrib.get("HighLimit", "")),
                "LowLimit": replace_placeholders(data_link.attrib.get("LowLimit", "")),
                "PropertyName": replace_placeholders(data_link.attrib.get("PropertyName", "")),
                "Value": replace_placeholders(data_link.attrib.get("Value", "")),
                "TransformFrom": None,
                "TransformTo": None,
                "OffSet": None  # <--- Añadido
            }

            # TransformFrom
            tf = data_link.find(".//{*}AdvanceDataLink.TransformFrom/{*}Double")
            if tf is not None:
                info["TransformFrom"] = float(tf.text)

            # TransformTo
            tt = data_link.find(".//{*}AdvanceDataLink.TransformTo/{*}Double")
            if tt is not None:
                info["TransformTo"] = float(tt.text)

            # OffSet <--- Nuevo
            offset = data_link.find(".//{*}AdvanceDataLink.OffSet/{*}Double")
            if offset is not None:
                info["OffSet"] = float(offset.text)

            poly1.DataLinkInfo.append(info)
    return poly1


def initEllipse(child, l, t, ro, aux, render_list, name, tuplas_report):
    ellipse = Ellipse.default()
    set_common_attributes(ellipse, child, ro, l, t, aux, render_list, name, tuplas_report)
    process_conditions(ellipse, child)
    process_bindings(ellipse, child)
    return ellipse
