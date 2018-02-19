#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinas.py
------------

Ejemplo de las n_reinas con búsquedas locales

"""

__author__ = 'juliowaissman'


import blocales
from random import shuffle
from random import sample
from itertools import combinations

from time import time
from math import sqrt
from math import log

class ProblemaNreinas(blocales.Problema):
    """
    Las N reinas en forma de búsqueda local se inicializa como

    entorno = ProblemaNreinas(n) donde n es el número de reinas a colocar

    Por default son las clásicas 8 reinas.

    """
    def __init__(self, n=8):
        self.n = n

    def estado_aleatorio(self):
        estado = list(range(self.n))
        shuffle(estado)
        return tuple(estado)

    @staticmethod
    def swap(x, i, j):
        """
        Intercambia los elemento i y j de la lista x

        """
        if not isinstance(x, type([1, 2])):
            raise TypeError("Este método solo se puede hacer con listas")
        x[i], x[j] = x[j], x[i]

    def vecinos(self, estado):
        """
        Generador vecinos de un estado, todas las 2 permutaciones

        @param estado: una tupla que describe un estado.

        @return: un generador de estados vecinos.

        """
        x = list(estado)
        for i, j in combinations(range(self.n), 2):
            self.swap(x, i, j)
            yield tuple(x)
            self.swap(x, i, j)

    def vecino_aleatorio(self, estado):
        """
        Genera un vecino de un estado intercambiando dos posiciones
        en forma aleatoria.

        @param estado: Una tupla que describe un estado

        @return: Una tupla con un estado vecino.

        """
        vecino = list(estado)
        i, j = sample(range(self.n), 2)
        self.swap(vecino, i, j)
        return tuple(vecino)

    def costo(self, estado):
        """
        Calcula el costo de un estado por el número de conflictos entre reinas

        @param estado: Una tupla que describe un estado

        @return: Un valor numérico, mientras más pequeño, mejor es el estado.

        """
        return sum((1 for (i, j) in combinations(range(self.n), 2)
                    if abs(estado[i] - estado[j]) == abs(i - j)))


def prueba_descenso_colinas(problema=ProblemaNreinas(8), repeticiones=10):
    """ Prueba el algoritmo de descenso de colinas con n repeticiones """

    print("\n\n" + "intento".center(10) +
          "estado".center(60) + "costo".center(10))
    for intento in range(repeticiones):
        solucion = blocales.descenso_colinas(problema)
        print(str(intento).center(10) +
              str(solucion).center(60) +
              str(problema.costo(solucion)).center(10))


def prueba_temple_simulado(problema=ProblemaNreinas(8)):
    """ Prueba el algoritmo de temple simulado """

    solucion = blocales.temple_simulado(problema)
    print("\n\nTemple simulado con calendarización To/(1 + i).")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)


if __name__ == "__main__":

    prueba_descenso_colinas(ProblemaNreinas(32), 10)
    prueba_temple_simulado(ProblemaNreinas(32))

    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    #
    # ¿Cual es el máximo número de reinas que se puede resolver en
    # tiempo aceptable con el método de 10 reinicios aleatorios?
    #
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan? ¿Cual es el mejor ajuste para el temple simulado
    # y hasta cuantas reinas puede resolver en un tiempo aceptable?
    #
    # En general para obtener mejores resultados del temple simulado,
    # es necesario probar diferentes metdos de
    # calendarización, prueba al menos otros dos métodos sencillos de
    # calendarización y ajusta los parámetros para que funcionen de la
    # mejor manera
    #
    # Escribe aqui tus conclusiones
    #
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #

"""
Descenso de colinas:
Asumiendo que maximo es aceptable esperar un minuto para encontrar una
solucion, entonces entre 50 y 60 reinas son aceptables en la computadora
donde corro los algoritmos, ya que cada corrida del descenso de colinas
dura al rededor de 6 segundos.


Otros calendarizadores:
Obtienen la misma temperatura inicial que el calendarizador originalmente propuesto, los cambios son solo de algunas operaciones en el generador.

Ejemplos:
1.- calendarizador = (T_ini/i for i in range(1, int(1e10), 2))
Este calendarizador es practicamente el mismo que el original pero avanza la variable i dos unidades en lugar de solo una, lo cual disminuye la temperatura inicial mas rapidamente.
En las pruebas que realize en realidad no se notan cambios con el original.

2.- calendarizador = (T_ini/i for i in range(1, int(1e10), 10))
Similar al anterior pero avanza 10 unidades. De igual manera no se notan cambios con el original.

3.- calendarizador = (T_ini/sqrt(i) for i in range(1, int(1e10)))
Saca raiz cuadrada a la variable i lo cual hace que la temperatura se enfrie mas lentamente. Con esta hubo cambios en el tiempo haciendolo mas lento comparado con el original.

4.- calendarizador = (T_ini/(log(i)+1) for i in range(1, int(1e10)))
Saca logaritmo en lugar de raiz cuadrada y lo enfria aun mas lento. El hecho de que se enfrie mas lento afecta gravemente al tiempo, haciendolo varias veces mas grande e innaceptable para reinas mayores a 32.

5.- calendarizador = (T_ini*0.995**i for i in range(1, int(1e10)))
En lugar de dividir entre la variable i, se eleva un porcentaje a la i y se multiplica por el.
Este fue de los unicos calendarizadores en los que no siempre se obtuvo una solucion optima (1 de 5 veces no la obtuvo) pero cuando la obtuvo, el tiempo fue similar al original.
"""

"""
Realiza una heurisitca y regresa una tupla con el costo de la solucion encontrada y el tiempo
que le tomo encontrarla
"""
def infoHeuristica(heuristica = blocales.temple_simulado, parametros = [ProblemaNreinas(8)]):
    tInicial = time()
    solucion = heuristica(*parametros)
    tFinal = time()
    costo = parametros[0].costo(solucion)
    tEjecucion = tFinal - tInicial

    return costo, tEjecucion

def calendarizar(problema, n):
    costos = [problema.costo(problema.estado_aleatorio())
              for _ in range(10 * len(problema.estado_aleatorio()))]
    minimo,  maximo = min(costos), max(costos)
    T_ini = 2 * (maximo - minimo)

    if n == 1:
        calendarizador = (T_ini/i for i in range(1, int(1e10)))
    elif n == 2:
        calendarizador = (T_ini/i for i in range(1, int(1e10), 2))
    elif n == 3:
        calendarizador = (T_ini/i for i in range(1, int(1e10), 10))
    elif n == 4:
        calendarizador = (T_ini/sqrt(i) for i in range(1, int(1e10)))
    elif n == 5:
        calendarizador = (T_ini/sqrt(i) for i in range(1, int(1e10), 2))
    elif n == 6:
        calendarizador = (T_ini/sqrt(i) for i in range(1, int(1e10), 10))
    elif n == 7:
        calendarizador = (T_ini/(log(i)+1) for i in range(1, int(1e10)))
    elif n == 8:
        calendarizador = (T_ini/(log(i)+1) for i in range(1, int(1e10), 2))
    elif n == 9:
        calendarizador = (T_ini/(log(i)+1) for i in range(1, int(1e10), 10))
    elif n == 10:
        calendarizador = (T_ini*0.995**i for i in range(1, int(1e10)))
    elif n == 11:
        calendarizador = (T_ini*0.95**i for i in range(1, int(1e10)))
    elif n == 12:
        calendarizador = (T_ini*0.9**i  for i in range(1, int(1e10)))
    else:
        calendarizador = (T_ini/i for i in range(1, int(1e10)))

    return calendarizador 

def cadenaCalendarizador(n):
    if n == 1:
        return "calendarizador = (T_ini/i for i in range(1, int(1e10)))"
    elif n == 2:
        return "calendarizador = (T_ini/i for i in range(1, int(1e10), 2))"
    elif n == 3:
        return "calendarizador = (T_ini/i for i in range(1, int(1e10), 10))"
    elif n == 4:
        return "calendarizador = (T_ini/sqrt(i) for i in range(1, int(1e10)))"
    elif n == 5:
        return "calendarizador = (T_ini/sqrt(i) for i in range(1, int(1e10), 2))"
    elif n == 6:
        return "calendarizador = (T_ini/sqrt(i) for i in range(1, int(1e10), 10))"
    elif n == 7:
        return "calendarizador = (T_ini/(log(i)+1) for i in range(1, int(1e10)))"
    elif n == 8:
        return "calendarizador = (T_ini/(log(i)+1) for i in range(1, int(1e10), 2))"
    elif n == 9:
        return "calendarizador = (T_ini/(log(i)+1) for i in range(1, int(1e10), 10))"
    elif n == 10:
        return "calendarizador = (T_ini*0.995**i for i in range(1, int(1e10)))"
    elif n == 11:
        return "calendarizador = (T_ini*0.95**i for i in range(1, int(1e10)))"
    elif n == 12:
        return "calendarizador = (T_ini*0.9**i  for i in range(1, int(1e10)))"
    else:
        return "calendarizador = (T_ini/i for i in range(1, int(1e10)))"

    def pruebaTiempo():

    reinas = 16
    rep = 10
    repeticiones = 5
    n = 1

    print("Reinicios aleatorios")
    for intento in range(rep):
        info = infoHeuristica(ProblemaNreinas(reinas), blocales.descenso_colinas)
        print(info)

        if info[0] is 0:
            mejores.append( ("Colinas", *info) )

    for reinas in [16, 32, 64, 100]:

        mejores = []

        print("##############################################################")

        print("Numero reinas: ", str(reinas))

        print("Temple")
        for _ in range(repeticiones):
            info = infoHeuristica(blocales.temple_simulado, [ProblemaNreinas(reinas)])
            if info[0] is 0:
                mejores.append(info)

        print("De {} veces, {} veces se llego a costo 0".format(repeticiones, len(mejores)))
        promedio1 = sum(info[1] for info in mejores) / len(mejores) if len(mejores) > 0 else 0

        for n in range(1,12):

            mejores = []

            print("Temple otra calendarizacion")

            print(cadenaCalendarizador(n))

            for _ in range(repeticiones):
                problema = ProblemaNreinas(reinas)

                info = infoHeuristica(blocales.temple_simulado,
                                      [problema, calendarizar(problema, n)])
 
                if info[0] is 0:
                    mejores.append(info)

            print("De {} veces, {} veces se llego a costo 0".format(repeticiones, len(mejores)))
            promedio2 = sum(info[1] for info in mejores) / len(mejores) if len(mejores) > 0 else 0
            print("Promedio calendarizacion original:\t\t", str(promedio1))
            print("Promedio otra calendarizacion:\t\t\t", str(promedio2))

            if promedio1 < promedio2:
                print("Promedio 1 es menor: ", str( (promedio1 + 1) / (promedio2 + 1)))
            elif promedio2 < promedio1:
                print("Promedio 2 es menor: ", str( (promedio2 + 1) / (promedio1 + 1)))
            else:
                print("Promedios iguales")
