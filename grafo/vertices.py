# -*- coding: utf-8 -*-

class Vertices:
	def __init__(self):
		self.vertices =[]
	def agregar(self, vertice):
		self.vertices.append(vertice)
	def agregarVertices(self, vertices):
		for vertice in vertices:
			self.vertices.append(vertice)
	def obtener(self, nombre):
		for vertice in self.vertices:
			if vertice.nombre == nombre:
				return vertice