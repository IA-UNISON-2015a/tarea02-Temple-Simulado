#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinas.py
------------

Ejemplo de las n_reinas con búsquedas locales

"""

__author__ = 'Erick Lopez Fimbres'

import time
import blocales
from random import shuffle
from random import sample
from itertools import combinations
from math import exp
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

    #print("\n\n" + "intento".center(10) +
    #      "estado".center(60) + "costo".center(10))
    for intento in range(repeticiones):
        solucion = blocales.descenso_colinas(problema)
    #    print(str(intento).center(10) +
    #          str(solucion).center(60) +
    #          str(problema.costo(solucion)).center(10))


def calendarizadorLog(problema):
    costos = [problema.costo(problema.estado_aleatorio())
            for _ in range(10 * len(problema.estado_aleatorio()))]
    minimo,  maximo = min(costos), max(costos)
    T0 = 10*(maximo-minimo)
    
    
    #calendarizador =(T0*(pow(0.99,i)) for i in range(int(1e10)))
    calendarizador = (T0/(1+log(i+1)) for i in range(int(1e10)))
    return calendarizador

def calendarizadorExp(K,delta):
    
    calendarizador = (K*(exp(-delta*i)) for i in range(int(1e10)))
    
    return calendarizador

def prueba_temple_simulado_logaritmico(problema=ProblemaNreinas(4),calendarizador=calendarizadorLog(ProblemaNreinas(4))):
    """ Prueba el algoritmo de temple simulado """

    solucion = blocales.temple_simulado(problema,calendarizador)
    print("\n\nTemple simulado con calendarización T0/(log(1+i)+1).")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)


def prueba_temple_simulado_exponencial(problema=ProblemaNreinas(256),calendarizador=calendarizadorExp(100,.001)):
    """ Prueba el algoritmo de temple simulado """

    solucion = blocales.temple_simulado(problema,calendarizador)
    print("\n\nTemple simulado con calendarización K *exp(-delta*i).")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)


def prueba_temple_simulado(problema=ProblemaNreinas(8)):
    """ Prueba el algoritmo de temple simulado """

    solucion = blocales.temple_simulado(problema)
    print("\n\nTemple simulado con calendarización To/(1 + i).")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)


if __name__ == "__main__":
    
    #t_inicialDescenso = time.time()
    #prueba_descenso_colinas(ProblemaNreinas(32), 10)
    #t_finalDescenso = time.time()
    
    #print("Tiempo de ejecución de descenso de colinas en segundos: {}".format(t_finalDescenso - t_inicialDescenso))
    
    #t_inicialTemple = time.time()
    #prueba_temple_simulado(ProblemaNreinas(5))
    #t_finalTemple = time.time()
    #print("Tiempo de ejecución del temple simulado en segundos: {}".format(t_finalTemple - t_inicialTemple))
    #"""
    
    """
    t_inicialTemple = time.time()
    prueba_temple_simulado_exponencial(ProblemaNreinas(256),calendarizadorExp(100,.001))
    t_finalTemple = time.time()
    print("Tiempo de ejecución del temple simulado en segundos: {}".format(t_finalTemple - t_inicialTemple))
    
    """
    
    #"""
    t_inicialTemple = time.time()
    prueba_temple_simulado_logaritmico(ProblemaNreinas(4),calendarizadorLog(ProblemaNreinas(4)))
    t_finalTemple = time.time()
    
    print("Tiempo de ejecución del temple simulado en segundos: {}".format(t_finalTemple - t_inicialTemple))
    #"""

    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    #
    # ¿Cual es el máximo número de reinas que se puede resolver en
    # tiempo aceptable con el método de 10 reinicios aleatorios?
    """
    8   reinas: 0.015s
    32  reinas: 22.59s
    64  reinas: 10min 17s
    100 reinas: 1h 51min
    """
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan? 
    """
    Calendarizador por default:
    32  reinas 21.63s 
    se puede reducir la tolerancia por ejemplo la bajamos de 
    0.001 a 0.01 y tardo 3.46s con un costo 0
    
    Calendarizador exponencial:
    K*exp(-delta*i) hemos obtenido una solucion a 64 reinas en
    14.26s lo cual supera muchisimo al calendarizador anterior
    pero con una tolerancia 1x10-25
    """
    #¿Cual es el mejor ajuste para el temple simulado
    # y hasta cuantas reinas puede resolver en un tiempo aceptable?
    """
    Dependiendo el problema obviamente, en este caso el mejor ajuste fue
    cambiar al calendarizado exponencial
    Exponencial
    128 reinas 8 min 55s con delta =.001 y tol 1x10-30
    200 reinas 22 min 57 s
    256 reinas 58 min 33 s
    """
    # En general para obtener mejores resultados del temple simulado,
    # es necesario utilizarprobar diferentes metdos de
    # calendarización, prueba al menos otros dis métodos sencillos de
    # calendarización y ajusta los parámetros para que funcionen de la
    # mejor manera
    #
    """
    Como dijimos anteriormente dependiendo del problema y el metodo 
    en que se genera un vecino depende el calendarizaor que utilizaremos,
    tambien hay que ajustarlo dependiendo de los parametros que requiera
    y por ejemplo el calendarizador logaritmico no funciona en este caso
    ya que tarda demasiado (y eso que puse 4 reinas).
    """