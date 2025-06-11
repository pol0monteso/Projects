import uuid
import xml.etree.ElementTree as ET

from Classes import LogicClass
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
                               Screen=touch.Screen,  #str(id_),
                               Height=touch.Height,
                               Width=touch.Width,
                               RenderTransform=touch.RenderTransform,
                               RenderTransformOrigin=touch.RenderTransformOrigin,
                               X=str(touch.X),
                               Y=str(touch.Y),
                               ShapeName=touch.ShapeName)


def writeTags(tag_list, tags, project_tree, tagName_list, alarms, units, alarmPriority_dict, id_):
    """
    Escribe las etiquetas en el árbol de tags, optimizado para mejorar la legibilidad y rendimiento.

    Parámetros:
    - tag_list: Lista de objetos con información de los tags.
    - tags: Objeto XML donde se añaden los nuevos tags.
    - project_tree: Parámetro no usado, puede ser útil para futuras mejoras.
    - tagName_list: Lista de nombres de tags ya procesados.
    """
    if id_ == "None" or id_ is None:
        id_=""
    else:
        id_=str(id_)
    # Convertimos tagName_list en un conjunto para acceso O(1)
    tagName_set = set(tagName_list)

    # Criterios de coincidencia de nombres de tag
    primary_conditions = [".PV", ".MV", "SCALE", ".#PV", ".ALRM", ".MODE", ".CMOD", ".OMOD", ".", ".SH", ".SL", ".HH",
                          ".LL", ".SHDN"]
    secondary_conditions = [".ALMPV"]
    alarm_list = []
    if tag_list:
        for t in tag_list:
            # Usar variable local para evitar múltiples llamadas a str(t.Name)
            tag_name = str(t.Name)

            # Reemplazo de texto en la variable HysysVar
            hysys_var = str(t.HysysVar).replace("0@@100@@IIS.Saw", "@@@@")

            # Verificar si el tag ya se ha procesado
            if tag_name in tagName_set:
                continue

            # Verificar si el tag cumple alguna de las condiciones
            if any(cond in tag_name for cond in primary_conditions) or any(
                    cond in tag_name for cond in secondary_conditions):
                prefix = tag_name.split('.')[0]
                if prefix in units:
                    alarm_comment = units[prefix]['Comment']
                elif prefix+'.HH' in alarmPriority_dict:
                    alarm_comment = alarmPriority_dict[prefix+'.HH'][-1]
                else:
                    alarm_comment = ""
                if prefix not in alarm_list and prefix+'.PV'==tag_name:
                    alarm_list.append(prefix)
                    id = ""
                    for tag_ in tag_list:
                        if tag_.Name == prefix + ".PV":
                            id = tag_.ID
                    if prefix+'.HH' in alarmPriority_dict:
                            if alarmPriority_dict[prefix+'.HH'][0] == "High":
                                priority = "100"
                            elif alarmPriority_dict[prefix+'.HH'][0] == "Medium":
                                priority = "0"
                            elif alarmPriority_dict[prefix+'.HH'][0] == "Low":
                                priority = "110"
                            else:
                                priority = "0"
                            tag_id = str(uuid.uuid4())
                            ET.SubElement(
                                tags,
                                "Tag",
                                ID=tag_id,
                                Name=prefix+'.ALMPVHH',
                                IsMaster="True",
                                HysysVar="@@@@"+prefix+'.ALMPVHH',
                                NumDecimals=str(getattr(t, "NumDecimals", "")),
                                HysysVarUnit=str(getattr(t, "HysysVarUnit", "")),
                                DefaultValue=str(getattr(t, "DefaultValue", "")))
                            element = ET.SubElement(alarms, "Alarm",
                                                    ID=str(uuid.uuid4()),
                                                    Name=prefix + '.ALMPVHH',
                                                    Tag=tag_id,
                                                    Description=alarm_comment,
                                                    Screen=str(id_),
                                                    Threshold=str(0.5),
                                                    Priority=priority)
                    elif prefix + '.HI' in alarmPriority_dict:
                        if alarmPriority_dict[prefix + '.HI'][0] == "High":
                            priority = "100"
                        elif alarmPriority_dict[prefix + '.HI'][0] == "Medium":
                            priority = "0"
                        elif alarmPriority_dict[prefix + '.HI'][0] == "Low":
                            priority = "110"
                        else:
                            priority = "0"
                        tag_id = str(uuid.uuid4())
                        ET.SubElement(
                            tags,
                            "Tag",
                            ID=tag_id,
                            Name=prefix + '.ALMPVHI',
                            IsMaster="True",
                            HysysVar="@@@@"+prefix+'.ALMPVHI',
                            NumDecimals=str(getattr(t, "NumDecimals", "")),
                            HysysVarUnit=str(getattr(t, "HysysVarUnit", "")),
                            DefaultValue=str(getattr(t, "DefaultValue", "")))
                        element = ET.SubElement(alarms, "Alarm",
                                                ID=str(uuid.uuid4()),
                                                Name=prefix + '.ALMPVHI',
                                                Tag=tag_id,
                                                Screen=str(id_),
                                                Description=alarm_comment,
                                                Threshold=str(0.5),
                                                Priority=priority)
                    if prefix + '.LO' in alarmPriority_dict:
                        if alarmPriority_dict[prefix + '.LO'][0] == "High":
                            priority = "100"
                        elif alarmPriority_dict[prefix + '.LO'][0] == "Medium":
                            priority = "0"
                        elif alarmPriority_dict[prefix + '.LO'][0] == "Low":
                            priority = "110"
                        else:
                            priority = "0"

                        tag_id = str(uuid.uuid4())
                        ET.SubElement(
                            tags,
                            "Tag",
                            ID=tag_id,
                            Name=prefix + '.ALMPVLO',
                            IsMaster="True",
                            HysysVar="@@@@"+prefix+'.ALMPVLO',
                            NumDecimals=str(getattr(t, "NumDecimals", "")),
                            HysysVarUnit=str(getattr(t, "HysysVarUnit", "")),
                            DefaultValue=str(getattr(t, "DefaultValue", "")))
                        element = ET.SubElement(alarms, "Alarm",
                                                ID=str(uuid.uuid4()),
                                                Name=prefix + '.ALMPVLO',
                                                Tag=tag_id,
                                                Screen=str(id_),
                                                Description=alarm_comment,
                                                Threshold=str(0.5),
                                                Priority=priority)
                    if prefix+'.LL' in alarmPriority_dict:
                        if alarmPriority_dict[prefix+'.LL'][0] == "High":
                            priority = "100"
                        elif alarmPriority_dict[prefix+'.LL'][0] == "Medium":
                            priority = "0"
                        elif alarmPriority_dict[prefix+'.LL'][0] == "Low":
                            priority = "110"
                        else:
                            priority = "0"
                        tag_id = str(uuid.uuid4())
                        ET.SubElement(
                            tags,
                            "Tag",
                            ID=tag_id,
                            Name=prefix + '.ALMPVLL',
                            IsMaster="True",
                            HysysVar="@@@@"+prefix+'.ALMPVLL',
                            NumDecimals=str(getattr(t, "NumDecimals", "")),
                            HysysVarUnit=str(getattr(t, "HysysVarUnit", "")),
                            DefaultValue=str(getattr(t, "DefaultValue", "")))
                        ET.SubElement(alarms, "Alarm",
                                                ID=str(uuid.uuid4()),
                                                Name=prefix + '.ALMPVLL',
                                                Tag=tag_id,
                                                Screen=id_,
                                                Description=alarm_comment,
                                                Threshold=str(0.5),
                                                Priority=priority)
                elif prefix + '.VL' == tag_name:
                    if prefix + '.VEL-' in alarmPriority_dict:
                        if alarmPriority_dict[prefix + '.VEL-'][0] == "High":
                            priority = "100"
                        elif alarmPriority_dict[prefix + '.VEL-'][0] == "Medium":
                            priority = "0"
                        elif alarmPriority_dict[prefix + '.VEL-'][0] == "Low":
                            priority = "110"
                        else:
                            priority = "0"
                        tag_id = str(uuid.uuid4())
                        ET.SubElement(
                            tags,
                            "Tag",
                            ID=tag_id,
                            Name=prefix + '.ALMVELLO',
                            IsMaster="True",
                            HysysVar="@@@@" + prefix + '.ALMVELLO',
                            NumDecimals=str(getattr(t, "NumDecimals", "")),
                            HysysVarUnit=str(getattr(t, "HysysVarUnit", "")),
                            DefaultValue=str(getattr(t, "DefaultValue", "")))
                        ET.SubElement(alarms, "Alarm",
                                      ID=str(uuid.uuid4()),
                                      Name=prefix + '.ALMVELLO',
                                      Tag=tag_id,
                                      Description=alarm_comment,
                                      Screen=str(id_),
                                      Threshold=str(0.5),
                                      Priority=priority)
                    if prefix + '.VEL+' in alarmPriority_dict:
                        if alarmPriority_dict[prefix + '.VEL+'][0] == "High":
                            priority = "100"
                        elif alarmPriority_dict[prefix + '.VEL+'][0] == "Medium":
                            priority = "0"
                        elif alarmPriority_dict[prefix + '.VEL+'][0] == "Low":
                            priority = "110"
                        else:
                            priority = "0"
                        tag_id = str(uuid.uuid4())
                        ET.SubElement(
                            tags,
                            "Tag",
                            ID=tag_id,
                            Name=prefix + '.ALMVELHI',
                            IsMaster="True",
                            HysysVar="@@@@" + prefix + '.ALMVELHI',
                            NumDecimals=str(getattr(t, "NumDecimals", "")),
                            HysysVarUnit=str(getattr(t, "HysysVarUnit", "")),
                            DefaultValue=str(getattr(t, "DefaultValue", "")))
                        ET.SubElement(alarms, "Alarm",
                                      ID=str(uuid.uuid4()),
                                      Name=prefix + '.ALMVELHI',
                                      Tag=tag_id,
                                      Screen=str(id_),
                                      Description=alarm_comment,
                                      Threshold=str(0.5),
                                      Priority=priority)

                num_decimals = 0
                high_value = '0'
                low_value = '0'
                if prefix in units and 'SH' in units[prefix]:
                    num = units[prefix]['SH']
                    high_value = (str(units[prefix]["SH"]))
                    low_value = (str(units[prefix]["SL"]))
                    if num:
                        num_str = str(num)
                        if '.' in num_str:
                            num_decimals = len(num_str.split('.')[1])
                        else:
                            num_decimals = 2

                if num_decimals > 3:
                    num_decimals = 3
                if high_value == "None" or low_value == "None":
                    high_value = '0'
                    low_value = '0'
                ET.SubElement(
                    tags,
                    "Tag",
                    ID=str(getattr(t, "ID", "")),
                    Name=tag_name,
                    IsMaster="True",
                    HysysVar=hysys_var,
                    NumDecimals=str(num_decimals),
                    HysysVarUnit=str(getattr(t, "HysysVarUnit", "")),
                    DefaultValue=str(getattr(t, "DefaultValue", "")),
                    HighLimit=high_value,
                    LowLimit=low_value)
                # Agregar a la lista de nombres de tags
                tagName_set.add(tag_name)

    # Actualizamos la lista original (convertimos el conjunto de vuelta a lista)
    tagName_list[:] = list(tagName_set)


"""def writeTags(tag_list, tags, project_tree, tagName_list):
    if tag_list:
        for t in tag_list:
            t.HysysVar = t.HysysVar.replace("0@@100@@IIS.Saw", "@@@@")
            if t.Name not in tagName_list and (
                    ".PV" in t.Name or ".MV" in t.Name or "SCALE" in t.Name or ".#PV" in t.Name or ".ALRM" in t.Name or
                    ".MODE" in t.Name or ".CMOD" in t.Name or ".OMOD" in t.Name ):
                ET.SubElement(tags, "Tag",
                              ID=str(t.ID),
                              IsMaster="True",
                              Name=str(t.Name),
                              HysysVar=str(t.HysysVar),
                              NumDecimals=str(t.NumDecimals),
                              HysysVarUnit=str(t.HysysVarUnit))
                tagName_list.append(str(t.Name))
            elif t.Name not in tagName_list and (
                    ".ALMPV" in t.Name):
                ET.SubElement(tags, "Tag",
                              ID=str(t.ID),
                              Name=str(t.Name),
                              IsMaster="True",
                              HysysVar=str(t.HysysVar),
                              NumDecimals=str(t.NumDecimals),
                              HysysVarUnit=str(t.HysysVarUnit))
                tagName_list.append(str(t.Name))"""


def initScreen(root, project, windows, project_tree, tags, name, tagName_list, units, tuplas_report, alarms,
               alarms_dict, window_dict, touch_list, alarmsPriority_dict, button_list, tag_list):
    print("Starting...")
    # Define la estructura del árbol XML con los valores proporcionados
    window = ET.SubElement(windows, "Window")
    size, id_ = writeWindow(root, window, name, window_dict)
    print("READ : ")
    tag_list, object_list, tuples = readRect_rec(root, 0, 0, "", "", False, tag_list, [], [], name, tuplas_report)
    object_list = orderByZIndex(object_list)
    for obj in object_list:
        if type(obj) == Touch:
            obj.Window = window
            touch_list.append(obj)
        elif type(obj) == Button:
            obj.Window = window
            button_list.append(obj)

    #print("TAGS llegits")
    #print("OBJECTES llegits")
    print("WRITE OBJECTS: ")
    writeObjects(object_list, window, project_tree, size, tag_list, units, alarms, alarms_dict, window_dict,
                 alarmsPriority_dict)
    print("WRITE TAGS: ")
    writeTags(tag_list, tags, project_tree, tagName_list, alarms, units, alarmsPriority_dict, id_)

    """indent(project)"""

    """project_tree.write("project.xml", encoding="utf-8", xml_declaration=True)"""
    return tuples, window_dict, touch_list, tag_list


def build_faceplate(tag, alarmsPriority_dict, touch):
    prefix_tag = tag
    hh_color = alarmsPriority_dict[prefix_tag + ".HH"][1]
    hi_color = alarmsPriority_dict[prefix_tag + ".HI"][1]
    li_color = alarmsPriority_dict[prefix_tag + ".LI"][1]
    ll_color = alarmsPriority_dict[prefix_tag + ".LL"][1]
    controller = ET.SubElement(touch.Window, "Controller",
                               Width=touch.Width,
                               Height=touch.Height,
                               X=touch.X,
                               Stroke="Transparent",
                               Fill="Transparent",
                               ShapeName="",
                               Header="",
                               Footer="",
                               FacePlateBackground="Transparent")
    CustomFacePlate = ET.SubElement(controller, "customFacePlate")
    window = ET.SubElement(CustomFacePlate, "Window",
                           WindowWidth="143",
                           WindowHeight="707",
                           Background="#FFC0C0C0",
                           MainWindow="False",
                           ID=str(uuid.uuid4()))
    ET.SubElement(window, "Rectangle",
                  Width="0.968531468531468",
                  Height="0.112022630834512",
                  X="0.013986013986014",
                  Y="0.0933521923620933",
                  ShapeName="ln_0",
                  Fill="#FF000000",
                  Stroke="#FF000000",
                  StrokeThickness="1",
                  Group="")
    ET.SubElement(window, "Rectangle",
                  Width="138.5",
                  Height="45.66",
                  X="2",
                  Y="138.5",
                  ShapeName="ln_1",
                  Fill="Black",
                  Stroke="Black",
                  StrokeThickness="1",
                  Group="")
    ET.SubElement(window, "Rectangle",
                  Width="0.974908308474742",
                  Height="0.0854314002828853",
                  X="0.013986013986014",
                  Y="0.912305516265912",
                  ShapeName="ln_2",
                  Fill="#00FFFFFF",
                  Stroke="#FF000000",
                  StrokeThickness="1",
                  Group="")

    ET.SubElement(window, "Rectangle",
                  Width="0.268531468531468",
                  Height="0.428854314002829",
                  X="0.307692307692308",
                  Y="337.2",
                  ShapeName="Background",
                  Fill="Black",
                  Stroke="Black",
                  StrokeThickness="1",
                  Group="")
    """ET.SubElement(window, "DynamicLevel",
                  ShapeName="lv_0",
                  X="0.335664335664336",
                  Y="0.383309759547383",
                  Width="0.142657342657342",
                  Height="0.411315417256012",
                  Group="",
                  Tag="",
                  LevelFill1="#00FFFFFF",
                  LevelFill2="#00FFFFFF",
                  LevelValue1="0",
                  LevelValue2="0",
                  Orientation="Vertical",
                  MinValue="0",
                  MaxValue="0",
                  Fill="#FF000000",
                  Stroke="#FF000000",
                  RenderTransform="Identity",
                  RenderTransformOrigin="0,0")"""
    ET.SubElement(window, "LabelText",
                  Width="0.318881118881122",
                  Height="0.031966053748232",
                  X="0.65034965034965",
                  Y="0.362093352192362",
                  ShapeName="lb_0",
                  Foreground="#FF000000",
                  Background="#00FFFFFF",
                  Tag="",
                  Format="",
                  Content="100",
                  FontAutoSize="True",
                  FontSize="12",
                  FontFamily="Consolas",
                  TextAlign="Right",
                  Alarm="",
                  Alarm2="",
                  Angle="0",
                  CenterX="0.5",
                  CenterY="0.5",
                  Group="")

    ET.SubElement(window, "LabelText",
                  Width="0.318881118881119",
                  Height="0.031966053748232",
                  X="0.65034965034965",
                  Y="0.444130127298444",
                  ShapeName="lb_1",
                  Foreground="#FF000000",
                  Background="#00FFFFFF",
                  Tag="",
                  Format="",
                  Content="80",
                  FontAutoSize="True",
                  FontSize="12",
                  FontFamily="Consolas",
                  TextAlign="Right",
                  Alarm="",
                  Alarm2="",
                  Angle="0",
                  CenterX="0.5",
                  CenterY="0.5",
                  Group="")

    ET.SubElement(window, "LabelText",
                  Width="0.318881118881119",
                  Height="0.031966053748232",
                  X="0.65034965034965",
                  Y="0.526166902404526",
                  ShapeName="lb_2",
                  Foreground="#FF000000",
                  Background="#00FFFFFF",
                  Tag="",
                  Format="",
                  Content="60",
                  FontAutoSize="True",
                  FontSize="12",
                  FontFamily="Consolas",
                  TextAlign="Right",
                  Alarm="",
                  Alarm2="",
                  Angle="0",
                  CenterX="0.5",
                  CenterY="0.5",
                  Group="")

    ET.SubElement(window, "LabelText",
                  Width="0.318881118881119",
                  Height="0.031966053748232",
                  X="0.65034965034965",
                  Y="0.60961810466761",
                  ShapeName="lb_3",
                  Foreground="#FF000000",
                  Background="#00FFFFFF",
                  Tag="",
                  Format="",
                  Content="40",
                  FontAutoSize="True",
                  FontSize="12",
                  FontFamily="Consolas",
                  TextAlign="Right",
                  Alarm="",
                  Alarm2="",
                  Angle="0",
                  CenterX="0.5",
                  CenterY="0.5",
                  Group="")

    ET.SubElement(window, "LabelText",
                  Width="0.318881118881119",
                  Height="0.031966053748232",
                  X="0.65034965034965",
                  Y="0.691654879773692",
                  ShapeName="lb_4",
                  Foreground="#FF000000",
                  Background="#00FFFFFF",
                  Tag="",
                  Format="",
                  Content="20",
                  FontAutoSize="True",
                  FontSize="12",
                  FontFamily="Consolas",
                  TextAlign="Right",
                  Alarm="",
                  Alarm2="",
                  Angle="0",
                  CenterX="0.5",
                  CenterY="0.5",
                  Group="")

    ET.SubElement(window, "LabelText",
                  Width="0.318881118881119",
                  Height="0.031966053748232",
                  X="0.65034965034965",
                  Y="0.769448373408769",
                  ShapeName="lb_5",
                  Foreground="#FF000000",
                  Background="#00FFFFFF",
                  Tag="",
                  Format="",
                  Content="0",
                  FontAutoSize="True",
                  FontSize="12",
                  FontFamily="Consolas",
                  TextAlign="Right",
                  Alarm="",
                  Alarm2="",
                  Angle="0",
                  CenterX="0.5",
                  CenterY="0.5",
                  Group="")
    dinamicRect1 = ET.SubElement(window, "DinamicRectangle",
                                 ShapeName="COLOR",
                                 X="0.216783216783217",
                                 Y="0.0961810466760962",
                                 Width="0.106293706293708",
                                 Height="0.0282885431400283",
                                 Group="",
                                 Fill="#FFFFFFFF",
                                 Stroke="#00FFFFFF",
                                 StrokeThickness="1",
                                 RenderTransform="Identity",
                                 RenderTransformOrigin="0,0",
                                 Rotation="0")
    cond_list = ET.SubElement(dinamicRect1, "ConditionsList")
    ET.SubElement(cond_list, "IISCondition",
                  Expression=str(tag + ".AOFS==1073741824"),
                  ColorChangeType1="NormalColorChange",
                  ColorC1="#FF0000FF",
                  PropertyNameCC1="Fill",
                  PropertyNameBLK1="Fill")
    ET.SubElement(cond_list, "IISCondition",
                  Expression=str(tag + ".ALRM==524288"),
                  ColorChangeType1="NormalColorChange",
                  ColorC1=str(hh_color),
                  PropertyNameCC1="Fill",
                  PropertyNameBLK1="Fill",
                  ColorB1="Red",
                  BlinkingType1="Yes")
    ET.SubElement(cond_list, "IISCondition",
                  Expression=str(tag + ".ALRM==32768"),
                  ColorChangeType1="NormalColorChange",
                  ColorC1=str(hi_color),
                  PropertyNameCC1="Fill",
                  PropertyNameBLK1="Fill",
                  ColorB1=str(hi_color),
                  BlinkingType1="Yes")
    ET.SubElement(cond_list, "IISCondition",
                  Expression=str(tag + ".ALRM==16384"),
                  ColorChangeType1="NormalColorChange",
                  ColorC1=str(li_color),
                  PropertyNameCC1="Fill",
                  PropertyNameBLK1="Fill",
                  ColorB1=str(li_color),
                  BlinkingType1="Yes")
    ET.SubElement(cond_list, "IISCondition",
                  Expression=str(tag + ".ALRM==262144"),
                  ColorChangeType1="NormalColorChange",
                  ColorC1=str(ll_color),
                  PropertyNameCC1="Fill",
                  PropertyNameBLK1="Fill",
                  ColorB1=str(ll_color),
                  BlinkingType1="Yes")
    ET.SubElement(cond_list, "IISCondition",
                  Expression="1==1",
                  ColorChangeType1="NormalColorChange",
                  ColorC1="#00ff00",
                  PropertyNameCC1="Fill",
                  PropertyNameBLK1="Fill",
                  ColorB1=str(ll_color),
                  BlinkingType1="Yes")
    bind_list = ET.SubElement(dinamicRect1, "BindingList")
    ET.SubElement(bind_list, "Binding",
                  GenerigName=str(tag + ".AOFS"),
                  Value=str(tag + ".AOFS"))
    ET.SubElement(bind_list, "Binding",
                  GenerigName=str(tag + ".ALRM"),
                  Value=str(tag + ".ALRM"))
    ET.SubElement(bind_list, "Binding",
                  GenerigName=str(tag + ".AFLS"),
                  Value=str(tag + ".AFLS"))
    # Crear el primer DynamicText (text_1294)
    dynamic_text_1294 = ET.SubElement(window, "DynamicText",
                                      ShapeName="text_1294",
                                      X="0.034965034965035",
                                      Y="0.124469589816124",
                                      Width="NaN",
                                      Height="NaN",
                                      Group="",
                                      Background="#00FFFFFF",
                                      Foreground="Cyan",
                                      Text="MODE",
                                      FontSize="17",
                                      FontFamily="Consolas",
                                      HorizontalAlignment="Stretch",
                                      ScaleX="1",
                                      ScaleY="1",
                                      RenderTransform="Identity",
                                      RenderTransformOrigin="0,0",
                                      FontWeight="Normal")

    # Añadir ConditionsList al DynamicText 1294
    cond_list_1294 = ET.SubElement(dynamic_text_1294, "ConditionsList")
    ET.SubElement(cond_list_1294, "IISCondition",
                  Expression="65TI440.MODE==262144",
                  ReplaceText="True", Text="ROUT")
    ET.SubElement(cond_list_1294, "IISCondition",
                  Expression="65TI440.MODE==524288",
                  ReplaceText="True", Text="RCAS")
    ET.SubElement(cond_list_1294, "IISCondition",
                  Expression="65TI440.MODE==1048576",
                  ReplaceText="True", Text="PRD")
    ET.SubElement(cond_list_1294, "IISCondition",
                  Expression="65TI440.MODE==2097152",
                  ReplaceText="True", Text="CAS")
    ET.SubElement(cond_list_1294, "IISCondition",
                  Expression="65TI440.MODE==4194304",
                  ReplaceText="True", Text="AUT")
    ET.SubElement(cond_list_1294, "IISCondition",
                  Expression="65TI440.MODE==8388608",
                  ReplaceText="True", Text="MAN")
    ET.SubElement(cond_list_1294, "IISCondition",
                  Expression="65TI440.MODE==16777216",
                  ReplaceText="True", Text="SEMI")
    ET.SubElement(cond_list_1294, "IISCondition",
                  Expression="65TI440.MODE==67108864",
                  ReplaceText="True", Text="TRK")
    ET.SubElement(cond_list_1294, "IISCondition",
                  Expression="65TI440.MODE==134217728",
                  ReplaceText="True", Text="IMAN")
    ET.SubElement(cond_list_1294, "IISCondition",
                  Expression="65TI440.MODE==2147483648",
                  ReplaceText="True", Text="OOS")

    # Añadir BindingList al DynamicText 1294
    bind_list_1294 = ET.SubElement(dynamic_text_1294, "BindingList")
    ET.SubElement(bind_list_1294, "Binding",
                  GenericName="65TI440.MODE",
                  Value="65TI440.MODE")


def writeObjects(object_list, window, project_tree, size, tag_list, units, alarms, alarms_dict, windows_dict,
                 alarmPriority_dict):
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
        Level: "level_",
        Button: "button_"
    }
    for idx, obj in enumerate(object_list):
        shape_type = type(obj)
        obj.ShapeName = str(shape_name_map[shape_type]) + str(idx)
        if obj.Width == size.Width:
            obj.Width = float(obj.Width) - 1
        elif obj.Height == size.Height:
            obj.Height = float(obj.Height) - 1
        if shape_type in shape_name_map:
            #obj.ShapeName = f"{shape_name_map[shape_type]}{idx}"
            if shape_type == Rectangle:
                writeRect(obj, window, project_tree, alarmPriority_dict, units)
            elif shape_type == Sector:
                writeSector(obj, window, project_tree, alarmPriority_dict)
            elif shape_type == Arc:
                writeArc(obj, window, project_tree, alarmPriority_dict)
            elif shape_type == Polygon:
                writePolygon(obj, window, project_tree, alarmPriority_dict, units)
            elif shape_type == Ellipse:
                writeEllipse(obj, window, project_tree, alarmPriority_dict)
            elif shape_type == Line:
                writePolyLine(obj, window, project_tree)
            elif shape_type == Text:
                writeText(obj, window, project_tree, units, tag_list, alarms, alarms_dict, alarmPriority_dict)
            elif shape_type == ProcessData:
                writeDataCharacter(obj, window, tag_list, units, project_tree, alarmPriority_dict)
            elif shape_type == Level:
                write_level(obj, window, project_tree, tag_list, units, alarmPriority_dict)
            """elif shape_type == Touch:
                writeTouch(window, obj, windows_dict)"""


def find_color_blinking(tag, alarmPriority):
    if tag in alarmPriority:
        return alarmPriority[tag][-1]
    return None


def writeShape(object, shape_type, window, project_tree, alarmPriority_dict):
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
    writePoints(object, shape_element)
    writeCondition(object, shape_element, project_tree, alarmPriority_dict)
    writeBinding(object, shape_element, project_tree)


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
    writeCondition(object, line_element, project_tree, [])
    writeBinding(object, line_element, project_tree)
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


def writeEllipse(object, window, project_tree, alarmPriority_dict):
    sector_element = ET.SubElement(window, "DynamicEllipse")
    writeShapeAttributes(sector_element, object)
    indent(sector_element)
    writeCondition(object, sector_element, project_tree, alarmPriority_dict)
    writeBinding(object, sector_element, project_tree)


def writePolygon(rect, window, project_tree, alarmPriority_dict, units):
    polygon = writeShape(rect, "Polygon", window, project_tree, alarmPriority_dict)
    if rect.DataLinkInfo != []:
        if "Left" in rect.DataLinkInfo[0]['PropertyName']:
            if '.' in rect.DataLinkInfo[0]['HighLimit']:
                prefix = rect.DataLinkInfo[0]['HighLimit'].split('.')[0]
                tag_ = rect.DataLinkInfo[0]['HighLimit'].split('.')[1]
                highlimitX = units[prefix][tag_]
                prefix = rect.DataLinkInfo[0]['LowLimit'].split('.')[0]
                tag_ = rect.DataLinkInfo[0]['LowLimit'].split('.')[1]
                lowlimitX = units[prefix][tag_]
                polygon.set("HighLimitX", str(highlimitX))
                polygon.set("LowLimitX", str(lowlimitX))
            XFrom = float(rect.DataLinkInfo[0]['TransformFrom'])
            XTo = rect.X + float(rect.DataLinkInfo[0]['TransformTo']) - XFrom
            polygon.set("Offset", str(rect.DataLinkInfo[0]['OffSet']))
            polygon.set("PropertyX", "true")
            polygon.set("TransformToX", str(XTo))
            polygon.set("TransformFromX", str(rect.X))
            polygon.set("TagValueX", str(rect.DataLinkInfo[0]['Value']))
        elif "Top" in rect.DataLinkInfo[0]['PropertyName']:
            if '.' in rect.DataLinkInfo[0]['HighLimit']:
                prefix = rect.DataLinkInfo[0]['HighLimit'].split('.')[0]
                tag_ = rect.DataLinkInfo[0]['HighLimit'].split('.')[1]
                highlimitY = units[prefix][tag_]
                prefix = rect.DataLinkInfo[0]['LowLimit'].split('.')[0]
                tag_ = rect.DataLinkInfo[0]['LowLimit'].split('.')[1]
                lowlimitY = units[prefix][tag_]
                polygon.set("HighLimitY", str(highlimitY))
                polygon.set("LowLimitY", str(lowlimitY))
            YFrom = float(rect.DataLinkInfo[0]['TransformFrom'])
            YTo = rect.Y + float(rect.DataLinkInfo[0]['TransformTo']) - YFrom
            polygon.set("Offset", str(rect.DataLinkInfo[0]['OffSet']))
            polygon.set("PropertyY", "true")
            polygon.set("TransformToY", str(YTo))
            polygon.set("TransformFromY", str(rect.Y))
            polygon.set("TagValueY", str(rect.DataLinkInfo[0]['Value']))



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


def writeSector(object, window, project_tree, alarmPriority_dict):
    sector_element = ET.SubElement(window, "Sector")
    writeShapeAttributes(sector_element, object)
    sector_element.set("StartAngle", str(object.StartAngle))
    sector_element.set("EndAngle", str(object.EndAngle))
    indent(sector_element)
    writeCondition(object, sector_element, project_tree, alarmPriority_dict)
    writeBinding(object, sector_element, project_tree)


def write_level(object, window, project_tree, tag_list, units, alarmPriority_dict):
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
                if tag1.Name == ".MV":
                    write = False
                else:
                    tag_list.append(tag1)
        elif "SCALE" in object.dataChar.Value:
            for tag in tag_list:
                type_scale = object.dataChar.Value.split('.')[-1]
                if str(object.dataChar.Value) == tag.Name:
                    object.LevelTag = tag.ID
                    #print(tag.Name)
                """if str(object.binding_dic[bind]) != str(type_scale):
                    if str(object.binding_dic[bind]) + '.' + str(type_scale) == tag.Name:
                        object.LevelTag = tag.ID
                        print(tag.Name)"""
                if object.LevelTag == "":
                    if bind == object.dataChar.GenericName.split('.')[0]:
                        tag1 = Tag.default()
                        tag1.ID = uuid.uuid4()
                        object.LevelTag = tag1.ID
                        tag1.Name = str(object.binding_dic[bind]) + '.' + str(type_scale)
                        #print(tag1.Name + f"------X:{object.X}-----Y:{object.Y}")
                        tag1.HysysVar = "0@@100@@IIS.Saw" + str(tag1.Name)
                        if tag1.Name == "." + str(type_scale):
                            write = False
                        else:
                            tag_list.append(tag1)

    if "$" in str(object.LevelValue1):
        level1 = object.LevelValue1
        pv_mv = 0
        data_level_list = level1.split('.')
        if len(data_level_list) > 1:
            for bind in object.binding_dic:
                if bind in data_level_list[0]:
                    level1 = level1.replace(bind, object.binding_dic[bind])
            tag_search = level1.split('.')[0]
            if data_level_list[-1] == "SL":
                if tag_search in units:
                    unit_info = units[tag_search]
                    object.LevelValue1 = str(unit_info['SL'])
                    pv_mv = -1
            elif data_level_list[-1] == "ML":
                if tag_search in units:
                    unit_info = units[tag_search]
                    object.LevelValue1 = str(unit_info['ML'])
                    pv_mv = 1
                """            for tag in tag_list:
                if pv_mv == -1:
                    if str(tag_search) + ".PV" == tag.Name:
                        object.LevelTag = tag.ID
                elif pv_mv == 1:
                    if str(tag_search) + ".MV" == tag.Name:
                        object.LevelTag = tag.ID"""
            if object.LevelTag == "":
                tag1 = Tag.default()
                tag1.ID = uuid.uuid4()
                object.LevelTag = tag1.ID
                if pv_mv == -1:
                    tag1.Name = str(tag_search) + ".PV"
                    tag1.HysysVar = "0@@100@@IIS.Saw" + str(tag1.Name)
                    if tag1.Name == ".PV":
                        write = False
                    else:
                        tag_list.append(tag1)
                elif pv_mv == 1:
                    tag1.Name = str(tag_search) + ".MV"
                    tag1.HysysVar = "0@@100@@IIS.Saw" + str(tag1.Name)
                    if tag1.Name == ".MV":
                        write = False
                    else:
                        tag_list.append(tag1)
        else:
            object.LevelValue1 = object.binding_dic[object.LevelValue1]
    if "$" in str(object.LevelValue2):
        level2 = object.LevelValue2
        data_level_list = level2.split('.')
        if len(data_level_list) > 1:
            for bind in object.binding_dic:
                if bind in data_level_list[0]:
                    level2 = level2.replace(bind, object.binding_dic[bind])
            tag_search = level2.split('.')[0]
            if data_level_list[-1] == "SH":
                if tag_search in units:
                    unit_info = units[tag_search]
                    object.LevelValue2 = str(unit_info['SH'])
            elif data_level_list[-1] == "MH":
                if tag_search in units:
                    unit_info = units[tag_search]
                    object.LevelValue2 = str(unit_info['MH'])
        else:
            object.LevelValue2 = object.binding_dic[object.LevelValue2]
    #print(object.LevelTag)
    level_element = ET.SubElement(window, "DynamicLevel",
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
                                  MaxValue=str(object.LevelValue2),
                                  RenderTransform=object.RenderTransform,
                                  RenderTransformOrigin=object.RenderTransformOrigin,
                                  ShapeName=object.ShapeName
                                  )
    writeCondition(object, level_element, project_tree, alarmPriority_dict)
    writeBinding(object, level_element, project_tree)


def writeDataCharacter(object, window, tag_list, units, project_tree, alarmPriority_dict):
    write = True
    if "-" in str(object.Y):
        object.Y = "0"
    if "-" in str(object.X):
        object.X = "0"
    for bind in object.binding_dic:
        if bind in object.dataChar.Value:
            if ".PV" in object.dataChar.Value and "UNIT" not in object.dataChar.Value:
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
                    if tag1.Name == ".MV":
                        write = False
                    else:
                        tag_list.append(tag1)
            elif "COMMENT" in object.dataChar.Value:
                if object.binding_dic[bind] in units:
                    unit_info = units[object.binding_dic[bind]]
                    object.Text = str(unit_info['Comment'])
                else:
                    object.Text = str("GGG")
            elif "UNIT" in object.dataChar.Value:
                if object.binding_dic[bind] in units:
                    unit_info = units[object.binding_dic[bind]]
                    object.Text = str(unit_info['Unit'])
                else:
                    object.Text = str("UUU")
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
        data_element = ET.SubElement(window, "ProcessData",
                                     FontAutoSize="True",
                                     ShapeName=object.ShapeName,
                                     Background=object.Background,
                                     Foreground=object.Foreground,
                                     FontSize=object.FontSize,
                                     FontFamily=object.FontFamily,
                                     TextAlign=object.TextAlign,
                                     RenderTransform=object.RenderTransform,
                                     RenderTransformOrigin=object.RenderTransformOrigin,
                                     Content=object.Text)
        data_element.set("Width", str(float(object.Width)))
        data_element.set("Height", str(object.Height))
        data_element.set("X", str(object.X))
        data_element.set("Y", str(object.Y))
        data_element.set("Tag", str(object.Tag))
        data_element.set("ShapeName", object.ShapeName)
        writeCondition(object, data_element, project_tree, alarmPriority_dict)
        writeBinding(object, data_element, project_tree)


def writeArc(object, window, project_tree, alarmPriority_dict):
    arc_element = ET.SubElement(window, "Arc")
    writeShapeAttributes(arc_element, object)
    arc_element.set("StartAngle", str(object.StartAngle))
    arc_element.set("EndAngle", str(object.EndAngle))
    indent(arc_element)
    writeCondition(object, arc_element, project_tree, alarmPriority_dict)
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
            #if (str(bind.Value) + '.ALRM<>"LL"') == cond.Expression:
            if (str(bind.Value) + '<>"LL"') == cond.Expression:
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
            elif (str(bind.Value) + '<>"LO"') == cond.Expression:
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
            elif (str(bind.Value) + '<>"HH"') == cond.Expression:
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
                        """alarms_dict[lista[1].Name] = lista[1]"""
                        bind.Value = bind.GenericName = lista[0].Name
            elif (str(bind.Value) + '<>"HI"') == cond.Expression:
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

    writeCondition(text_obj, text_element, project_tree, alarmPriority_dict)
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


"""def writeText(text_list, window, project_tree):
    for text_obj in text_list:
        text_element = writeTextElement(text_obj, window)
        indent(text_element)
    project_tree.write("project.xml", encoding="utf-8", xml_declaration=True)"""


def writeText(text, window, project_tree, units, tag_list, alarm_list, alarm_dict, alarmPriority_dict):
    text_element = writeTextElement(text, window, units, tag_list, alarm_list, project_tree, alarm_dict,
                                    alarmPriority_dict)
    if text_element:
        indent(text_element)


def writeRect(rect, window, project_tree, alarmPriority_dict, units):
    rectangle = ET.SubElement(window, "DinamicRectangle")
    if rect.DataLinkInfo != []:
        if "Left" in rect.DataLinkInfo[0]['PropertyName']:
            if '.' in rect.DataLinkInfo[0]['HighLimit']:
                prefix = rect.DataLinkInfo[0]['HighLimit'].split('.')[0]
                tag_ = rect.DataLinkInfo[0]['HighLimit'].split('.')[1]
                highlimitX = units[prefix][tag_]
                prefix = rect.DataLinkInfo[0]['LowLimit'].split('.')[0]
                tag_ = rect.DataLinkInfo[0]['LowLimit'].split('.')[1]
                lowlimitX = units[prefix][tag_]
                rectangle.set("HighLimitX", str(highlimitX))
                rectangle.set("LowLimitX", str(lowlimitX))
            XFrom = float(rect.DataLinkInfo[0]['TransformFrom'])
            XTo = rect.X + float(rect.DataLinkInfo[0]['TransformTo']) - XFrom
            rectangle.set("Offset", str(rect.DataLinkInfo[0]['OffSet']))
            rectangle.set("PropertyX", "true")
            rectangle.set("TransformToX", str(XTo))
            rectangle.set("TransformFromX", str(rect.X))
            rectangle.set("TagValueX", str(rect.DataLinkInfo[0]['Value']))
        elif "Top" in rect.DataLinkInfo[0]['PropertyName']:
            if '.' in rect.DataLinkInfo[0]['HighLimit']:
                prefix = rect.DataLinkInfo[0]['HighLimit'].split('.')[0]
                tag_ = rect.DataLinkInfo[0]['HighLimit'].split('.')[1]
                highlimitY = units[prefix][tag_]
                prefix = rect.DataLinkInfo[0]['LowLimit'].split('.')[0]
                tag_ = rect.DataLinkInfo[0]['LowLimit'].split('.')[1]
                lowlimitY = units[prefix][tag_]
                rectangle.set("HighLimitY", str(highlimitY))
                rectangle.set("LowLimitY", str(lowlimitY))
            YFrom = float(rect.DataLinkInfo[0]['TransformFrom'])
            YTo = rect.Y + float(rect.DataLinkInfo[0]['TransformTo']) - YFrom
            rectangle.set("Offset", str(rect.DataLinkInfo[0]['OffSet']))
            rectangle.set("PropertyY", "true")
            rectangle.set("TransformToY", str(YTo))
            rectangle.set("TransformFromY", str(rect.Y))
            rectangle.set("TagValueY", str(rect.DataLinkInfo[0]['Value']))
    writeShapeAttributes(rectangle, rect)
    indent(rectangle)
    writeCondition(rect, rectangle, project_tree, alarmPriority_dict)
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

    return size, id_screen


def writeBinding(rect, rect_label, project_tree):
    """if type(rect) == Text:
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
                #pattern = r'\b[\w-]+\.(?:PV|MV)[\w]*\b'
                pattern = r'\b[\w$-]*STATIONNAME[\w$-]*\.(?:PV|MV)[\w]*\b'
                matches = re.findall(pattern, cond.Expression)
                for match in matches:
                    bind = Binding.default()
                    bind.GenericName = match
                    bind.Value = match
                    if not any(bindi.GenericName == bind.GenericName for bindi in rect.Binding):
                        rect.Binding.append(bind)"""

    if rect.Binding:
        bindList = ET.SubElement(rect_label, "BindingList")
        for bind in rect.Binding:
            if bind.Value != "":
                ET.SubElement(bindList, "Binding",
                              GenericName=str(bind.GenericName),
                              Value=str(bind.Value))
        indent(bindList)
        """project_tree.write("project.xml", encoding="utf-8", xml_declaration=True)"""


def writeCondition(rect, rect_label, project_tree, alarmPriority_dict):
    if rect.IISCondition:
        for cond in rect.IISCondition:
            expression = change_condition(cond.Expression)
            cond.Expression = expression
            for binding in rect.Binding:
                expression = force_condition(cond.Expression, binding.Value)
                cond.Expression = expression
                #forceCondition(cond, binding)
            """for cond in rect.IISCondition:"""
            """expression_list = filtrar_y_separar(cond.Expression)
            nueva_expresion = cond.Expression"""
            """for e in expression_list:
                nueva_expresion = re.sub(r'\b' + re.escape(e) + r'\b', '"' + str(e) + '"', nueva_expresion)
            cond.Expression = nueva_expresion"""
        condList = ET.SubElement(rect_label, "ConditionsList")
        attrb = False
        if hasattr(rect, "Fill") and hasattr(rect, "Stroke"):
            attrb = True
        for cond in rect.IISCondition:
            if attrb:
                if rect.Fill == "#00FF0000" and cond.PropertyNameBLK1 == "Fill":
                    cond.PropertyNameBLK1 = "Stroke"
                elif rect.Stroke == "#00FF0000" and cond.PropertyNameBLK1 == "Stroke":
                    cond.PropertyNameBLK1 = "Fill"
                if rect.Fill == "#00FF0000" and cond.PropertyNameCC1 == "Fill":
                    cond.PropertyNameCC1 = "Stroke"
                elif rect.Fill == "#00FF0000" and cond.PropertyNameCC2 == "Fill":
                    cond.PropertyNameCC2 = "Stroke"
                elif rect.Stroke == "#00FF0000" and cond.PropertyNameCC1 == "Stroke":
                    cond.PropertyNameCC1 = "Fill"
                elif rect.Stroke == "#00FF0000" and cond.PropertyNameCC2 == "Stroke":
                    cond.PropertyNameCC2 = "Fill"
            if not ((cond.ColorC1 == "" and cond.ColorB1 == "" and cond.ReplaceText == "False") or
                    (cond.Expression == "2<1,0" or cond.Expression == "2<1,0 and 2<1,0" or cond.Expression == "2<1,0 "
                                                                                                              "or "
                                                                                                              "2<1,0")):
                # TODO: DEBUG
                if cond.ColorB1 == "FindColor":
                    for bind in rect.Binding:
                        if bind.GenericName in cond.Expression and ".ALRM" in bind.GenericName:
                            #color = find_color_blinking(bind.GenericName, alarmPriority_dict)
                            cond.ColorB1 = cond.ColorC1
                            """if color:
                                cond.ColorB1 = color
                            else:
                                cond.BlinkingType1 = "False"""
                condition = ET.SubElement(condList, "IISCondition",
                                          Expression=str(cond.Expression),
                                          ColorChangeType1=str(cond.ColorChangeType1),
                                          ColorC1=str(cond.ColorC1),
                                          ColorB1=str(cond.ColorB1),
                                          PropertyNameCC1=str(cond.PropertyNameCC1),
                                          PropertyNameBLK1=str(cond.PropertyNameBLK1),
                                          IsContinuous=str(cond.IsContinuous),
                                          ReplaceText=cond.ReplaceText,
                                          Text=cond.Text,
                                          BlinkingType1=cond.BlinkingType1,
                                          ColorChangeType2=str(cond.ColorChangeType2),
                                          ColorC2=str(cond.ColorC2),
                                          ColorB2=str(cond.ColorB2),
                                          PropertyNameCC2=str(cond.PropertyNameCC2),
                                          PropertyNameBLK2=str(cond.PropertyNameBLK2),
                                          BlinkingType2="False"
                                          )
            else:
                condition = ET.SubElement(condList, "IISCondition",
                                          Expression=str(cond.Expression),
                                          ColorChangeType1=str(cond.ColorChangeType1),
                                          ColorC1=str(cond.ColorC1),
                                          ColorB1=str(cond.ColorB1),
                                          PropertyNameCC1=str(cond.PropertyNameCC1),
                                          PropertyNameBLK1=str(cond.PropertyNameBLK1),
                                          IsContinuous="True",
                                          ReplaceText=cond.ReplaceText,
                                          Text=cond.Text,
                                          BlinkingType1=cond.BlinkingType1,
                                          ColorChangeType2=str(cond.ColorChangeType2),
                                          ColorC2=str(cond.ColorC2),
                                          ColorB2=str(cond.ColorB2),
                                          PropertyNameCC2=str(cond.PropertyNameCC2),
                                          PropertyNameBLK2=str(cond.PropertyNameBLK2),
                                          BlinkingType2="False",
                                          )
            indent(condList)
        """project_tree.write("project.xml", encoding="utf-8", xml_declaration=True)"""


