#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinas.py
------------

Ejemplo de las n_reinas con búsquedas locales

"""

__author__ = 'RaulPerez'


import blocales
from random import shuffle
from random import sample
from itertools import combinations
from time import time
from math import exp

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

    print("\n\n" + "intento".center(10) + "estado".center(60) + "costo".center(10))
    t_inicial = time()
    for intento in range(repeticiones):
        solucion = blocales.descenso_colinas(problema)
        print(str(intento).center(10) +
              str(solucion).center(60) +
              str(problema.costo(solucion)).center(10)) 
    print(f"Tiempo = {time() - t_inicial} seg")

def prueba_temple_simulado(problema=ProblemaNreinas(8), eleccion=0):
    """ Prueba el algoritmo de temple simulado """

    def calendarizador():
        costos = [problema.costo(problema.estado_aleatorio())
            for _ in range(10 * len(problema.estado_aleatorio()))]
        minimo, maximo = min(costos), max(costos)
        To = 2 * (maximo - minimo)

        return ( ((To * exp(-i/(problema.n*To))) for i in range(int(1e10))) if eleccion == 1
            else ( (To * exp(-i/((problema.n**(1/2)) * To))) for i in range(int(1e10))) if eleccion == 2
            else None)

    t_inicial = time()
    solucion = blocales.temple_simulado(problema, calendarizador=calendarizador())
    print("\n\nTemple simulado con calendarización " + 
        ("To * exp(-i/(n*To))" if eleccion == 1 
            else "To * exp(-i/(((n^(1/2))*To)))" if eleccion == 2
            else "To/(i+1)") )
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)
    print(f"Tiempo = {time() - t_inicial} seg")

if __name__ == "__main__":
    
    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    #
    # ¿Cual es el máximo número de reinas que se puede resolver en
    # tiempo aceptable con el método de 10 reinicios aleatorios?
    #
    #   NReinas     |   Costo Minimo   |     Tiempo
    #      8                 0             0.031 seg
    #     16                 0             0.65 seg
    #     32                 0             20.35 seg
    #     64                 0             693.01 seg ~ 11.55 min         
    #     80                 0             1895.77 seg ~ 31.58 min
    #    100                 0             1 hora posiblemente
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
    #   NReinas     |   Costo Menor   |   Calendarizador                |     Tiempo
    #      8                 0               To/(1 + i)                        1.76 seg
    #      8                 0           To * exp(-x/(n*To))                   0.13 seg
    #      8                 0           To * exp(-i/(((n^(1/2))*To)))         0.04 seg    
    #
    #     16                 0               To/(1 + i)                        6.37 seg
    #     16                 0           To * exp(-x/(n*To))                   1.07 seg
    #     16                 0           To * exp(-i/(((n^(1/2))*To)))         0.25 seg
    #
    #     32                 0               To/(1 + i)                       29.31 seg
    #     32                 0           To * exp(-x/(n*To))                   9.50 seg
    #     32                 0           To * exp(-i/(((n^(1/2))*To)))         2.07 seg
    #
    #     64                 0               To/(1 + i)                      140.08 seg ~ 2.33 min
    #     64                 0           To * exp(-x/(n*To))                 118.47 seg ~ 1.97 min
    #     64                 0           To * exp(-i/(((n^(1/2))*To)))        15.77 seg 
    #
    #    100                 0               To/(1 + i)                      516.19 seg ~ 8.66 min
    #    100                 0           To * exp(-x/(n*To))                 636.45 seg ~ 10.60 min
    #    100                0~1          To * exp(-i/(((n^(1/2))*To)))        63.16 seg ~ 1.05 min
    #       
    #    Con el To/(x+1) el tiempo aumenta considerablemente, lo mismo con To * exp(-x/(n*To)) ya que  
    #    con n = 100 lo supera. Para To * exp(-i/(((n^(1/2))*To))) el tiempo es muy menor comparado con los demas
    #    solo que varia el costo para n = 100.
    #
    #prueba_descenso_colinas(ProblemaNreinas(80), 10)
    prueba_temple_simulado(ProblemaNreinas(100), eleccion=2)
