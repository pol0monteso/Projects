from enum import Enum


class ReportLine:
    def __init__(self, Id, ObjectName, ObjectType, Priority, Description):
        self.Id = Id
        self.ObjectName = ObjectName
        self.ObjectType = ObjectType
        self.Priority = Priority
        self.Description = Description

    @classmethod
    def default(cls):
        return cls(Id=0, ObjectName="", ObjectType=None, Priority=None, Description=0)


class Priority(Enum):
    LOW = "#008000"
    MEDIUM = "#FFFF00"
    HIGH = "#FF0000"


LegendID = {
    1: 'Color Attribute for an object property is defined as "Null" in Yokogawa. Thus, for emulation, the object property is defined as  "Transparent".',
    2: "Image added to The screen",
    3: "Non-emulated Yokogawa object. IIS does not have this object to add to the screen."
}



def create_tuple_report(object, id):
    report = ReportLine.default()
