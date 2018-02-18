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
from math import log
from math import exp
from time import time


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


def prueba_temple_simulado(problema=ProblemaNreinas(8), calendarizador=None, cadCal="To/(1 + i)"):
    """ Prueba el algoritmo de temple simulado """

    solucion = blocales.temple_simulado(problema, calendarizador)
    print("\n\nTemple simulado con calendarización " + cadCal+ ".")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)


    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    #
    # ¿Cual es el máximo número de reinas que se puede resolver en
    # tiempo aceptable con el método de 10 reinicios aleatorios?
    #
    # Después de 60 reinas considero que el tiempo que transcurre  por cada
    # iteración es mucho para llamarla aceptable.
    #
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan? ¿Cual es el mejor ajuste para el temple simulado
    # y hasta cuantas reinas puede resolver en un tiempo aceptable?
    #
    # En general para obtener mejores resultados del temple simulado,
    # es necesario probar diferentes metodos de
    # calendarización, prueba al menos otros dos métodos sencillos de
    # calendarización y ajusta los parámetros para que funcionen de la
    # mejor manera
    #
    # Escribe aqui tus conclusiones
    #
    # Mover la temperatura inicial a algo más pequeño hara que generalmente se
    # llegue a un resultado más rápido pero también hara que el resultado no sea
    # uno deseado. También se puede cambiar la cantidad de temperatura a la que
    # se esta cambiando con cada iteración, si esta se hace más pequeña con cada
    # iteración entonces se llegara a un resultado más rápido, pero igual que con
    # la temperatura, si ocurre esto entonces es muy probable que el resultado
    # no sea uno muy deseado.
    #
    # Con los cambios que he hecho en la calendarización he logrado hacer que
    # el recocido simulado lograra resolver el problema de las reinas de hasta
    # 150 reinas en un tiempo más aceptable que el método que ya venía el
    # calendarizador por defecto, pero es también es más probable tener costos
    # de 1.
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #
def genCalendarizadorLog(problema):
    costos = [problema.costo(problema.estado_aleatorio())
              for _ in range(len(problema.estado_aleatorio()))]
    minimo,  maximo = min(costos), max(costos)
    T_ini = 3*(maximo - minimo)
    return  (T_ini/(1 + i*log(i)) for i in range(1,int(1e10)+1))

def genCalendarizadorExp(problema):
    costos = [problema.costo(problema.estado_aleatorio())
              for _ in range(10 * len(problema.estado_aleatorio()))]
    minimo,  maximo = min(costos), max(costos)
    T_ini = 3*(maximo - minimo)
    return (T_ini*exp(-0.0015*i) for i in range(1,int(1e10)+1))

if __name__ == "__main__":

    #prueba_descenso_colinas(ProblemaNreinas(32), 1)
    #start = time()
    #prueba_temple_simulado(ProblemaNreinas(150))
    #end = time()
    #print(end-start)

    start = time()
    prueba_temple_simulado(ProblemaNreinas(50), genCalendarizador1(ProblemaNreinas(50)), "To/(1+i*log(i))")
    end = time()
    print(end-start)

    start = time()
    prueba_temple_simulado(ProblemaNreinas(50), genCalendarizador2(ProblemaNreinas(50)), "To*exp(-0.0015*i)")
    end = time()
    print(end-start)
