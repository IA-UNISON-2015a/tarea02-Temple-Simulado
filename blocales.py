#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
blocales.py
------------

Algoritmos generales para búsquedas locales

"""

__author__ = 'Miguel Romero Valdés'

from itertools import takewhile
from math import exp
from random import random
import math


class Problema(object):
    """
    Definición formal de un problema de búsqueda local. Es necesario
    adaptarla a cada problema en específico, en particular:

    a) Todos los métodos requieren de implementar costo y estado_aleatorio

    b) descenso_colinas  requiere de implementar el método vecinos

    c) temple_simulado requiere vecino_aleatorio

    """
    def estado_aleatorio(self):
        """
        @return Una tupla que describe un estado

        """
        raise NotImplementedError("Este metodo debe ser implementado")

    def vecinos(self, estado):
        """
        Generador de los vecinos de un estado

        @param estado: Una tupla que describe un estado

        @return: Un generador de estados vecinos

        """
        raise NotImplementedError("Este metodo debe ser implementado")

    def vecino_aleatorio(self, estado):
        """
        Genera un vecino de un estado en forma aleatoria.
        Procurar generar el estado  vecino a partir de una
        distribución uniforme de ser posible.

        @param estado: Una tupla que describe un estado

        @return: Una tupla con un estado vecino.
        """
        raise NotImplementedError("Este metodo debe ser implementado")

    def costo(self, estado):
        """
        Calcula el costo de un estado dado

        @param estado: Una tupla que describe un estado

        @return: Un valor numérico, mientras más pequeño, mejor es el estado.

        """
        raise NotImplementedError("Este metodo debe ser implementado")


def descenso_colinas(problema, maxit=1e6):
    """
    Busqueda local por descenso de colinas.

    @param problema: Un objeto de una clase heredada de Problema
    @param maxit: Máximo número de iteraciones

    @return: El estado con el menor costo encontrado

    """
    estado = problema.estado_aleatorio()
    costo = problema.costo(estado)

    for _ in range(int(maxit)):
        e = min(problema.vecinos(estado), key=problema.costo)
        c = problema.costo(e)
        if c >= costo:
            break
        estado, costo = e, c
    return estado


def temple_simulado(problema, calendarizador=None, tol=0.001):
    """
    Busqueda local por temple simulado

    @param problema: Un objeto de la clase `Problema`.
    @param calendarizador: Un generador de temperatura (simulación).
    @param tol: Temperatura mínima considerada diferente a cero.

    @return: El estado con el menor costo encontrado

    """
    if calendarizador is None:
        #Se crea una lista con 10*n elementos que represenan el costo de estados aleatorios
        costos = [problema.costo(problema.estado_aleatorio())
                  for _ in range(10 * len(problema.estado_aleatorio()))]
        minimo,  maximo = min(costos), max(costos)
        T_ini = 2 * (maximo - minimo)
        #calendarizador es un generador en el que cada valor va disminuyendo con respecto al anterior
        calendarizador = (T_ini/(1 + i) for i in range(int(1e10)))

    estado = problema.estado_aleatorio()
    costo = problema.costo(estado)

    for T in takewhile(lambda i: i > tol, calendarizador):

        vecino = problema.vecino_aleatorio(estado)
        costo_vecino = problema.costo(vecino)
        incremento_costo = costo_vecino - costo

        if incremento_costo <= 0 or random() < exp(-incremento_costo / T):
            estado, costo = vecino, costo_vecino
    return estado

#FIN función temple_simulado


def calendarizador_uno(p1= 0.7, pn=0.001, n=1e6):

    """
    @param p1 Probabilidad de aceptar una peor solución al principio.
    @param pn Probabilidad de aceptar una peor solución al final.
    @param n Número de iteraciones.
    @return Un generador cuyos elemntos son las soluciones en cada iteración.
    """

    # Initial temperature 
    t1 = -1.0/math.log(p1)
    # Final temperature 
    tn = -1.0/math.log(pn)
    # Fractional reduction every cycle 
    frac = (tn/t1)**(1.0/(n-5.0))

    
    t = t1
    for i in range(int(n)):    
        yield t
        t = frac*t

#FIN función calendarizador_uno

def exponential_multiplicative_cooling(t0=1, alfa=0.999, n=1e10):

    """
    @param t0 Temperatura inicial.
    @param alfa Fracción en un intervalo [0.8, 1) que determina la razón a la
    cual disminuye la temperatura.
    @param n Número de iteraciones.
    @return Un generador cuyos elemntos son las soluciones en cada iteración.
    """

    tn = t0
    for i in range(1, int(n+1)):
        yield tn
        tn = t0*(alfa**i)

#FIN función exponential_multiplicative_cooling


def logarithmical_multiplicative_cooling(t0=1, alfa=1, n=1e6):

    """
    @param t0 Temperatura inicial.
    @param alfa Un número mayor a la unidad que determina la razón a la
    cual disminuye la temperatura.
    @param n Número de iteraciones.
    @return Un generador cuyos elemntos son las soluciones en cada iteración.
    """


    tn = t0
    for i in range(1, int(n+1)):
        yield tn
        tn = t0 / (1+alfa*math.log(1+i))

#FIN función logarithmical_multiplicative_cooling

