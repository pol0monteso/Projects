from uuid import uuid4

from Body.Faceplate import faceplate_pid, _faceplate_pvi, faceplate_template
from Body.ReadingAlgorithm import *
from tkinter import ttk
import tkinter as tk
from colorama import init, Fore, Back, Style
from Connection.DataBase import *
import csv
from Connection.Filtre import *
from Body.ReadWriteXML import initScreen, faceplate_pvi
import xml.etree.ElementTree as ET

from Utils.TuningFiles import build_tuning_window, build_hystoric_window
from Utils.Utils import indent
from datetime import datetime

from testCase import build_project_xml


def test_emulation(alarm_dir, directorio, tuning_params, database_path, filter_string, template_directory):
    tag_tuning_list = []
    plotmanager, root = build_tuning_window()
    hystoric, tags_hys = build_hystoric_window()
    filter_string.strip()
    filter_list = filter_string.split(":")
    tags, alarms, curves, trends, maps, windows, project_tree, project = build_project_xml()

    i = 1
    tagName_list = []
    alarm_dict = {}
    units = load_units(database_path)
    cascade_dict = load_connect_mapping(database_path)
    template_dict = check_template(template_directory)
    #xlsx_directory = r'C:\Emulation\HMIscreensYOKOGAWA\Source\TuningParameters'
    xlsx_data = generate_csv_data(tuning_params)
    # units = {key: {**units[key], **xlsx_data[key]} for key in units if key in xlsx_data}
    #units = {key: {**units[key], **xlsx_data.get(key, {})} for key in units}
    all_keys = set(units.keys()) | set(xlsx_data.keys())
    units = {key: {**units.get(key, {}), **xlsx_data.get(key, {})} for key in all_keys}
    tuples = []
    window_dict = {}
    touch_list = []
    button_list = []
    tag_list = []

    print("Reading alarms:")
    #alarmsPriority_dict = leer_y_modificar_excel(r'C:\Emulation\HMIscreensYOKOGAWA\Source\CAMSAlm-CENTUM.xlsx')
    alarmsPriority_dict = leer_y_modificar_csv(alarm_dir)
    if filter_list and "Ex" not in filter_list[0]:
        archivos_pro = [archivo for archivo in os.listdir(directorio) if archivo.startswith(tuple(filter_list))]
        total = len(archivos_pro)
    else:
        total = len(os.listdir(directorio))
    for archivo in os.listdir(directorio):
        if filter_list and "Ex" not in filter_list[0]:
            #if (archivo.startswith(tuple(filter_list))) and archivo.endswith('.xaml'):
            if (archivo.startswith("PRO-001")) and archivo.endswith('.xaml'):
                point = archivo.find('.')
                ruta_archivo = os.path.join(directorio, archivo)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

                # Cargar el archivo XML específico
                tree1 = ET.parse(ruta_archivo)
                root1 = tree1.getroot()
                print(f"Translating window {archivo} number {i} "
                      f"----------------------------------------------------------------------------------------------- [{timestamp}]")
                tuples, window_dict, touch_list, tag_list = initScreen(root1, project, windows, project_tree, tags,
                                                             archivo[:point],
                                                             tagName_list, units, tuples, alarms, alarm_dict,
                                                             window_dict,
                                                             touch_list, alarmsPriority_dict, button_list, tag_list)
                print("Done")
                i = i + 1
        else:
            if archivo.endswith('.xaml'):
                point = archivo.find('.')
                ruta_archivo = os.path.join(directorio, archivo)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                # Cargar el archivo XML específico
                tree1 = ET.parse(ruta_archivo)
                root1 = tree1.getroot()
                print(f"Translating window {archivo} number {i} "
                      f"----------------------------------------------------------------------------------------------- [{timestamp}]")
                tuples, window_dict, touch_list, tag_list = initScreen(root1, project, windows, project_tree, tags,
                                                             archivo[:point],
                                                             tagName_list, units, tuples, alarms, alarm_dict,
                                                             window_dict,
                                                             touch_list, alarmsPriority_dict, button_list, tag_list)
                print("Done")
                i = i + 1

    """window_dict = {}
    touch_list = []
    button_list = []
    tuples = []
    root = tree.getroot()
    tuples, window_dict, touch_list = initScreen(root, project, windows, project_tree, tags, "Test",
                                                 tagName_list, [], tuples, alarms, alarm_dict, window_dict,
                                                 touch_list, [], button_list)"""

    for touch in touch_list:
        if touch.FunctionType == "callWindow":
            if touch.Screen in window_dict.keys():
                # touch.Screen = window_dict[touch.Screen]
                window_name = window_dict.get(touch.Screen)
                if window_name:  # Verificamos que el nombre de la ventana existe
                    # Encontrar la ventana existente en el XML
                    window_elem = windows.find(f"Window[@ID='{window_name}']")

                    if window_elem is not None:  # Verificamos que la ventana fue encontrada
                        # Agregar el elemento 'Touch' dentro de la ventana encontrada
                        touch_elem = ET.SubElement(touch.Window, "Touch",
                                                   Stroke=touch.Stroke,
                                                   Screen=window_name,
                                                   Height=touch.Height,
                                                   Width=touch.Width,
                                                   RenderTransform=touch.RenderTransform,
                                                   RenderTransformOrigin=touch.RenderTransformOrigin,
                                                   X=str(touch.X),
                                                   Y=str(touch.Y),
                                                   TypeFunction="callWindow")
        elif touch.FunctionType == "instrumentCommand":
            button_elem = ET.SubElement(touch.Window, "Touch",
                                        Screen="",
                                        Stroke=touch.Stroke,
                                        Height=touch.Height,
                                        Width=touch.Width,
                                        RenderTransform=touch.RenderTransform,
                                        ShapeName="",
                                        RenderTransformOrigin=touch.RenderTransformOrigin,
                                        X=str(touch.X),
                                        Y=str(touch.Y),
                                        Command=str(touch.CommandData),
                                        CommandData=str(touch.CommandData),
                                        DataTag=str(touch.DataTag),
                                        TypeFunction=str(touch.FunctionType))
        elif touch.Faceplate:
            if touch.Faceplate in units:
                prefix_tag = touch.Faceplate
                if "Block" in units[prefix_tag]:
                    if units[prefix_tag]["Block"] == "PVI":
                        _faceplate_pvi(tag_list, prefix_tag, alarmsPriority_dict, units, touch, tags, tagName_list, alarms, plotmanager, tags_hys, tag_tuning_list)
                    elif units[prefix_tag]["Block"] == "PID":
                        tag_tuning_list = faceplate_pid(tag_list, prefix_tag, alarmsPriority_dict, units, touch, tags, tagName_list, cascade_dict, alarms, plotmanager, tags_hys, tag_tuning_list)
                    if template_dict != {}:
                        for key, item in template_dict.items():
                            if units[prefix_tag]["Block"] == key:
                                faceplate_template(tag_list, prefix_tag, alarmsPriority_dict, units, touch, tags, tagName_list, cascade_dict, alarms, item)
    for button in button_list:
        if button.FunctionType == "callWindow":
            if button.Screen in window_dict.keys():
                window_name = window_dict.get(button.Screen)
                if window_name:  # Verificamos que el nombre de la ventana existe
                    # Encontrar la ventana existente en el XML
                    """window_elem = windows.find(f"Window[@ID='{window_name}']")"""
                    button_elem = ET.SubElement(button.Window, "Button",
                                                Background=button.Background,
                                                Foreground=button.Foreground,
                                                Screen=window_name,
                                                Height=button.Height,
                                                Width=button.Width,
                                                FontFamily=button.FontFamily,
                                                FontWeight=str(button.FontWeight),
                                                Text=button.Text,
                                                RenderTransform=button.RenderTransform,
                                                FontSize=str(button.FontSize),
                                                RenderTransformOrigin=button.RenderTransformOrigin,
                                                ShapeName="",
                                                TypeFunction=button.FunctionType,
                                                X=str(button.X),
                                                Y=str(button.Y))
            else:
                button_elem = ET.SubElement(button.Window, "Button",
                                            Background=button.Background,
                                            Foreground=button.Foreground,
                                            Screen="",
                                            Height=button.Height,
                                            Width=button.Width,
                                            FontFamily=button.FontFamily,
                                            FontWeight=str(button.FontWeight),
                                            Text=button.Text,
                                            RenderTransform=button.RenderTransform,
                                            FontSize=str(button.FontSize),
                                            RenderTransformOrigin=button.RenderTransformOrigin,
                                            ShapeName="",
                                            TypeFunction=button.FunctionType,
                                            X=str(button.X),
                                            Y=str(button.Y))
        elif button.FunctionType == "instrumentCommand":
            button_elem = ET.SubElement(button.Window, "Button",
                                        Background=button.Background,
                                        Foreground=button.Foreground,
                                        Screen="",
                                        Height=button.Height,
                                        Width=button.Width,
                                        FontFamily=button.FontFamily,
                                        FontWeight=button.FontWeight,
                                        Text=button.Text,
                                        RenderTransform=button.RenderTransform,
                                        FontSize=button.FontSize,
                                        ShapeName="",
                                        RenderTransformOrigin=button.RenderTransformOrigin,
                                        X=str(button.X),
                                        Y=str(button.Y),
                                        Command=str(button.CommandData),
                                        CommandData=str(button.CommandData),
                                        DataTag=str(button.DataTag),
                                        TypeFunction=str(button.FunctionType))
        else:
            """window_elem = windows.find(f"Window[@ID='{window_name}']")"""
            button_elem = ET.SubElement(button.Window, "Button",
                                        Background=button.Background,
                                        Foreground=button.Foreground,
                                        Screen="",
                                        Height=button.Height,
                                        Width=button.Width,
                                        FontFamily=button.FontFamily,
                                        FontWeight=str(button.FontWeight),
                                        Text=button.Text,
                                        RenderTransform=button.RenderTransform,
                                        FontSize=str(button.FontSize),
                                        ShapeName="",
                                        RenderTransformOrigin=button.RenderTransformOrigin,
                                        X=str(button.X),
                                        Y=str(button.Y))
    indent(project)

    titulos = [
        "Window", "Name", "Object Type Yokogawa", "Object Type IIS", "Priority", "Description"
    ]

    # Escribir en el archivo CSV
    """with open('./Report/report.csv', mode='w', newline='', encoding='utf-8') as report_csv:
        escritor = csv.writer(report_csv, delimiter=',')  # Cambia el delimitador a coma

        # Escribir los títulos primero
        escritor.writerow(titulos)

        # Escribir todas las tuplas de datos
        escritor.writerows(tuples)"""

    config = ET.SubElement(plotmanager, "Configuration", {
        "ServerAddress": "http://localhost:8086",
        "Database": "DBdemo1",
        "Table": "DBdemo1",
        "QueryInterval": "1000",
        "LastValueIndex": "1",
        "UserName": "ISInflux",
        "Password": "Inprocess.100",
        "xmlns": "http://schemas.datacontract.org/2004/07/ISChartEngine"
    })
    project_tree.write("project.xml", encoding="utf-8", xml_declaration=True)
    os.system(f"start notepad++ project.xml")
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    tree.write("pmanager.cfg", encoding="utf-8", xml_declaration=True)
    os.system(f"start notepad++ pmanager.cfg")
    tree = ET.ElementTree(hystoric)
    ET.indent(tree, space="  ", level=0)

    tree.write("C:\BAPCO\project.xml", encoding="utf-8", xml_declaration=True)
    os.system(f"start notepad++ C:\BAPCO\project.xml")


test_emulation(
    r'C:\Emulation\HMIscreensYOKOGAWA\Source\CAMSAlm-CENTUM.csv',
    r"C:\Emulation\HMIscreensYOKOGAWA",
    r'C:\Emulation\HMIscreensYOKOGAWA\Source\TuningParameters',
    r'C:\Emulation\HMIscreensYOKOGAWA\Source',
    "",
    ""
)
