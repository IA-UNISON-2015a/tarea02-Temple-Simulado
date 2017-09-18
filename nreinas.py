# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 08:45:29 2017

@author: Yocu
"""

__author__ = 'Yocu'


import blocales
import time
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
        return sum([1 for (i, j) in combinations(range(self.n), 2)
                    if abs(estado[i] - estado[j]) == abs(i - j)])


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

    t_inicial = time.time()
    prueba_descenso_colinas(ProblemaNreinas(16), 10)
    t_final = time.time()
    print("Tiempo de ejecución en segundos: {}".format(t_final - t_inicial))
    
    t_inicial = time.time()
    prueba_temple_simulado(ProblemaNreinas(16))
    t_final = time.time()
    print("Tiempo de ejecución en segundos: {}".format(t_final - t_inicial))
    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    #
    # ¿Cual es el máximo número de reinas que se puede resolver en
    # tiempo aceptable con el método de 10 reinicios aleatorios?
    # 16 reinas = .003 segs
    # 32 reinas = 13 segs
    # 64 reinas = 3 min 6 seg
    # 128 reinas = 2 hr 16 min
    #
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan? ¿Cual es el mejor ajuste para el temple simulado
    # y hasta cuantas reinas puede resolver en un tiempo aceptable?
    # tolerancia = 0.005
    # 32 reinas = 0.04 segs 
    # 64 reinas = 0.17 segs
    # 128 reinas = 1 min 2 segs
    # 256 reinas = 7 min 7 segs
    # 512 reinas = 44min
    #
    # En general para obtener mejores resultados del temple simulado,
    # es necesario utilizarprobar diferentes metdos de
    # calendarización, prueba al menos otros dos métodos sencillos de
    # calendarización y ajusta los parámetros para que funcionen de la
    # mejor manera
    # cal_exponencial tol
    # 16 reinas = 0.02 segs
    # 32 reinas = 0.07 segs
    # 64 reinas = 32 segs
    # 128 reinas = 1 min 37 segs
    # 256 reinas = 5 min 30 segs
    # cal_log
    # Escribe aqui tus conclusiones
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #