#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinas.py
------------

Ejemplo de las n_reinas con búsquedas locales

"""

__author__ = 'juliowaissman'


import blocales
import time
from random import shuffle
from math import sqrt
from math import log
from math import exp
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


def prueba_descenso_colinas(problema=ProblemaNreinas(8), repeticiones=10, tiempo_aceptable = 10):
    """ Prueba el algoritmo de descenso de colinas con n repeticiones """

    print("\n\n" + "intento".center(10) +
          "estado".center(60) + "costo".center(10))

    tiempo_inicial = time.time()
    for intento in range(repeticiones):
        solucion = blocales.descenso_colinas(ProblemaNreinas(x))
        print(str(intento).center(10) +
              str(solucion).center(60) +
              str(problema.costo(solucion)).center(10))
    tiempo_final = time.time()
    if (tiempo_final - tiempo_inicial) < tiempo_aceptable:
        print('El resultado ha sido satisfactorio para {} reinas en {:.8f} segundos'.format(x,tiempo_final - tiempo_inicial))
    else:
        print('Los resultados no son satisfactorios para {} reinas pues demora {:.8f} segundos'.format(x,tiempo_final - tiempo_inicial))

def crear_calendario(problema = ProblemaNreinas(8), n = 0):
    costos = [problema.costo(problema.estado_aleatorio()) for _ in range(10 * len(problema.estado_aleatorio()))]
    minimo,  maximo = min(costos), max(costos)
    T_ini = 2 * (maximo - minimo)

    if n == 0:
        calendarizador = (T_ini * sqrt(0.9**i) for i in range(1,int(1e10)))
    elif n == 1:
        calendarizador = (T_ini * (sqrt(0.9**i)/(0.9)) for i in range(1,int(1e10)))
    elif n == 2:
        calendarizador = (T_ini * (0.96**i / 2*(log(i) + 1)) for i in range(1,int(1e10)))
    elif n == 3:
        calendarizador = (T_ini*(0.9**i) for i in range(1,int(1e10)))
    elif n == 4:
        # Mejor opción por mucho
        calendarizador = (T_ini*exp(0.99**i)/(0.5 * i) for i in range(1,int(1e10)))
    else:
        calendarizador = (T_ini/(1 + i) for i in range(int(1e10),4)) # default
    return calendarizador

def prueba_temple_simulado(problema=ProblemaNreinas(8), reinas = 8):
    """ Prueba el algoritmo de temple simulado """

    for i in range(5):
        tiempo_inicial = time.time()
        solucion = blocales.temple_simulado(problema, crear_calendario(problema, i), 0.00001)
        tiempo_final = time.time()

        if i == 0:
            print("\n\nTemple simulado con calendarización To * sqrt(0.9^t).")
        elif i == 1:
            print("\n\nTemple simulado con calendarización To * sqrt(t) / 0.9.")
        elif i == 2:
            print("\n\nTemple simulado con calendarización To * 0.96^t / 2(log(t) + 1)")
        elif i == 3:
            print("\n\nTemple simulado con calendarización To * 0.9^t.")
        elif i == 4:
            print("\n\nTemple simulado con calendarización To * e^(0.99^t) / 0.5t")
        print('Costo de la solución: {} para {} reinas'.format(problema.costo(solucion),reinas))
        print('En un tiempo de: {:.2f}'.format(tiempo_final - tiempo_inicial))
        print("Y la solución es: ")
        print(solucion)

if __name__ == "__main__":

    tiempo_aceptable = 40
    intentos = 10
    #for x in [8,16,32,40]: # Diferentes cantidades de reinas
    #    prueba_descenso_colinas(ProblemaNreinas(x),intentos,tiempo_aceptable)

    for x in [8,16,32,64,128]:
        prueba_temple_simulado(ProblemaNreinas(x),x)

    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    #
    # ¿Cual es el máximo número de reinas que se puede resolver en
    # tiempo aceptable con el método de 10 reinicios aleatorios?
    #
    # R. Considerando 'aceptable' como 40 segundos funciona bien para 40 reinas
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
    # R.  Si el enfriamiento es rápido la tolerancia debe ser pequeña para poder iterar.
    # La quinta calanderización, ie n = 4, resultó ser la mejor pues puede
    # resolver 128 reinas con costos en 0 para un tiempo inferior al del algoritmo
    # genético, o sea, en menos de 58s.
    #
    # Escribe aqui tus conclusiones
    #
    # R. Se debe escoger una calanderización donde el enfriamiento del sistema no ocurra
    # demasiado rápido y fijar una tolerancia aceptable.
    # En general los 5 métodos de calendarización me dieron 'buenos' resultados pero
    # la forma de enfriamiento del quinto permite llegar a la solución optima en todos
    # los casos donde fueron comparados los 5 métodos
    # Temple simulado demostró un mejor desempeño que los algoritmos genéticos y el descenso
    # de colinas al menos para este problema
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
     # El código está arriba dentro de las funciones crear_calendario, prueba_temple_simulado y prueba_descenso_colinas
    #
