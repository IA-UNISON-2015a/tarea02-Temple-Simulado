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
    start = time.time()
    print("\n\n" + "intento".center(10) +
          "estado".center(60) + "costo".center(10))
    for intento in range(repeticiones):
        solucion = blocales.descenso_colinas(problema)
        print(str(intento).center(10) +
              str(solucion).center(60) +
              str(problema.costo(solucion)).center(10))
    end = time.time()
    print("Segundos..: " + str(end - start))



def prueba_temple_simulado(problema=ProblemaNreinas(8),calendarizacion=None):
    """ Prueba el algoritmo de temple simulado """
    start = time.time()
    solucion = blocales.temple_simulado(problema,calendarizacion)
    #print("\n\nTemple simulado con calendarización To/(1 + i).")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)
    end = time.time()
    print("Tiempo que tarda: Segundos..: " + str(end - start))

if __name__ == "__main__":

    #prueba_descenso_colinas(ProblemaNreinas(80), 10)
    #prueba_temple_simulado(ProblemaNreinas(50),lineal)

    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    #   
    # ¿Cual es el máximo número de reinas que se puede resolver en
    # tiempo aceptable con el método de 10 reinicios aleatorios?
    # Se hicieron varias pruebas, y se observo que:
    # con N = 8 tarda 0.01519 segundos
    # con N = 32 tarda 4.57777 segundos 
    # con N = 50 tarda 45.76 segundos
    # con N = 64 tarda  2.47 minutos
    # con N = 70 tarda 3.7 minutos 
    # con N = 80 tarda 7.1 minutos
    # Por lo que vemos que no es tanto, pero ya empezo a tardar, entonces
    # mi opinión es que entre 64 y 70 estra bien, para que no pase mucho tiempo.
    #
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan?
    # La tolerancia dada esta  bien porque nos da siempre costo de 0 y lo 
    # resuelve en un tiempo aceptable
    
    #¿Cual es el mejor ajuste para el temple simulado
    # y hasta cuantas reinas puede resolver en un tiempo aceptable?
    #El metodo exponencial lo hizo muchisimo más rapido, por ejemplo
    #con N = 64 el metodo que ya traia por default lo hacia en  2.47 minutos
    # el exponencial lo hace en 5.29 segundos
    #
    # En general para obtener mejores resultados del temple simulado,
    # es necesario probar diferentes metdos de
    # calendarización, prueba al menos otros dos métodos sencillos de
    # calendarización y ajusta los parámetros para que funcionen de la
    # mejor manera
    #
    # Escribe aqui tus conclusiones
    #
    # Yo busque otro metodo que es el que le puse lineal que es (k-t0*i) 
    # pero resulta que no me da una solución y tiene un costo muy elevado.
    # Tambien escogi un metodo exponencial que es t0 * math.exp(-k*i)
    # Y este es por mucho el mejor, el tiempo se reduce mucho, y el costo tambien.
    #
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #
    
    #print("\n\nTemple simulado con calendarización To/(1 + i).")
    #prueba_temple_simulado(ProblemaNreinas())
    
   # print("\n\nTemple simulado con calendarización k-t0*i")

   # prueba_temple_simulado(ProblemaNreinas(4), "lineal")
    
    print("\n\nTemple simulado con calendarización k*math.exp(-tol*i)")
    prueba_temple_simulado(ProblemaNreinas(64), "exponencial")
       











