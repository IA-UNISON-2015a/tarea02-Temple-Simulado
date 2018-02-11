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
    """ Prueba el algoritmo de descenso de colinas con n repeticiones."""
    tiempo_acum = 0

    print("\n\n" + "Intento".center(10) +
          "Costo".center(30) + "Tiempo".center(10))
    for intento in range(repeticiones):
        t_inicial = time()
        solución = blocales.descenso_colinas(problema)
        t_final = time()

        tiempo_total = t_final - t_inicial
        tiempo_acum += tiempo_total
        print(str(intento).center(10) +
              str(problema.costo(solución)).center(30) +
              str(tiempo_total).center(10))
        print("Estado: " + str(solución))

    print("Tiempo total para llevar a cabo " + str(repeticiones) + " repeticiones: " + str(tiempo_acum) + "s.")

def prueba_temple_simulado(problema=ProblemaNreinas(8)):
    """ Prueba el algoritmo de temple simulado """

    solucion = blocales.temple_simulado(problema)
    print("\n\nTemple simulado con calendarización To/(1 + i).")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)


if __name__ == "__main__":
    prueba_temple_simulado(ProblemaNreinas(8))

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
    # El número máximo de reinas que 10 reinicios aleatorios puede resolver
    # en tiempo 'aceptable' es 90 reinas. Tomando como aceptable 20 minutos
    # o menos. Este criterio fue elegido debido a que descenso de colinas
    # es un algoritmo tardado por tener que revisar todos los vecinos, y,
    # honestamente, no vale la pena seguir aumentando la dimensión del problema
    # cuando existe el temple simulado.
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #

    for n in (8, 16, 32, 50, 64, 70, 80, 85, 90):
        print("Prueba de descenso de colinas para: " + str(n) + " reinas.")
        prueba_descenso_colinas(ProblemaNreinas(n), 10)
