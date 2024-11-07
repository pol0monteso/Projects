import math
from enum import Enum


class XPoint:
    def __init__(self, x=0.0, y=0.0):
        self.X = x
        self.Y = y

    def __sub__(self, other):
        return XPoint(self.X - other.X, self.Y - other.Y)

    def __add__(self, other):
        return XPoint(self.X + other.X, self.Y + other.Y)

    def __mul__(self, scalar):
        return XPoint(self.X * scalar, self.Y * scalar)

    def distance_to(self, other):
        return math.sqrt((self.X - other.X) ** 2 + (self.Y - other.Y) ** 2)

    def normalize(self):
        dist = self.distance_to(XPoint(0, 0))
        return XPoint(self.X / dist, self.Y / dist) if dist != 0 else XPoint(0, 0)

    def __repr__(self):
        return f"Point({self.X}, {self.Y})"


class Size:
    def __init__(self, width=0.0, height=0.0):
        self.Width = width
        self.Height = height


class SweepDirection(Enum):
    Clockwise = 0
    Counterclockwise = 1


class EqualityResult(Enum):
    Equal = 0
    GreaterThan = 1
    LessThan = -1


class Constants:
    PrecisionErrorMargin = 1E-07  # Precision error margin for comparison


class PrecisionHelper:
    @staticmethod
    def IsFirstNumEqualToSecondNum(first_number, second_number):
        return PrecisionHelper.IsFirstNumEqualToSecondNumWithPrecision(first_number, second_number,
                                                                       Constants.PrecisionErrorMargin)

    @staticmethod
    def IsFirstNumEqualToSecondNumWithPrecision(first_number, second_number, precision_margin):
        num = first_number - second_number
        if math.fabs(num) >= precision_margin:
            return EqualityResult.GreaterThan if num > 0.0 else EqualityResult.LessThan
        else:
            return EqualityResult.Equal


class PathGeometryHelper:
    @staticmethod
    def TransformPoint(base_point, point, rotate_angle, translate_point):
        cos_angle = math.cos(rotate_angle)
        sin_angle = math.sin(rotate_angle)

        transformed_x = (point.X - base_point.X) * cos_angle + (
                point.Y - base_point.Y) * sin_angle + base_point.X + translate_point.X
        transformed_y = (point.Y - base_point.Y) * cos_angle - (
                point.X - base_point.X) * sin_angle + base_point.Y + translate_point.Y

        return XPoint(transformed_x, transformed_y)

    @staticmethod
    def GetArcSizeRoot(point, rotate_angle, size):
        point1 = PathGeometryHelper.TransformPoint(XPoint(), point, rotate_angle * math.pi / 180.0, XPoint())
        return size.Width * size.Height * (size.Width * size.Height) - size.Width * point1.Y * (
                size.Width * point1.Y) - size.Height * point1.X * (size.Height * point1.X)


def calcular_angulo(punto_a, punto_b):
    # Extraemos las coordenadas x e y de los puntos usando los métodos x y y de Point
    x_a, y_a = punto_a.X, punto_a.Y
    x_b, y_b = punto_b.X, punto_b.Y

    # Calculamos la diferencia en coordenadas respecto al punto B (origen)
    dx = x_a - x_b
    dy = y_b - y_a  # En canvas, invertimos la dirección de dy respecto a la geometría estándar

    # Usamos la función arcotangente para obtener el ángulo en radianes
    angulo_rad = math.atan2(dy, dx)

    # Convertimos el ángulo a grados
    angulo_grados = math.degrees(angulo_rad)

    # Ajustamos el ángulo para que esté entre 0 y 360 grados
    if angulo_grados < 0:
        angulo_grados += 360

    return angulo_grados


def redondear_angulo(angulo):
    # Definir los ángulos cercanos que queremos redondear
    thresholds = [0, 90, 180, 360, 270]

    # Comprobar si el ángulo está cerca de alguno de los thresholds
    for threshold in thresholds:
        if abs(angulo - threshold) < 5:  # Ajusta el valor de 5 según qué tan cerca quieres considerar
            return round(threshold)  # Redondear y devolver el ángulo entero

    return angulo  # Devolver el ángulo sin cambios si no está cerca de ningún threshold


def GetArcCenterPoint(start_point, end_point, rotate_angle, size, is_large_arc, sweep_direction):
    center_point = XPoint()

    point1 = XPoint((start_point.X - end_point.X) / 2.0, (start_point.Y - end_point.Y) / 2.0)
    first_number = PathGeometryHelper.GetArcSizeRoot(point1, rotate_angle, size)

    if PrecisionHelper.IsFirstNumEqualToSecondNum(first_number, 0.0) == EqualityResult.Equal:
        first_number = 0.0

    if first_number < 0.0:
        return None

    point2 = PathGeometryHelper.TransformPoint(XPoint(), point1, rotate_angle * math.pi / 180.0, XPoint())

    num1 = size.Width * point2.Y * (size.Width * point2.Y) + size.Height * point2.X * (size.Height * point2.X)
    num2 = math.sqrt(first_number / num1)

    point3 = XPoint(num2 * size.Width * point2.Y / size.Height, -1.0 * num2 * size.Height * point2.X / size.Width)

    if (is_large_arc and sweep_direction == SweepDirection.Clockwise) or (
            not is_large_arc and sweep_direction == SweepDirection.Counterclockwise):
        point3 = XPoint(-1.0 * point3.X, -1.0 * point3.Y)

    point4 = PathGeometryHelper.TransformPoint(XPoint(), point3, -1.0 * (rotate_angle * math.pi / 180.0), XPoint())
    point5 = XPoint((start_point.X + end_point.X) / 2.0, (start_point.Y + end_point.Y) / 2.0)

    center_point = XPoint(point4.X + point5.X, point4.Y + point5.Y)
    angle_start_deg = calcular_angulo(start_point, center_point)
    angle_end_deg = calcular_angulo(end_point, center_point)

    angle_start_deg = redondear_angulo(angle_start_deg)
    angle_end_deg = redondear_angulo(angle_end_deg)

    # Calcular los ángulos con respecto al centro del arco
    """angle_start = math.atan2(start_point.Y - center_point.Y, start_point.X - center_point.X)
    angle_end = math.atan2(end_point.Y - center_point.Y, end_point.X - center_point.X)

    # Convertir a grados
    angle_start_deg = math.degrees(angle_start)
    angle_end_deg = math.degrees(angle_end)"""

    return center_point, angle_start_deg, angle_end_deg


# Ejemplo de uso con los puntos proporcionados y ángulo de rotación específico:
if __name__ == "__main__":
    """start_point = Point(30,13)
    end_point = Point(0,13)
    rotate_angle = 0  # Ángulo de rotación en grados
    size = Size(15,13)  # Tamaño de la elipse (por ejemplo, el radio en ambas direcciones)"""
    start_point = XPoint(48.0869564925201, 0.00138186952171324)
    end_point = XPoint(0, 21.7776608936385)
    rotate_angle = 0  # Ángulo de rotación en grados
    size = Size(47.5753931255783, 22.294761858027)  # Tamaño de la elipse (por ejemplo, el radio en ambas direcciones)
    is_large_arc = False
    sweep_direction = SweepDirection.Counterclockwise

    result = GetArcCenterPoint(start_point, end_point, rotate_angle, size, is_large_arc, sweep_direction)

    if result is not None:
        center_point, angle_start_deg, angle_end_deg = result
        print(f"Center Point: ({center_point.X}, {center_point.Y})")
        print(f"Angle of start_point with x-axis: {angle_start_deg} degrees")
        print(f"Angle of end_point with x-axis: {angle_end_deg} degrees")
    else:
        print("No se pudo calcular el centro del arco.")
