#!/usr/bin/python
# -*- coding: utf-8 -*-
import cmath
import math
from Tkinter import *

class Ventana:
    def __init__(self, tamano):
        self.tamano = tamano
        self.ventana = Tk()
        self.ventana.title('Vehiculos')
        # self.ventana.geometry("1000x500")
        self.ventana.geometry(str(tamano['ancho']) + "x" + str(tamano['alto']))
        # self.ventana.geometry(tamano['ancho'], tamano['alto'])
        self.canvas = Canvas(width=tamano['ancho'], height=tamano['alto'], bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)

        self.dibujarVias()

    def dibujarVias(self):
        anchoVia = 100
        # Se dibuja en la mitad
        limiteSuperior = (self.tamano['alto'] / 2) - (anchoVia / 2)
        limiteInferior = (self.tamano['alto'] / 2) + (anchoVia / 2)
        lineaDivisionCarril = limiteSuperior + ((limiteInferior - limiteSuperior) / 2)
        self.via = {'ancho': anchoVia, 'limiteSuperior': limiteSuperior, 'limiteInferior': limiteInferior, 'divisionCarriles': lineaDivisionCarril}

        # Dibuja via
        self.canvas.create_line(0, limiteSuperior, self.tamano['ancho'], limiteSuperior, width=2)
        self.canvas.create_line(0, limiteInferior, self.tamano['ancho'], limiteInferior, width=2)

        self.canvas.create_line(0, lineaDivisionCarril, self.tamano['ancho'], lineaDivisionCarril, width=1, fill='gray')

    def dibujarOvalos(self, particulas):
        for particula in particulas:
            x = particula.posicion[0]
            y = particula.posicion[1]

            self.canvas.delete(particula.dibujo)  # Borra el dibujo anterior

            # Dibuja el circulo
            coord = x, y, x + particula.height, y + particula.width
            xy = [(coord[0], coord[1]), (coord[0], coord[3]), (coord[2], coord[3]), (coord[2], coord[1])]
            dibujo = self.canvas.create_polygon(xy, fill=particula.color)
            angle = cmath.exp(math.radians(particula.angle) * 1j)
            center = x + (particula.height / 2), y + (particula.width / 2)
            offset = complex(center[0], center[1])
            newxy = []
            for x, y in xy:
                v = angle * (complex(x, y) - offset) + offset
                newxy.append(v.real)
                newxy.append(v.imag)
            self.canvas.coords(dibujo, *newxy)
            particula.setDibujo(dibujo)

    def mostrar(self):
        self.ventana.mainloop()
