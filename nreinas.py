#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinas.py
------------

Ejemplo de las n_reinas con búsquedas locales

"""

__author__ = 'Carlos_Huguez'


import blocales
import time
import numpy as np
from random import shuffle
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
        estado = list( range( self.n ) )
        shuffle( estado )
        return tuple( estado )

    def vecinos(self, estado):
        """
        Generador vecinos de un estado, todas las 2 permutaciones

        @param estado: una tupla que describe un estado.

        @return: un generador de estados vecinos.

        """
        edo_lista = list(estado)
        
        for i, j in combinations( range( self.n ), 2 ):

            edo_lista[i], edo_lista[j] = edo_lista[j], edo_lista[i]
            
            yield tuple( edo_lista )
            
            edo_lista[i], edo_lista[j] = edo_lista[j], edo_lista[i]

    def vecino_aleatorio(self, estado):
        """
        Genera un vecino de un estado intercambiando dos posiciones
        en forma aleatoria.

        @param estado: Una tupla que describe un estado

        @return: Una tupla con un estado vecino.

        """
        vecino = list( estado )
        
        i, j = sample( range(self.n), 2 )
        
        vecino[i], vecino[j] = vecino[j], vecino[i]
        
        return tuple( vecino )

    def costo(self, estado):
        """
        Calcula el costo de un estado por el número de conflictos entre reinas

        @param estado: Una tupla que describe un estado

        @return: Un valor numérico, mientras más pequeño, mejor es el estado.

        """
        return sum( [ 1 for ( i, j ) in combinations( range( self.n ), 2 ) if abs( estado[ i ] - estado[ j ] ) == abs( i - j ) ] )

def prueba_descenso_colinas( problema = ProblemaNreinas( 8 ), repeticiones = 10 ):
    """ Prueba el algoritmo de descenso de colinas con n repeticiones """

    print("\n\n" + "intento".center( 10 ) + "estado".center( 60 ) + "costo".center( 10 ) )
    
    for intento in range(repeticiones):
        solucion = blocales.descenso_colinas( problema )
        
        print( str( intento ).center( 10 ) + str( solucion ).center( 60 ) + str( problema.costo( solucion ) ).center( 10 ) )

def prueba_temple_simulado( problema = ProblemaNreinas( 8 ) ):
    """ Prueba el algoritmo de temple simulado """

    solucion = blocales.temple_simulado_exp( problema )

    print("\n\nTemple simulado con calendarización Cale_Exp")
    print("Costo de la solución: ", problema.costo( solucion ) )
    print("Y la solución es: ")
    print( solucion )


if __name__ == "__main__":

	tiempo_ini = time.time()
	reinas = 90

	prueba_descenso_colinas( ProblemaNreinas( reinas ), 10 )
	prueba_temple_simulado( ProblemaNreinas( reinas ) )

	tiempo_final = time.time()
	print( "El tiempo final de ejecuacion fue: ", ( tiempo_final - tiempo_ini ) / 60.0 )
	print

	##########################################################################
	#                          20 PUNTOS
	##########################################################################
	#
	# ¿Cual es el máximo número de reinas que se puede resolver en
	# tiempo aceptable con el método de 10 reinicios aleatorios?
	#
    # T0/i+1,  85 reinas,  42.20 minutos, 100 reinas 114.5434 minutos 
    # T0*e^( -0.001 * i ),  90 reinas,  63.1261 minutos
    # T0 / ( log( i ) + 1 ),  24 reinas,  mas de 60 minutos
	#
    # ¿Que valores para ajustar el temple simulado son los que mejor
	# resultado dan? ¿Cual es el mejor ajuste para el temple simulado
	# y hasta cuantas reinas puede resolver en un tiempo aceptable?
	#  con iteraciones de 1e10 y tolerancia de 0.001
    #  en si la tolerancia es el mejor ajuste, en una horas (en mi computadora procesador AMD E2 con 4 GB de ram) mas de 100
    #  con el calendarizador del exponenecial   
    #
	# En general para obtener mejores resultados del temple simulado,
	# es necesario utilizarprobar diferentes metdos de
	# calendarización, prueba al menos otros dis métodos sencillos de
	# calendarización y ajusta los parámetros para que funcionen de la
	# mejor manera
	#
	# Escribe aqui tus conclusiones
	#
	# ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
	#  codigo esta en blocales.py
    #   funcion:
    #   def temple_simulado_exp
    #   intento fallido de clase iterador (Cale_exp)
	#   def temple_simulado_log
    #
