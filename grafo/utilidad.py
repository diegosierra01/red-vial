# -*- coding: utf-8 -*-

def dijkstra(Grafo, a, z):
    path, _ = dijkstra_info(Grafo, a, z)
    return path

def dijkstra_info(Grafo, verticeInicial, verticeFinal):

    print "Calculando la ruta mas corta entre ",verticeInicial," y ",verticeFinal
    etiquetas = {n: (n, float('inf')) for n in Grafo.vertices}
    marcas = {}
    etiquetas[verticeInicial] = (verticeInicial, 0)
    marcas[verticeInicial] = 'temp'

    def get_temporary_marks():
        return filter(lambda y: marcas[y] == 'temp', marcas.keys())

    def d_a(n):
        # Returns dist(a, n), where a is the inicial node in the algorithm 
        # and n is a previously marked node
        return etiquetas[n][1]
    
    def antecesor(n):
        return etiquetas[n][0]

    def elegir_vertice(marcas):
        return min(get_temporary_marks(), key= d_a)

    def mejor_ruta(n):
        ruta = [n]
        while ruta[0] != verticeInicial:
            ruta.insert(0, antecesor(ruta[0]))
        return ruta

    def w(n1,n2):
        return Grafo.getPeso(n1,n2)


    while(get_temporary_marks()):
        v = elegir_vertice(marcas)  # TODO, Devuelve el vértice v marcado temporalmente cuya d(a,v) sea menor (los desempates se dan por nomenclatura)
        marcas[v] = 'final'

        if v == verticeFinal:
            return mejor_ruta(verticeFinal), etiquetas
        for k in Grafo.vertices[v]:
            if not marcas.has_key(k):
                marcas[k] = 'temp'
                etiquetas[k] = (v, d_a(v)+w(v,k))
            if marcas[k] == 'temp' and (d_a(v) + w(v,k) < d_a(k)):
                etiquetas[k] = (v, d_a(v) + w(v,k))
    
    print "No existe ruta de '",verticeInicial,"'' a '",verticeFinal,"'"
    return None

def toMatrixAdyacencia(Grafo): # Weight adjacency matrix
    tamano = len(Grafo)
    
    # tags is a dictionary of the previous names of each node.
    # e.g. a possible tag value is  0:"node_name"
    #print zip(range(tamano),G.vertices[:])
    #    print "i:",i,"    n:",n
    tags = {i:n for i, n in zip(range(tamano),sorted(Grafo.vertices.keys()))}
    matrix = [[float("inf") for _ in xrange(tamano)] for _ in xrange(tamano)] 

    for y in xrange(tamano):
        for x in xrange(tamano):
                matrix[y][x] = Grafo.getPeso(tags[y], tags[x])
    return (matrix, tags)