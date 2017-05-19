# -*- coding: utf-8 -*-

from grafo import *
from utilidad import *
from vertice import *
from vertices import *
from aristas import *
from arista import *

Grafo = Grafo('Red vial')

vertices = Vertices()

vertices.agregar(Vertice("A", {'x': 10, 'y': 10}))
vertices.agregar(Vertice("B", {'x': 130, 'y': 10}))
vertices.agregar(Vertice("C", {'x': 10, 'y': 130}))
vertices.agregar(Vertice("D", {'x': 130, 'y': 130}))

Grafo.agregarVertices(vertices.vertices)

aristas = Aristas()
aristas.agregar(Arista(vertices.obtener("A"), vertices.obtener("B")))
aristas.agregar(Arista(vertices.obtener("A"), vertices.obtener("C")))
aristas.agregar(Arista(vertices.obtener("B"), vertices.obtener("C")))
aristas.agregar(Arista(vertices.obtener("D"), vertices.obtener("B")))
aristas.agregar(Arista(vertices.obtener("D"), vertices.obtener("C")))

for arista in aristas.aristas:
	Grafo.agregarArista(arista)

print Grafo

print 'ruta mas corta= ' + str(dijkstra(Grafo, "A", "D"))

print toMatrixAdyacencia(Grafo)
