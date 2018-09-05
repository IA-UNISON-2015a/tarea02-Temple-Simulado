# Temple Simulado

Algoritmo de búsqueda meta-heurística para problemas de optimización global; el objetivo general de este tipo de algoritmos es encontrar una buena  aproximación al valor óptimo de una función en un espacio de búsqueda grande.

En cada iteración, el método de recocido simulado evalúa algunos vecinos del estado actual s y probabilísticamente decide entre efectuar una transición a un nuevo estado s' o quedarse en el estado s. Típicamente la comparación entre estados vecinos se repite hasta que se encuentre un estado óptimo que minimice la energía del sistema o hasta que se cumpla cierto tiempo computacional u otras condiciones.

### Vecindario de estado

El vecindario de un estado *s* está compuesto por todos los estados a los que se pueda llegar a partir de *s* mediante un cambio en la conformación del sistema. Los estados vecinos son generados mediante métodos de Montecarlo.

Los **algoritmos heurísticos**, basados en buscar siempre un estado vecino mejor (con energía más baja) que el actual se detienen en el momento que encuentran un mínimo local de energía. El problema con este método es que no puede asegurar que la solución encontrada sea un óptimo global, pues el espacio de búsqueda explorado no abarca todas las posibles variaciones del sistema.

**Temperatura**, es la probabilidad que un estado sea aceptado.
