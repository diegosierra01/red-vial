# -*- coding: utf-8 -*-
from arista import *
from vertice import *

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
            if( (arista.vertice1.position == aristalista.vertice1.position and  arista.vertice2.position == aristalista.vertice2.position ) or (aristaInvertida.vertice1.position == aristalista.vertice1.position and  aristaInvertida.vertice2.position == aristalista.vertice2.position ) ):
                return True
        return False