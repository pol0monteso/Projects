import uuid

"""class IISCondition:
    def __init__(self, Expression, ColorChangeType, ColorC, PropertyNameCC, PropertyNameBLK, ColorB, IsContinuous, BlinkingType, ReplaceText, Text):
        self.Expression = Expression
        self.ColorChangeType = ColorChangeType
        self.ColorB1 = ColorB
        self.ColorC = ColorC
        self.PropertyNameCC = PropertyNameCC
        self.PropertyNameBLK = PropertyNameBLK
        self.IsContinuous = IsContinuous
        self.BlinkingType = BlinkingType
        self.ReplaceText = ReplaceText
        self.Text = Text

    @classmethod
    def default(cls):
        return cls(Expression="", ColorChangeType="", ColorC="", ColorB="", PropertyNameCC="", PropertyNameBLK="",
                   IsContinuous=False, BlinkingType="False", ReplaceText="False", Text="")"""

class IISCondition:
    def __init__(self, Expression, ColorChangeType1, ColorC1, PropertyNameCC1, PropertyNameBLK1, ColorB1, IsContinuous, BlinkingType1, ReplaceText, Text,
                 ColorChangeType2, ColorC2, PropertyNameCC2, PropertyNameBLK2, ColorB2, BlinkingType2):
        self.Expression = Expression
        self.ColorChangeType1 = ColorChangeType1
        self.ColorB1 = ColorB1
        self.ColorC1 = ColorC1
        self.PropertyNameCC1 = PropertyNameCC1
        self.PropertyNameBLK1 = PropertyNameBLK1
        self.IsContinuous = IsContinuous
        self.BlinkingType1 = BlinkingType1
        self.ReplaceText = ReplaceText
        self.Text = Text
        self.ColorChangeType2 = ColorChangeType2
        self.ColorB2 = ColorB2
        self.ColorC2 = ColorC2
        self.PropertyNameCC2 = PropertyNameCC2
        self.PropertyNameBLK2 = PropertyNameBLK2
        self.BlinkingType2 = BlinkingType2

    @classmethod
    def default(cls):
        return cls(Expression="", ColorChangeType1="", ColorC1="", ColorB1="", PropertyNameCC1="", PropertyNameBLK1="",
                   IsContinuous=False, BlinkingType1="False", ReplaceText="False", Text="",ColorChangeType2="", ColorC2="",
                   ColorB2="", PropertyNameCC2="", PropertyNameBLK2="", BlinkingType2="")
class Button:
    def __init__(self, Background, Text, FontFamily, FontWeight, FontSize, Height, Width, RenderTransform,
                 RenderTransformOrigin, ShapeName, Screen, X, Y, Window, ZIndex, CommandData, FunctionType, DataTag,
                 Binding, IISCondition):
        self.Background = Background
        self.Text = Text
        self.FontFamily = FontFamily
        self.FontWeight = FontWeight
        self.FontSize = FontSize
        self.Height = Height
        self.Width = Width
        self.RenderTransform = RenderTransform
        self.ShapeName = ShapeName
        self.X = X
        self.Y = Y
        self.Screen = Screen
        self.RenderTransformOrigin = RenderTransformOrigin
        self.Window = Window
        self.ZIndex = ZIndex
        self.CommandData = CommandData
        self.DataTag = DataTag
        self.FunctionType = FunctionType
        self.Binding = Binding
        self.IISCondition = IISCondition


    @classmethod
    def default(cls):
        return cls(Background="Gray", ShapeName="", Height="100", Width="100", Screen="", RenderTransformOrigin="",
                   RenderTransform="", X="0", Y="0", Text="", FontWeight="", FontSize="", FontFamily="", Window="",
                   ZIndex=1000, FunctionType="", DataTag="", CommandData="", Binding=[], IISCondition=[])


class Tag:
    def __init__(self, ID, Name, HysysVar, NumDecimals, UnitID, UnitEng, HysysVarUnit, DefaultValue):
        self.ID = ID
        self.Name = Name
        self.HysysVar = HysysVar
        self.NumDecimals = NumDecimals
        self.UnitID = UnitID
        self.UnitEng = UnitEng
        self.HysysVarUnit = HysysVarUnit
        self.DefaultValue = DefaultValue
    @classmethod
    def default(cls):
        return cls(ID=str(uuid.uuid4()), Name="", HysysVar="", NumDecimals=3, UnitID=None, UnitEng=None, HysysVarUnit="", DefaultValue=0)


