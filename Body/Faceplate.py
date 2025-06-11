import copy

import Classes
import xml.etree.ElementTree as ET

from Body.ReadWriteXML import *
from Classes.ClassControls import Tag
import uuid
from decimal import Decimal, ROUND_HALF_UP

from Utils.TuningFiles import add_chart, add_tag_hystoric

"""def find_faceplate_tags(tag_list, prefix_tag, units):
    tag_Mode = None
    tag_ALRM = None
    tag_AFLS = None
    tag_AOFS = None
    tag__PV = None
    tag_SV = None
    tag_HH = None
    tag_PH = None
    tag_PL = None
    tag_LL = None
    tag_PV = None
    tag_MV = None

    for tag in tag_list:
        if tag.Name == f"{prefix_tag}.PV":
            tag_PV = tag
        elif tag.Name == f"{prefix_tag}.MV":
            tag_MV = tag
        elif tag.Name == f"{prefix_tag}.MODE":
            tag_Mode = tag
        elif tag.Name == f"{prefix_tag}.AOFS":
            tag_AOFS = tag
        elif tag.Name == f"{prefix_tag}.#PV":
            tag__PV = tag
        elif tag.Name == f"{prefix_tag}.SV":
            tag_SV = tag
        elif tag.Name == f"{prefix_tag}.HH":
            tag_HH = tag
        elif tag.Name == f"{prefix_tag}.PH":
            tag_PH = tag
        elif tag.Name == f"{prefix_tag}.PL":
            tag_PL = tag
        elif tag.Name == f"{prefix_tag}.LL":
            tag_LL = tag
        elif tag.Name == f"{prefix_tag}.ALRM":
            tag_ALRM = tag
        elif tag.Name == f"{prefix_tag}.AFLS":
            tag_AFLS = tag

    # Crear los tags que no existen
    if tag_PV is None:
        tag_PV = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.PV", HysysVar=f"@@@@{prefix_tag}.PV", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_PV)

    if tag_MV is None:
        tag_MV = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.MV", HysysVar=f"@@@@{prefix_tag}.MV", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_MV)
    if tag_Mode is None:
        tag_Mode = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.MODE", HysysVar=f"@@@@{prefix_tag}.MODE",
                       NumDecimals=3,
                       UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_Mode)
    if tag_AOFS is None:
        tag_AOFS = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.AOFS", HysysVar=f"@@@@{prefix_tag}.AOFS",
                       NumDecimals=3,
                       UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_AOFS)

    if tag__PV is None:
        tag__PV = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.#PV", HysysVar=f"@@@@{prefix_tag}.#PV", NumDecimals=3,
                      UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag__PV)
    if tag_SV is None:
        tag_SV = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.SV", HysysVar=f"@@@@{prefix_tag}.SV", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_SV)
    if tag_HH is None:
        tag_HH = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.HH", HysysVar=f"@@@@{prefix_tag}.HH", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["HH"])
        tag_list.append(tag_HH)
    if tag_PH is None:
        tag_PH = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.PH", HysysVar=f"@@@@{prefix_tag}.PH", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["PH"])
        tag_list.append(tag_PH)
    if tag_PL is None:
        tag_PL = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.PL", HysysVar=f"@@@@{prefix_tag}.PL", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["PL"])
        tag_list.append(tag_PL)
    if tag_LL is None:
        tag_LL = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.LL", HysysVar=f"@@@@{prefix_tag}.LL", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["LL"])
        tag_list.append(tag_LL)
    if tag_ALRM is None:
        tag_ALRM = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.ALRM", HysysVar=f"@@@@{prefix_tag}.ALRM",
                       NumDecimals=3,
                       UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_ALRM)
    if tag_AFLS is None:
        tag_AFLS = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.AFLS", HysysVar=f"@@@@{prefix_tag}.AFLS",
                       NumDecimals=3,
                       UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_AFLS)

    return [tag_Mode, tag_ALRM, tag_AFLS, tag_AOFS, tag__PV, tag_SV, tag_HH, tag_PH, tag_PL, tag_LL, tag_PV, tag_MV]"""
