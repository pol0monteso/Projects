from tkinter import ttk
import tkinter as tk
from colorama import init, Fore, Back, Style
from Connection.DataBase import *
import csv
from Connection.Filtre import *
from Body.ReadWriteXML import initScreen
import xml.etree.ElementTree as ET
from Utils.Utils import indent
from datetime import datetime


#tree = ET.parse(r'C:\Emulation\Process Trainer MV-31\Prova\main.xaml')
#tree1 = ET.parse(r"C:\Users\pol.monteso\OneDrive - Inprocess Technology and consulting group, S.L\Desktop\HMIscreensYOKOGAWA\PRO-055.xaml")
#tree1 = ET.parse(r"C:\Users\pol.monteso\OneDrive - Inprocess Technology and consulting group, S.L\Desktop\Projectes\PRO-062~EDF\main.xaml")
#tree2 = ET.parse(r"C:\Users\pol.monteso\OneDrive - Inprocess Technology and consulting group, S.L\Desktop\Projectes\PRO-074~EDF\main.xaml")


def build_project_xml():
    project = ET.Element("Project")
    project_type = ET.SubElement(project, "ProjectType", Value="0")
    project_version = ET.SubElement(project, "ProjectVersion", Value="3.6.4.0 [master-57b7df6f]")

    sections_params = ET.SubElement(project, "SectionsParams")
    params_dll = ET.SubElement(sections_params, "Params", Section="DLL")
    ET.SubElement(params_dll, "Param", Name="Folder", Description="Folder", Value="OPCServerUAfx", Type="File")
    ET.SubElement(params_dll, "Param", Name="Name", Description="Name", Value="OpcServerUAfx", Type="Data")
    ET.SubElement(params_dll, "Param", Name="Version", Description="Version", Value="4.0.2.0", Type="Data")
    params_dll_params = ET.SubElement(sections_params, "Params", Section="DLL Parameters")
    ET.SubElement(params_dll_params, "Param", Name="OPCServerName", Description="Server name",
                  Value="opc.tcp://localhost:62886/IIS/OPCUA", Type="Data")
    params_interface = ET.SubElement(sections_params, "Params", Section="InterfaceType")
    ET.SubElement(params_interface, "Param", Name="Type", Description="CommDA", Value="DA", Type="Data")
    globals_elem = ET.SubElement(project, "Globals")
    global_elem = ET.SubElement(globals_elem, "Global", CasePath="C:\\", ConnectionType="70", CaseName="",
                                SimulationDataTableName="", HysysVisible="False", RefreshTimeValues="1000",
                                DesiredRealTimeFactor="1", DesiredRealTimeFactorUnits="seconds",
                                GraphicXAxisUnits="seconds",
                                LanguageID="English", OPCServerName="", OPCIPAddress="127.0.0.1", OPCGroup="Test",
                                OPCGroupRate="100", LeaveHysysOpened="False", SimulationTimeTag="",
                                IsHysysRuntime="False",
                                KillHysys="False", StartOpcServerAutomatically="False", ExecuteStepByStep="False",
                                ExecuteStepByStep_Steps="0", OPCSnapshotID="", ExecuteStepByStep_Running="False",
                                ExecuteStepByStep_Speed="0", CloseSimitProject="False", NoLookForSpeed="False",
                                NoInitialSpeed="False", AlarmSoundFileCritical="", AlarmSoundFileWarning="",
                                DisableAlarmSound="False", HysysIndependent="False", HysysVersion="",
                                DeltaV_Workstation="",
                                AlarmSoundFileLow="", SteppingType="Async", HighlightMouseOver="false", Tooltip="false",
                                EditWindow="false", VariableLimits="false", ReadonlyChangeColor="false", Priority="0",
                                Affinity="0", HideColumnAlarms="false", ScreenType="None", LastAlarms="false",
                                NumLastAlarms="0", LastAlarmsBackground="", ShowFlashingAlarms="false",
                                ScrollTopPosition="false", ExpandAlarmScreen="false", AlarmsWindowBlinkStyle="false",
                                LabelRedAlarm="false", KeyboardType="None", KeyboardConfig="", Watchdog="false",
                                WatchdogRetries="5", BackgroundWindows="White", OPCServerSimTags="false",
                                OPCDevice="false",
                                BlinkRed="true", AskConfirmButton="false", DisplayArrows="false", TimesToLdSnapshot="1",
                                TimeToIntegrateBetweenLdSnapshot="0", OpeningBehaviorCustomFaceplate="Single",
                                OpeningPositionCustomFaceplate="TopRight", MaxNumberPinnedFaceplate="0",
                                BorderCustomFaceplateShape="")
    tags = ET.SubElement(project, "Tags")
    alarms = ET.SubElement(project, "Alarms")
    curves = ET.SubElement(project, "Curves")
    trends = ET.SubElement(curves, "Trends")
    maps = ET.SubElement(curves, "Maps")
    windows = ET.SubElement(project, "Windows")
    project_tree = ET.ElementTree(project)
    return tags, alarms, curves, trends, maps, windows, project_tree, project

def start_emulation(alarm_dir, directorio, tuning_params, database_path, filter_string, ventana):
    filter_string.strip()
    filter_list = filter_string.split(":")
    tags, alarms, curves, trends, maps, windows, project_tree, project = build_project_xml()

    i = 1
    tagName_list = []
    alarm_dict = {}
    units = load_units(database_path)

    #xlsx_directory = r'C:\Emulation\HMIscreensYOKOGAWA\Source\TuningParameters'
    xlsx_data = generate_csv_data(tuning_params)
    # units = {key: {**units[key], **xlsx_data[key]} for key in units if key in xlsx_data}
    units = {key: {**units[key], **xlsx_data.get(key, {})} for key in units}
    tuples = []
    window_dict = {}
    touch_list = []
    button_list = []
    barra_progress = ttk.Progressbar(ventana, style="TProgressbar", length=300, maximum=100)
    barra_progress.grid(row=7, column=1, padx=10, pady=10, sticky="ew")
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
            if (archivo.startswith(tuple(filter_list))) and archivo.endswith('.xaml'):
                point = archivo.find('.')
                ruta_archivo = os.path.join(directorio, archivo)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

                # Cargar el archivo XML específico
                tree1 = ET.parse(ruta_archivo)
                root1 = tree1.getroot()
                print(f"Translating window {archivo} number {i} "
                      f"----------------------------------------------------------------------------------------------- [{timestamp}]")
                tuples, window_dict, touch_list = initScreen(root1, project, windows, project_tree, tags,
                                                             archivo[:point],
                                                             tagName_list, units, tuples, alarms, alarm_dict,
                                                             window_dict,
                                                             touch_list, alarmsPriority_dict, button_list)
                print("Done")
                i = i + 1
                barra_progress['value'] = (i / total) * 100
                if barra_progress['value'] == 100:
                    barra_progress.grid_remove()
                    ttk.Label(ventana, text="TRANSLATION COMPLETED", background="lightgray", font=("Arial", 20, "bold")).grid(row=7, column=1)
                ventana.update_idletasks()
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
                tuples, window_dict, touch_list = initScreen(root1, project, windows, project_tree, tags,
                                                             archivo[:point],
                                                             tagName_list, units, tuples, alarms, alarm_dict,
                                                             window_dict,
                                                             touch_list, alarmsPriority_dict, button_list)
                print("Done")
                i = i + 1
                barra_progress['value'] = (i / total) * 100
                if barra_progress['value'] == 100:
                    barra_progress.grid_remove()
                    ttk.Label(ventana, text="TRANSLATION COMPLETED", background="lightgray" ,font=("Arial", 20, "bold")).grid(row=7, column=1)
                ventana.update_idletasks()

    """window_dict = {}
    touch_list = []
    button_list = []
    tuples = []
    root = tree.getroot()
    tuples, window_dict, touch_list = initScreen(root, project, windows, project_tree, tags, "Test",
                                                 tagName_list, [], tuples, alarms, alarm_dict, window_dict,
                                                 touch_list, [], button_list)"""

    """for touch in touch_list:
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

    for button in button_list:
        if button.FunctionType == "callWindow":
            if button.Screen in window_dict.keys():
                window_name = window_dict.get(button.Screen)
                if window_name:  # Verificamos que el nombre de la ventana existe
                    # Encontrar la ventana existente en el XML
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
                                        Y=str(button.Y))"""
    indent(project)

    titulos = [
        "Window", "Name", "Object Type Yokogawa", "Object Type IIS", "Priority", "Description"
    ]

    # Escribir en el archivo CSV
    with open('./Report/report.csv', mode='w', newline='', encoding='utf-8') as report_csv:
        escritor = csv.writer(report_csv, delimiter=',')  # Cambia el delimitador a coma

        # Escribir los títulos primero
        escritor.writerow(titulos)

        # Escribir todas las tuplas de datos
        escritor.writerows(tuples)

    project_tree.write("project.xml", encoding="utf-8", xml_declaration=True)
    os.system(f"start notepad++ project.xml")
    #return "project.xml"
"""def start_emulation(alarm_dir, directorio, tuning_params, database_path, filter_string, ventana, done_event):
    filter_string.strip()
    filter_list = filter_string.split(":")
    button_list = []
    # Build XML Project
    tags, alarms, curves, trends, maps, windows, project_tree, project = build_project_xml()
    # Parse Folder and Translate
    parse_folder(filter_list, directorio, tuning_params,
                                                   database_path, ventana, alarm_dir, project,
                                                   windows, project_tree, tags, alarms)

    

    project_tree.write(r'C:\Emulation\Process Trainer MV-31\project.xml', encoding="utf-8", xml_declaration=True)
    os.system(f"start notepad++ project.xml")
    done_event.set()"""


def write_touch_button(window_dict, touch_list, button_list, windows):
    for touch in touch_list:
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

    for button in button_list:
        if button.FunctionType == "callWindow":
            if button.Screen in window_dict.keys():
                window_name = window_dict.get(button.Screen)
                if window_name:  # Verificamos que el nombre de la ventana existe
                    # Encontrar la ventana existente en el XML
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


def parse_folder(filter_list, directorio, tuning_params, database_path, ventana, alarm_dir, project, windows,
                 project_tree, tags, alarms):
    i = 1
    tagName_list = []
    alarm_dict = {}
    units = load_units(database_path)

    # xlsx_directory = r'C:\Emulation\HMIscreensYOKOGAWA\Source\TuningParameters'
    xlsx_data = generate_csv_data(tuning_params)
    # units = {key: {**units[key], **xlsx_data[key]} for key in units if key in xlsx_data}
    units = {key: {**units[key], **xlsx_data.get(key, {})} for key in units}
    tuples = []
    window_dict = {}
    touch_list = []
    button_list = []

    barra_progress = ttk.Progressbar(ventana, style="TProgressbar", length=300, maximum=100)
    barra_progress.grid(row=7, column=1, padx=10, pady=10, sticky="ew")
    print("Reading alarms:")
    # alarmsPriority_dict = leer_y_modificar_excel(r'C:\Emulation\HMIscreensYOKOGAWA\Source\CAMSAlm-CENTUM.xlsx')
    alarmsPriority_dict = leer_y_modificar_csv(alarm_dir)
    """if filter_list and "Ex" not in filter_list[0]:
        folder_filter = [xaml_folder for xaml_folder in os.listdir(directorio) if xaml_folder.startswith(tuple(filter_list) and xaml_folder.endswith("~EDF"))]
        total = len(folder_filter)
    else:
        folder_filter = [xaml_folder for xaml_folder in os.listdir(directorio) if xaml_folder.endswith("~EDF")]
        total = len(folder_filter)"""
    if filter_list and "Ex" not in filter_list[0]:
        # Filtrar carpetas que comienzan con los elementos de filter_list y terminan con "~EDF"
        folder_filter = [
            xaml_folder for xaml_folder in os.listdir(directorio)
            if os.path.isdir(os.path.join(directorio, xaml_folder))  # Asegurarse de que es un directorio
               and xaml_folder.startswith(tuple(filter_list))
               and xaml_folder.endswith("~EDF")
        ]
        total = len(folder_filter)
    else:
        # Filtrar carpetas que terminan con "~EDF"
        folder_filter = [
            xaml_folder for xaml_folder in os.listdir(directorio)
            if os.path.isdir(os.path.join(directorio, xaml_folder))  # Asegurarse de que es un directorio
               and xaml_folder.endswith("~EDF")
        ]
        total = len(folder_filter)
    for xaml_folder in folder_filter:
        # Obtener el nombre de la carpeta hasta ~EDF
        folder_name = xaml_folder.split('~EDF')[0]

        folder_path = os.path.join(directorio, xaml_folder)
        for xaml_file in os.listdir(folder_path):
            if xaml_file.endswith(".xaml"):
                item_path = os.path.join(xaml_folder, xaml_file)
                # Verificar si el item es una carpeta y si su nombre comienza con los filtros
                point = xaml_file.find('.')
                ruta_archivo = os.path.join(folder_path, xaml_file)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

                # Cargar el archivo XML específico
                tree1 = ET.parse(ruta_archivo)
                root1 = tree1.getroot()
                print(f"Translating window {xaml_file} from folder {folder_name} number {i} "
                      f"----------------------------------------------------------------------------------------------- [{timestamp}]")

                tuples, window_dict, touch_list = initScreen(root1, project, windows, project_tree, tags,
                                                             folder_name,  # Usamos folder_name hasta ~EDF
                                                             tagName_list, units, tuples, alarms, alarm_dict,
                                                             window_dict,
                                                             touch_list, alarmsPriority_dict, button_list)
                print("Done")
                i = i + 1
                barra_progress['value'] = (i / total) * 100
                if barra_progress['value'] == 100:
                    barra_progress.grid_remove()
                    ttk.Label(ventana, text="TRANSLATION COMPLETED", background="lightgray",
                              font=("Arial", 20, "bold")).grid(row=7, column=1)
                ventana.update_idletasks()
        """write_touch_button(window_dict, touch_list, button_list, windows)"""
        write_report(tuples)
    #return tuples, window_dict, touch_list, button_list


