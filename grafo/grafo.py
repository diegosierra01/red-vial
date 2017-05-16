# -*- coding: utf-8 -*-
"""
Implementación de grafo, tanto dirigido como no dirigido
"""

import random

class Grafo:
    def __init__(self, nombre_='', dirigido=False):
        """
        usar dirigido = True si se esta trabajando con grafo dirigdo
        """
        self.nombre = nombre_
        self.vertices = {}
        self.dirigido = dirigido

    def __contains__(self, vertice): #Para usarlo: print "A" in Grafo
        return (vertice in self.vertices)

    def __str__(self): #Para usarlo: print Grafo
        def vertice2str(n):
            if n in self:
                vertice_str = str(n) + " : " + str(self.vertices[n])
                return vertice_str
            else:
                return False
                
        grafo_str = "Grafo nombre: "+ self.nombre + "\n"
        if len(self) == 0:
            grafo_str += "- Grafo vacio -\n"
        else:
            for n in self.vertices:
                grafo_str += vertice2str(n) + "\n"
        return grafo_str
    
    def __len__(self): #Para usarlo: len(Grafo)
        return len(self.vertices)

    def __iter__(self):#Para usarlo: for i in iter(Grafo): print i
        return iter(self.vertices.keys())

    def agregarVertices(self, lista_vertices, G = None):
        for n in lista_vertices:
            self.agregar(n, G)

    def agregarArista(self, n1, n2, peso=1):
        if not n1 in self.vertices:
            self.vertices[n1] = {}
        self.vertices[n1][n2] = peso

        if self.dirigido is False:
            if not n2 in self.vertices:
                self.vertices[n2] = {}
            self.vertices[n2][n1] = peso

        return True
    
    def agregar(self, n, G = None):
        if not n in self:
            self.vertices[n] = {}

        if G:
            if n in G:
                self.vertices[n] = G.getAristas(n)

    def verticeAleatorio(self):
        n = random.choice(self.vertices.keys())
        return (n, self.vertices[n])
    
    def contarAristas(self, vertice=None): #se puede mencionar el vertice
        if vertice:
            return len(self.vertices[vertice])
        else:
            if self.dirigido:
                return sum(map(lambda x: len(self.vertices[x]), self.getVertices()))
            else:
                return sum(map(lambda x: len(self.vertices[x]), self.getVertices()))/2

    def grado(self, n = None):
        return len(self.getAristas(n))

    def tamano(self):
        return len(self.vertices)
        
    def peso(self):
        w = 0
        for n in self.vertices.values():
            w += sum(n.values())
        if not self.dirigido:
            w = w/2
            
        return w
    
    def getNombre(self):
        return self.nombre

    def getVertices(self):
        return self.vertices.copy()

    def getPeso(self, n1, n2):
        """
        Obtiene el peso de un arco unido entre n1 y n2
        
        si n1 y n2 son iguales, retorna 0

        Si n1 y n2 pertenecen al grafo, pero no son adyacentes, retorna Infinite

        Si n1 o n2 no estan en el grado, retorna False
        """
        if n1 in self and n2 in self:
            if n2 in self.vertices[n1]:
                return self.vertices[n1][n2]
            elif n1 == n2:
                return 0
            return float("inf")
        return False

    def getAristas(self, n = None):
        if n:
            if n in self:
                return self.vertices[n]
            else:
                return None
        aristas = []
        for n in self:
            for v in self.vertices[n]:
                aristas.append( (n, v, self.vertices[n][v]) )
        return aristas


    def esDirigido(self):
        return self.dirigido