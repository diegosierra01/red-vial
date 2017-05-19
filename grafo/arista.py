# -*- coding: utf-8 -*-
import math

class Arista:
    def __init__(self, vertice1, vertice2):
        self.vertice1 = vertice1
        self.vertice2 = vertice2
        self.calcularDistancia()

    def calcularDistancia(self):
    	self.distancia = math.sqrt(pow((self.vertice2.position['x'] - self.vertice1.position['x']),2)+pow((self.vertice2.position['y'] - self.vertice1.position['y']),2))