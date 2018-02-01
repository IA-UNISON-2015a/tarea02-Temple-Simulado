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

def prueba2_temple_simulado(problema=ProblemaNreinas(8)):

    t0 = T_inicial(problema)
    solucion = blocales.temple_simulado(problema,calend_geom(t0))
    print("\n\nTemple simulado con calendarización to*\u0391^k.")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)
    
def prueba3_temple_simulado(problema=ProblemaNreinas(8)):
    t0 = T_inicial(problema)
    solucion = blocales.temple_simulado(problema,calend_exp(t0,problema.n))
    print("\n\nTemple simulado con calendarización To*exp^(-\u0391*k^(1/N)).")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)
    
def prueba4_temple_simulado(problema=ProblemaNreinas(8)):
    t0 = T_inicial(problema)
    solucion = blocales.temple_simulado(problema,calend_log(t0))
    print("\n\nTemple simulado con calendarización To*\u0391/log(1 + k).")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)

def T_inicial(problema=ProblemaNreinas(8)):
    costos = [problema.costo(problema.estado_aleatorio())
              for _ in range(10 * len(problema.estado_aleatorio()))]
    minimo,  maximo = min(costos), max(costos)
    return 2 * (maximo - minimo)      
    
if __name__ == "__main__":
    
    

    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    #
    # ¿Cual es el máximo número de reinas que se puede resolver en
    # tiempo aceptable con el método de 10 reinicios aleatorios?
    
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan? ¿Cual es el mejor ajuste para el temple simulado
    # y hasta cuantas reinas puede resolver en un tiempo aceptable?
    #
    # En general para obtener mejores resultados del temple simulado,
    # es necesario utilizarprobar diferentes metdos de
    # calendarización, prueba al menos otros dos métodos sencillos de
    # calendarización y ajusta los parámetros para que funcionen de la
    # mejor manera
    #
    # Escribe aqui tus conclusiones
    #En base a la subjetividad del término 'aceptable' diría que 78 reinas.
    # Me tomó alrededor de dos horas correr de 10 reinas hasta 78
    #(tomando en cuenta que hice corridas para los pares entre 10 y 78 reinas)
    #
    #Para el temple_simulado, modifiqué el nivel de tolerancia pero el tiempo se
    #elevava significativamente. Cuando utilicé otros métodos de calendarización 
    #resultó que el calend_geom fue el mejor en tiempos con alpha igual a 0.9. De hecho 
    # el tiempo siempre fue muy muy bueno, sin embargo los costos se veían afectados. Para
    # alphas menores a 0.8, los costos eran considerablemente altos en promedio. Para 
    # alpha = 0.9 el costo promedio oscilaba entre 0 y 1 pero el tiempo fue tan pequeño que
    #que marcaba 0s.
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #
    """archivo = open("nreinas_dc.txt",'a')

    for i in range(32,80,2):
           
        t_inicial = time.time()
        prueba_descenso_colinas(ProblemaNreinas(i), 10)
        t_final = time.time()
            
        t_dc = t_final - t_inicial
            
        archivo.write("{} \t {} ".format(i,t_dc))
        archivo.write("\n")
    """    
    """ t_inicial = time.time()
    prueba_descenso_colinas(ProblemaNreinas(32), 10)
    t_final = time.time()
    print("Tiempo - descenso_colinas: {} s".format(t_final - t_inicial))
    """
    
    t_inicial = time.time()
    prueba2_temple_simulado(ProblemaNreinas(32))
    t_final = time.time()
    print("Tiempo - temple_simulado: {} s".format(t_final - t_inicial))
    
    

def calend_geom(To,alpha=0.9):
    k=0
    
    for k in range(int(1e10)):
        k+=1
        T = math.pow(alpha,k)*To
        yield T
        
def calend_exp(To,N,alpha=0.01):
    k=0
    for k in range(int(1e10)):
        k+=1
        T = To*math.exp(-1*alpha* math.pow(k,1/N))
        yield T
    
    
def calend_log(To,alpha=1):
    k=0
    for k in range(int(1e10)):
        k+=1
        T = alpha*To/math.log(1+k,math.e)
        yield T
    
  
    
    