def find_faceplate_tags(tag_list, prefix_tag, units):
    tag_Mode = None
    tag_ALRM = None
    tag_AFLS = None
    tag_AOFS = None
    tag__PV = None
    tag_SV = None
    tag_HH = None
    tag_PH = None
    tag_PL = None
    tag_LL = None
    tag_PV = None
    tag_MV = None
    tag_P = None
    tag_I = None
    tag_VL = None
    tag_D = None
    tag_DL = None
    tag_GW = None
    tag_SVH = None
    tag_DB = None
    tag_SVL = None
    tag_CB = None
    tag_CK = None
    tag_MH = None
    tag_ML = None
    tag_PMV = None

    for tag in tag_list:
        if tag.Name == f"{prefix_tag}.PV":
            tag_PV = tag
        elif tag.Name == f"{prefix_tag}.MV":
            tag_MV = tag
        elif tag.Name == f"{prefix_tag}.MH":
            tag_MH = tag
        elif tag.Name == f"{prefix_tag}.ML":
            tag_ML = tag
        elif tag.Name == f"{prefix_tag}.MODE":
            tag_Mode = tag
        elif tag.Name == f"{prefix_tag}.AOFS":
            tag_AOFS = tag
        elif tag.Name == f"{prefix_tag}.#PV":
            tag__PV = tag
        elif tag.Name == f"{prefix_tag}.SV":
            tag_SV = tag
        elif tag.Name == f"{prefix_tag}.ML":
            tag_ML = tag
        elif tag.Name == f"{prefix_tag}.HH":
            tag_HH = tag
        elif tag.Name == f"{prefix_tag}.PH":
            tag_PH = tag
        elif tag.Name == f"{prefix_tag}.PL":
            tag_PL = tag
        elif tag.Name == f"{prefix_tag}.LL":
            tag_LL = tag
        elif tag.Name == f"{prefix_tag}.ALRM":
            tag_ALRM = tag
        elif tag.Name == f"{prefix_tag}.AFLS":
            tag_AFLS = tag
        elif tag.Name == f"{prefix_tag}.P":
            tag_P = tag
        elif tag.Name == f"{prefix_tag}.I":
            tag_I = tag
        elif tag.Name == f"{prefix_tag}.VL":
            tag_VL = tag
        elif tag.Name == f"{prefix_tag}.D":
            tag_D = tag
        elif tag.Name == f"{prefix_tag}.DL":
            tag_DL = tag
        elif tag.Name == f"{prefix_tag}.GW":
            tag_GW = tag
        elif tag.Name == f"{prefix_tag}.SVH":
            tag_SVH = tag
        elif tag.Name == f"{prefix_tag}.DB":
            tag_DB = tag
        elif tag.Name == f"{prefix_tag}.SVL":
            tag_SVL = tag
        elif tag.Name == f"{prefix_tag}.CB":
            tag_CB = tag
        elif tag.Name == f"{prefix_tag}.CK":
            tag_CK = tag
        elif tag.Name == f"{prefix_tag}.PMV":
            tag_PMV = tag


    # Crear los tags que no existen
    if tag_PV is None:
        tag_PV = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.PV", HysysVar=f"@@@@{prefix_tag}.PV", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_PV)

    if tag_MV is None:
        tag_MV = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.MV", HysysVar=f"@@@@{prefix_tag}.MV", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_MV)
    if tag_Mode is None:
        tag_Mode = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.MODE", HysysVar=f"@@@@{prefix_tag}.MODE",
                       NumDecimals=3,
                       UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_Mode)
    if tag_AOFS is None:
        tag_AOFS = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.AOFS", HysysVar=f"@@@@{prefix_tag}.AOFS",
                       NumDecimals=3,
                       UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_AOFS)

    if tag__PV is None:
        tag__PV = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.#PV", HysysVar=f"@@@@{prefix_tag}.#PV", NumDecimals=3,
                      UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag__PV)
    if tag_SV is None:
        tag_SV = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.SV", HysysVar=f"@@@@{prefix_tag}.SV", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_SV)
    if tag_HH is None:
        tag_HH = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.HH", HysysVar=f"@@@@{prefix_tag}.HH", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["HH"])
        tag_list.append(tag_HH)
    if tag_PH is None:
        tag_PH = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.PH", HysysVar=f"@@@@{prefix_tag}.PH", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["PH"])
        tag_list.append(tag_PH)
    if tag_PL is None:
        tag_PL = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.PL", HysysVar=f"@@@@{prefix_tag}.PL", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["PL"])
        tag_list.append(tag_PL)
    if tag_LL is None:
        tag_LL = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.LL", HysysVar=f"@@@@{prefix_tag}.LL", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["LL"])
        tag_list.append(tag_LL)
    if tag_ALRM is None:
        tag_ALRM = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.ALRM", HysysVar=f"@@@@{prefix_tag}.ALRM",
                       NumDecimals=3,
                       UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_ALRM)
    if tag_AFLS is None:
        tag_AFLS = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.AFLS", HysysVar=f"@@@@{prefix_tag}.AFLS",
                       NumDecimals=3,
                       UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_AFLS)
    if tag_P is None:
        tag_P = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.P", HysysVar=f"@@@@{prefix_tag}.P", NumDecimals=3,
                    UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_P)
    if tag_I is None:
        tag_I = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.I", HysysVar=f"@@@@{prefix_tag}.I", NumDecimals=3,
                    UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_I)
    if tag_VL is None:
        tag_VL = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.VL", HysysVar=f"@@@@{prefix_tag}.VL", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_VL)
    if tag_D is None:
        tag_D = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.D", HysysVar=f"@@@@{prefix_tag}.D", NumDecimals=3,
                    UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_D)
    if tag_DL is None:
        tag_DL = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.DL", HysysVar=f"@@@@{prefix_tag}.DL", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_DL)
    if tag_GW is None:
        tag_GW = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.GW", HysysVar=f"@@@@{prefix_tag}.GW", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_GW)
    if tag_SVH is None:
        tag_SVH = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.SVH", HysysVar=f"@@@@{prefix_tag}.SVH", NumDecimals=3,
                      UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_SVH)
    if tag_DB is None:
        tag_DB = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.DB", HysysVar=f"@@@@{prefix_tag}.DB", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_DB)
    if tag_SVL is None:
        tag_SVL = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.SVL", HysysVar=f"@@@@{prefix_tag}.SVL", NumDecimals=3,
                      UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_SVL)
    if tag_CB is None:
        tag_CB = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.CB", HysysVar=f"@@@@{prefix_tag}.CB", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_CB)
    if tag_CK is None:
        tag_CK = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.CK", HysysVar=f"@@@@{prefix_tag}.CK", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_CK)
    if tag_MH is None:
        tag_MH = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.MH", HysysVar=f"@@@@{prefix_tag}.MH", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
    if tag_ML is None:
        tag_ML = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.ML", HysysVar=f"@@@@{prefix_tag}.ML", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
    if tag_PMV is None:
        tag_PMV = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.PMV", HysysVar=f"@@@@{prefix_tag}.PMV", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)

    return [tag_Mode, tag_ALRM, tag_AFLS, tag_AOFS, tag__PV, tag_SV, tag_HH, tag_PH, tag_PL, tag_LL, tag_PV, tag_MV, tag_P, tag_I, tag_VL, tag_D, tag_DL, tag_GW, tag_SVH, tag_DB, tag_SVL, tag_CB, tag_CK, tag_MH, tag_ML, tag_PMV]

