#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinas.py
------------

Ejemplo de las n_reinas con búsquedas locales

"""

__author__ = 'juliowaissman'


import blocales
import math
from random import shuffle
from random import sample
from itertools import combinations


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

    def arrays(self, s):
        d1 = [0 for i in range(2*self.n - 1)]
        d2 = [0 for i in range(2*self.n - 1)]

        for i in range(len(s)):
            aux = i + s[i]
            d1[aux]+=1
            aux = 7 + i - s[i]
            d2[aux] += 1

        return (d1,d2)

    def vecinos(self, estado):
        """
        Generador vecinos de un estado, todas las 2 permutaciones

        @param estado: una tupla que describe un estado.

        @return: un generador de estados vecinos.

        """
        edo_lista = list(estado)
        for i, j in combinations(range(self.n), 2):
            edo_lista[i], edo_lista[j] = edo_lista[j], edo_lista[i]
            yield tuple(edo_lista)
            edo_lista[i], edo_lista[j] = edo_lista[j], edo_lista[i]

    def vecino_aleatorio(self, estado):
        """
        Genera un vecino de un estado intercambiando dos posiciones
        en forma aleatoria.

        @param estado: Una tupla que describe un estado

        @return: Una tupla con un estado vecino.

        """
        vecino = list(estado)
        i, j = sample(range(self.n), 2)
        vecino[i], vecino[j] = vecino[j], vecino[i]
        return tuple(vecino)

    def costo(self, estado):
        """
        Calcula el costo de un estado por el número de conflictos entre reinas

        @param estado: Una tupla que describe un estado

        @return: Un valor numérico, mientras más pequeño, mejor es el estado.

        """
        d1,d2 = self.arrays(estado)
        ataques = 0
        for i in range(2*self.n - 1):
            if d1[i] > 1:
                ataques += 2*d1[i] - 2
            if d2[i] > 1:
                ataques += 2*d2[i] - 2

        return ataques


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

    solucion = blocales.temple_simulado(problema,calendarizadorNewton(30000,0.0001))
    print("\n\nTemple simulado con calendarización To/(1 + i).")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)

def calendarizadorNewton(t0,k=0.05):
    t = t0
    i = 0
    while True:
        t = t0*math.exp(-k*i)
        i+=1
        yield t

def calendarizador(t0,alpha=0.999):
    while True:
        t0 *= alpha
        yield t0

if __name__ == "__main__":

    #prueba_descenso_colinas(ProblemaNreinas(140), 10)
    prueba_temple_simulado(ProblemaNreinas(150))

    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    #
    # ¿Cual es el máximo número de reinas que se puede resolver en
    # tiempo aceptable con el método de 10 reinicios aleatorios?
    #
    # Pues con 140 reinas aún lo resuelve, pero tarda bastante en hacerlo.
    #
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan? ¿Cual es el mejor ajuste para el temple simulado
    # y hasta cuantas reinas puede resolver en un tiempo aceptable?
    #
    # Con 150 reynas aún encuentra el optimo global, pero tarda mucho tiempo.
    # la funcipon de calendarizació que mejor soluciones me dio fue la ecuación
    # de la ley de enfriamiento de newton, con temperatura inicial 30000, k = 0.0001
    # y tolerancia de 0.001
    #
    # En general para obtener mejores resultados del temple simulado,
    # es necesario utilizarprobar diferentes metdos de
    # calendarización, prueba al menos otros dos métodos sencillos de
    # calendarización y ajusta los parámetros para que funcionen de la
    # mejor manera
    #
    # La mejor función de calendarización que mejor se ajustó fue la de la
    # ley de enfriamiento de newton, la explicación a esto supongo que es
    # porque se acerca un poco mas a la realidad.
    # La otra función de calendarizacion que probé fue multiplicar la temperatura actual
    # por un alfa entre 0 y 1, este método es el mas rápido de los que probé, pero
    # también es el menos eficiente.
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #
