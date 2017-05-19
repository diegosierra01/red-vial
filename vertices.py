# -*- coding: utf-8 -*-


class Vertices:
    def __init__(self):
        self.vertices = []

    def __len__(self):  
        return len(self.vertices)

    def __iter__(self):  
        return iter(self.vertices)

    def agregar(self, vertice):
        if len(self.vertices) == 0:
            self.vertices.append(vertice)
        else:
            flag = False
            for verticeLista in self.vertices:
                if(verticeLista.position['x'] == vertice.position['x'] and verticeLista.position['y'] == vertice.position['y']):
                    flag=True
            if not flag:
                self.vertices.append(vertice)        
                

    def agregarVertices(self, vertices):
        for vertice in vertices:
            self.vertices.append(vertice)

    def obtener(self, nombre):
        for vertice in self.vertices:
            if vertice.nombre == nombre:
                return vertice
    def obtenerUltimoAgregado(self):
        return self.vertices[len(self.vertices)-1]

    def existeVertice(self, position):
        for vertice in self.vertices:
            if vertice.position == position:
                return True
        return False