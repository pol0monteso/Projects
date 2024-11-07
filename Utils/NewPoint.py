from Classes.LogicClass import *

points_str = "0,81.2 138,24 138,0"

points = [XPoint(*map(float, pair.split(','))) for pair in points_str.split()]


def getNewPoint(points):
    b_point = XPoint(*points[1])
    a_point = XPoint(*points[0])
    y_point = XPoint(*points[-2])
    z_point = XPoint(*points[-1])
    vector_BA = a_point - b_point
    vector_YZ = z_point - y_point

    # Calcular la distancia entre B y A
    dist_BA = b_point.distance_to(a_point)
    dist_YZ = z_point.distance_to(y_point)

    # Nueva longitud de la recta
    nueva_longitud_BA = dist_BA - 10
    nueva_longitud_YZ = dist_YZ - 10
    # Normalizar el vector dirección

    vector_unitario_YZ = vector_YZ.normalize()
    vector_unitario_BA = vector_BA.normalize()

    # Calcular el nuevo punto A' que está a 15 píxeles más corto que A
    A_prime = b_point + vector_unitario_BA * nueva_longitud_BA
    Z_prime = y_point + vector_unitario_YZ * nueva_longitud_YZ
    return A_prime, Z_prime
