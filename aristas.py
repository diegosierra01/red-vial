# -*- coding: utf-8 -*-
from vertices import *
import math

class Aristas:
    def __init__(self):
        self.aristas = []

    def __len__(self):  
        return len(self.aristas)

    def __iter__(self):  
        return iter(self.aristas)

    def agregar(self, arista):
        self.aristas.append(arista)

    def agregarAristas(self, aristas):
        for arista in aristas:
            self.aristas.append(arista)

    def existeArista(self,arista):        
        aristaInvertida = Arista(Vertice(arista.vertice2.nombre,{'x':arista.vertice2.position['x'],'y':arista.vertice2.position['y']}),Vertice(arista.vertice1.nombre,{'x':arista.vertice1.position['x'],'y':arista.vertice1.position['y']}))
        return self.estaRepetido(arista,aristaInvertida)

    def estaRepetido(self,arista,aristaInvertida):
        for aristalista in self.aristas:
            if( (arista.vertice1.position == aristalista.vertice1.position and  arista.vertice2.position == aristalista.vertice2.position ) or 
                (aristaInvertida.vertice1.position == aristalista.vertice1.position and  aristaInvertida.vertice2.position == aristalista.vertice2.position ) ):
                return True
        return False


class Arista:
    def __init__(self, vertice1, vertice2):
        self.vertice1 = vertice1
        self.vertice2 = vertice2
        self.calcularDistancia()

    def calcularDistancia(self):
        self.distancia = math.sqrt(pow((self.vertice2.position['x'] - self.vertice1.position['x']),2)+pow((self.vertice2.position['y'] - self.vertice1.position['y']),2))

    def calcularAngulo(self): # Angulo con respecto a x