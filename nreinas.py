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
import time


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
    #start_time = time.time()
    #prueba_descenso_colinas(ProblemaNreinas(25), 10)
    #print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    prueba_temple_simulado(ProblemaNreinas(50))
    print("--- %s seconds ---" % (time.time() - start_time))


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
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #

    """
    T. Inicial Reinicios aleatorios (15 rep)
    6.1566
    T. Inicial temple simulado(15 rep)
    7.859

    10 Reinicios aleatorios con 50 reinas: 54s
    10 reinicios aleatorios con 100 reinas: aprox 20 min
    Es aceptable? puede que para mi no. Pero es muestra de que ira creciendo
    muy muy rapido

    Reinas  25      32       50     100
    Tiempo  2s      6s      54s     20min

    Temple simulado base(el que viene en el github del curso): 8s
    Temple simulado con 10 * (max-min) :40s
    Con 3 * (max-min): 15s
    con 4: 19
    Con tolerancia 0.0001: un chingo
    con tolerancia 0.01: 1.5s y encontrando la solucion siempre
    Con tol 0.1: 0.2s; casi nunca encuentra la solucion

    2*len(estado_aleatorio()): <1s siempre encuentra sol

    Reinas 100   200    250     300
    Tiempo 14s   81s    156s    307s

    Para llegar a los 20 min que llegamos de reinicios aleatorios, deberiamos
    meter 400 reinas

    El codigo de los calendarizadores los agregue en blocales.py para hacer
    las pruebas mas comodamente


    """
