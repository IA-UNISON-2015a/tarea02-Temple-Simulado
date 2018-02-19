#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinas.py
------------

Ejemplo de las n_reinas con búsquedas locales

"""

__author__ = 'Jordan Urias'


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
        
        return sum((1 for (i, j) in combinations(range(self.n), 2) if abs(estado[i] - estado[j]) == abs(i - j)))

        
def prueba_descenso_colinas(problema=ProblemaNreinas(8), repeticiones=10):
    """ Prueba el algoritmo de descenso de colinas con n repeticiones """

    print("\n\n" + "intento".center(10) +
          "estado".center(60) + "costo".center(10))
    for intento in range(repeticiones):
        solucion = blocales.descenso_colinas(problema)
        print(str(intento).center(10) +
              str(solucion).center(60) +
              str(problema.costo(solucion)).center(10))
        if(problema.costo(solucion) == 0):
            break


def prueba_temple_simulado(problema=ProblemaNreinas(8)):
    """ Prueba el algoritmo de temple simulado """
    
    t0 = [400,500,600,1000]
    
    for x in t0:
        t_inicial = time.time()
        solucion = blocales.temple_simulado(problema,calendarizador2(x,0.999))
        print("\n\nTemple simulado con calendarización To/(1 + i).")
        print("Costo de la solución: ", problema.costo(solucion))
        print("Y la solución es: ")
        print(solucion)
        t_final = time.time()
        print("Tiempo de ejecución en segundos: {}".format(t_final - t_inicial))



def calendarizador1(t0,k=0.05):
    #Descenso exponencial.
    t = t0
    i = 0
    while True:
        t = t0*math.exp(-k*i)
        i+=1
        yield t

def calendarizador2(t0,alpha=0.95):
    #Descenso lineal
    'incluso se podria modificar alpha con cada iteracion'
    while True:
        t0 *= alpha
        yield t0

if __name__ == "__main__":
    
    #prueba_descenso_colinas(ProblemaNreinas(100), 10)
    prueba_temple_simulado(ProblemaNreinas(64))
        

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
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #
'''
Nota: No me paraece que usr combinaciones para calcular los ataques sea lo mejor.
Realmente lo mejor seria usar algo mas lineal como la solucion plamteada aqui:
https://stackoverflow.com/questions/35432855/more-efficient-algorithm-to-count-attacks-in-n-queens

1. Implementando un halt al encontrar una respuesta optima.
Con 60 me parece un tiempo aceptable y aun se encuentra la solucion optima.
Con 70 aun encuentra respueta pero ya se empieza a sentir la diferencia
Con 80 aun encuentra pero ya esta tardando.
Con 90 aun encuentra pero no me parece que el tiempo sea bueno en relacion o lo que se pide.
Con 100 aun encuentra pero definitibamente el tiempo es malo.

Con 100 reinas sin halt dura entre 60 y 90 minutos.


2.
    
    Definitivamante lo que mas afecta al temple es la relacion entre la temperatura 
    inicial y como baja esta.
    
    Con una temperatura inicial alta que en los primeros pasos baja rapidamente, 
    es decir, de exponencial es mejor. Aunque hay riesgos de quedar atrapados en 
    minimos locales si la temperatura baja demasiado rapido.
    Un metodo auto daptativo mejoraria las cosas
    
    A mi parecer incluso con 256 reinas ya es tardado (2539 s), pero podria considerar 
    hasta hacerlo hasta 450-500 si se cambia la funcion de costo.
    
    Fuentes: 
    https://stuff.mit.edu/afs/athena/course/6/6.435/www/Hajek88.pdf
    http://www.fys.ku.dk/~andresen/BAhome/ownpapers/permanents/annealSched.pdf

3.
    Para hacer comparaciones entre los calendarios usare las reinas con 64
    Con el calenderizador por default toma 80 s
    
    El calenderizador 1 con la exponencial con una temperatura inicial de 1000 
    y k de 0.0001 tarda 10 s
    
    en el limite donde no siempre se encuetra solucion con t0 de 600 y  k de 
    0.0003 tarda 5 s
    
    
    con el calendarizador 2 con alpha de .999, donde t0 puede variar de 400 a 
    1000, sin un cambio muy notorio se tarda 13 s
    
'''
