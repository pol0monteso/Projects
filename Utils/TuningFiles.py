import os
import xml.etree.ElementTree as ET

def build_tuning_window():

    # PlotManager
    plotmanager = ET.Element( "PlotManager", {
        "xmlns": "http://schemas.datacontract.org/2004/07/ISChartEngine.Controls"
    })
    return plotmanager, plotmanager

def build_hystoric_window():
    project = ET.Element("Project")

    # ProjectType y ProjectVersion
    ET.SubElement(project, "ProjectType", {"Value": "0"})
    ET.SubElement(project, "ProjectVersion", {"Value": "4.1.1.0 [Releases/4.1.1.0-cca87ae1]"})

    # SectionsParams
    sections = ET.SubElement(project, "SectionsParams")

    # Section: DLL
    params_dll = ET.SubElement(sections, "Params", {"Section": "DLL"})
    ET.SubElement(params_dll, "Param", {"Name": "Folder", "Description": "Folder", "Value": "InfluxDB", "Type": "File"})
    ET.SubElement(params_dll, "Param", {"Name": "Name", "Description": "Name", "Value": "InfluxDB", "Type": "Data"})
    ET.SubElement(params_dll, "Param",
                  {"Name": "Version", "Description": "Version", "Value": "4.2.1.0", "Type": "Data"})

    # Section: DLL Parameters
    params_dll_params = ET.SubElement(sections, "Params", {"Section": "DLL Parameters"})
    dll_params = [
        ("Server", "Server", "http://localhost:8086", "Data"),
        ("dbName", "DB Name", "DBdemo1", "Data"),
        ("User", "User", "ISInflux", "Data"),
        ("Pass", "Pass", "zk/+F6DiSBy4/OtKUt+uuA==", "Password"),
        ("Client", "Client", "false", "Boolean"),
        ("Https", "Https", "false", "Boolean"),
        ("KeepDatabase", "Keep database", "false", "Boolean"),
        ("DisableSnapshots", "Disable snapshots", "false", "Boolean"),
        ("PruneHours", "Timespan to store in hours (0 = unlimited)", "8", "Data")
    ]
    for name, desc, value, typ in dll_params:
        ET.SubElement(params_dll_params, "Param", {"Name": name, "Description": desc, "Value": value, "Type": typ})

    # Section: InterfaceType
    params_interface = ET.SubElement(sections, "Params", {"Section": "InterfaceType"})
    ET.SubElement(params_interface, "Param", {"Name": "Type", "Description": "CommDA", "Value": "DA", "Type": "Data"})

    # Globals
    globals_ = ET.SubElement(project, "Globals")
    ET.SubElement(globals_, "Global", {
        "CasePath": "C:\\",
        "ConnectionType": "70",
        "CaseName": "",
        "RefreshTimeValues": "1000",
        "LanguageID": "English",
        "OPCServerName": "",
        "OPCIPAddress": "127.0.0.1",
        "OPCGroup": "Test",
        "OPCGroupRate": "100",
        "StartOpcServerAutomatically": "False",
        "NoLookForSpeed": "False",
        "NoInitialSpeed": "False",
        "AlarmSoundFileCritical": "",
        "AlarmSoundFileWarning": "",
        "DisableAlarmSound": "False",
        "AlarmSoundFileLow": "",
        "SteppingType": "Async",
        "HighlightMouseOver": "false",
        "Tooltip": "false",
        "EditWindow": "false",
        "VariableLimits": "false",
        "ReadonlyChangeColor": "false",
        "Priority": "0",
        "Affinity": "0",
        "KeyboardType": "None",
        "KeyboardConfig": "",
        "Watchdog": "false",
        "WatchdogRetries": "5",
        "BackgroundWindows": "White",
        "OPCDevice": "false",
        "BlinkRed": "true",
        "AskConfirmButton": "false",
        "DisplayArrows": "false",
        "TimesToLdSnapshot": "1",
        "TimeToIntegrateBetweenLdSnapshot": "0",
        "OpeningBehaviorCustomFaceplate": "Single",
        "OpeningPositionCustomFaceplate": "TopRight",
        "MaxNumberPinnedFaceplate": "0",
        "CloseUnpinnedFaceplateNavigatingAway": "false",
        "BorderCustomFaceplateShape": "",
        "ClampScreenValues": "False",
        "ClampInletValuesToComm": "False",
        "ClampOutletValuesFromComm": "False",
        "ScreenType": "None",
        "LastAlarms": "false",
        "NumLastAlarms": "0",
        "LastAlarmsBackground": "",
        "ShowFlashingAlarms": "false",
        "ShowTextFlashingAlarms": "false",
        "ShowBackgroundFlashingAlarms": "false",
        "ScrollTopPosition": "false",
        "ExpandAlarmScreen": "false",
        "AlarmsWindowBlinkStyle": "false",
        "LabelRedAlarm": "false",
        "IISRemoteSubscriptorType": ".",
        "IISRemoteParentProject": "",
        "IISRemoteParentProjectIP": "127.0.0.1",
        "IISRemoteParentProjectPort": "9000"
    })
    tags = ET.SubElement(project, "Tags")
    ET.SubElement(project, "AlarmsColumnsSettings")
    alarms = ET.SubElement(project, "Alarms")
    ET.SubElement(alarms, "Connection",{
        "Type":"",
        "Url":""
    })
    ET.SubElement(project, "Windows")


    return project, tags

def add_tag_hystoric(tags, tag_list):
    for tag in tag_list:
            ET.SubElement(tags,"Tag",
                          ID=str(tag.ID),
                          Name=str(tag.Name),
                          HysysVar="@@@@"+tag.Name)


def add_chart(plotmanager, tag_list, prefix, plotID, ID_parameter):
    ischart = ET.SubElement(plotmanager, "ISChartControl", {
        "i:type": "ISLineChart",
        "PlotName": f"Plot_{prefix}",
        "Background": "#FF000000",
        "PlotNameBackground": "#FF7FFF00",
        "ID": plotID,
        "FontFamily": "New Courser",
        "FontSize": "10",
        "Height": "600",
        "Width": "800",
        "EmbeddedType": "EMBEDDED",
        "xmlns:i":"http://www.w3.org/2001/XMLSchema-instance"
    })

    embedded = ET.SubElement(ischart, "EmbeddedParameters")
    ET.SubElement(embedded, "Parameter").text = ID_parameter
    is_cartesian = ET.SubElement(ischart, "ISCartesianChart", {
        "FormatterActualTime": "hh_mm_ss",
        "FormatterSessionTime": "hh_mm_ss",
        "TimeRangeActualTime": "HOUR_1",
        "TimeRangeSessionTime": "HOUR_1",
        "IsActualTime": "True",
        "MaxPointCount": "25000",
        "RefreshEverySeconds": "120",
        "ShowDetailedPlot": "True",
        "ShowAxes": "True",
        "NumberVerticalBars": "4"
    })

    axes = ET.SubElement(is_cartesian, "Axes", {"xmlns": "ISChartEngine.Controls"})
    ET.SubElement(axes, "ISAxis", {
        "Name": "Axis0",
        "Foreground": "#FF808080",
        "MinValue": "NaN",
        "MaxValue": "NaN",
        "IsAutoScaling": "True",
        "ShowAxisName": "True",
        "From": "0",
        "To": "100",
        "NumberDecimals": "2",
        "ColorSelectionBrush": "#FF808080",
        "SelectedLineTagName": "",
        "UsingSelectionColor": "True",
        "xmlns": "http://schemas.datacontract.org/2004/07/ISChartEngine.Controls"
    })
    series = ET.SubElement(is_cartesian, "Series", {"xmlns": "ISChartEngine.Controls"})
    stroke_colors = {"PV": "Cyan", "MV": "White", "SV": "#FFFF00FF"}
    for tag_ in tag_list:
        suffix = tag_.Name.split('.')[1]
        ET.SubElement(series, "ISLine", {
            "ID": str(tag_.ID),
            "Name": tag_.Name,
            "Stroke": stroke_colors.get(suffix, "#FFFFFFFF"),
            "StrokeThickness": "1",
            "Axis": "0",
            "ISTag": tag_.Name,
            "LineSmoothness": "0",
            "SerieType": "LINE",
            "PointGeometry": "",
            "UseStrokeAsFillColor": "False",
            "StoredFillColor": "#00FFFFFF",
            "GroupID": "",
            "xmlns": "http://schemas.datacontract.org/2004/07/ISChartEngine.Controls"
        })


"""tree = ET.ElementTree(root)
ET.indent(tree, space="  ", level=0)
tree.write("pmanager.cfg", encoding="utf-8", xml_declaration=True)
os.system(f"start notepad++ pmanager.cfg")"""

build_tuning_window()