class Touch:
    def __init__(self, Stroke, Height, Width, Shapename, Screen, RenderTransform, RenderTransformOrigin, ZIndex, X, Y, Window, FunctionType, DataTag, CommandData, Faceplate):
        self.Stroke = Stroke
        self.Height = Height
        self.Width = Width
        self.ShapeName = Shapename
        self.Screen = Screen
        self.RenderTransform = RenderTransform
        self.ZIndex = ZIndex
        self.X = X
        self.Y = Y
        self.Window = Window
        self.FunctionType = FunctionType
        self.DataTag = DataTag
        self.CommandData = CommandData
        self.Faceplate = Faceplate
    @classmethod
    def default(cls):
        return cls(Stroke="White", Shapename="", Height="100", Width="100", Screen="", RenderTransformOrigin="",
                   RenderTransform="", ZIndex=1000, X="0", Y="0", Window="", FunctionType="", DataTag="", CommandData="",
                   Faceplate="")


class Alarm:
    def __init__(self, ID, Name, Tag, Threshold, Condition, UnitEng, Screen, Priority):
        self.ID = ID
        self.Name = Name
        self.Tag = Tag
        self.Threshold = Threshold
        self.Condition = Condition
        self.UnitEng = UnitEng
        self.Screen = Screen
        self.Priority = Priority

    @classmethod
    def default(cls):
        return cls(ID=str(uuid.uuid4()), Tag="", Threshold="0.5", Condition="100", Screen="", UnitEng=None, Name="", Priority="110")


class Binding:
    def __init__(self, GenericName, Value):
        self.GenericName = GenericName
        self.Value = Value

    @classmethod
    def default(cls):
        return cls(GenericName="", Value="")


class Level:
    def __init__(self, Width, Height, X, Y, ShapeName, Fill, Stroke, StrokeThickness, LevelTag, IISCondition, Binding,
                 ZIndex, LevelFill1, LevelValue1, LevelValue2, Orientation, dataChar, binding_dic, RenderTransform, RenderTransformOrigin):
        self.Width = Width
        self.Height = Height
        self.X = X
        self.Y = Y
        self.ShapeName = ShapeName
        self.Fill = Fill
        self.Stroke = Stroke
        self.StrokeThickness = StrokeThickness
        self.LevelTag = LevelTag
        self.IISCondition = IISCondition
        self.Binding = Binding
        self.ZIndex = ZIndex
        self.LevelFill1 = LevelFill1
        self.LevelValue1 = LevelValue1
        self.LevelValue2 = LevelValue2
        self.Orientation = Orientation
        self.dataChar = dataChar
        self.binding_dic = binding_dic
        self.RenderTransform = RenderTransform
        self.RenderTransformOrigin = RenderTransformOrigin

    @classmethod
    def default(cls):
        return cls(Width=100, Height=100, X=0, Y=0, ShapeName="Rectangle", Fill="Transparent", Stroke="Black",
                   StrokeThickness=1, LevelTag="", IISCondition=[], Binding=[], ZIndex=0, LevelFill1="", Orientation="",
                   LevelValue1="", LevelValue2="", dataChar=None, binding_dic={}, RenderTransform="1,0,0,1,0,0", RenderTransformOrigin="")

class Rectangle:
    def __init__(self, Width, Height, X, Y, ShapeName, Fill, Stroke, StrokeThickness, Name, Tag,
                 RenderTransform, RenderTransformOrigin, IISCondition, Binding, Rotation, ZIndexGroup, ZIndex,
                 OffsetX, TransformFromX, TransformToX, TagValueX,
                 OffsetY, TransformFromY, TransformToY, TagValueY, PropertyX, PropertyY, DataLinkInfo):
        self.Width = Width
        self.Height = Height
        self.X = X
        self.Y = Y
        self.ShapeName = ShapeName
        self.Fill = Fill
        self.Stroke = Stroke
        self.StrokeThickness = StrokeThickness
        self.Name = Name
        self.Tag = Tag
        self.RenderTransform = RenderTransform
        self.RenderTransformOrigin = RenderTransformOrigin
        self.IISCondition = IISCondition
        self.Binding = Binding
        self.Rotation = Rotation
        self.ZIndex = ZIndex
        self.ZIndexGroup = ZIndexGroup
        self.DataLinkInfo = DataLinkInfo

    @classmethod
    def default(cls):
        return cls(
            Width=100, Height=100, X=0, Y=0, ShapeName="Rectangle", Fill="White", Stroke="Black",
            StrokeThickness=1, Name="", Tag=-1, RenderTransform="", RenderTransformOrigin="",
            IISCondition=[], Binding=[], Rotation=0, ZIndex=0, ZIndexGroup=0,
            OffsetX=None, TransformFromX=None, TransformToX=None, TagValueX=None,
            OffsetY=None, TransformFromY=None, TransformToY=None, TagValueY=None,
            PropertyX=None, PropertyY=None, DataLinkInfo=[]
        )


class Text:
    def __init__(self, ShapeName, X, Y, Width, Height, Background, Foreground, Text, FontSize, FontFamily, TextAlign,
                 IISCondition, Binding, Rotation, ZIndex, ZIndexGroup, ScaleX, ScaleY, RenderTransform, RenderTransformOrigin, FontWeight):
        self.ShapeName = ShapeName
        self.X = X
        self.Y = Y
        self.Width = Width
        self.Height = Height
        self.Background = Background
        self.Foreground = Foreground
        self.Text = Text
        self.FontSize = FontSize
        self.FontFamily = FontFamily
        self.TextAlign = TextAlign
        self.IISCondition = IISCondition
        self.Binding = Binding
        self.Rotation = Rotation
        self.ZIndex = ZIndex
        self.ZIndexGroup = ZIndexGroup
        self.ScaleX = ScaleX
        self.ScaleY = ScaleY
        self.RenderTransform = RenderTransform
        self.RenderTransformOrigin = RenderTransformOrigin
        self.FontWeight = FontWeight

    @classmethod
    def default(cls):
        return cls(ShapeName="", X=0, Y=0, Width=300, Height=300, Background="#00FF0000", Foreground="Black",
                   Text="Label",
                   FontSize="12", FontFamily="Segoe UI", TextAlign="Left", IISCondition=[], Binding=[], Rotation=0,
                   ZIndex=0, ZIndexGroup=0, ScaleX=1, ScaleY=1, RenderTransform="", RenderTransformOrigin="", FontWeight="Normal")


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Sector:
    def __init__(self, Width, Height, X, Y, ShapeName, Fill, Stroke, StrokeThickness, Name, Tag,
                 RenderTransform, RenderTransformOrigin, IISCondition, Binding, Rotation, StartAngle, EndAngle, ZIndex,
                 ZIndexGroup):
        self.Width = Width
        self.Height = Height
        self.X = X
        self.Y = Y
        self.ShapeName = ShapeName
        self.Fill = Fill
        self.Stroke = Stroke
        self.StrokeThickness = StrokeThickness
        self.Name = Name
        self.Tag = Tag
        self.RenderTransform = RenderTransform
        self.RenderTransformOrigin = RenderTransformOrigin
        self.IISCondition = IISCondition
        self.Binding = Binding
        self.Rotation = Rotation
        self.StartAngle = StartAngle
        self.EndAngle = EndAngle
        self.ZIndex = ZIndex
        self.ZIndexGroup = ZIndexGroup

    @classmethod
    def default(cls):
        return cls(Width=100, Height=100, X=0, Y=0, ShapeName="Rectangle", Fill="White", Stroke="Black",
                   StrokeThickness=1, Name="", Tag=-1, RenderTransform="", RenderTransformOrigin="",
                   IISCondition=[], Binding=[], Rotation=0, StartAngle="", EndAngle="", ZIndex=0, ZIndexGroup=0)


class Arc:
    def __init__(self, Width, Height, X, Y, ShapeName, Fill, Stroke, StrokeThickness, Name, Tag,
                 RenderTransform, RenderTransformOrigin, IISCondition, Binding, Rotation, StartAngle, EndAngle, ZIndex,
                 ZIndexGroup):
        self.Width = Width
        self.Height = Height
        self.X = X
        self.Y = Y
        self.ShapeName = ShapeName
        self.Fill = Fill
        self.Stroke = Stroke
        self.StrokeThickness = StrokeThickness
        self.Name = Name
        self.Tag = Tag
        self.RenderTransform = RenderTransform
        self.RenderTransformOrigin = RenderTransformOrigin
        self.IISCondition = IISCondition
        self.Binding = Binding
        self.Rotation = Rotation
        self.StartAngle = StartAngle
        self.EndAngle = EndAngle
        self.ZIndex = ZIndex
        self.ZIndexGroup = ZIndexGroup

    @classmethod
    def default(cls):
        return cls(Width=100, Height=100, X=0, Y=0, ShapeName="Rectangle", Fill="White", Stroke="Black",
                   StrokeThickness=1, Name="", Tag=-1, RenderTransform="", RenderTransformOrigin="",
                   IISCondition=[], Binding=[], Rotation=0, StartAngle="", EndAngle="", ZIndex=0, ZIndexGroup=0)