def write_report(tuples):
    titulos = [
        "Window", "Name", "Object Type Yokogawa", "Object Type IIS", "Priority", "Description"
    ]

    # Escribir en el archivo CSV
    with open('./Report/report.csv', mode='w', newline='', encoding='utf-8') as report_csv:
        escritor = csv.writer(report_csv, delimiter=',')  # Cambia el delimitador a coma

        # Escribir los títulos primero
        escritor.writerow(titulos)

        # Escribir todas las tuplas de datos
        escritor.writerows(tuples)


"""os.system(f"start notepad++ project.xml")"""

"""tree = ET.parse(r'C:\Emulation\Process Trainer MV-31\Prova\main.xaml')


project = ET.Element("Project")
project_type = ET.SubElement(project, "ProjectType", Value="0")
project_version = ET.SubElement(project, "ProjectVersion", Value="3.6.4.0 [master-57b7df6f]")
sections_params = ET.SubElement(project, "SectionsParams")
globals_elem = ET.SubElement(project, "Globals")
global_elem = ET.SubElement(globals_elem, "Global", CasePath="C:\\", ConnectionType="70", CaseName="",
                            SimulationDataTableName="", HysysVisible="False", RefreshTimeValues="1000",
                            DesiredRealTimeFactor="1", DesiredRealTimeFactorUnits="seconds",
                            GraphicXAxisUnits="seconds",
                            LanguageID="English", OPCServerName="", OPCIPAddress="127.0.0.1", OPCGroup="Test",
                            OPCGroupRate="100", LeaveHysysOpened="False", SimulationTimeTag="", IsHysysRuntime="False",
                            KillHysys="False", StartOpcServerAutomatically="False", ExecuteStepByStep="False",
                            ExecuteStepByStep_Steps="0", OPCSnapshotID="", ExecuteStepByStep_Running="False",
                            ExecuteStepByStep_Speed="0", CloseSimitProject="False", NoLookForSpeed="False",
                            NoInitialSpeed="False", AlarmSoundFileCritical="", AlarmSoundFileWarning="",
                            DisableAlarmSound="False", HysysIndependent="False", HysysVersion="", DeltaV_Workstation="",
                            AlarmSoundFileLow="", SteppingType="Async", HighlightMouseOver="false", Tooltip="false",
                            EditWindow="false", VariableLimits="false", ReadonlyChangeColor="false", Priority="0",
                            Affinity="0", HideColumnAlarms="false", ScreenType="None", LastAlarms="false",
                            NumLastAlarms="0", LastAlarmsBackground="", ShowFlashingAlarms="false",
                            ScrollTopPosition="false", ExpandAlarmScreen="false", AlarmsWindowBlinkStyle="false",
                            LabelRedAlarm="false", KeyboardType="None", KeyboardConfig="", Watchdog="false",
                            WatchdogRetries="5", BackgroundWindows="White", OPCServerSimTags="false", OPCDevice="false",
                            BlinkRed="true", AskConfirmButton="false", DisplayArrows="false", TimesToLdSnapshot="1",
                            TimeToIntegrateBetweenLdSnapshot="0", OpeningBehaviorCustomFaceplate="Single",
                            OpeningPositionCustomFaceplate="TopRight", MaxNumberPinnedFaceplate="0",
                            BorderCustomFaceplateShape="")
tags = ET.SubElement(project, "Tags")
alarms = ET.SubElement(project, "Alarms")
curves = ET.SubElement(project, "Curves")
trends = ET.SubElement(curves, "Trends")
maps = ET.SubElement(curves, "Maps")
windows = ET.SubElement(project, "Windows")
project_tree = ET.ElementTree(project)

directorio = (r"C:\Emulation\HMIscreensYOKOGAWA")

# Iterar sobre todos los archivos que comienzan con 'PRO' en el directorio
i = 1
tagName_list = []
alarm_dict = {}
units = generate_units_json()

xlsx_directory = r'C:\Emulation\HMIscreensYOKOGAWA\Source\TuningParameters'
xlsx_data = generate_excel_data(xlsx_directory)
#units = {key: {**units[key], **xlsx_data[key]} for key in units if key in xlsx_data}
units = {key: {**units[key], **xlsx_data.get(key, {})} for key in units}
tuples = []
window_dict = {}
touch_list = []
button_list = []
print("llegint propietats de les alarmes:")
#alarmsPriority_dict = leer_y_modificar_excel(r'C:\Emulation\HMIscreensYOKOGAWA\Source\CAMSAlm-CENTUM.xlsx')
for archivo in os.listdir(directorio):
    if (archivo.startswith('PRO-001')) and archivo.endswith('.xaml'):
        point = archivo.find('.')
        ruta_archivo = os.path.join(directorio, archivo)

        # Cargar el archivo XML específico
        tree1 = ET.parse(ruta_archivo)
        root1 = tree1.getroot()
        print("Carregant la pantalla " + archivo + " número  " + str(
            i) + "-----------------------------------------------------------------------------------------------")
        tuples, window_dict, touch_list = initScreen(root1, project, windows, project_tree, tags, archivo[:point],
                                                     tagName_list, units, tuples, alarms, alarm_dict, window_dict,
                                                     touch_list,  [], button_list)
        print("Done " + str(archivo) + " número  " + str(
            i) + "-----------------------------------------------------------------------------------------------")
        i = i + 1


for touch in touch_list:
    if touch.Screen in window_dict.keys():
        #touch.Screen = window_dict[touch.Screen]
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


for button in button_list:
    if button.Screen in window_dict.keys():
        window_name = window_dict.get(button.Screen)
        if window_name:  # Verificamos que el nombre de la ventana existe
            # Encontrar la ventana existente en el XML
            #window_elem = windows.find(f"Window[@ID='{window_name}']")
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
        #window_elem = windows.find(f"Window[@ID='{window_name}']")
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
with open('Report/report.csv', mode='w', newline='', encoding='utf-8') as report_csv:
    escritor = csv.writer(report_csv, delimiter=',')  # Cambia el delimitador a coma

    # Escribir los títulos primero
    escritor.writerow(titulos)

    # Escribir todas las tuplas de datos
    escritor.writerows(tuples)

project_tree.write("project.xml", encoding="utf-8", xml_declaration=True)

os.system(f"start notepad++ project.xml")"""
"""directorio = (r"C:\Emulation\HMIscreensYOKOGAWA")
start_emulation(r'C:\Emulation\HMIscreensYOKOGAWA\Source\CAMSAlm-CENTUM.xlsx', directorio)"""
