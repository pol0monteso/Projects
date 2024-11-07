import xml.etree.ElementTree as ET
from Classes.LogicClass import *
from Body.ReadingAlgorithm import readRect_rec
from Utils.Utils import *


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


def writeTouch(window_elem, touch, windows_dict):
    """id_ = uuid.uuid4()
    windows_dict[touch.Screen] = str(id_)"""

    touch_elem = ET.SubElement(window_elem, "Touch",
                               Stroke=touch.Stroke,
                               Screen=touch.Screen, #str(id_),
                               Height=touch.Height,
                               Width=touch.Width,
                               RenderTransform=touch.RenderTransform,
                               RenderTransformOrigin=touch.RenderTransformOrigin,
                               X=str(touch.X),
                               Y=str(touch.Y),
                               ShapeName=touch.ShapeName)

def writeTags(tag_list, tags, project_tree, tagName_list):
    if tag_list:
        for t in tag_list:
            if t.Name not in tagName_list and (
                    ".PV" in t.Name or ".MV" in t.Name):  # Verificamos si el nombre no está en la lista
                ET.SubElement(tags, "Tag",
                              ID=str(t.ID),
                              Name=str(t.Name),
                              HysysVar=str(t.HysysVar),
                              NumDecimals=str(t.NumDecimals),
                              HysysVarUnit=str(t.HysysVarUnit))
                tagName_list.append(str(t.Name))  # Añadimos el nombre a la lista después de crear el subelemento
            elif t.Name not in tagName_list and (
                    ".ALMPV" in t.Name):
                ET.SubElement(tags, "Tag",
                              ID=str(t.ID),
                              Name=str(t.Name),
                              HysysVar=str(t.HysysVar),
                              NumDecimals=str(t.NumDecimals),
                              HysysVarUnit=str(t.HysysVarUnit))
                tagName_list.append(str(t.Name))  # Añadimos el nombre a la lista después de crear el subelemento
        #Escribimos el archivo solo una vez después de añadir todos los elementos
        """project_tree.write("project.xml", encoding="utf-8", xml_declaration=True)"""


def initScreen(root, project, windows, project_tree, tags, name, tagName_list, units, tuplas_report, alarms,
               alarms_dict, window_dict, touch_list, alarmsPriority_dict, button_list):
    print("Starting...")
    # Define la estructura del árbol XML con los valores proporcionados
    window = ET.SubElement(windows, "Window")
    size = writeWindow(root, window, name, window_dict)

    tag_list, object_list, tuples = readRect_rec(root, 0, 0, "", "", False, [], [], [], name, tuplas_report)
    object_list = orderByZIndex(object_list)
    for obj in object_list:
        if type(obj) == Touch:
            obj.Window = window
            touch_list.append(obj)
        elif type(obj) == Button:
            obj.Window = window
            button_list.append(obj)

    print("TAGS llegits")
    print("OBJECTES llegits")
    writeObjects(object_list, window, project_tree, size, tag_list, units, alarms, alarms_dict, window_dict, alarmsPriority_dict)
    writeTags(tag_list, tags, project_tree, tagName_list)
    print("AFEGIT A XML")
    indent(project)

    """project_tree.write("project.xml", encoding="utf-8", xml_declaration=True)"""
    return tuples, window_dict, touch_list


def writeObjects(object_list, window, project_tree, size, tag_list, units, alarms, alarms_dict, windows_dict, alarmPriority_dict):
    shape_name_map = {
        Rectangle: "rect_",
        Sector: "sect_",
        Arc: "arc_",
        Polygon: "polygon_",
        Ellipse: "ellipse_",
        Line: "polyline_",
        Text: "text_",
        ProcessData: "dataChar_",
        Touch: "touch_",
        Level:"level_"
    }
    for idx, obj in enumerate(object_list):
        shape_type = type(obj)
        if obj.Width == size.Width:
            obj.Width = float(obj.Width) - 1
        elif obj.Height == size.Height:
            obj.Height = float(obj.Height) - 1
        if shape_type in shape_name_map:
            #obj.ShapeName = f"{shape_name_map[shape_type]}{idx}"
            if shape_type == Rectangle:
                writeRect(obj, window, project_tree)
            elif shape_type == Sector:
                writeSector(obj, window, project_tree)
            elif shape_type == Arc:
                writeArc(obj, window, project_tree)
            elif shape_type == Polygon:
                writePolygon(obj, window, project_tree)
            elif shape_type == Ellipse:
                writeEllipse(obj, window, project_tree)
            elif shape_type == Line:
                writePolyLine(obj, window, project_tree)
            elif shape_type == Text:
                writeText(obj, window, project_tree, units, tag_list, alarms, alarms_dict, alarmPriority_dict)
            elif shape_type == ProcessData:
                writeDataCharacter(obj, window, tag_list, units)
            elif shape_type == Level:
                write_level(obj, window, project_tree, tag_list)
            """elif shape_type == Touch:
                writeTouch(window, obj, windows_dict)"""


def writeShape(object, shape_type, window, project_tree):
    shape_element = ET.SubElement(window, shape_type,
                                  Width=str(object.Width),
                                  Height=str(object.Height),
                                  X=str(object.X),
                                  Y=str(object.Y),
                                  ShapeName=object.ShapeName,
                                  Fill=str(object.Fill),
                                  Stroke=str(object.Stroke),
                                  StrokeThickness=str(object.StrokeThickness),
                                  RenderTransform=str(object.RenderTransform),
                                  RenderTransformOrigin=str(object.RenderTransformOrigin),
                                  Rotation=str(object.Rotation))

    indent(shape_element)
    writeCondition(object, shape_element, project_tree)
    writeBinding(object, shape_element, project_tree)
    writePoints(object, shape_element)

    # Solo escribir el archivo una vez después de procesar todos los elementos
    # Esto evita múltiples escrituras durante el procesamiento
    return shape_element


def writeEndArrow(object, element):
    if object.arrowEnd is not None:
        ET.SubElement(element, "ArrowShapeProperty",
                      Width=str("10"),
                      Height=str(10),
                      Stroke=str(object.Stroke),
                      StrokeThickness=str(object.StrokeThickness),
                      isVisible=str(object.arrowEnd.isVisible),
                      FacingOutside="True",
                      FillEnabled="True",
                      PropertyName="EndArrow")
    else:
        ET.SubElement(element, "ArrowShapeProperty",
                      Width=str("10"),
                      Height=str(10),
                      Stroke=str(object.Stroke),
                      StrokeThickness=str(object.StrokeThickness),
                      IsVisible="False",
                      FacingOutside="True",
                      FillEnabled="True",
                      PropertyName="EndArrow")


def writeStartArrow(object, element):
    if object.arrowStart is not None:
        ET.SubElement(element, "ArrowShapeProperty",
                      Width=str("10"),
                      Height=str(10),
                      Stroke=str(object.Stroke),
                      StrokeThickness=str(object.StrokeThickness),
                      IsVisible=str(object.arrowStart.isVisible),
                      FacingOutside="True",
                      FillEnabled="True",
                      PropertyName="StartArrow")
    else:
        ET.SubElement(element, "ArrowShapeProperty",
                      Width=str("10"),
                      Height=str(10),
                      Stroke=str(object.Stroke),
                      StrokeThickness=str(object.StrokeThickness),
                      IsVisible="False",
                      FacingOutside="True",
                      FillEnabled="True",
                      PropertyName="StartArrow")

def writePolyLine(object, window, project_tree):
    line_element = ET.SubElement(window, "Line",
                                 Width=str(object.Width),
                                 Height=str(object.Height),
                                 X=str(object.X),
                                 Y=str(object.Y),
                                 ShapeName=object.ShapeName,
                                 RenderTransform=str(object.RenderTransform),
                                 RenderTransformOrigin=str(object.RenderTransformOrigin),
                                 Group="",
                                 TriggerTag="",
                                 TriggerValue="0")

    writeEndArrow(object, line_element)
    writeStartArrow(object, line_element)

    writeBindablePoints(object, line_element)
    ET.SubElement(line_element, "ShapeLayoutProperty",
                  Stroke=str(object.Stroke),
                  Thickness=str(object.StrokeThickness),
                  Layout=str(object.LineStyle),
                  PropertyName="LowerLayout")


def writeBindablePoints(object, element):
    if object.Points:
        polyline = ET.SubElement(element, "ISPolyline")
        points = ET.SubElement(polyline, "Points")
        for point in object.Points:
            ET.SubElement(points, "BindablePoint",
                          X=str(point.X),
                          Y=str(point.Y))


def writeEllipse(object, window, project_tree):
    sector_element = ET.SubElement(window, "Ellipse")
    writeShapeAttributes(sector_element, object)
    indent(sector_element)
    writeCondition(object, sector_element, project_tree)
    writeBinding(object, sector_element, project_tree)


def writePolygon(object, window, project_tree):
    writeShape(object, "Polygon", window, project_tree)


def writePoints(object, element):
    if object.Points:
        points = ET.SubElement(element, "Points")
        for point in object.Points:
            ET.SubElement(points, "Point",
                          X=str(point.X),
                          Y=str(point.Y))


def writeShapeAttributes(shape_element, shape_obj):
    shape_element.set("Width", str(shape_obj.Width))
    shape_element.set("Height", str(shape_obj.Height))
    shape_element.set("X", str(shape_obj.X))
    shape_element.set("Y", str(shape_obj.Y))
    shape_element.set("ShapeName", shape_obj.ShapeName)
    shape_element.set("Fill", str(shape_obj.Fill))
    shape_element.set("Stroke", str(shape_obj.Stroke))
    shape_element.set("StrokeThickness", str(shape_obj.StrokeThickness))
    shape_element.set("RenderTransform", str(shape_obj.RenderTransform))
    shape_element.set("RenderTransformOrigin", str(shape_obj.RenderTransformOrigin))
    shape_element.set("Angle", str(shape_obj.Rotation))


def writeSector(object, window, project_tree):
    sector_element = ET.SubElement(window, "Sector")
    writeShapeAttributes(sector_element, object)
    sector_element.set("StartAngle", str(object.StartAngle))
    sector_element.set("EndAngle", str(object.EndAngle))
    indent(sector_element)
    writeCondition(object, sector_element, project_tree)
    writeBinding(object, sector_element, project_tree)


def write_level(object, window, project_tree, tag_list):
    for bind in object.binding_dic:
        if ".PV" in object.dataChar.Value:
            for tag in tag_list:
                if str(object.binding_dic[bind]) + ".PV" == tag.Name:
                    object.LevelTag = tag.ID
            if object.LevelTag == "":
                tag1 = Tag.default()
                tag1.ID = uuid.uuid4()
                object.LevelTag = tag1.ID
                tag1.Name = str(object.binding_dic[bind]) + ".PV"
                tag1.HysysVar = "0@@100@@IIS.Saw" + str(tag1.Name)
                if tag1.Name == ".PV":
                    write = False
                else:
                    tag_list.append(tag1)
        elif ".MV" in object.dataChar.Value:
            for tag in tag_list:
                if str(object.binding_dic[bind]) + ".MV" == tag.Name:
                    object.LevelTag = tag.ID
            if object.LevelTag == "":
                tag1 = Tag.default()
                tag1.ID = uuid.uuid4()
                object.LevelTag = tag1.ID
                tag1.Name = str(object.binding_dic[bind]) + ".MV"
                tag1.HysysVar = "0@@100@@IIS.Saw" + str(tag1.Name)
                if tag1.Name == ".PV":
                    write = False
                else:
                    tag_list.append(tag1)

    level_element = ET.SubElement(window, "Level",
                                  Fill=str(object.Fill),
                                  Stroke=str(object.Stroke),
                                  StrokeThickness=str(object.StrokeThickness),
                                  Width=str(object.Width),
                                  Height=str(object.Height),
                                  X=str(object.X),
                                  Y=str(object.Y),
                                  LevelFill1=str(object.LevelFill1),
                                  Orientation=str(object.Orientation),
                                  LevelValue1=str(object.LevelValue1),
                                  LevelValue2=str(object.LevelValue2),
                                  LevelTag=str(object.LevelTag),
                                  MinValue=str(object.LevelValue1),
                                  MaxValue=str(object.LevelValue2)
    )