class PolyLine:
    def __init__(self, Width, Height, X, Y, ShapeName, Fill, Stroke, StrokeThickness, Name, Tag,
                 RenderTransform, RenderTransformOrigin, IISCondition, Binding, Points, Rotation, ZIndex, ZIndexGroup):
        self.Width = Width
        self.Height = Height
        self.X = X
        self.Y = Y
        self.ShapeName = ShapeName
        self.Fill = Fill
        self.Stroke = Stroke
        self.StrokeThickness = StrokeThickness
        self.Name = Name
        self.Tag = Tag
        self.RenderTransform = RenderTransform
        self.RenderTransformOrigin = RenderTransformOrigin
        self.IISCondition = IISCondition
        self.Binding = Binding
        self.Points = Points
        self.Rotation = Rotation
        self.ZIndex = ZIndex
        self.ZIndexGroup = ZIndexGroup

    @classmethod
    def default(cls):
        return cls(Width=100, Height=100, X=0, Y=0, ShapeName="Line", Fill="White", Stroke="Black",
                   StrokeThickness=1, Name="", Tag=-1, RenderTransform="", RenderTransformOrigin="",
                   IISCondition=[], Binding=[], Points=[], Rotation=0, ZIndex=0, ZIndexGroup=0)


class Ellipse:
    def __init__(self, Width, Height, X, Y, ShapeName, Fill, Stroke, StrokeThickness, Name, Tag,
                 RenderTransform, RenderTransformOrigin, IISCondition, Binding, Points, Rotation, ZIndex, ZIndexGroup):
        self.Width = Width
        self.Height = Height
        self.X = X
        self.Y = Y
        self.ShapeName = ShapeName
        self.Fill = Fill
        self.Stroke = Stroke
        self.StrokeThickness = StrokeThickness
        self.Name = Name
        self.Tag = Tag
        self.RenderTransform = RenderTransform
        self.RenderTransformOrigin = RenderTransformOrigin
        self.IISCondition = IISCondition
        self.Binding = Binding
        self.Points = Points
        self.Rotation = Rotation
        self.ZIndex = ZIndex
        self.ZIndexGroup = ZIndexGroup


    @classmethod
    def default(cls):
        return cls(Width=100, Height=100, X=0, Y=0, ShapeName="elip_", Fill="White", Stroke="Black",
                   StrokeThickness=1, Name="", Tag=-1, RenderTransform="", RenderTransformOrigin="",
                   IISCondition=[], Binding=[], Points=[], Rotation=0, ZIndex=0, ZIndexGroup=0)


class DataChar:
    def __init__(self, GenericName, Value):
        self.GenericName = GenericName
        self.Value = Value

    @classmethod
    def default(cls):
        return cls(GenericName="", Value="")

class Polygon:
    def __init__(self, Width, Height, X, Y, ShapeName, Fill, Stroke, StrokeThickness, Name, Tag,
                 RenderTransform, RenderTransformOrigin, IISCondition, Binding, Points, Rotation, ZIndex, ZIndexGroup,
                 DataLinkInfo):
        self.Width = Width
        self.Height = Height
        self.X = X
        self.Y = Y
        self.ShapeName = ShapeName
        self.Fill = Fill
        self.Stroke = Stroke
        self.StrokeThickness = StrokeThickness
        self.Name = Name
        self.Tag = Tag
        self.RenderTransform = RenderTransform
        self.RenderTransformOrigin = RenderTransformOrigin
        self.IISCondition = IISCondition
        self.Binding = Binding
        self.Points = Points
        self.Rotation = Rotation
        self.ZIndex = ZIndex
        self.ZIndexGroup = ZIndexGroup
        self.DataLinkInfo = DataLinkInfo

    @classmethod
    def default(cls):
        return cls(Width=100, Height=100, X=0, Y=0, ShapeName="poly", Fill="White", Stroke="Black",
                   StrokeThickness=1, Name="", Tag=-1, RenderTransform="", RenderTransformOrigin="",
                   IISCondition=[], Binding=[], Points=[], Rotation=0, ZIndex=0, ZIndexGroup=0, DataLinkInfo=[])

    class Tag:
        def __init__(self, ID, Name, HysysVar, NumDecimals):
            self.ID = ID
            self.Name = Name
            self.HysysVar = HysysVar
            self.NumDecimals = NumDecimals

        @classmethod
        def default(cls):
            return cls(ID=str(uuid.uuid4()), Name="", HysysVar="", NumDecimals=3)


