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
import math


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


def prueba_temple_simulado(problema=ProblemaNreinas(8),calendarizador=None):
    """ Prueba el algoritmo de temple simulado """

    solucion = blocales.temple_simulado(problema,calendarizador)
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)

def calendarizacionLogaritmica(problema):
    costos = [problema.costo(problema.estado_aleatorio())
                  for _ in range(10 * len(problema.estado_aleatorio()))]
    minimo,  maximo = min(costos), max(costos)
    T_ini = 2 * (maximo - minimo)
    calendarizador = (T_ini/(1+i*math.log(i+1)) for i in range(int(1e10)))
    return calendarizador
    
def calendarizacionCuadratica(problema):
    costos = [problema.costo(problema.estado_aleatorio())
                  for _ in range(10 * len(problema.estado_aleatorio()))]
    minimo,  maximo = min(costos), max(costos)
    T_ini = 3 * (maximo - minimo)
    calendarizador = (T_ini/i**2 for i in range(1,int(1e10)))
    return calendarizador

if __name__ == "__main__":
    t_inicial = time.time()
    prueba_descenso_colinas(ProblemaNreinas(64), 10)
    t_final = time.time()
    print("Tiempo de ejecución en segundos: {}".format(t_final - t_inicial))
    
    t_inicial1 = time.time()
    print("\n\nTemple simulado con calendarización To/(1 + i).")
    prueba_temple_simulado(ProblemaNreinas(64))
    t_final1 = time.time()
    print("Tiempo de ejecución en segundos: {}".format(t_final1 - t_inicial1))
    
    t_inicial2 = time.time()
    print("\n\nTemple simulado con calendarización To/(1 + i*log(i+1)).")
    prueba_temple_simulado(ProblemaNreinas(64),calendarizacionLogaritmica(ProblemaNreinas(64)))
    t_final2 = time.time()
    print("Tiempo de ejecución en segundos: {}".format(t_final2 - t_inicial2))

    t_inicial3 = time.time()
    print("\n\nTemple simulado con calendarización To/(1 + i^2).")
    prueba_temple_simulado(ProblemaNreinas(64),calendarizacionCuadratica(ProblemaNreinas(64)))
    t_final3 = time.time()
    print("Tiempo de ejecución en segundos: {}".format(t_final3 - t_inicial3))
    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    #
    # ¿Cual es el máximo número de reinas que se puede resolver en
    # tiempo aceptable con el método de 10 reinicios aleatorios?
    # Con 101 reinas hizo 22.95 minutos. Con 64 hizo 2.35 minutos.
    # Yo diría que hasta ahi es considerable aceptable.
    
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan? ¿Cual es el mejor ajuste para el temple simulado
    # y hasta cuantas reinas puede resolver en un tiempo aceptable?
    # El calendarizador logaritmico es el que mejor resultados me da, con un tiempo
    # aprox de 4 segundos y un costo de 0.
    #El calendarizador cuadratico es muy rapido (0.4 segundos aprox), sin embargo
    #el costo suele ser mayor a 0 (muy indeseable) y con ninguna modificación de parametos
    #que probe me dio mejores resultados que la logaritmica
    #
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
