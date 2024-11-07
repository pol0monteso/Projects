import re
import numpy as np
from Classes.ClassControls import *
import xml.etree.ElementTree as ET
from Classes.LogicClass import *


# Funciones utilitarias para reducir redundancias
def parse_size(child):
    size_components = child.attrib["Size"].split(',')
    return float(size_components[0]), float(size_components[1])


def parse_point(attr):
    return Point(*map(float, attr.split(',')))


def parse_render_transform(rt, child):
    if rt == "":
        if "RenderTransform" in child.attrib:
            return child.attrib["RenderTransform"]
        else:
            return rt
    else:
        if rt == "Identity":
            return "1,0,0,1,0,0"
        else:
            if rt != "" and "RenderTransform" not in child.attrib:
                elements = rt.split(',')
                if elements is not None:
                    for i, val in enumerate(elements):
                        if (float(elements[i]) < 1 and float(elements[i])) > 0 or (-1 < float(elements[i]) < 0):
                            elements[i] = 0
                    return (
                        "{0},{1},{2},{3},{4},{5}".format(str(elements[0]), str(elements[1]), str(elements[2]),
                                                         str(elements[3]), str(elements[4]), str(elements[5])))
            else:
                return rt


def parse_render_transform2(child, render_list):
    if render_list:
        if len(render_list) > 1:
            acc_matrix = np.array([[1, 0], [0, 1]])
            for render in render_list:
                render_matrix = string_to_matrix(sanitZero(render))
                acc_matrix = np.dot(acc_matrix, np.transpose(render_matrix))
            if "RenderTransform" in child.attrib:
                return matrix_to_string(np.dot(acc_matrix, np.transpose(child.attrib("RenderTransform"))))
            else:
                return matrix_to_string(acc_matrix)
        else:
            return render_list[0]
    else:
        if "RenderTransform" in child.attrib:
            return child.attrib("RenderTransform")
        else:
            return "1,0,0,1,0,0"
















"""if rt == "Identity":
        return "1,0,0,1,0,0"
    if rt and "RenderTransform" not in child.attrib:
        # Convertir los valores a enteros cuando sea necesario
        elements = [0 if (-1 < float(e) < 0 or 0 < float(e) < 1) else int(1) for e in rt.split(',')]
        return "{},{},{},{},{},{}".format(*elements)
    if rt == "" and "RenderTransform" in child.attrib:
        return child.attrib["RenderTransform"]
    return rt"""


def parse_fill(fill):
    match = re.search(r'Color1=([#A-Fa-f0-9]+), Color2=([#A-Fa-f0-9]+)', fill)
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


def set_common_attributes(obj, child, rt, ro, l, t, aux):
    attrs = {"Tag", "Stroke", "StrokeThickness", "Fill", "ShapeWidth", "ShapeHeight", "Canvas.Left", "Canvas.Top"}
    for attr in attrs:
        if attr in child.attrib:
            setattr(obj, attr.replace("Canvas.", ""), child.attrib[attr])

    obj.Fill = parse_fill(child.attrib["Fill"]) if "Fill" in child.attrib else obj.Fill
    obj.RenderTransform = parse_render_transform(rt, child)

    if aux and "Canvas.Left" in child.attrib and "Canvas.Top" in child.attrib:
        calculateTransHelper(obj.RenderTransform, child.attrib["Canvas.Left"], l, child.attrib["Canvas.Top"], t,
                                   obj)
    elif "Canvas.Left" in child.attrib and "Canvas.Top" in child.attrib:
        obj.X = float(child.attrib["Canvas.Left"]) + float(l)
        obj.Y = float(child.attrib["Canvas.Top"]) + float(t)

    if "RenderTransformOrigin" in child.attrib:
        obj.RenderTransformOrigin = child.attrib["RenderTransformOrigin"]
    else:
        obj.RenderTransformOrigin = ro


def process_conditions(obj, child):
    for condition in child.findall('.//{clr-namespace:Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel'
                                   ';assembly=Yokogawa.IA.iPCS.Platform.View.Graphic.DataLink.DataModel}Condition'):
        cond = IISCondition.default()
        cond.Expression = re.sub(r'\b0\b', '0,0', condition.attrib.get("Expression", ""))
        cond.IISCondition = condition.attrib.get("Continuous", "")
        for action in condition:
            for type in action:
                if type.tag.endswith("ColorChange"):
                    cond.ColorC = type.attrib.get("Color", "")
                    cond.ColorChangeType = type.attrib.get("ColorChangeType", "")
                    cond.PropertyNameCC = type.attrib.get("PropertyName", "")
                if type.tag.endswith("Blinking"):
                    cond.PropertyNameBLK = type.attrib.get("PropertyName", "")
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


def readText(child, l, t, rt, ro, aux):
    text1 = Text.default()

    xml_data = ET.tostring(child, encoding='unicode')
    pattern = r'</[^:]*:GenericNameComponent\.GenericName>(.*?)</[^:]*:Text>'
    matches = re.findall(pattern, xml_data, re.DOTALL)

    if matches:
        text1.Text = matches[0]

    attrib = child.attrib
    text1.FontSize = attrib.get("FontSize", "")
    text1.FontFamily = attrib.get("FontFamily", "")
    text1.Foreground = attrib.get("Foreground", "")
    text1.Background = attrib.get("Background", "")

    if "Canvas.Left" in attrib and "Canvas.Top" in attrib:
        x_offset = float(attrib["Canvas.Left"]) + float(l)
        y_offset = float(attrib["Canvas.Top"]) + float(t)
        text1.X = x_offset
        text1.Y = y_offset

    process_conditions(text1, child)
    process_bindings(text1, child)

    return text1


def initRectangles(child, l, t, rt, ro, aux):
    rect1 = Rectangle.default()
    attrib = child.attrib

    rect1.Width = attrib.get("ShapeWidth", "")
    rect1.Height = attrib.get("ShapeHeight", "")
    rect1.Tag = attrib.get("Tag", "")
    rect1.Stroke = attrib.get("Stroke", "")
    rect1.StrokeThickness = attrib.get("StrokeThickness", "")

    fill = attrib.get("Fill", "")
    rect1.Fill = parse_fill(fill) if 'Gradient' in fill else fill

    rect1.RenderTransform = parse_render_transform(rt, child)

    if "Canvas.Left" in attrib and "Canvas.Top" in attrib:
        x_offset = float(attrib["Canvas.Left"]) + float(l)
        y_offset = float(attrib["Canvas.Top"]) + float(t)
        if aux:
            calculateTransHelper(rect1.RenderTransform, attrib["Canvas.Left"], l, attrib["Canvas.Top"], t, rect1)
        else:
            rect1.X = x_offset
            rect1.Y = y_offset

    rect1.RenderTransformOrigin = ro

    process_conditions(rect1, child)
    process_bindings(rect1, child)

    return rect1


def initGroupComp(child, l, t, rt, ro, aux, tag_list, object_list):
    cl = float(child.attrib["Canvas.Left"]) + float(l)
    ct = float(child.attrib["Canvas.Top"]) + float(t)

    if "RenderTransform" in child.attrib:
        if aux:
            rt = child.attrib["RenderTransform"]
        else:
            rt = str(child.attrib["RenderTransform"])
        ro = str(child.attrib["RenderTransformOrigin"])
        readRect_rec(child, cl, ct, rt, ro, True, tag_list, object_list)
    else:
        rt = ""
        ro = ""
        aux = False
        readRect_rec(child, cl, ct, rt, ro, aux, tag_list, object_list)


def initGroupComp2(child, l, t, rt, ro, aux, tag_list, object_list, render_list):
    cl = float(child.attrib["Canvas.Left"]) + float(l)
    ct = float(child.attrib["Canvas.Top"]) + float(t)

    if "RenderTransform" in child.attrib:
        render_list.append(child.attrib["RenderTransform"])
        ro = str(child.attrib["RenderTransformOrigin"])
    else:
        rt = ""
        ro = ""
        aux = False
    readRect_rec(child, cl, ct, rt, ro, aux, tag_list, object_list)


def readRect_rec(node, l, t, rt, ro, aux, tag_list, object_list):
    for child in node:
        tag = child.tag
        if tag.endswith("IPCSRectangle"):
            rect1 = initRectangles(child, l, t, rt, ro, aux)
            update_tags_and_lists(rect1, None, tag_list, object_list)
        elif tag.endswith("IPCSSector"):
            sect1 = initSector(child, l, t, rt, ro, aux, False)
            update_tags_and_lists(sect1, None, tag_list, object_list)
        elif tag.endswith("IPCSArc"):
            arc1 = initSector(child, l, t, rt, ro, aux, True)
            update_tags_and_lists(arc1, None, tag_list, object_list)
        elif tag.endswith("IPCSEllipse") or tag.endswith("IPCSCircle"):
            elip = initEllipse(child, l, t, rt, ro, aux)
            update_tags_and_lists(elip, None, tag_list, object_list)
        elif tag.endswith("GroupComponent"):
            initGroupComp(child, l, t, rt, ro, aux, tag_list, object_list)
        elif tag.endswith("IPCSFillArea"):
            poly1 = initFillArea(child, l, t, rt, ro, aux)
            update_tags_and_lists(poly1, None, tag_list, object_list)

    return tag_list, object_list


def readTags(object):
    tag_list = []
    for cond in object.IISCondition:
        for bind in object.Binding:
            tag1 = Tag.default()
            if str(bind.GenericName) + ".MV" in cond.Expression:
                if bind.Value != None: tag1.Name = str(bind.Value) + ".MV"
                tag1.HysysVar = "@@@@" + str(tag1.Name)
            elif str(bind.GenericName) + ".PV" in cond.Expression:
                if bind.Value != None: tag1.Name = str(bind.Value) + ".PV"
                tag1.HysysVar = "@@@@" + str(tag1.Name)
            tag_list.append(tag1)
    return tag_list


"""def readTags(object):
    tag_list = []
    # Utilizamos un set para evitar etiquetas duplicadas
    seen_tags = set()

    for cond in object.IISCondition:
        for bind in object.Binding:
            generic_name_mv = f"{bind.GenericName}.MV"
            generic_name_pv = f"{bind.GenericName}.PV"

            if generic_name_mv in cond.Expression or generic_name_pv in cond.Expression:
                if bind.Value != "":
                    tag_name = f"{bind.Value}.{generic_name_mv.split('.')[-1]}"
                    if tag_name not in seen_tags:
                        tag1 = Tag.default()
                        tag1.Name = tag_name
                        tag1.HysysVar = f"@@@@@{tag_name}"
                        tag_list.append(tag1)
                        seen_tags.add(tag_name)

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


def initSector(child, l, t, rt, ro, aux, is_arc):
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

    set_common_attributes(sect1, child, rt, ro, l, t, aux)
    process_conditions(sect1, child)
    process_bindings(sect1, child)

    return sect1


def initFillArea(child, l, t, rt, ro, aux):
    poly1 = Polygon.default()
    if "Points" in child.attrib:
        points = [tuple(map(float, pair.split(','))) for pair in child.attrib["Points"].split()]
        poly1.Width = max(x for x, y in points)
        poly1.Height = max(y for x, y in points)
        poly1.Points.extend(Point(x, y) for x, y in points)

    set_common_attributes(poly1, child, rt, ro, l, t, aux)
    process_conditions(poly1, child)
    process_bindings(poly1, child)
    return poly1


def initEllipse(child, l, t, rt, ro, aux):
    ellipse = Ellipse.default()
    set_common_attributes(ellipse, child, rt, ro, l, t, aux)
    process_conditions(ellipse, child)
    process_bindings(ellipse, child)
    return ellipse