def faceplate_pvi(tag_list, prefix_tag, alarmsPriority_dict, units, touch, tags, tagName_list):
    from Body.Faceplate import find_faceplate_tags
    """id = ""
    for tag1 in tag_list:
        if tag1.Name == str(prefix_tag + ".PV"):
            id = tag1.ID
    tag_ALRM = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.ALRM", HysysVar=f"@@@@{prefix_tag}.ALRM", NumDecimals=3,
                   UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
    tag_MODE = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.MODE", HysysVar=f"@@@@{prefix_tag}.MODE", NumDecimals=3,
                   UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
    tag_AFLS = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.AFLS", HysysVar=f"@@@@{prefix_tag}.AFLS", NumDecimals=3,
                   UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
    tag_AOFS = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.AOFS", HysysVar=f"@@@@{prefix_tag}.AOFS", NumDecimals=3,
                   UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
    tag__PV = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.#PV", HysysVar=f"@@@@{prefix_tag}.#PV", NumDecimals=3,
                  UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)

    new_tag = [tag_MODE, tag_ALRM, tag_AFLS, tag_AOFS, tag__PV]

    hh_color = str(alarmsPriority_dict.get(prefix_tag + ".HH", [None, None])[1])
    hi_color = str(alarmsPriority_dict.get(prefix_tag + ".HI", [None, None])[1])
    li_color = str(alarmsPriority_dict.get(prefix_tag + ".LO", [None, None])[1])
    ll_color = str(alarmsPriority_dict.get(prefix_tag + ".LL", [None, None])[1])
    high_value = float(units[prefix_tag]["SH"])
    low_value = float(units[prefix_tag]["SL"])
    ph_value = float(units[prefix_tag]["PH"])
    pl_value = float(units[prefix_tag]["PL"])
    puntos = [low_value + i * (high_value - low_value) / (6 - 1) for i in range(6)]
    if hh_color is None:
        hh_color = hi_color
    tag_HH = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.HH", HysysVar=f"@@@@{prefix_tag}.HH", NumDecimals=3,
                 UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["HH"])
    tag_PH = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.PH", HysysVar=f"@@@@{prefix_tag}.PH", NumDecimals=3,
                 UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["PH"])
    tag_PL = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.PL", HysysVar=f"@@@@{prefix_tag}.PL", NumDecimals=3,
                 UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["PL"])
    tag_LL = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.LL", HysysVar=f"@@@@{prefix_tag}.LL", NumDecimals=3,
                 UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["LL"])
    new_tag.append(tag_HH)
    new_tag.append(tag_PH)
    new_tag.append(tag_PL)
    new_tag.append(tag_LL)
    writeTags(new_tag, tags, "", tagName_list)"""
    new_tag = find_faceplate_tags(tag_list, prefix_tag, units)

    # Obtener los colores de alarmas
    hh_color = str(alarmsPriority_dict.get(f"{prefix_tag}.HH", [None, None])[1])
    hi_color = str(alarmsPriority_dict.get(f"{prefix_tag}.HI", [None, None])[1])
    li_color = str(alarmsPriority_dict.get(f"{prefix_tag}.LO", [None, None])[1])
    ll_color = str(alarmsPriority_dict.get(f"{prefix_tag}.LL", [None, None])[1])

    # Obtener los valores de los límites
    high_value = float(units[prefix_tag]["SH"])
    low_value = float(units[prefix_tag]["SL"])

    # Calcular los puntos intermedios
    puntos = [round(low_value + i * (high_value - low_value) / (6 - 1), 2) for i in range(6)]

    # Si hh_color no está definido, usar hi_color
    if hh_color is None:
        hh_color = hi_color
    tag_MODE, tag_ALRM, tag_AFLS, tag_AOFS, tag__PV, tag_SV, tag_HH, tag_PH, tag_PL, tag_LL, tag_PV, tag_MV = new_tag
    # Escribir los tags en la base de datos
    writeTags(new_tag, tags, "", tagName_list)
    #TODO: SCALE trobar max i minim i dividir per 5
    # Si LL no existe, usa LO
    if ll_color is None:
        ll_color = li_color
    unit = units[prefix_tag]["Unit"]
    comment = units[prefix_tag]["Comment"]
    com_ = comment.strip(" ")

    # Encuentra la posición del segundo espacio
    space_count = 0
    for i, char in enumerate(com_):
        if char == " ":
            space_count += 1
        if space_count == 2:
            # Inserta un salto de línea real
            comment = com_[:i + 1] + "\n" + com_[i + 1:]
            break
    controller = ET.SubElement(touch.Window, "Controller",
                               Width=str(touch.Width),
                               Height=str(touch.Height),
                               X=str(touch.X),
                               Y=str(touch.Y),
                               Stroke="Transparent",
                               Fill="Transparent",
                               ShapeName="",
                               Header="",
                               Footer="",
                               FacePlateBackground="Transparent")
    ET.SubElement(controller, "Faceplate")
    CustomFacePlate = ET.SubElement(controller, "CustomFacePlate")
    window = ET.SubElement(CustomFacePlate, "Window",
                           WindowWidth="143",
                           WindowHeight="807",
                           Background="#FFC0C0C0",
                           MainWindow="False",
                           ID=str(uuid.uuid4()))
    ET.SubElement(window, "Rectangle",
                  Width="138.5",
                  Height="90.4",
                  X="2",
                  Y="75.3352",
                  ShapeName="ln_0",
                  Fill="#FF000000",
                  Stroke="#FF000000",
                  StrokeThickness="1",
                  Group="")
    ET.SubElement(window, "Rectangle",
                  Width="138.3",
                  Height="45.657",
                  X="2",
                  Y="168.3",
                  ShapeName="ln_44",
                  Fill="Black",
                  Stroke="#FF000000",
                  StrokeThickness="1",
                  Group="")
    ET.SubElement(window, "Rectangle",
                  Width="0.974908308474742",
                  Height="0.0854314002828853",
                  X="0.013986013986014",
                  Y="0.912305516265912",
                  ShapeName="ln_2",
                  Fill="#00FFFFFF",
                  Stroke="#FF000000",
                  StrokeThickness="1",
                  Group="")

    ET.SubElement(window, "Rectangle",
                  Width="0.268531468531468",
                  Height="0.428854314002829",
                  X="50",
                  Y="354.48",
                  ShapeName="Background",
                  Fill="#FF808080",
                  Stroke="#FF000000",
                  StrokeThickness="1",
                  Group="")
    """ET.SubElement(window, "Rectangle",
                  Width="138.5",
                  Height="45.66",
                  X="2",
                  Y="216.30",
                  ShapeName="rec_0",
                  Fill="Black",
                  Stroke="Black",
                  StrokeThickness="1",
                  Group="")"""
    """ET.SubElement(window, "Rectangle",
                  Width="138.5",
                  Height="45.66",
                  X="2",
                  Y="265",
                  ShapeName="rec_1",
                  Fill="Black",
                  Stroke="Black",
                  StrokeThickness="1",
                  Group="")"""
    dyn_lev = ET.SubElement(window, "DynamicLevel",
                            ShapeName="lv_0",
                            X="53",
                            Y="363",
                            Width="21.2",
                            Height="322.331",
                            Stroke="Transparent",
                            Fill="Black",
                            LevelTag=str(tag_PV.ID),
                            LevelFill1="#00ff00",
                            MinValue=str(low_value),
                            MaxValue=str(high_value),
                            LevelValue1=str(low_value),
                            LevelValue2=str(high_value))
    cond_list_ = ET.SubElement(dyn_lev, "ConditionsList")
    ET.SubElement(cond_list_, "IISCondition",
                  Expression=str(prefix_tag + ".#PV==16777216"),
                  ColorChangeType1="NormalColorChange",
                  ColorC1="Cyan",
                  PropertyNameCC1="Foreground")
    ET.SubElement(cond_list_, "IISCondition",
                  Expression=str(prefix_tag + ".ALRM==524288"),
                  ColorChangeType1="NormalColorChange",
                  ColorC1=str(hh_color),
                  PropertyNameCC1="Foreground",
                  ColorB1=str(hh_color),
                  PropertyNameBLK1="Foreground",
                  BlinkingType1="Yes")
    ET.SubElement(cond_list_, "IISCondition",
                  Expression=str(prefix_tag + ".ALRM==32768"),
                  ColorChangeType1="NormalColorChange",
                  ColorC1=str(hi_color),
                  PropertyNameCC1="Foreground",
                  ColorB1=str(hi_color),
                  PropertyNameBLK1="Foreground",
                  BlinkingType1="Yes")
    ET.SubElement(cond_list_, "IISCondition",
                  Expression=str(prefix_tag + ".ALRM==16384"),
                  ColorChangeType1="NormalColorChange",
                  ColorC1=str(li_color),
                  PropertyNameCC1="Foreground",
                  ColorB1=str(li_color),
                  PropertyNameBLK1="Foreground",
                  BlinkingType1="Yes")
    ET.SubElement(cond_list_, "IISCondition",
                  Expression=str(prefix_tag + ".ALRM==262144"),
                  ColorChangeType1="NormalColorChange",
                  ColorC1=str(ll_color),
                  PropertyNameCC1="Foreground",
                  ColorB1=str(ll_color),
                  PropertyNameBLK1="Foreground",
                  BlinkingType1="Yes")
    ET.SubElement(cond_list_, "IISCondition",
                  Expression="1==1",
                  ColorChangeType1="NormalColorChange",
                  ColorC1="#00ff00",
                  PropertyNameCC1="Foreground",
                  ColorB1=str(ll_color),
                  PropertyNameBLK1="Foreground",
                  BlinkingType1="False")
    bind1 = ET.SubElement(dyn_lev, "BindingList")
    ET.SubElement(bind1, "Binding",
                  GenericName=str(prefix_tag + ".ALRM"),
                  Value=str(prefix_tag + ".ALRM"))
    ET.SubElement(bind1, "Binding",
                  GenericName=str(prefix_tag + ".#PV"),
                  Value=str(prefix_tag + ".#PV"))
    labels = [
        ("lb_0", str(puntos[-1]), "355"),
        ("lb_1", str(puntos[-2]), "419"),
        ("lb_2", str(puntos[3]), "484"),
        ("lb_3", str(puntos[2]), "548.4"),
        ("lb_4", str(puntos[1]), "612.864"),
        ("lb_5", str(puntos[0]), "675"),
    ]
    #print(prefix_tag)
    for shape_name, content, y_pos in labels:
        ET.SubElement(window, "LabelText",
                      Width="29.6",
                      Height="21",
                      X="105",
                      Y=str(y_pos),
                      ShapeName=shape_name,
                      Foreground="#FF000000",
                      Background="#00FFFFFF",
                      Tag="",
                      Format="",
                      Content=content,
                      FontAutoSize="True",
                      FontSize="12",
                      FontFamily="Courier New",
                      TextAlign="Right",
                      Alarm="",
                      Alarm2="",
                      Angle="0",
                      CenterX="0.5",
                      CenterY="0.5",
                      Group="")

    din_rect1 = ET.SubElement(window, "DinamicRectangle",
                              ShapeName="COLOR",
                              X="0.216783216783217",
                              Y="0.0961810466760962",
                              Width="0.106293706293708",
                              Height="0.0282885431400283",
                              Fill="#FFFFFFFF",
                              Stroke="#00FFFFFF",
                              StrokeThickness="1")
    cond_list1 = ET.SubElement(din_rect1, "ConditionsList")
    ET.SubElement(cond_list1, "IISCondition",
                  Expression=str(prefix_tag + ".AOFS==1073741824"),
                  ColorChangeType1="NormalColorChange",
                  ColorC1="#FF0000FF",
                  PropertyNameCC1="Fill")
    ET.SubElement(cond_list1, "IISCondition",
                  Expression=str(prefix_tag + ".ALRM==524288"),
                  ColorChangeType1="NormalColorChange",
                  ColorC1=str(hh_color),
                  PropertyNameCC1="Fill",
                  ColorB1=str(hh_color),
                  PropertyNameBLK1="Fill",
                  BlinkingType1="Yes")
    ET.SubElement(cond_list1, "IISCondition",
                  Expression=str(prefix_tag + ".ALRM==32768"),
                  ColorChangeType1="NormalColorChange",
                  ColorC1=str(hi_color),
                  PropertyNameCC1="Fill",
                  ColorB1=str(hi_color),
                  PropertyNameBLK1="Fill",
                  BlinkingType1="Yes")
    ET.SubElement(cond_list1, "IISCondition",
                  Expression=str(prefix_tag + ".ALRM==16384"),
                  ColorChangeType1="NormalColorChange",
                  ColorC1=str(li_color),
                  PropertyNameCC1="Fill",
                  ColorB1=str(li_color),
                  PropertyNameBLK1="Fill",
                  BlinkingType1="Yes")
    ET.SubElement(cond_list1, "IISCondition",
                  Expression=str(prefix_tag + ".ALRM==262144"),
                  ColorChangeType1="NormalColorChange",
                  ColorC1=str(ll_color),
                  PropertyNameCC1="Fill",
                  ColorB1=str(ll_color),
                  PropertyNameBLK1="Fill",
                  BlinkingType1="Yes")
    ET.SubElement(cond_list1, "IISCondition",
                  Expression="1==1",
                  ColorChangeType1="NormalColorChange",
                  ColorC1="#00ff00",
                  PropertyNameCC1="Fill",
                  ColorB1=str(ll_color),
                  PropertyNameBLK1="Fill",
                  BlinkingType1="False")
    bind_list1 = ET.SubElement(din_rect1, "BindingList")
    ET.SubElement(bind_list1, "Binding",
                  GenericName=str(prefix_tag + ".AOFS"),
                  Value=str(prefix_tag + ".AOFS"))
    ET.SubElement(bind_list1, "Binding",
                  GenericName=str(prefix_tag + ".ALRM"),
                  Value=str(prefix_tag + ".ALRM"))
    ET.SubElement(bind_list1, "Binding",
                  GenericName=str(prefix_tag + ".AFLS"),
                  Value=str(prefix_tag + ".AFLS"))
    dyn_text1 = ET.SubElement(window, "DynamicText",
                              ShapeName="text_1294",
                              X="5",
                              Y="110",
                              Background="#00FFFFFF",
                              Foreground="Cyan",
                              Text="AUT",
                              FontSize="17",
                              FontFamily="Courier New",
                              HorizontalAlignment="Stretch",
                              ScaleX="1",
                              ScaleY="1",
                              FontWeight="Normal")
    cond_list2 = ET.SubElement(dyn_text1, "ConditionsList")
    modes = {
        262144: "ROUT",
        524288: "RCAS",
        1048576: "PRD",
        2097152: "CAS",
        4194304: "AUT",
        8388608: "MAN",
        16777216: "SEMI",
        67108864: "TRK",
        134217728: "IMAN",
        2147483648: "OOS"
    }
    for value, text in modes.items():
        ET.SubElement(cond_list2, "IISCondition",
                      Expression=f"{prefix_tag}.MODE=={value}",
                      ColorChangeType1="",
                      ColorC1="",
                      ColorB1="",
                      PropertyNameCC1="",
                      PropertyNameBLK1="",
                      BlinkingType1="",
                      ColorChangeType2="",
                      ColorC2="",
                      ColorB2="",
                      PropertyNameCC2="",
                      PropertyNameBLK2="",
                      BlinkingType2="",
                      IsContinuous="False",
                      ReplaceText="True",
                      Text=text)
    bind_list2 = ET.SubElement(dyn_text1, "BindingList")
    ET.SubElement(bind_list2, "Binding",
                  GenericName=str(prefix_tag + ".MODE"),
                  Value=str(prefix_tag + ".MODE"))
    dyn_text2 = ET.SubElement(window, "DynamicText",
                              ShapeName="text_1295",
                              X="5",
                              Y="141",
                              Background="#00FFFFFF",
                              Foreground="Cyan",
                              Text="ALARM",
                              FontSize="17",
                              FontFamily="Courier New",
                              HorizontalAlignment="Stretch",
                              ScaleX="1",
                              ScaleY="1")

    alarms = {
        524288: "HH",
        32768: "HI",
        16384: "LO",
        262144: "LL",
        "1==1": "NR"
    }

    # Crear el elemento ConditionsList dentro de dyn_text1
    cond_list3 = ET.SubElement(dyn_text2, "ConditionsList")

    # Agregar las condiciones
    for value, text in alarms.items():
        ET.SubElement(cond_list3, "IISCondition",
                      Expression=f"{prefix_tag}.ALRM=={value}" if isinstance(value, int) else value,
                      ColorChangeType1="",
                      ColorC1="",
                      ColorB1="",
                      PropertyNameCC1="",
                      PropertyNameBLK1="",
                      BlinkingType1="",
                      ColorChangeType2="",
                      ColorC2="",
                      ColorB2="",
                      PropertyNameCC2="",
                      PropertyNameBLK2="",
                      BlinkingType2="",
                      IsContinuous="False",
                      ReplaceText="True",
                      Text=text)
    bind_list3 = ET.SubElement(dyn_text2, "BindingList")
    ET.SubElement(bind_list3, "Binding",
                  GenericName=str(prefix_tag + ".ALRM"),
                  Value=str(prefix_tag + ".ALRM"))
    ET.SubElement(window, "LabelText",
                  Width="0.537062937062938",
                  Height="0.0263083451202263",
                  X="0.034965034965035",
                  Y="0.209335219236209",
                  ShapeName="lb_8",
                  Foreground="#FFFFFFFF",
                  Background="#00FFFFFF",
                  Tag="",
                  Content="PV",
                  FontAutoSize="True",
                  FontSize="12",
                  FontFamily="Courier New",
                  TextAlign="Left",
                  CenterX="0.5",
                  CenterY="0.5")
    ET.SubElement(window, "LabelText",
                  Width="39.2",
                  Height="23.06",
                  X="104",
                  Y="168",
                  ShapeName="lb_9",
                  Foreground="#FFFFFFFF",
                  Background="#00FFFFFF",
                  Tag="",
                  Content=unit,
                  FontAutoSize="True",
                  FontSize="12",
                  FontFamily="Courier New",
                  TextAlign="Left",
                  CenterX="0.5",
                  CenterY="0.5")
    ET.SubElement(window, "LabelText",
                  Width="100.2",
                  Height="50",
                  X="36",
                  Y="192",
                  ShapeName="lb_10",
                  Foreground="Cyan",
                  Background="#00FFFFFF",
                  Tag=str(tag_PV.ID),
                  Content="VALUE",
                  FontAutoSize="False",
                  FontSize="16",
                  FontFamily="Courier New",
                  TextAlign="Right",
                  CenterX="0.5",
                  CenterY="0.5")
    ET.SubElement(window, "LabelText",
                  Width="0.699300699300699",
                  Height="0.0353606789250354",
                  X="0.153846153846154",
                  Y="0",
                  ShapeName="lb_10",
                  Foreground="Black",
                  Background="#00FFFFFF",
                  Tag="",
                  Content=prefix_tag,
                  FontAutoSize="True",
                  FontSize="14",
                  FontFamily="Courier New",
                  TextAlign="Left",
                  CenterX="0.5",
                  CenterY="0.5")
    ET.SubElement(window, "DynamicText",
                  ShapeName="text_1298",
                  X="0.034965034965035",
                  Y="0.0381895332390382",
                  Background="#00FFFFFF",
                  Foreground="#FF000000",
                  Text=comment,
                  FontSize="14",
                  FontFamily="Courier New",
                  HorizontalAlignment="Stretch",
                  ScaleX="1",
                  ScaleY="1"
                  )
    polygon = ET.SubElement(window, "Polygon",
                            ShapeName="polygon_0",
                            X="0.398601398601399",
                            Y="0.936350777934936",
                            Width="0.240559440559439",
                            Height="0.0407355021216408",
                            Group="",
                            Fill="#FF483D8B",
                            Stroke="#FF000000",
                            StrokeThickness="1",
                            RenderTransform="Identity",
                            RenderTransformOrigin="0,0",
                            Rotation="0")

    points = ET.SubElement(polygon, "Points")

    point_coords = [
        {"X": "10", "Y": "50"},
        {"X": "50", "Y": "0"},
        {"X": "90", "Y": "50"},
        {"X": "50", "Y": "90"}
    ]

    for point in point_coords:
        ET.SubElement(points, "Point", X=point["X"], Y=point["Y"])
    dyn_level = ET.SubElement(window, "DynamicLevel",
                              X="77",
                              Y="363",
                              Width="4",
                              Height="322.331",
                              Fill="Transparent",
                              Stroke="Transparent",
                              LevelTag=str(tag_HH.ID),
                              LevelValue1=str(low_value),
                              LevelValue2=str(high_value),
                              LevelFill1="Red",
                              MinValue=str(low_value),
                              MaxValue=str(high_value),
                              ShapeName="Red2 Level")
    cond_list = ET.SubElement(dyn_level, "ConditionsList")
    ET.SubElement(cond_list, "IISCondition",
                  Expression=f"{low_value}=={prefix_tag}.LL && {high_value}=={prefix_tag}.HH",
                  ColorC1="Transparent",
                  PropertyNameCC1="Foreground",
                  ColorChangeType1="NormalColorChange")
    bind_list = ET.SubElement(dyn_level, "BindingList")
    ET.SubElement(bind_list, "Binding",
                  GenericName=f"{prefix_tag}.LL",
                  Value=f"{prefix_tag}.LL")
    ET.SubElement(bind_list, "Binding",
                  GenericName=f"{prefix_tag}.HH",
                  Value=f"{prefix_tag}.HH")
    ET.SubElement(window, "DynamicLevel",
                  X="77",
                  Y="363",
                  Width="4",
                  Height="322.331",
                  Fill="Transparent",
                  Stroke="Transparent",
                  LevelTag=str(tag_PH.ID),
                  LevelValue1=str(low_value),
                  LevelValue2=str(high_value),
                  LevelFill1="#00ff00",
                  MinValue=str(low_value),
                  MaxValue=str(high_value),
                  ShapeName="Green Level")

    dyn_level = ET.SubElement(window, "DynamicLevel",
                  X="77",
                  Y="363",
                  Width="4",
                  Height="322.331",
                  Fill="Transparent",
                  Stroke="Transparent",
                  LevelTag=str(tag_PL.ID),
                  LevelValue1=str(low_value),
                  LevelValue2=str(high_value),
                  LevelFill1="Red",
                  MinValue=str(low_value),
                  MaxValue=str(high_value),
                  ShapeName="Red1 Level")
    cond_list = ET.SubElement(dyn_level, "ConditionsList")
    ET.SubElement(cond_list, "IISCondition",
                  Expression=f"{low_value}=={prefix_tag}.LL AND {high_value}=={prefix_tag}.HH",
                  ColorC1="#FF808080",
                  PropertyNameCC1="Foreground",
                  ColorChangeType1="NormalColorChange")
    bind_list = ET.SubElement(dyn_level, "BindingList")

    ET.SubElement(bind_list, "Binding",
                  GenericName=f"{prefix_tag}.LL",
                  Value=f"{prefix_tag}.LL")
    ET.SubElement(bind_list, "Binding",
                  GenericName=f"{prefix_tag}.HH",
                  Value=f"{prefix_tag}.HH")

    ET.SubElement(window, "DynamicLevel",
                  X="77",
                  Y="363",
                  Width="4",
                  Height="322.331",
                  Fill="Transparent",
                  Stroke="Transparent",
                  LevelTag=str(tag_LL.ID),
                  LevelValue1=str(low_value),
                  LevelValue2=str(high_value),
                  LevelFill1="#FF808080",
                  MinValue=str(low_value),
                  MaxValue=str(high_value),
                  ShapeName="Red3 Level")
    ET.SubElement(window, "ModeControl",
                  X="5",
                  Y="110",
                  Width="24.60",
                  Height="30.4",
                  Tag=str(tag_MODE.ID))
    y_values = [365, 429, 494, 558.4, 622.864, 685]
    lines = []
    for y in y_values:
        point_1 = LogicClass.XPoint()
        point_2 = LogicClass.XPoint()
        point_3 = LogicClass.XPoint()

        point_1.X, point_1.Y = 30.4, 0.4
        point_2.X, point_2.Y = 28.1, 0
        point_3.X, point_3.Y = 14.1, 0

        line = Line(
            X="59", Y=str(y), Width="30.4", Height="10", ShapeName="line1", Fill="", Stroke="White",
            StrokeThickness="2", Name="", Tag="", RenderTransform="", RenderTransformOrigin="",
            IISCondition=[], Binding=[], Points=[point_1, point_2, point_3], Rotation="",
            LineStyle="LINE", arrowStart=None, arrowEnd=None, ZIndex="", ZIndexGroup=[]
        )
        writePolyLine(line, window, "")
        lines.append(line)



    """line1 = Line(X="59", Y="365", Width="30.4", Height="10", ShapeName="line1", Fill="", Stroke="White", StrokeThickness="3",
                 Name="", Tag="", RenderTransform="", RenderTransformOrigin="", IISCondition=[], Binding=[], Points=[[30.4, 0.4], [28.1, 0], [14.1, 0]],
                 Rotation="", LineStyle="LINE", arrowStart=None, arrowEnd=None, ZIndex="", ZIndexGroup=[])
    writePolyLine(line1, window, "")
    line2 = Line(X="59", Y="429", Width="30.4", Height="10", ShapeName="line1", Fill="", Stroke="White",
                 StrokeThickness="3",
                 Name="", Tag="", RenderTransform="", RenderTransformOrigin="", IISCondition=[], Binding=[],
                 Points=[[30.4, 0.4], [28.1, 0], [14.1, 0]],
                 Rotation="", LineStyle="LINE", arrowStart=None, arrowEnd=None, ZIndex="", ZIndexGroup=[])
    line3 = Line(X="59", Y="494", Width="30.4", Height="10", ShapeName="line1", Fill="", Stroke="White",
                 StrokeThickness="3",
                 Name="", Tag="", RenderTransform="", RenderTransformOrigin="", IISCondition=[], Binding=[],
                 Points=[[30.4, 0.4], [28.1, 0], [14.1, 0]],
                 Rotation="", LineStyle="LINE", arrowStart=None, arrowEnd=None, ZIndex="", ZIndexGroup=[])
    line4 = Line(X="59", Y="558.4", Width="30.4", Height="10", ShapeName="line1", Fill="", Stroke="White",
                 StrokeThickness="3",
                 Name="", Tag="", RenderTransform="", RenderTransformOrigin="", IISCondition=[], Binding=[],
                 Points=[[30.4, 0.4], [28.1, 0], [14.1, 0]],
                 Rotation="", LineStyle="LINE", arrowStart=None, arrowEnd=None, ZIndex="", ZIndexGroup=[])
    line5 = Line(X="59", Y="622.864", Width="30.4", Height="10", ShapeName="line1", Fill="", Stroke="White",
                 StrokeThickness="3",
                 Name="", Tag="", RenderTransform="", RenderTransformOrigin="", IISCondition=[], Binding=[],
                 Points=[[30.4, 0.4], [28.1, 0], [14.1, 0]],
                 Rotation="", LineStyle="LINE", arrowStart=None, arrowEnd=None, ZIndex="", ZIndexGroup=[])
    line6 = Line(X="59", Y="685", Width="30.4", Height="10", ShapeName="line1", Fill="", Stroke="White",
                 StrokeThickness="3",
                 Name="", Tag="", RenderTransform="", RenderTransformOrigin="", IISCondition=[], Binding=[],
                 Points=[[30.4, 0.4], [28.1, 0], [14.1, 0]],
                 Rotation="", LineStyle="LINE", arrowStart=None, arrowEnd=None, ZIndex="", ZIndexGroup=[])"""


