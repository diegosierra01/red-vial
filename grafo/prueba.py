# -*- coding: utf-8 -*-

from grafo import *
from utilidad import *

Grafo = Grafo("Red vial")

Grafo.agregarVertices(["A", "B", "C", "D"])

Grafo.agregarArista("A","B",5)
Grafo.agregarArista("A","C",5)
Grafo.agregarArista("B","C",7)
Grafo.agregarArista("D","B",5)
Grafo.agregarArista("D","C",6)

print Grafo	

print 'ruta mas corta= '+str(dijkstra(Grafo,"A","D"))

print toMatrixAdyacencia(Grafo)