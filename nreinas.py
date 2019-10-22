#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinas.py
------------

Ejemplo de las n_reinas con búsquedas locales

"""

__author__ = 'Miguel Romero'


import blocales
from random import shuffle
from random import sample
from itertools import combinations
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

    if problema.n <= 32:

        print("\n\n" + "intento".center(10) +
              "estado".center(60) + "costo".center(10))
        for intento in range(repeticiones):
            solucion = blocales.descenso_colinas(problema)
            print(str(intento).center(10) +
                  str(solucion).center(60) +
                  str(problema.costo(solucion)).center(10))

    else:
        print("\n\n" + "intento".center(10) + "costo".center(10))
        for intento in range(repeticiones):
            solucion = blocales.descenso_colinas(problema)
            print(str(intento).center(10) +
                  str(problema.costo(solucion)).center(10))


def prueba_temple_simulado(problema=ProblemaNreinas(8), calendarizador=None):
    """ Prueba el algoritmo de temple simulado """

    solucion = blocales.temple_simulado(problema, calendarizador)
    print("\n\nTemple simulado con calendarización To/(1 + i).")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución para n = %d, es: " % problema.n)
    print(solucion)


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

    
    


if __name__ == "__main__":
        

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
    # es necesario probar diferentes metodos de
    # calendarización, prueba al menos otros dos métodos sencillos de
    # calendarización y ajusta los parámetros para que funcionen de la
    # mejor manera
    #
    # Escribe aqui tus conclusiones
    #
    # PARA DESCENSO DE COLINAS:
    #
    # 1. El número máximo de reinas que se puede resolver en un tiempo
    # aceptable es de 48 y tarda alrededor de un minuto.
    #
    # PARA TEMPLE SIMULADO:
    #
    # 2.- Los parámetros sobre los que tenemos que poner más atención son la temperatura
    # inicial, la temperatura final, la razón a la cual disminuye la temperatura y la razón
    # a la cual disminuye la probabilidad de aceptar un estado de mayor costo conforme se
    # avanza en las iteraciones, la cual depende de la temperatura.
    # Es muy difícil estimar un óptimo ajuste a los parámetros, sin embargo, se pueden
    # seguir algunas recomendaciones. Uno puede consultar los calendarizadores más comunes
    # y probarlo con el problema en manos ajustando los parámetros de manera conveniente
    # para alcanzar una solción satisfactoria. Algunos calendarizadores simples se pueden
    # encontrar en la siguiente liga:
    # http://what-when-how.com/artificial-intelligence/
    # a-comparison-of-cooling-schedules-for-simulated-annealing-artificial-intelligence/
    #
    # 3.- Uno de los parámetros que afecta el desempeño de temple simulado es la razón a la
    # que disminuye la temperatura. Solo a prueba y error se puede saber el efecto que tendrá.
    #
    # DESEMPEÑO DE LOS CALENDARIZADORES UTILIZADOS
    #
    # 4.- El calendarizador_uno resuelve de manera correcta para n = 32 en casi 4 minutos
    # lo cual me parece razonable para el tamaño del problema.
    # Para reinas de 64 en adelante el programa se tarda mucho y a veces el *resultado tiene un costo
    # muy alto, casi igual al número de reinas!
    #
    # 5.- El calendarizador exponential_multiplicative_cooling se comporta bastante bien.
    # Para 80 reinas el programa tardó casi 10 segundos en devolver una solución con costo cero.
    # Para n > 80, el programa devuelve un resultado en menos de un minuto pero aveces con un
    # poco de costo. Entonces, para ese caso se prodría probar con un número mayor de iteraciones.
    #
    # 6.- El calendarizador logarithmical_multiplicative_cooling resuelve para n = 16 en poco más de
    # un minuto. Para n = 32 el programa se tarda casi 4 minutos en devolver una solución de costo cero,
    # lo cual es razonable tomando en cuenta el tamaño del problema.
    #
    # Los parametros de estos calendarizadores fueron ajustados hasta que el programa devolviera una
    # solución de costo cero en un tiempo razonable.
    #
    # CONCLUSIONES
    # El algoritmo de Temple Simulado es bastante noble, sin embargo, resulta difícil encontrar un
    # calendarizador que trabaje bien con el problema en mano, además de que se tienen que ajustar
    # los parámetros a prueba y error, lo cual puede resultar tedioso para el programador.
    # Tomando en cuenta que este algoritmo es capaz de resolver problemas muy grandes en un tiempo
    # razonable, cosidero que es una opción viable para aplicaciones del mundo real.
    #
    # *Recordemos que el algoritmo de temple simulado no es completo.
    # 
    #
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #


##    tiempos_colinas = []
##
##    for i in range(1, 11):
##        tiempo_inicial = time()
##        prueba_descenso_colinas(ProblemaNreinas(8*i), 10)
##        tiempo_final = time()
##        tiempos_colinas.append(tiempo_final - tiempo_inicial)
##
##
##    print("\nTiempo de ejecucion para descenso de colinas:")
##    print("n".center(5) + "segundos".center(10))
##    
##    for i in range(len(tiempos_colinas)):
##        print("%3d %10.4f" %((i+1)*8, tiempos_colinas[i]))


    #prueba_temple_simulado(ProblemaNreinas(48))
    
    calendarizador_1 = calendarizador_uno()
    calendarizador_2 = exponential_multiplicative_cooling()
    calendarizador_3 = logarithmical_multiplicative_cooling()

##    tiempo_inicial = time()
##    prueba_temple_simulado(ProblemaNreinas(24), calendarizador_1)
##    tiempo_final = time()
##    print("Tiempo: %.4f segundos." % (tiempo_final - tiempo_inicial)) 


##    tiempo_inicial = time()    
##    prueba_temple_simulado(ProblemaNreinas(80), calendarizador_2)
##    tiempo_final = time()
##    print("Tiempo: %.4f segundos." % (tiempo_final - tiempo_inicial)) 

    tiempo_inicial = time()
    prueba_temple_simulado(ProblemaNreinas(32), calendarizador_3)
    tiempo_final = time()
    print("Tiempo: %.4f segundos." % (tiempo_final - tiempo_inicial)) 



    


    
    