def writeDataCharacter(object, window, tag_list, units):
    write = True
    for bind in object.binding_dic:
        if bind in object.dataChar.Value:
            if ".PV" in object.dataChar.Value:
                for tag in tag_list:
                    if str(object.binding_dic[bind]) + ".PV" == tag.Name:
                        object.Tag = tag.ID
                if object.Tag == "":
                    tag1 = Tag.default()
                    tag1.ID = uuid.uuid4()
                    object.Tag = tag1.ID
                    tag1.Name = str(object.binding_dic[bind]) + ".PV"
                    tag1.HysysVar = "0@@100@@IIS.Saw" + str(tag1.Name)
                    if tag1.Name == ".PV":
                        write = False
                    else:
                        tag_list.append(tag1)
            elif ".MV" in object.dataChar.Value:
                for tag in tag_list:
                    if str(object.binding_dic[bind]) + ".MV" == tag.Name:
                        object.Tag = tag.ID
                if object.Tag == "":
                    tag1 = Tag.default()
                    tag1.ID = uuid.uuid4()
                    object.Tag = tag1.ID
                    tag1.Name = str(object.binding_dic[bind]) + ".MV"
                    tag1.HysysVar = "0@@100@@IIS.Saw" + str(tag1.Name)
                    if tag1.Name == ".PV":
                        write = False
                    else:
                        tag_list.append(tag1)
            elif "COMMENT" in object.dataChar.Value:
                if object.binding_dic[bind] in units:
                    unit_info = units[object.binding_dic[bind]]
                    object.Text = str(unit_info['Comment'])
                else:
                    object.Text = str("GGG")
            elif "." not in object.dataChar.Value:
                object.Text = str(object.binding_dic[bind])
            else:

                object.Text = "RRR"
    for tag_ in tag_list:
        if tag_.ID == object.Tag:
            if object.isVisibleUnits:
                # Aquí verificamos si la base del tag está en units
                tag_base_name = tag_.Name.split('.')[0]
                if tag_base_name in units:
                    unit_info = units[tag_base_name]
                    tag_.HysysVarUnit = unit_info['Unit']  # Asignamos la unidad
                    # No asignamos SH y SL a menos que se desee específicamente
                    """ Si quieres asignar SH y SL a algún lugar específico, 
                    puedes hacerlo aquí, por ejemplo:
                    tag_.SH = unit_info['SH']  
                    tag_.SL = unit_info['SL']
                    """
                else:
                    object.Text = ""
                    object.Tag = ""
                    tag_list.remove(tag_)  # Eliminar el tag de la lista
    """for tag_ in tag_list:
        if tag_.ID == object.Tag:
            if object.isVisibleUnits:
                if tag_.Name.split('.')[0] in units:
                    tag_.HysysVarUnit = units[tag_.Name.split('.')[0]]
                else:
                    object.Text = ""
                    object.Tag = ""
                    del tag_"""

    if write:
        data_element = ET.SubElement(window, "LabelText",
                                     FontAutoSize="True",
                                     Background=object.Background,
                                     Foreground=object.Foreground,
                                     FontSize=object.FontSize,
                                     FontFamily=object.FontFamily,
                                     TextAlign=object.TextAlign,
                                     Content=object.Text)
        data_element.set("Width", str(float(object.Width)))
        data_element.set("Height", str(object.Height))
        data_element.set("X", str(object.X))
        data_element.set("Y", str(object.Y))
        data_element.set("Tag", str(object.Tag))
        data_element.set("ShapeName", object.ShapeName)


def writeArc(object, window, project_tree):
    arc_element = ET.SubElement(window, "Arc")
    writeShapeAttributes(arc_element, object)
    arc_element.set("StartAngle", str(object.StartAngle))
    arc_element.set("EndAngle", str(object.EndAngle))
    indent(arc_element)
    writeCondition(object, arc_element, project_tree)
    writeBinding(object, arc_element, project_tree)


def writeTextElement(text_obj, window, units, tag_list, alarms, project_tree, alarms_dict, alarmPriority_dict):
    text_element = ET.SubElement(window, "DynamicText",
                                 FontAutoSize="False",
                                 Background=text_obj.Background,
                                 Foreground=text_obj.Foreground,
                                 Text=text_obj.Text,
                                 FontSize=text_obj.FontSize,
                                 FontFamily=text_obj.FontFamily,
                                 TextAlign=text_obj.TextAlign,
                                 ScaleX=str(text_obj.ScaleX),
                                 ScaleY=str(text_obj.ScaleY),
                                 RenderTransform=text_obj.RenderTransform,
                                 RenderTransformOrigin=text_obj.RenderTransformOrigin,
                                 FontWeight=text_obj.FontWeight)
    text_element.set("X", str(text_obj.X))
    text_element.set("Y", str(text_obj.Y))
    text_element.set("ShapeName", text_obj.ShapeName)
    for bind in text_obj.Binding:
        newBind = Binding.default()
        newBind.Value = newBind.GenericName = bind.GenericName
        for cond in text_obj.IISCondition:
            if (str(bind.Value) + '.ALRM<>"LL"') == cond.Expression:
                lista = check_alarm(units, bind.Value, "LL", window.attrib["ID"])
                if len(lista) == 2:
                    if lista[1].Name not in alarms_dict:
                        if str(bind.Value) + ".LL" in alarmPriority_dict:
                            if alarmPriority_dict[str(bind.Value) + ".LL"][0] == "High":
                                lista[1].Priority = "100"
                            elif alarmPriority_dict[str(bind.Value) + ".LL"][0] == "Medium":
                                lista[1].Priority = "0"
                            elif alarmPriority_dict[str(bind.Value) + ".LL"][0] == "Low":
                                lista[1].Priority = "110"
                            color = alarmPriority_dict[str(bind.Value) + ".LL"][1]
                            if color != "None":
                                cond.ColorC = alarmPriority_dict[str(bind.Value) + ".LL"][1]
                            else:
                                cond.ColorC = "Red"
                            if lista[1].Name not in alarms_dict:
                                alarms_dict[lista[1].Name] = lista[1]
                            writeAlarm(lista[1], alarms)
                        if cond.ColorC == "None":
                            cond.ColorC = ""
                        cond.Expression = str(lista[0].Name) + "==0,0"
                        tag_list.append(lista[0])
                        """alarms_dict[lista[1].Name] = lista[1]"""
                        bind.Value = bind.GenericName = lista[0].Name
            elif (str(bind.Value) + '.ALRM<>"LO"') == cond.Expression:
                lista = check_alarm(units, bind.Value, "L0", window.attrib["ID"])
                if len(lista) == 2:
                    if lista[1].Name not in alarms_dict:
                        if str(bind.Value) + ".LO" in alarmPriority_dict:
                            if alarmPriority_dict[str(bind.Value) + ".LO"][0] == "High":
                                lista[1].Priority = "100"
                            elif alarmPriority_dict[str(bind.Value) + ".LO"][0] == "Medium":
                                lista[1].Priority = "0"
                            elif alarmPriority_dict[str(bind.Value) + ".LO"][0] == "Low":
                                lista[1].Priority = "110"
                            color = alarmPriority_dict[str(bind.Value) + ".LO"][1]
                            if color != "None":
                                cond.ColorC = alarmPriority_dict[str(bind.Value) + ".LO"][1]
                            else:
                                cond.ColorC = "Yellow"
                            writeAlarm(lista[1], alarms)
                        cond.Expression = str(lista[0].Name) + "==0,0"
                        tag_list.append(lista[0])
                        """alarms_dict[lista[1].Name] = lista[1]"""
                        bind.Value = bind.GenericName = lista[0].Name
            elif (str(bind.Value) + '.ALRM<>"HH"') == cond.Expression:
                lista = check_alarm(units, bind.Value, "HH", window.attrib["ID"])
                if len(lista) == 2:
                    if lista[1].Name not in alarms_dict:
                        if str(bind.Value) + ".HH" in alarmPriority_dict:
                            if alarmPriority_dict[str(bind.Value) + ".HH"][0] == "High":
                                lista[1].Priority = "100"
                            elif alarmPriority_dict[str(bind.Value) + ".HH"][0] == "Medium":
                                lista[1].Priority = "0"
                            elif alarmPriority_dict[str(bind.Value) + ".HH"][0] == "Low":
                                lista[1].Priority = "110"
                            color = alarmPriority_dict[str(bind.Value) + ".HH"][1]
                            if color != "None":
                                cond.ColorC = alarmPriority_dict[str(bind.Value) + ".HH"][1]
                            else:
                                cond.ColorC = "Red"
                            writeAlarm(lista[1], alarms)
                        cond.Expression = str(lista[0].Name) + "==0,0"
                        tag_list.append(lista[0])
                        """alarms_dict[lista[1].Name] = lista[1]"""
                        bind.Value = bind.GenericName = lista[0].Name
            elif (str(bind.Value) + '.ALRM<>"HI"') == cond.Expression:
                lista = check_alarm(units, bind.Value, "HI", window.attrib["ID"])
                if len(lista) == 2:
                    if lista[1].Name not in alarms_dict:
                        if str(bind.Value) + ".HI" in alarmPriority_dict:
                            if alarmPriority_dict[str(bind.Value) + ".HI"][0] == "High":
                                lista[1].Priority = "100"
                            elif alarmPriority_dict[str(bind.Value) + ".HI"][0] == "Medium":
                                lista[1].Priority = "0"
                            elif alarmPriority_dict[str(bind.Value) + ".HI"][0] == "Low":
                                lista[1].Priority = "110"
                            color = alarmPriority_dict[str(bind.Value) + ".HI"][1]
                            if color != "None":
                                cond.ColorC = alarmPriority_dict[str(bind.Value) + ".HI"][1]
                            else:
                                cond.ColorC = "Yellow"
                            writeAlarm(lista[1], alarms)
                        cond.Expression = str(lista[0].Name) + "==0,0"
                        tag_list.append(lista[0])
                        """alarms_dict[lista[1].Name] = lista[1]"""
                        bind.Value = bind.GenericName = lista[0].Name
            elif cond.Expression == str(bind.Value):
                cond.Expression = "True"
            else:
                if newBind.GenericName == cond.Expression:
                    cond.Expression = "True"
                """forceCondition(cond, newBind)"""

    writeCondition(text_obj, text_element, project_tree)
    writeBinding(text_obj, text_element, project_tree)
    return text_element


def writeAlarm(alarm, alarms):
    element = ET.SubElement(alarms, "Alarm",
                            ID=alarm.ID,
                            Name=alarm.Name,
                            Condition=alarm.Condition,
                            Tag=alarm.Tag,
                            Threshold=alarm.Threshold,
                            Screen=alarm.Screen,
                            Priority=alarm.Priority)
    indent(element)


def write1Text(text_obj, window, project_tree, units, tag_list, alarm_list):
    text_element = writeTextElement(text_obj, window, units, tag_list, alarm_list, project_tree)
    indent(text_element)
    project_tree.write("project.xml", encoding="utf-8", xml_declaration=True)


"""def writeText(text_list, window, project_tree):
    for text_obj in text_list:
        text_element = writeTextElement(text_obj, window)
        indent(text_element)
    project_tree.write("project.xml", encoding="utf-8", xml_declaration=True)"""


def writeText(text, window, project_tree, units, tag_list, alarm_list, alarm_dict, alarmPriority_dict):
    text_element = writeTextElement(text, window, units, tag_list, alarm_list, project_tree, alarm_dict, alarmPriority_dict)
    if text_element:
        indent(text_element)


def writeRect(rect, window, project_tree):
    rectangle = ET.SubElement(window, "DinamicRectangle")
    writeShapeAttributes(rectangle, rect)
    indent(rectangle)
    writeCondition(rect, rectangle, project_tree)
    writeBinding(rect, rectangle, project_tree)


"""def writeAlarm(alarm_list, alarms, project_tree):
    if alarm_list:
        for alarm in alarm_list:
            ET.SubElement(alarms, "Alarm",
                          ID=alarm.ID,
                          Name=alarm.Name,
                          Condition=alarm.Condition,
                          Tag=alarm.Tag,
                          Area=alarm.Tag,
                          Threshold=alarm.Threshold,
                          EngineeringUnits=alarm.EngineeringUnits,
                          AckDisplay=alarm.AckDisplay,
                          Priority=alarm.Priority)
    project_tree.write("project.xml", encoding="utf-8", xml_declaration=True)
"""


def writeWindow(root, window, name, window_dict):
    """if name in window_dict:
        window.set("ID", window_dict[name])
    else:
        id_screen = str(uuid.uuid4())
        window.set("ID", id_screen)"""

    window.set("Header", name)
    size = Size(root.attrib["Width"], root.attrib["Height"])
    """if "Name" in root.attrib:
        window.set("Header", root.attrib["Name"])"""
    """else:
        window.set("Header", "Window")"""
    if "Width" in root.attrib:
        window.set("WindowWidth", root.attrib["Width"])
    if "Height" in root.attrib:
        window.set("WindowHeight", root.attrib["Height"])
    if "Background" in root.attrib:
        window.set("Background", root.attrib["Background"])

    """for key, value in root.attrib.items():
        if key == "Name":
            window.set("Header", value)
        if key == "Width":
            window.set("WindowWidth", value)
        if key == "Height":
            window.set("WindowHeight", value)
        if key == "Background":
            window.set("Background", value)
        if key == "Width":
            window.set("WindowWidth", value)"""
    id_screen = str(uuid.uuid4())
    window_dict[name] = id_screen
    window.set("ID", id_screen)
    window.set("MenuEnabled", "True")
    window.set("TraceWindow", "True")
    window.set("MainWindow", "False")
    window.set("VisibleWindow", "True")
    window.set("AllowResizing", "True")
    indent(window)

    return size


def writeBinding(rect, rect_label, project_tree):
    if type(rect) == Text:
        if rect.Binding:
            bindList = ET.SubElement(rect_label, "BindingList")
            for bind in rect.Binding:
                if bind.Value != "":
                    ET.SubElement(bindList, "Binding",
                                  GenericName=str(bind.GenericName),
                                  Value=str(bind.Value))
            indent(bindList)
    else:
        if rect.IISCondition:
            rect.Binding.clear()
            for cond in rect.IISCondition:
                pattern = r'\b[\w-]+\.(?:PV|MV)[\w]*\b'
                matches = re.findall(pattern, cond.Expression)
                for match in matches:
                    bind = Binding.default()
                    bind.GenericName = match
                    bind.Value = match
                    if not any(bindi.GenericName == bind.GenericName for bindi in rect.Binding):
                        rect.Binding.append(bind)

        if rect.Binding:
            bindList = ET.SubElement(rect_label, "BindingList")
            for bind in rect.Binding:
                if bind.Value != "":
                    ET.SubElement(bindList, "Binding",
                                  GenericName=str(bind.GenericName),
                                  Value=str(bind.Value))
            indent(bindList)
        """project_tree.write("project.xml", encoding="utf-8", xml_declaration=True)"""


def writeCondition(rect, rect_label, project_tree):
    if rect.IISCondition:
        for cond in rect.IISCondition:
            for binding in rect.Binding:
                forceCondition(cond, binding)
        for cond in rect.IISCondition:
            expression_list = filtrar_y_separar(cond.Expression)
            nueva_expresion = cond.Expression
            for e in expression_list:
                """cond.Expression = cond.Expression.replace(e, '"' + str(e) + '"')"""
                nueva_expresion = re.sub(r'\b' + re.escape(e) + r'\b', '"' + str(e) + '"', nueva_expresion)
            cond.Expression = nueva_expresion
        condList = ET.SubElement(rect_label, "ConditionsList")
        for cond in rect.IISCondition:
            if not ((cond.ColorC == "" and cond.ColorB == "" and cond.ReplaceText == "False") or
                    (cond.Expression == "2<1,0" or cond.Expression == "2<1,0 and 2<1,0" or cond.Expression == "2<1,0 "
                                                                                                              "or "
                                                                                                              "2<1,0")):
                condition = ET.SubElement(condList, "IISCondition",
                                          Expression=str(cond.Expression),
                                          ColorChangeType=str(cond.ColorChangeType),
                                          ColorC=str(cond.ColorC),
                                          ColorB=str(cond.ColorB),
                                          PropertyNameCC=str(cond.PropertyNameCC),
                                          PropertyNameBLK=str(cond.PropertyNameBLK),
                                          IsContinuous=str(cond.IsContinuous),
                                          ReplaceText=cond.ReplaceText,
                                          Text=cond.Text, #TODO: CHANGE TEXT NAME IN SCRIPT AND IIS CONTROL DYNAMICTEXT
                                          BlinkingType="False")


            indent(condList)
        """project_tree.write("project.xml", encoding="utf-8", xml_declaration=True)"""
