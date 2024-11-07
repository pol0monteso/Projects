import xml.etree.ElementTree as ET
import numpy as np
from matplotlib.transforms import Affine2D

# Definir la función para analizar el XML y extraer la información relevante
def parse_xml(xml_string):
    root = ET.fromstring(xml_string)
    components = []

    # Función auxiliar para extraer atributos de transformaciones
    def parse_transform(transform_str):
        values = [float(val) for val in transform_str.split(',')]
        return Affine2D(values)

    for group in root.findall('.//{*}GroupComponent'):
        component_info = {
            'name': group.attrib.get('{yiapcspvgbdc:ComponentProperties.Name}', ''),
            'width': float(group.attrib.get('Width', '0')),
            'height': float(group.attrib.get('Height', '0')),
            'left': float(group.attrib.get('Canvas.Left', '0')),
            'top': float(group.attrib.get('Canvas.Top', '0')),
            'render_transform': parse_transform(group.attrib.get('RenderTransform', '1,0,0,1,0,0')),
            'children': []
        }

        for child in group.findall('{*}GroupComponent'):
            child_info = {
                'name': child.attrib.get('{yiapcspvgbdc:ComponentProperties.Name}', ''),
                'width': float(child.attrib.get('Width', '0')),
                'height': float(child.attrib.get('Height', '0')),
                'left': float(child.attrib.get('Canvas.Left', '0')),
                'top': float(child.attrib.get('Canvas.Top', '0')),
                'render_transform': parse_transform(child.attrib.get('RenderTransform', '1,0,0,1,0,0')),
                'children': []
            }
            component_info['children'].append(child_info)

        components.append(component_info)

    return components

xml_string = '''<yiapcspvgbdc0:GroupComponent
        RenderTransform="1,-2.44921270764475E-16,2.44921270764475E-16,1,0,0"
        RenderTransformOrigin="0,0"
        Tag=""
        Visibility="Visible"
        Width="70.0000000000003"
        Height="63.9999998655688"
        Canvas.Left="300"
        Canvas.Top="230"
        Panel.ZIndex="108"
        yiapcspvgbdc:ComponentProperties.Name="LinkedPart - STRAINER2"
        yiapcspvgbdc:ComponentProperties.LayerID="Normal Drawing Layer 1">
        <yiapcspvgbdc0:GroupComponent.Information>
            <yiapcspvgbmdg:LinkedPartInformation
                Name="STRAINER"
                OriginalWidth="26.1945205996612"
                OriginalHeight="23.999999865569"
                CreationDateTime="23/07/2019 03:46:39"
                LastModifiedDateTime="12/11/2019 09:58:31"
                LinkedPartId="bd8263da-78fb-4dd2-8492-1608abd6b9fe"
                Magnification="0"
                FileFormatRev="0" />
        </yiapcspvgbdc0:GroupComponent.Information>
        <yiapcspvgbdc0:GroupComponent
            RenderTransform="6.12303176911189E-17,1,-1,6.12303176911189E-17,0,0"
            RenderTransformOrigin="0,0"
            Tag="Id=8"
            Information="{x:Null}"
            Visibility="Visible"
            Width="63.9999998655688"
            Height="70.0000000000004"
            Canvas.Left="70.0000000000003"
            Canvas.Top="0"
            Panel.ZIndex="108"
            yiapcspvgbdc:ComponentProperties.Name="Group0"
            yiapcspvgbdc:ComponentProperties.LayerID="Normal Drawing Layer 1">
            <yiapcspvgbdc0:GroupComponent
                RenderTransform="6.12303176911189E-17,1,1,-6.12303176911189E-17,0,0"
                RenderTransformOrigin="0,0"
                Focusable="False"
                Tag="Id=9"
                Information="{x:Null}"
                Visibility="Visible"
                Width="14.4413593793926"
                Height="10.6666667040086"
                Canvas.Left="21.3333334080172"
                Canvas.Top="55.5586406206077"
                Panel.ZIndex="108"
                yiapcspvgbdc:ComponentProperties.Name="AAA"
                yiapcspvgbdc:ComponentProperties.LayerID="Normal Drawing Layer 1"
                yiapcspvgccd:DebuggerProperties.SetDebugData="False">
                <yiapcspvgccbsc:IPCSRectangle
                    Focusable="False"
                    ShapeHeight="6.9019608084761686"
                    ShapeWidth="11.346782369522774"
                    Stroke="#FF666666"
                    StrokeThickness="1"
                    Tag="Id=232"
                    Fill="{rcsr:iPCSBrushExtension Style=Gradient_0004, Color1=#3F3F3F, Color2=#E5E5E5}"
                    Canvas.Left="1.66533453693773E-15"
                    Canvas.Top="1.88235294776623"
                    Panel.ZIndex="569"
                    yiapcspvgbdc:ComponentProperties.Name="Rectangle_0025"
                    yiapcspvgbdc:ComponentProperties.LayerID="Normal Drawing Layer 1"
                    yiapcspvgccd:DebuggerProperties.SetDebugData="False">
                    <yiapcspvggn:GenericNameComponent.GenericName>
                        <yiapcspvggn:GenericName />
                    </yiapcspvggn:GenericNameComponent.GenericName>
                </yiapcspvgccbsc:IPCSRectangle>
                <yiapcspvgccbsc:IPCSRectangle
                    Focusable="False"
                    ShapeHeight="10.666666704008625"
                    ShapeWidth="3.0945770098698517"
                    Stroke="#FF666666"
                    StrokeThickness="1"
                    Tag="Id=233"
                    Fill="{rcsr:iPCSBrushExtension Style=Gradient_0004, Color1=#3F3F3F, Color2=#E5E5E5}"
                    Canvas.Left="11.3467823695228"
                    Canvas.Top="1.17614251671227E-15"
                    Panel.ZIndex="570"
                    yiapcspvgbdc:ComponentProperties.Name="Rectangle_0026"
                    yiapcspvgbdc:ComponentProperties.LayerID="Normal Drawing Layer 1"
                    yiapcspvgccd:DebuggerProperties.SetDebugData="False">
                    <yiapcspvggn:GenericNameComponent.GenericName>
                        <yiapcspvggn:GenericName />
                    </yiapcspvggn:GenericNameComponent.GenericName>
                </yiapcspvgccbsc:IPCSRectangle>
            </yiapcspvgbdc0:GroupComponent>
            <yiapcspvgccbsc:IPCSRectangle
                Rotation="-90"
                Visibility="Visible"
                Focusable="False"
                RenderTransform="6.12303176911189E-17,-1,1,6.12303176911189E-17,0,0"
                RenderTransformOrigin="0,0"
                ShapeHeight="4.7296898260834332"
                ShapeWidth="54.208680814128549"
                Stroke="#FF666666"
                StrokeThickness="1"
                Tag="Id=10"
                Fill="{rcsr:iPCSBrushExtension Style=Gradient_0004, Color1=#3F3F3F, Color2=#E5E5E5}"
                Canvas.Left="4.42056219860041"
                Canvas.Top="62.3117932228294"
                Panel.ZIndex="109"
                yiapcspvgbdc:ComponentProperties.Name="Rectangle_0017"
                yiapcspvgbdc:ComponentProperties.LayerID="Normal Drawing Layer 1"
                yiapcspvgccd:DebuggerProperties.SetDebugData="False">
                <yiapcspvggn:GenericNameComponent.GenericName>
                    <yiapcspvggn:GenericName />
                </yiapcspvggn:GenericNameComponent.GenericName>
            </yiapcspvgccbsc:IPCSRectangle>
            <yiapcspvgbdc0:GroupComponent
                RenderTransform="6.12303176911189E-17,-1,1,6.12303176911189E-17,0,0"
                RenderTransformOrigin="0,0"
                Focusable="False"
                Tag="Id=11"
                Information="{x:Null}"
                Visibility="Visible"
                Width="14.4413593793927"
                Height="10.6666667040086"
                Canvas.Left="21.3333334080172"
                Canvas.Top="14.4413593793927"
                Panel.ZIndex="110"
                yiapcspvgbdc:ComponentProperties.Name="Group_0014"
                yiapcspvgbdc:ComponentProperties.LayerID="Normal Drawing Layer 1"
                yiapcspvgccd:DebuggerProperties.SetDebugData="False">
                <yiapcspvgccbsc:IPCSRectangle
                    Focusable="False"
                    ShapeHeight="6.9019608084761686"
                    ShapeWidth="11.34678236952279"
                    Stroke="#FF666666"
                    StrokeThickness="1"
                    Tag="Id=232"
                    Fill="{rcsr:iPCSBrushExtension Style=Gradient_0004, Color1=#3F3F3F, Color2=#E5E5E5}"
                    Canvas.Left="1.22124532708767E-15"
                    Canvas.Top="1.88235294776623"
                    Panel.ZIndex="569"
                    yiapcspvgbdc:ComponentProperties.Name="Rectangle_0025"
                    yiapcspvgbdc:ComponentProperties.LayerID="Normal Drawing Layer 1"
                    yiapcspvgccd:DebuggerProperties.SetDebugData="False">
                    <yiapcspvggn:GenericNameComponent.GenericName>
                        <yiapcspvggn:GenericName />
                    </yiapcspvggn:GenericNameComponent.GenericName>
                </yiapcspvgccbsc:IPCSRectangle>
                <yiapcspvgccbsc:IPCSRectangle
                    Focusable="False"
                    ShapeHeight="10.666666704008625"
                    ShapeWidth="3.0945770098698553"
                    Stroke="#FF666666"
                    StrokeThickness="1"
                    Tag="Id=233"
                    Fill="{rcsr:iPCSBrushExtension Style=Gradient_0004, Color1=#3F3F3F, Color2=#E5E5E5}"
                    Canvas.Left="11.3467823695228"
                    Canvas.Top="1.17614251671227E-15"
                    Panel.ZIndex="570"
                    yiapcspvgbdc:ComponentProperties.Name="Rectangle_0026"
                    yiapcspvgbdc:ComponentProperties.LayerID="Normal Drawing Layer 1"
                    yiapcspvgccd:DebuggerProperties.SetDebugData="False">
                    <yiapcspvggn:GenericNameComponent.GenericName>
                        <yiapcspvggn:GenericName />
                    </yiapcspvggn:GenericNameComponent.GenericName>
                </yiapcspvgccbsc:IPCSRectangle>
            </yiapcspvgbdc0:GroupComponent>
            <yiapcspvgccbsc:IPCSRectangle
                Rotation="-90"
                Visibility="Visible"
                Focusable="False"
                RenderTransform="6.12303176911189E-17,-1,1,6.12303176911189E-17,0,0"
                RenderTransformOrigin="0,0"
                ShapeHeight="47.083081891359669"
                ShapeWidth="48.502503886325542"
                Stroke="#00FFFFFF"
                StrokeThickness="1"
                Tag="Id=12"
                Fill="{rcsr:iPCSBrushExtension Style=Gradient_0003, Color1=#666666, Color2=#F2F2F2}"
                Canvas.Left="8.9152553756519"
                Canvas.Top="58.9831900149445"
                Panel.ZIndex="111"
                yiapcspvgbdc:ComponentProperties.Name="Rectangle_0016"
                yiapcspvgbdc:ComponentProperties.LayerID="Normal Drawing Layer 1"
                yiapcspvgccd:DebuggerProperties.SetDebugData="False">
                <yiapcspvggn:GenericNameComponent.GenericName>
                    <yiapcspvggn:GenericName />
                </yiapcspvggn:GenericNameComponent.GenericName>
            </yiapcspvgccbsc:IPCSRectangle>
            <yiapcspvgccbsc:IPCSSector
                Rotation="-90"
                Visibility="Visible"
                Focusable="False"
                RenderTransform="6.12303176911189E-17,-1,1,6.12303176911189E-17,0,0"
                RenderTransformOrigin="0,0"
                Stroke="#00FFFFFF"
                StrokeThickness="2"
                Tag="Id=13;R50300"
                EndPoint="25.7065405123475,0.181630249106887"
                Fill="{rcsr:iPCSBrushExtension Style=Gradient_0010, Color1=#666666, Color2=#F2F2F2}"
                IsLargeArc="False"
                RotationAngle="0"
                Size="24.9032111213367,9.90239420730979"
                StartPoint="0,9.89718682986419"
                SweepDirection="Counterclockwise"
                Canvas.Left="54.0975994962263"
                Canvas.Top="35.8743232287476"
                Panel.ZIndex="112"
                yiapcspvgbdc:ComponentProperties.Name="Fan_0003"
                yiapcspvgbdc:ComponentProperties.LayerID="Normal Drawing Layer 1">
                <yiapcspvggn:GenericNameComponent.GenericName>
                    <yiapcspvggn:GenericName />
                </yiapcspvggn:GenericNameComponent.GenericName>
            </yiapcspvgccbsc:IPCSSector>
            <yiapcspvgccbsc:IPCSSector
                Rotation="-90"
                Visibility="Visible"
                Focusable="False"
                RenderTransform="6.12303176911189E-17,-1,1,6.12303176911189E-17,0,0"
                RenderTransformOrigin="0,0"
                Stroke="#00FFFFFF"
                StrokeThickness="2"
                Tag="Id=14;R50300"
                EndPoint="23.1844635990099,9.89729442509355"
                Fill="{rcsr:iPCSBrushExtension Style=Gradient_0008, Color1=#666666, Color2=#F2F2F2}"
                IsLargeArc="False"
                RotationAngle="0"
                Size="23.9572790523102,9.90239420730978"
                StartPoint="0,0.18173784433627"
                SweepDirection="Counterclockwise"
                Canvas.Left="54.0974919009963"
                Canvas.Top="58.8205787117949"
                Panel.ZIndex="113"
                yiapcspvgbdc:ComponentProperties.Name="Fan_0004"
                yiapcspvgbdc:ComponentProperties.LayerID="Normal Drawing Layer 1">
                <yiapcspvggn:GenericNameComponent.GenericName>
                    <yiapcspvggn:GenericName />
                </yiapcspvggn:GenericNameComponent.GenericName>
            </yiapcspvgccbsc:IPCSSector>
            <yiapcspvgccbsc:IPCSRectangle
                Rotation="-90"
                Visibility="Visible"
                Focusable="False"
                RenderTransform="6.12303176911189E-17,-1,1,6.12303176911189E-17,0,0"
                RenderTransformOrigin="0,0"
                ShapeHeight="4.729689826083435"
                ShapeWidth="54.208680814128549"
                Stroke="#FF666666"
                StrokeThickness="1"
                Tag="Id=15"
                Fill="{rcsr:iPCSBrushExtension Style=Gradient_0004, Color1=#3F3F3F, Color2=#E5E5E5}"
                Canvas.Left="0"
                Canvas.Top="62.3117932228294"
                Panel.ZIndex="114"
                yiapcspvgbdc:ComponentProperties.Name="Rectangle_0017"
                yiapcspvgbdc:ComponentProperties.LayerID="Normal Drawing Layer 1"
                yiapcspvgccd:DebuggerProperties.SetDebugData="False">
                <yiapcspvggn:GenericNameComponent.GenericName>
                    <yiapcspvggn:GenericName />
                </yiapcspvggn:GenericNameComponent.GenericName>
            </yiapcspvgccbsc:IPCSRectangle>
        </yiapcspvgbdc0:GroupComponent>
    </yiapcspvgbdc0:GroupComponent>'''  # Pega el XML aquí