class ProcessData:
    def __init__(self, ShapeName, X, Y, Width, Height, Background, Foreground, Text, FontSize, FontFamily, TextAlign,
                 IISCondition, Binding, Rotation, ZIndex, dataChar, binding_dic, Tag, ZIndexGroup, isVisibleUnits,
                 RenderTransform, RenderTransformOrigin):
        self.ShapeName = ShapeName
        self.X = X
        self.Y = Y
        self.Width = Width
        self.Height = Height
        self.Background = Background
        self.Foreground = Foreground
        self.Text = Text
        self.FontSize = FontSize
        self.FontFamily = FontFamily
        self.TextAlign = TextAlign
        self.IISCondition = IISCondition
        self.Binding = Binding
        self.Rotation = Rotation
        self.ZIndex = ZIndex
        self.dataChar = dataChar
        self.binding_dic = binding_dic
        self.Tag = Tag
        self.ZIndexGroup = ZIndexGroup
        self.isVisibleUnits = isVisibleUnits
        self.RenderTransform = RenderTransform
        self.RenderTransformOrigin = RenderTransformOrigin

    @classmethod
    def default(cls):
        return cls(ShapeName="", X=0, Y=0, Width=300, Height=300, Background="#00FF0000", Foreground="Black",
                   Text="???????",
                   FontSize="12", FontFamily="Segoe UI", TextAlign="Left", IISCondition=[], Binding=[], Rotation=0,
                   ZIndex=0, dataChar=None, binding_dic={}, Tag="", ZIndexGroup=0, isVisibleUnits=False, RenderTransform="1,0,0,1,0,0",
                   RenderTransformOrigin="")

class Line:
    def __init__(self, Width, Height, X, Y, ShapeName, Fill, Stroke, StrokeThickness, Name, Tag,
                 RenderTransform, RenderTransformOrigin, IISCondition, Binding, Points, Rotation, LineStyle,
                 arrowStart, arrowEnd, ZIndex, ZIndexGroup ):
        self.Width = Width
        self.Height = Height
        self.X = X
        self.Y = Y
        self.ShapeName = ShapeName
        self.Fill = Fill
        self.Stroke = Stroke
        self.StrokeThickness = StrokeThickness
        self.Name = Name
        self.Tag = Tag
        self.RenderTransform = RenderTransform
        self.RenderTransformOrigin = RenderTransformOrigin
        self.IISCondition = IISCondition
        self.Binding = Binding
        self.Points = Points
        self.Rotation = Rotation
        self.LineStyle = LineStyle
        self.arrowStart = arrowStart
        self.arrowEnd = arrowEnd
        self.ZIndex = ZIndex
        self.ZIndexGroup = ZIndexGroup


    @classmethod
    def default(cls):
        return cls(Width=100, Height=100, X=0, Y=0, ShapeName="Line", Fill="White", Stroke="Black",
                   StrokeThickness=1, Name="", Tag=-1, RenderTransform="", RenderTransformOrigin="",
                   IISCondition=[], Binding=[], Points=[], Rotation=0, LineStyle="LINE", arrowEnd=None, arrowStart=None,
                   ZIndex=0, ZIndexGroup=0)


class Arrow:
    def __init__(self, Width, Height, X, Y, ShapeName, Fill, Stroke, StrokeThickness, Name, Tag,
                 RenderTransform, RenderTransformOrigin, IISCondition, Binding, Points, Rotation, ArrowStart, ArrowEnd,
                 isVisible, ZIndex, ZIndexGroup):
        self.Width = Width
        self.Height = Height
        self.X = X
        self.Y = Y
        self.ShapeName = ShapeName
        self.Fill = Fill
        self.Stroke = Stroke
        self.StrokeThickness = StrokeThickness
        self.Name = Name
        self.Tag = Tag
        self.RenderTransform = RenderTransform
        self.RenderTransformOrigin = RenderTransformOrigin
        self.IISCondition = IISCondition
        self.Binding = Binding
        self.Points = Points
        self.Rotation = Rotation
        self.ArrowStart = ArrowStart
        self.ArrowEnd = ArrowEnd
        self.isVisible = isVisible
        self.ZIndex = ZIndex
        self.ZIndexGroup = ZIndexGroup

    @classmethod
    def default(cls):
        return cls(Width=20, Height=20, X=0, Y=0, ShapeName="arrow", Fill="White", Stroke="Black",
                   StrokeThickness=1, Name="", Tag=-1, RenderTransform="", RenderTransformOrigin="",
                   IISCondition=[], Binding=[], Points=[], Rotation=0, ArrowEnd=False, ArrowStart=False, isVisible=False,
                   ZIndex=0, ZIndexGroup=0)