def find_PVI_faceplate_tags(tag_list, prefix_tag, units):
    tag_Mode = None
    tag_ALRM = None
    tag_AFLS = None
    tag_AOFS = None
    tag__PV = None
    tag_HH = None
    tag_PH = None
    tag_PL = None
    tag_LL = None
    tag_PV = None
    tag_VL = None

    for tag in tag_list:
        if tag.Name == f"{prefix_tag}.PV":
            tag_PV = tag
        elif tag.Name == f"{prefix_tag}.MODE":
            tag_Mode = tag
        elif tag.Name == f"{prefix_tag}.AOFS":
            tag_AOFS = tag
        elif tag.Name == f"{prefix_tag}.#PV":
            tag__PV = tag
        elif tag.Name == f"{prefix_tag}.PH":
            tag_PH = tag
        elif tag.Name == f"{prefix_tag}.PL":
            tag_PL = tag
        elif tag.Name == f"{prefix_tag}.LL":
            tag_LL = tag
        elif tag.Name == f"{prefix_tag}.ALRM":
            tag_ALRM = tag
        elif tag.Name == f"{prefix_tag}.AFLS":
            tag_AFLS = tag
        elif tag.Name == f"{prefix_tag}.VL":
            tag_VL = tag


    # Crear los tags que no existen
    if tag_PV is None:
        tag_PV = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.PV", HysysVar=f"@@@@{prefix_tag}.PV", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_PV)

    if tag_Mode is None:
        tag_Mode = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.MODE", HysysVar=f"@@@@{prefix_tag}.MODE",
                       NumDecimals=3,
                       UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_Mode)
    if tag_AOFS is None:
        tag_AOFS = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.AOFS", HysysVar=f"@@@@{prefix_tag}.AOFS",
                       NumDecimals=3,
                       UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_AOFS)

    if tag__PV is None:
        tag__PV = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.#PV", HysysVar=f"@@@@{prefix_tag}.#PV", NumDecimals=3,
                      UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag__PV)
    if tag_HH is None:
        tag_HH = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.HH", HysysVar=f"@@@@{prefix_tag}.HH", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["HH"])
        tag_list.append(tag_HH)
    if tag_PH is None:
        tag_PH = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.PH", HysysVar=f"@@@@{prefix_tag}.PH", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["PH"])
        tag_list.append(tag_PH)
    if tag_PL is None:
        tag_PL = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.PL", HysysVar=f"@@@@{prefix_tag}.PL", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["PL"])
        tag_list.append(tag_PL)
    if tag_LL is None:
        tag_LL = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.LL", HysysVar=f"@@@@{prefix_tag}.LL", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=units[prefix_tag]["LL"])
        tag_list.append(tag_LL)
    if tag_ALRM is None:
        tag_ALRM = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.ALRM", HysysVar=f"@@@@{prefix_tag}.ALRM",
                       NumDecimals=3,
                       UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_ALRM)
    if tag_AFLS is None:
        tag_AFLS = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.AFLS", HysysVar=f"@@@@{prefix_tag}.AFLS",
                       NumDecimals=3,
                       UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_AFLS)
    if tag_VL is None:
        tag_VL = Tag(ID=str(uuid.uuid4()), Name=f"{prefix_tag}.VL", HysysVar=f"@@@@{prefix_tag}.VL", NumDecimals=3,
                     UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
        tag_list.append(tag_VL)

    return [tag_Mode, tag_ALRM, tag_AFLS, tag_AOFS, tag__PV, tag_HH, tag_PH, tag_PL, tag_LL, tag_PV, tag_VL]

def faceplate_pid(tag_list, prefix_tag, alarmsPriority_dict, units, touch, tags, tagName_list, cascade_dict, alarms, plotmanager, tags_hys, tuning_tag_list):
    new_tag = find_faceplate_tags(tag_list, prefix_tag, units)

    # Obtener los colores de alarmas
    hh_color = str(alarmsPriority_dict.get(f"{prefix_tag}.HH", [None, None])[1])
    hi_color = str(alarmsPriority_dict.get(f"{prefix_tag}.HI", [None, None])[1])
    li_color = str(alarmsPriority_dict.get(f"{prefix_tag}.LO", [None, None])[1])
    ll_color = str(alarmsPriority_dict.get(f"{prefix_tag}.LL", [None, None])[1])

    high_value = Decimal(str(units[prefix_tag]["SH"]))
    low_value = Decimal(str(units[prefix_tag]["SL"]))

    decimal_places = abs(high_value.as_tuple().exponent)

    # Calcular los puntos intermedios con la misma precisión
    puntos = [
        (low_value + i * (high_value - low_value) / (6 - 1)).quantize(Decimal(10) ** -decimal_places,
                                                                      rounding=ROUND_HALF_UP)
        for i in range(6)
    ]
    # Si hh_color no está definido, usar hi_color
    if hh_color is None:
        hh_color = hi_color
    tag_Mode, tag_ALRM, tag_AFLS, tag_AOFS, tag__PV, tag_SV, tag_HH, tag_PH, tag_PL, tag_LL, tag_PV, tag_MV, tag_P, tag_I, tag_VL, tag_D, tag_DL, tag_GW, tag_SVH, tag_DB, tag_SVL, tag_CB, tag_CK, tag_MH, tag_ML, tag_PMV = new_tag
    # Escribir los tags en la base de datos
    writeTags(new_tag, tags, "", tagName_list, alarms, units, alarmsPriority_dict, None)

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
                  Height="74.4",
                  X="2",
                  Y="70.3352",
                  ShapeName="ln_0",
                  Fill="#FF000000",
                  Stroke="#FF000000",
                  StrokeThickness="1",
                  Group="")
    ET.SubElement(window, "Rectangle",
                  Width="138.3",
                  Height="45.657",
                  X="2",
                  Y="149",
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
    ET.SubElement(window, "Rectangle",
                  Width="138.5",
                  Height="45.66",
                  X="2",
                  Y="198",
                  ShapeName="rec_0",
                  Fill="Black",
                  Stroke="Black",
                  StrokeThickness="1",
                  Group="")
    ET.SubElement(window, "Rectangle",
                  Width="138.5",
                  Height="45.66",
                  X="2",
                  Y="246",
                  ShapeName="rec_1",
                  Fill="Black",
                  Stroke="Black",
                  StrokeThickness="1",
                  Group="")
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
                            LevelFill2="#00ff00",
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
        ("lb_0", str(puntos[-1]), "360"),
        ("lb_1", str(puntos[-2]), "424"),
        ("lb_2", str(puntos[3]), "489"),
        ("lb_3", str(puntos[2]), "553.4"),
        ("lb_4", str(puntos[1]), "617.864"),
        ("lb_5", str(puntos[0]), "680"),
    ]
    print(prefix_tag)
    for shape_name, content, y_pos in labels:
        ET.SubElement(window, "LabelText",
                      Width="46.4",
                      Height="11.4",
                      X="93",
                      Y=str(y_pos),
                      ShapeName=shape_name,
                      Foreground="#FF000000",
                      Background="#00FFFFFF",
                      Tag="",
                      Format="",
                      Content=content,
                      FontAutoSize="False",
                      FontSize="10",
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
                              Y="103",
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
                              Y="121",
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
                  Y="151",
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
                  Width="89.6",
                  Height="23.06",
                  X="48",
                  Y="200",
                  ShapeName="lb_9",
                  Foreground="#FFFFFFFF",
                  Background="#00FFFFFF",
                  Tag="",
                  Content=unit,
                  FontAutoSize="False",
                  FontSize="17",
                  FontFamily="Courier New",
                  TextAlign="Right",
                  CenterX="0.5",
                  CenterY="0.5")
    ET.SubElement(window, "InputText",
                  Width="101.8",
                  Height="22.8",
                  X="35",
                  Y="174",
                  ShapeName="lb_11",
                  Foreground="Cyan",
                  Background="#00FFFFFF",
                  Tag=str(tag_PV.ID),
                  Content="VALUE",
                  FontAutoSize="False",
                  FontSize="19",
                  FontFamily="Courier New",
                  TextAlign="Right",
                  CenterX="0.5",
                  CenterY="0.5",
                  Stroke="Transparent")
    ET.SubElement(window, "LabelText",
                  Width="0.699300699300699",
                  Height="0.0353606789250354",
                  X="0.153846153846154",
                  Y="0",
                  ShapeName="lb_13",
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
                              LevelFill2="Red",
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
                  LevelFill2="#00ff00",
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
                              LevelFill2="Red",
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
                  LevelFill2="#FF808080",
                  MinValue=str(low_value),
                  MaxValue=str(high_value),
                  ShapeName="Red3 Level")

    ET.SubElement(window, "LabelText",
                  Width="0.537062937062938",
                  Height="0.0263083451202263",
                  X="0.034965034965035",
                  Y="200",
                  ShapeName="lb_8",
                  Foreground="#FFFFFFFF",
                  Background="#00FFFFFF",
                  Tag="",
                  Content="SV",
                  FontAutoSize="True",
                  FontSize="12",
                  FontFamily="Courier New",
                  TextAlign="Left",
                  CenterX="0.5",
                  CenterY="0.5")
    ET.SubElement(window, "LabelText",
                  Width="89.6",
                  Height="23.06",
                  X="48",
                  Y="151",
                  ShapeName="lb_9",
                  Foreground="#FFFFFFFF",
                  Background="#00FFFFFF",
                  Tag="",
                  Content=unit,
                  FontAutoSize="False",
                  FontSize="17",
                  FontFamily="Courier New",
                  TextAlign="Right",
                  CenterX="0.5",
                  CenterY="0.5")
    ET.SubElement(window, "LabelText",
                  Width="0.537062937062938",
                  Height="0.0263083451202263",
                  X="0.034965034965035",
                  Y="246",
                  ShapeName="lb_8",
                  Foreground="#FFFFFFFF",
                  Background="#00FFFFFF",
                  Tag="",
                  Content="MV",
                  FontAutoSize="True",
                  FontSize="12",
                  FontFamily="Courier New",
                  TextAlign="Left",
                  CenterX="0.5",
                  CenterY="0.5")
    """cascade_tag = next((k for k, v in cascade_dict.items() if v == prefix_tag), None)
    if cascade_tag:
        unit_mv = units[cascade_tag]['Unit']
    else:
        unit_mv = "%"
        """
    if prefix_tag in cascade_dict:
        unit_mv = units[cascade_dict[prefix_tag]]['Unit']
    else:
        unit_mv = "%"
    ET.SubElement(window, "LabelText",
                  Width="88",
                  Height="22.06",
                  X="48",
                  Y="246",
                  ShapeName="lb_9",
                  Foreground="#FFFFFFFF",
                  Background="#00FFFFFF",
                  Tag="",
                  Content=unit_mv,
                  FontAutoSize="False",
                  FontSize="17",
                  FontFamily="Courier New",
                  TextAlign="Right",
                  CenterX="0.5",
                  CenterY="0.5")
    ET.SubElement(window, "InputText",
                  Width="90.4",
                  Height="25",
                  X="47",
                  Y="221",
                  ShapeName="lb_12",
                  Foreground="Cyan",
                  Background="#00FFFFFF",
                  Tag=str(tag_SV.ID),
                  Content="VALUE",
                  FontAutoSize="False",
                  FontSize="19",
                  FontFamily="Courier New",
                  TextAlign="Right",
                  CenterX="0.5",
                  CenterY="0.5",
                  Stroke="Transparent")
    ET.SubElement(window, "InputText",
                  Width="90.4",
                  Height="25.2",
                  X="47",
                  Y="271",
                  ShapeName="lb_10",
                  Foreground="Cyan",
                  Background="#00FFFFFF",
                  Tag=str(tag_MV.ID),
                  Content="VALUE",
                  FontAutoSize="False",
                  FontSize="19",
                  FontFamily="Courier New",
                  TextAlign="Right",
                  CenterX="0.5",
                  CenterY="0.5",
                  Stroke="Transparent")
    ET.SubElement(window, "ModeControl",
                  X="9",
                  Y="98",
                  Width="24.60",
                  Height="30.4",
                  Tag=tag_Mode.ID)
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
    ophi = float(units[prefix_tag]["OPHI"])
    oplo = float(units[prefix_tag]["OPLO"])
    msh = float(units[prefix_tag]["MSH"])
    msl = float(units[prefix_tag]["MSL"])
    if ophi > msh:
        ophi = msh
    if oplo < msl:
        oplo = msl
    y_hi = 322.331 - 2 + 363 - ((float(ophi) - msl) / (msh - msl)) * 322.331
    y_lo = 322.331 - 2 + 363 - ((float(oplo) - msl) / (msh - msl)) * 322.331
    poly_HI = ET.SubElement(window,"Polygon",
                  Shapename="oph1",
                  Width="20",
                  Height="4",
                  Fill="#00fffd",
                  Stroke="DarkBlue",
                  X="12",
                  Y=str(y_hi))
    points = ET.SubElement(poly_HI, "Points")

    point_coords = [
        {"X": "0", "Y": "0"},
        {"X": "0", "Y": "50"},
        {"X": "50", "Y": "50"},
        {"X": "50", "Y": "37.5"},
        {"X": "100", "Y": "37.5"},
        {"X": "100", "Y": "12.5"},
        {"X": "50", "Y": "12.5"},
        {"X": "50", "Y": "0"}
    ]

    for point in point_coords:
        ET.SubElement(points, "Point", X=point["X"], Y=point["Y"])
    poly_LO = ET.SubElement(window, "Polygon",
                  Shapename="oplo",
                  Width="20",
                  Height="4",
                  Fill="#00fffd",
                  Stroke="DarkBlue",
                  X="12",
                  Y=str(y_lo))

    points = ET.SubElement(poly_LO, "Points")

    point_coords = [
        {"X": "0", "Y": "0"},
        {"X": "0", "Y": "50"},
        {"X": "50", "Y": "50"},
        {"X": "50", "Y": "37.5"},
        {"X": "100", "Y": "37.5"},
        {"X": "100", "Y": "12.5"},
        {"X": "50", "Y": "12.5"},
        {"X": "50", "Y": "0"}
    ]
    for point in point_coords:
        ET.SubElement(points, "Point", X=point["X"], Y=point["Y"])

    if prefix_tag in cascade_dict:
        #unit_mv = units[cascade_tag]['Unit']
        high_value_mv = f"{prefix_tag}.HH"
        low_value_mv = f"{prefix_tag}.LL"
    else:
        high_value_mv = "100"
        low_value_mv = "0"
    offset_polygon1 = ET.SubElement(window, "Polygon",
                                    X="33",
                                    Y="678",
                                    Width="16.8",
                                    Height="14.4",
                                    Stroke="Red",
                                    Fill="Red",
                                    OffsetY="0",
                                    TransformFromY="678",
                                    TransformToY="357",
                                    TagValueY=f"{prefix_tag}.MV",
                                    PropertyY="true",
                                    HighLimitY=high_value_mv,
                                    LowLimitY=low_value_mv)
    points = ET.SubElement(offset_polygon1, "Points")

    point_coords = [
        {"X": "0", "Y": "0"},
        {"X": "0", "Y": "100"},
        {"X": "50", "Y": "50"}
    ]

    for point in point_coords:
        ET.SubElement(points, "Point", X=point["X"], Y=point["Y"])
    offset_polygon2 = ET.SubElement(window, "Polygon",
                                    X="90",
                                    Y="678",
                                    Width="16.8",
                                    Height="14.4",
                                    Stroke="Yellow",
                                    Fill="Yellow",
                                    OffsetY="0",
                                    TransformFromY="678",
                                    TransformToY="355",
                                    TagValueY=f"{prefix_tag}.SV",
                                    PropertyY="true",
                                    HighLimitY=f"{prefix_tag}.HH",
                                    LowLimitY=f"{prefix_tag}.LL")
    points = ET.SubElement(offset_polygon2, "Points")

    point_coords = [
        {"X": "100", "Y": "0"},
        {"X": "100", "Y": "100"},
        {"X": "0", "Y": "50"}
    ]

    for point in point_coords:
        ET.SubElement(points, "Point", X=point["X"], Y=point["Y"])

    ET.SubElement(window, "LabelText",
                  ShapeName="tuningText",
                  X="81",
                  Y="121",
                  Width="55.9999999999998",
                  Height="24.8",
                  Foreground="White",
                  Background="#00FFFFFF",
                  Tag="",
                  Content="Tuning",
                  FontAutoSize="True",
                  FontSize="17",
                  FontFamily="Courier New",
                  TextAlign="Left",
                  CenterX="0.5",
                  CenterY="0.5")
    if "\n" in comment:
        tuningComment = comment.replace("\n", ' ')
    else:
        tuningComment = comment
    plotID = uuid.uuid4()
    tuning_list = [tag_PV, tag_MV, tag_SV]
    if tag_PV not in tuning_tag_list:
        tuning_tag_list.append(tag_PV)
        add_tag_hystoric(tags_hys, tuning_list)
    add_chart(plotmanager, tuning_list, prefix_tag, str(plotID), "")

    ET.SubElement(window, "TuningWindow",
                  ShapeName="tuning_window",
                  X="81",
                  Y="121",
                  Width="55.9999999999998",
                  Height="24.8",
                  PlotID=str(plotID),
                  TagName=prefix_tag,
                  TagBlock="PID",
                  TagMode=f"{prefix_tag}.MODE",
                  TagPV=f"{prefix_tag}.PV",
                  TagComment=tuningComment,
                  TagAlarm=f"{prefix_tag}.ALRM",
                  TagHH=f"{prefix_tag}.HH",
                  TagMH=f"{prefix_tag}.MH",
                  TagSL=units[prefix_tag]['SL'],
                  TagSH=units[prefix_tag]['SH'],
                  TagPH=f"{prefix_tag}.PH",
                  TagML=f"{prefix_tag}.ML",
                  TagPL=f"{prefix_tag}.PL",
                  TagP=f"{prefix_tag}.P",
                  TagSV=f"{prefix_tag}.SV",
                  TagLL=f"{prefix_tag}.LL",
                  TagI=f"{prefix_tag}.I",
                  TagMV=f"{prefix_tag}.MV",
                  TagVL=f"{prefix_tag}.VL",
                  TagD=f"{prefix_tag}.D",
                  TagDL=f"{prefix_tag}.DL",
                  TagGW=f"{prefix_tag}.GW",
                  TagSVH=f"{prefix_tag}.SVH",
                  TagDB=f"{prefix_tag}.DB",
                  TagOPHI=str(units[prefix_tag]['OPHI']),
                  TagOPLO=str(units[prefix_tag]['OPLO']),
                  TagCB=f"{prefix_tag}.CB",
                  TagMSH=str(units[prefix_tag]['MSH']),
                  TagMSL=str(units[prefix_tag]['MSL']),
                  TagPMV=f"{prefix_tag}.PMV",
                  TagCK=f"{prefix_tag}.CK",
                  TagSVL=f"{prefix_tag}.SVL",
                  HHColor=hh_color,
                  HIColor=hi_color,
                  LOColor=li_color,
                  LLColor=ll_color
                  )

    return tuning_tag_list

def _faceplate_pvi(tag_list, prefix_tag, alarmsPriority_dict, units, touch, tags, tagName_list, alarms, plotmanager, tags_hys, tag_tuning_list):
    new_tag = find_PVI_faceplate_tags(tag_list, prefix_tag, units)

    hh_color = str(alarmsPriority_dict.get(f"{prefix_tag}.HH", [None, None])[1])
    hi_color = str(alarmsPriority_dict.get(f"{prefix_tag}.HI", [None, None])[1])
    li_color = str(alarmsPriority_dict.get(f"{prefix_tag}.LO", [None, None])[1])
    ll_color = str(alarmsPriority_dict.get(f"{prefix_tag}.LL", [None, None])[1])

    """high_value = float(units[prefix_tag]["SH"])
    low_value = float(units[prefix_tag]["SL"])

    # Calcular los puntos intermedios
    puntos = [round(low_value + i * (high_value - low_value) / (6 - 1), 2) for i in range(6)]"""
    high_value = Decimal(str(units[prefix_tag]["SH"]))
    low_value = Decimal(str(units[prefix_tag]["SL"]))

    decimal_places = abs(high_value.as_tuple().exponent)

    puntos = [
        (low_value + i * (high_value - low_value) / (6 - 1)).quantize(Decimal(10) ** -decimal_places,
                                                                      rounding=ROUND_HALF_UP)
        for i in range(6)
    ]
    if hh_color is None:
        hh_color = hi_color
    tag_Mode, tag_ALRM, tag_AFLS, tag_AOFS, tag__PV, tag_HH, tag_PH, tag_PL, tag_LL, tag_PV, tag_VL = new_tag
    # Escribir los tags en la base de datos
    writeTags(new_tag, tags, "", tagName_list, alarms, units,alarmsPriority_dict, None)

    if ll_color is None:
        ll_color = li_color
    unit = units[prefix_tag]["Unit"]
    comment = units[prefix_tag]["Comment"]
    com_ = comment.strip(" ")

    space_count = 0
    for i, char in enumerate(com_):
        if char == " ":
            space_count += 1
        if space_count == 2:
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
                  Height="74.4",
                  X="2",
                  Y="70.3352",
                  ShapeName="ln_0",
                  Fill="#FF000000",
                  Stroke="#FF000000",
                  StrokeThickness="1",
                  Group="")
    ET.SubElement(window, "Rectangle",
                  Width="138.3",
                  Height="45.657",
                  X="2",
                  Y="149",
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
                            LevelFill2="#00ff00",
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
        ("lb_0", str(puntos[-1]), "360"),
        ("lb_1", str(puntos[-2]), "424"),
        ("lb_2", str(puntos[3]), "489"),
        ("lb_3", str(puntos[2]), "553.4"),
        ("lb_4", str(puntos[1]), "617.864"),
        ("lb_5", str(puntos[0]), "680"),
    ]
    print(prefix_tag)
    for shape_name, content, y_pos in labels:
        ET.SubElement(window, "LabelText",
                      Width="46.4",
                      Height="11.4",
                      X="93",
                      Y=str(y_pos),
                      ShapeName=shape_name,
                      Foreground="#FF000000",
                      Background="#00FFFFFF",
                      Tag="",
                      Format="",
                      Content=content,
                      FontAutoSize="False",
                      FontSize="10",
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
                              Y="103",
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
                              Y="121",
                              Background="#00FFFFFF",
                              Foreground="Cyan",
                              Text="ALARM",
                              FontSize="17",
                              FontFamily="Courier New",
                              HorizontalAlignment="Stretch",
                              ScaleX="1",
                              ScaleY="1")
    ET.SubElement(window, "LabelText",
                              ShapeName="text_1295",
                              X="81",
                              Y="121",
                              Width="55.9999999999998",
                              Height="24.8",
                              Foreground="White",
                              Background="#00FFFFFF",
                              Tag="",
                              Content="Tuning",
                              FontAutoSize="True",
                              FontSize="17",
                              FontFamily="Courier New",
                              TextAlign="Left",
                              CenterX="0.5",
                              CenterY="0.5")
    if "\n" in comment:
        tuningComment = comment.replace("\n", ' ')
    else:
        tuningComment = comment
    tuning_list = [tag_PV]
    plotID = uuid.uuid4()
    if tag_PV not in tag_tuning_list:
        tag_tuning_list.append(tag_PV)
        add_tag_hystoric(tags_hys, tuning_list)
    add_chart(plotmanager, tuning_list, prefix_tag, str(plotID), "")
    ET.SubElement(window, "TuningWindow",
                  ShapeName="tuning_window",
                  X="81",
                  Y="121",
                  PlotID=str(plotID),
                  Width="55.9999999999998",
                  Height="24.8",
                  TagName=prefix_tag,
                  TagBlock="PVI",
                  TagMode=f"{prefix_tag}.MODE",
                  TagPV=f"{prefix_tag}.PV",
                  TagComment=tuningComment,
                  TagAlarm=f"{prefix_tag}.ALRM",
                  TagHH=f"{prefix_tag}.HH",
                  TagSL=units[prefix_tag]['SL'],
                  TagSH=units[prefix_tag]['SH'],
                  TagPH=f"{prefix_tag}.PH",
                  TagPL=f"{prefix_tag}.PL",
                  TagLL=f"{prefix_tag}.LL",
                  TagVL=f"{prefix_tag}.VL",
                  HHColor=hh_color,
                  HIColor=hi_color,
                  LOColor=li_color,
                  LLColor=ll_color
    )
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
                  Y="151",
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
    ET.SubElement(window, "InputText",
                  Width="101.8",
                  Height="22.8",
                  X="35",
                  Y="174",
                  ShapeName="lb_11",
                  Foreground="Cyan",
                  Background="#00FFFFFF",
                  Tag=str(tag_PV.ID),
                  Content="VALUE",
                  FontAutoSize="False",
                  FontSize="19",
                  FontFamily="Courier New",
                  TextAlign="Right",
                  CenterX="0.5",
                  CenterY="0.5",
                  Stroke="Transparent")
    ET.SubElement(window, "LabelText",
                  Width="0.699300699300699",
                  Height="0.0353606789250354",
                  X="0.153846153846154",
                  Y="0",
                  ShapeName="lb_13",
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
                              LevelFill2="Red",
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
                  LevelFill2="#00ff00",
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
                              LevelFill2="Red",
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
                  LevelFill2="#FF808080",
                  MinValue=str(low_value),
                  MaxValue=str(high_value),
                  ShapeName="Red3 Level")

    ET.SubElement(window, "LabelText",
                  Width="89.6",
                  Height="23.06",
                  X="48",
                  Y="151",
                  ShapeName="lb_9",
                  Foreground="#FFFFFFFF",
                  Background="#00FFFFFF",
                  Tag="",
                  Content=unit,
                  FontAutoSize="False",
                  FontSize="17",
                  FontFamily="Courier New",
                  TextAlign="Right",
                  CenterX="0.5",
                  CenterY="0.5")
    ET.SubElement(window, "ModeControl",
                  X="9",
                  Y="98",
                  Width="24.60",
                  Height="30.4",
                  Tag=tag_Mode.ID)
    y_values = [363, 427, 492, 556.4, 620.864, 683]
    """lines = []
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







    point_coords = [
        {"X": "0", "Y": "0"},
        {"X": "0", "Y": "50"},
        {"X": "50", "Y": "50"},
        {"X": "50", "Y": "37.5"},
        {"X": "100", "Y": "37.5"},
        {"X": "100", "Y": "12.5"},
        {"X": "50", "Y": "12.5"},
        {"X": "50", "Y": "0"}
    ]
    for point in point_coords:
        ET.SubElement(points, "Point", X=point["X"], Y=point["Y"])"""
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

def faceplate_template(tag_list, prefix_tag, alarmsPriority_dict, units, touch, tags, tagName_list, cascade_dict, alarms, item):
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
    tag_ = None
    id_tag = None
    id_template = None
    # Renombrar etiquetas y verificar en tag_list
    for elem in item.iter():
        for attr_key, attr_val in elem.attrib.items():
            if "TagTemplate" in elem.tag:
                if attr_key == "Name":
                    attr_val = elem.attrib[attr_key]
                    tag_template = attr_val.replace("TAG", prefix_tag)
                    tag_ = None
                    for tag1 in tag_list:
                        if tag1.Name == tag_template:
                            tag_ = tag1
                        if tag_ is None:
                            idtag = str(uuid.uuid4())
                            tag_ = Tag(ID=idtag, Name=tag_template, HysysVar=f"@@@@{tag_template}",
                                         NumDecimals=2,
                                         UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)
                            writeTags([tag_], tags, "", tagName_list, alarms, units, alarmsPriority_dict, None)

            if attr_key == "ID":
                if tag_ is not None:
                    id_tag = tag_.ID
                    id_template = elem.attrib[attr_key]

            if "TAG." in attr_val:
                # Reemplazar TAG. por prefix_tag.
                new_val = attr_val.replace("TAG.", f"{prefix_tag}.")
                elem.set(attr_key, new_val)

            if "ID" in attr_val:
                if id_tag is not None and id_template is not None:
                    new_val = attr_val.replace(id_template, id_tag)
                    elem.set(attr_key, new_val)
    window = ET.SubElement(CustomFacePlate, "Window",
                           WindowWidth="143",
                           WindowHeight="807",
                           Background="#FFC0C0C0",
                           MainWindow="False",
                           ID=str(uuid.uuid4()))

    for child in item:
        window.append(copy.deepcopy(child))



