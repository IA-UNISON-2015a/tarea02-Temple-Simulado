#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinas.py
------------

Ejemplo de las n_reinas con búsquedas locales

"""

__author__ = 'Adrian Emilio Vazquez Icedo'


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

    print("\n\n" + "intento".center(10) +
          "estado".center(60) + "costo".center(10))
    for intento in range(repeticiones):
        solucion = blocales.descenso_colinas(problema)
        print(str(intento).center(10) +
              str(solucion).center(60) +
              str(problema.costo(solucion)).center(10))
        
        


def prueba_temple_simulado(problema=ProblemaNreinas(8), i=0):
    """ Prueba el algoritmo de temple simulado """
    if i==0:
        solucion = blocales.temple_simulado(problema)
        print("\n\nTemple simulado con calendarización To/(1 + i).")
    elif i==1:
        solucion = blocales.temple_simulado(problema, calendarizacion1(problema))
        print("\n\nTemple simulado con calendarización To*enfriador.")
    else:
        solucion = blocales.temple_simulado(problema, calendarizacion2(problema))
        print("\n\nTemple simulado con calendarización To*e(-cambio*i).")
        
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)
    

def calendarizacion1(problema, enfriador=0.999):
    
    costos = [problema.costo(problema.estado_aleatorio())
        for _ in range(10 * len(problema.estado_aleatorio()))]
    minimo,  maximo = min(costos), max(costos)
    T_ini = 2 * (maximo - minimo)
    for i in range (0, int(1e10)):
        T_ini = T_ini*enfriador
        yield T_ini

def calendarizacion2(problema, cambio=.0009):
    
    costos = [problema.costo(problema.estado_aleatorio())
                  for _ in range(10 * len(problema.estado_aleatorio()))]
    minimo,  maximo = min(costos), max(costos)
    T_ini = 2 * (maximo - minimo)
    for i in range (0, int(1e10)):
        t = T_ini*(exp(-cambio*i))
        yield t
         
if __name__ == "__main__":
    tiempo_inicial = time() 
    
    prueba_descenso_colinas(ProblemaNreinas(64), 10)
    prueba_temple_simulado(ProblemaNreinas(64), 1)
    tiempo_final = time() 
 
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    
    print ('El tiempo de ejecucion fue:',tiempo_ejecucion)
    
    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    #
    # ¿Cual es el máximo número de reinas que se puede resolver en
    # tiempo aceptable con el método de 10 reinicios aleatorios?
    #
    #
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan? ¿Cual es el mejor ajuste para el temple simulado
    # y hasta cuantas reinas puede resolver en un tiempo aceptable?
    #
    #
    # En general para obtener mejores resultados del temple simulado,
    # es necesario probar diferentes metodos de
    # calendarización, prueba al menos otros dos métodos sencillos de
    # calendarización y ajusta los parámetros para que funcionen de la
    # mejor manera
    #
    # Escribe aqui tus conclusiones:
    #
    #   1)
    #   32:4s
    #   40:Sin problemas, encuentra solucion y el tiempo de aumento no es considerable.(11s)
    #   48:Se encuentra solucion y un pequeño aumento de tiempo pero insignificante.(14s)
    #   56:Se encuetra solucion con un poco mas de tiempo de ejecucion pero no tan importante.(70s)
    #   64:Se sigue encontrando solucion pero ya es un cambio de tiempo considerabe con respecto a 32.(145s)
    #   72:Se encuentran soluciones pero ya son tiempos grandes en comparacion a 32.(238s)
    #   80:Se encuentran soluciones pero el tiempo ya es algo grande.(378s)
    #   90:Se encuentran soluciones pero el tiempo ya es demaciado grande.(724s)
    #   100:Se encuentra solucion pero el tiempo es demaciado grande para este problema.(1128s)
    #
    #   Nota:Si se detuvieran los reinicios cuando se encuentra una solucion tardaria menos, pero de esta forma
    #   permite encontrar varias soluciones.
    #
    #   
    #   2)
    #   Para conseguir los mejores resultados posibles es importante saber contralar el , desde la 
    #   temperatura inicial y el ritmo con el cual baja. Ademas establecer bien la tolerancia para evitar
    #   que se realicen demaciados ciclos donde no se permite el explorar nuevas sonas debido a la baja temperatura.
    #   
    #   En estos ejemplos se llega a costo 0
    #   con 0.01 de tolerancia y 150 reinas:35s 
    #   con 0.01 de tolerancia y 200 reinas:78s
    #   con 0.001 de tolerancia y 150 reinas:341s
    #   con 0.001 de tolerancia y 200 reinas:569s
    #   
    #   Con 150 y 200 con 0.01 de tolerancia se consigue una solucion en un tiempo aceptable, al probarlo con 0.02, 0.03 o
    #   0.05 no me llega a costo 0 y al hacerlo con 0.001 el tiempo aumenta considerablemente.
    #      
    #
    #   3)
    #   calendarizacion 1: En esta la temperatura se va reduciendo un 5% ya que se multiplica la temperatura actual
    #   por .999 lo cual permite que con temperaturas altas la temperatura disminuya mas que con una baja.
    #
    #   calendarizacion 2:En esta la temperatura dependera de la iteracion en que nos encontremos ya que
    #   se multiplicara la iteracion por el factor de cambio negativo, este valor se usara en una exponencial 
    #   y se multiplicara por la temperatura inicial.
    #
    #   Ejemplo: 64, 0.001 tol = default=(30s,31s,35s), calendarizacion 1=(4.8s,5s,4.8s), calendarizacion2=(5.1s, 5.3s, 5.2s)
    #
    #   En el ejemplo de 64 por default se resolvia entre 30 y 35 segundos y con los dos metodos de calendarizacion se logro 
    #   bajar a 5s aproximadamente.
    #
    #   El temple es mucho mejor que el desenso de colinas pero para lograr la mayor efectividad se debe
    #   manejar de la mejor manera el factor de la temperatura.
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #
