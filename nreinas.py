#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinas.py
------------

Ejemplo de las n_reinas con búsquedas locales

"""

__author__ = 'CesarSalazar'


import blocales
from random import shuffle
from random import sample
from itertools import combinations
#Para calcular el tiempo
from time import time
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
    acum=0
    print("\n\n" + "intento".center(10) +
          "estado".center(60) + "costo".center(10))
    for intento in range(repeticiones):
        tInicial = time()
        solucion = blocales.descenso_colinas(problema)
        tFinal = time()
        tTotal = tFinal - tInicial
        acum+=tTotal
        print(str(intento).center(10) +
              str(solucion).center(60) +
              str(problema.costo(solucion)).center(10))
    print("Tiempo total:",acum)


def prueba_temple_simulado(problema=ProblemaNreinas(8)):
    """ Prueba el algoritmo de temple simulado """
    tInicial = time()
    solucion = blocales.temple_simulado(problema)
    tFinal = time()
    print("\n\nTemple simulado con calendarización To/(1 + i).")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Tiempo total:", tFinal - tInicial)
    print("Y la solución es: ")
    print(solucion)
#calcular la t0 para los candelarizadores
def calcularT0(problema):
    #calcula el t0 para el calendarizador
    costos = [problema.costo(problema.estado_aleatorio())
        for _ in range(10 * len(problema.estado_aleatorio()))]
    minimo,  maximo = min(costos), max(costos)
    return 2 * (maximo - minimo)     
#calendarizacion multiplicar por .9991
def calend_1(To):
    for _ in range(int(1e10)):
        To *=0.9991
        yield To     
def prueba_temple_simulado_1(problema=ProblemaNreinas(8)):
    """ Prueba el algoritmo de temple simulado """
    #t0
    t0=calcularT0(problema)
    tInicial = time()
    solucion = blocales.temple_simulado(problema,calend_1(t0))
    tFinal = time()
    print("\n\nTemple simulado con calendarización To*0.9991")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Tiempo total:", tFinal - tInicial)
    print("Y la solución es: ")
    print(solucion)
#calendarizador exp
def calend_exp(To,d=0.000001):
    for i in range(int(1e10)):
        To *=math.exp(-d*i)
        yield To     
#Prueba temple simulado con calendarizacion exp
def prueba_temple_simulado_exp(problema=ProblemaNreinas(8)):
    """ Prueba el algoritmo de temple simulado """
    To=1000
    tInicial = time()
    solucion = blocales.temple_simulado(problema,calend_exp(To),tol=.000000001)
    tFinal = time()
    print("\n\nTemple simulado con calendarización To*exp^-di.")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Tiempo total:", tFinal - tInicial)
    print("Y la solución es: ")
    print(solucion)

if __name__ == "__main__":
    for i in (8,16,32,64,100):
        print("\nPrueba con",i,"reinas")
        #prueba_descenso_colinas(ProblemaNreinas(i), 10)
        #prueba_temple_simulado(ProblemaNreinas(i))
        #prueba_temple_simulado_1(ProblemaNreinas(i))
        prueba_temple_simulado_exp(ProblemaNreinas(i))
    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    #
    # ¿Cual es el máximo número de reinas que se puede resolver en
    # tiempo aceptable con el método de 10 reinicios aleatorios?
    #
    """ RESPUESTA
        El tiempo "aceptable" mas grande me parece que es de 19.9 minutos que es el de 80 reinas
        con los 10 reinicios aleatorios, para el de 100 reinas el tiempo es de 61.13 minutos.
    """
    #
    #
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan? ¿Cual es el mejor ajuste para el temple simulado
    # y hasta cuantas reinas puede resolver en un tiempo aceptable?
    #
    """Respuesta
       El calendarizador pro default el tiempo para 100 reinas fue de 5 min y el costo resultaba 0 
       Al modificar el valor de la tolerancia el tiempo se elevaba mucho
       Al probar otros metodos de calendarizacion, el de exp, era mucho mas rapido, con temperatura inicial de
       1000 y una delta de 0.000001, pero conforme la n era mas grande el costo emepzaba a aumentar, 
       el costo de 100 reinas era de 2 a 4 con un timepo de 17 segundos.
       La calendarizacion de multiplicar por una constante .9991 el tiempo era menor que el default pero al aumentar n,
       el costo aumentaba, con 100 reinas el tiempo era de 38 seg, con costo de 0 o 1, para 130 reinas apenas pasaba 
       del minuto con el mismo costo.
    """
    # En general para obtener mejores resultados del temple simulado,
    # es necesario probar diferentes metdos de
    # calendarización, prueba al menos otros dos métodos sencillos de
    # calendarización y ajusta los parámetros para que funcionen de la
    # mejor manera
    #
    # Escribe aqui tus conclusiones
    #
    """Conclusiones
        El metodo de temple simulado supero por mucho los tiempos de los reinicios aleatorios.
        El metodo de calendarizacion depende del problema y dependiendo de eso se modifican los 
        distintos parametros. En el problema de las nreinas, la solucion ya es conocida y por ejemplo 
        el costo 2 no es una solucion pero habra otros problemas en los que un costo 2 no sera tan malo, asi que
        dependiendo del problema se puede elegir un mejor metodo de calendarizacion y los mejores parametros.
    """
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #
