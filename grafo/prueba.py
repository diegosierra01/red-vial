# -*- coding: utf-8 -*-

from grafo import *
from utilidad import *
from vertice import *
from vertices import *

Grafo = Grafo('Red vial')

vertices = Vertices()
vertices.agregar(Vertice("A", {'x': 500, 'y': 200}))
vertices.agregar(Vertice("B", {'x': 540, 'y': 200}))
vertices.agregar(Vertice("C", {'x': 600, 'y': 200}))
vertices.agregar(Vertice("D", {'x': 640, 'y': 200}))

Grafo.agregarVertices(vertices.vertices)


Grafo.agregarArista(vertices.obtener("A"), vertices.obtener("B"), 5)
Grafo.agregarArista(vertices.obtener("A"), vertices.obtener("C"), 5)
Grafo.agregarArista(vertices.obtener("B"), vertices.obtener("C"), 7)
Grafo.agregarArista(vertices.obtener("D"), vertices.obtener("B"), 5)
Grafo.agregarArista(vertices.obtener("D"), vertices.obtener("C"), 6)

print Grafo

print 'ruta mas corta= ' + str(dijkstra(Grafo, "A", "D"))

print toMatrixAdyacencia(Grafo)