components = parse_xml(xml_string)


def apply_transform(transform, point):
    # Aplica la transformación a un punto
    return transform.transform_point(point)

def calculate_global_positions(components):
    results = []

    for component in components:
        left = component['left']
        top = component['top']
        width = component['width']
        height = component['height']
        transform = component['render_transform']

        # Posición de referencia en el componente
        center = np.array([width / 2.0, height / 2.0])

        # Aplicar transformación a la posición del centro del componente
        global_center = apply_transform(transform, center) + np.array([left, top])
        results.append({
            'name': component['name'],
            'global_center': global_center.tolist()
        })

        # Repetir para los hijos
        for child in component['children']:
            child_left = child['left']
            child_top = child['top']
            child_width = child['width']
            child_height = child['height']
            child_transform = child['render_transform']

            # Posición de referencia en el componente hijo
            child_center = np.array([child_width / 2.0, child_height / 2.0])

            # Posición global del componente hijo
            global_child_center = apply_transform(child_transform, child_center) + np.array([child_left, child_top])
            results.append({
                'name': child['name'],
                'global_center': global_child_center.tolist()
            })

    return results

# Calcular posiciones globales
positions = calculate_global_positions(components)

# Mostrar resultados
for pos in positions:
    print(f"Component {pos['name']} has global center at {pos['global_center']}")

