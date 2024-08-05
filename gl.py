#from ctypes.wintypes import POINT
import struct #para generar tipo de variables con el tama�o especifico
from math import tan, pi
from tkinter import SEL
from turtle import position  #para generar tipo de variables con el tama�o especifico
from camara import Camara
import random
from Mathlib import barycentricCoords
from shaders import vertexShader

#funciones para asegurar el tama�o: 
def char(c): #lo que sea de tipo char, lo va a convertir en 1 byte
    #para crear una variable que ocupe 1 byte
    return struct.pack("=c", c.encode("ascii")) #"=c" que sea de tipo char

def word(w): #lo que sea de tipo word, lo va a convertir en 2 bytes
    #para crear una variable que ocupe 2 bytes
    return struct.pack("=h", w) #"=h" que sea de tipo short

def dword(d): #lo que sea de tipo dword, lo va a convertir en 4 bytes
    #para crear una variable que ocupe 4 bytes
    return struct.pack("=l", d) #"=l" que sea de tipo long

POINTS = 0
LINES = 1
TRIANGLES = 2

class Render(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        
        self.camara = Camara()
        self.glViewport(0,0, self.width, self.height)
        self.glProjection()

        self.glColor(1,1,1)
        self.glClearColor(0,0,0)
        self.glClear()

        self.vertexShader=None
        self.fragmentShader=None
        
        self.primitiveType = POINTS
        
        self.models =[]
    
    def glViewport(self, x, y, width, height):
        self.vpX = int(x) #posicion en x
        self.vpY = int(y) #posicion en y
        self.vpWidth = width #ancho
        self.vpHeight = height #alto

        self.viewportMatrix = [[width/2, 0, 0, x + width/2],
                                [0, height/2, 0, y + height/2],
                                [0, 0, 0.5, 0.5],
                                [0, 0, 0, 1]]
    
    def glProjection(self,n = 0.1, f= 1000, fov = 60): # n es el near, f es el far, fov = angulo de vista y esta en grados
        aspectRatio = self.vpWidth/ self.vpHeight
        fov *=  pi/180 #convertir a radianes
        #t = tangente
        t = tan(fov/2) * n #tangente de la mitad del angulo de vista por el near
        r = t * aspectRatio #tangente por el aspect ratio

        #construir la matriz de proyeccion
        
        self.projectionMatrix = [[n/r,0,0,0],
                                [0,n/t,0,0],
                                [0,0,-(f+n)/(f-n),-(2*f*n)/(f-n)],
                                [0,0,-1,0]]
        
           

    def glColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.currColor = [ r, g, b]

    def glClearColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.clearColor = [r,g,b]

    def glClear(self):
        color = [int(i * 255) for i in self.clearColor] #convertir a entero
        self.screen.fill(color)

        self.frameBuffer = [[self.clearColor for y in range(self.height)]
                    for x in range(self.width)]
        
        self.zbuffer = [[float('inf') for y in range(self.height)]
					   for x in range(self.width)]

                        

    def glPoint(self, x, y, color = None):
        # Pygame empieza a renderizar desde la esquina 
        # superior izquierda. Hay que volter el valor 
        x = round(x)
        y = round(y)
        
        if (0<=x<self.width) and (0 <= y <self.height):
            # Pygame recibe los colores en un rango de 0 a 255
            color = [int(i * 255) for i in (color or self.currColor)]
            self.screen.set_at((x, self.height - 1 - y), color)
            self.frameBuffer[x][y] = color           


    def glLine(self, vo,  v1, color = None):
        # y = mx + b
        # xo = round(vo[0])
        # x1 = round(v1[0])
        # yo = round(vo[1])
        # y1 = round(v1[1])
        xo = vo[0]
        x1 = v1[0]	
        yo = vo[1]	
        y1 = v1[1]

        # Algoritmo de Lineas de Bresenham

        #Si el punto 0 es igual punto 1, solo se dibuja un punto
        if xo == x1 and yo == y1:
            self.glPoint(xo,yo)
            return
        
        dy = abs(y1 - yo)
        dx = abs(x1 - xo) 

        steep = dy > dx

        if steep:
            xo, yo = yo, xo
            x1, y1 = y1, x1
        
        if xo > x1:
            xo, x1 = x1, xo
            yo, y1 = y1, yo

        dy = abs(y1 - yo)
        dx = abs(x1 - xo) 

        offset = 0
        limit = 0.75
        m = dy / dx
        y = yo

        for x in range(xo, x1 + 1):

            if steep:
                self.glPoint(y, x, color or self.currColor)
            else:
                self.glPoint(x, y, color or self.currColor)

            offset += m

            if offset >= limit:
                if yo < y1:
                    y += 1
                else:
                    y -= 1
                limit += 1

#Generacion del frame buffer
    def glGenerateFrameBuffer(self, filename):
        with open(filename, "wb") as file: 
            # header 14 bytes
            # signature (2 bytes) | file size (4 bytes) | reserved (4 bytes) | offset (4 bytes)
            file.write(char("B")) #1 byte
            file.write(char("M")) #1 byte
            #info header 40 bytes
            file.write(dword(14 + 40 + (self.width * self.height *3 )))
            #reserved
            file.write(dword(0)) 
            #offset
            file.write(dword(14+40)) 

            #info header
            #size
            file.write(dword(40))
            #width
            file.write(dword(self.width))
            #height
            file.write(dword(self.height))
            #planes
            file.write(word(1))
            # bits per pixel
            #depende de cuanto bits le diga, este va a interpretar el interpretador de imagenes cuantos bits representan un pixel, aca es donde va la profundidad
            file.write(word(24)) # (rgb) = (8,8,8) bits 8+8+8=24 = 1pixel
            #compression
            file.write(dword(0)) #0 para decirle que no tiene compression
            #image size
            file.write(dword(self.width*self.height* 3))
            #todaslasdemas tienen 4 bytes, realmente no importan
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #color table, donde se va a guardar todos los colores
            #recorre la cuadricula entera
            #pasa en cada x y y y agarra el color del lugar y se escribe en el archivo
            for y in range(self.height):
                for x in range(self.width):
                    color =self.frameBuffer[x][y]
                    color = bytes([color[2],
                                   color[1],
                                   color[0]])
                    file.write(color) 

    def glRender(self):
        
        for model in self.models: 
            #por cada modelo en la list, los dibujo
            # agarrar su matriz modelo 
            mMat  = model.GetModelMatrix()
            
            # Aqui vamos a guardar todos los vertices y su info correspondiente
            vertexBuffer  = []
            
            #en el modelo hay que agarrar las caras y los vertices
            #por cada cara del modelo
            for face in model.faces: 
                # Aqui vamos a guardar los vertices de esta cara
                faceVerts = []
                
                for i in range(len(face)):
					
                    # Aqui vamos a guardar los valores individuales de 
                    # posicion, coordenadas de textura y normales
                    vert = []
                    # Obtenemos los vertices de la cara actual
                    pos = model.vertices[face[i][0]- 1]
                
               
                    
                #SI contmos un vertex shader, se manda 
                #cada vertice para transformalor. recordr
                #pasar las matrices necesrias para usarlas
                #dentro del shader    
                if self.vertexShader:
                    pos = self.vertexShader(pos, 
                                            modelMatrix = mMat,
                                            viewMatrix = self.camara.GetViewMatrix(),
                                            projectionMatrix = self.projectionMatrix,
                                            viewportMatrix = self.viewportMatrix)
                # Agregamos los valores de posicion al contenedor del vertice
                for value in pos: 
                    vert.append(value)
                    
                # Agregamos la informacion de este vertices a la
				# lista de vertices de esta cara
                faceVerts.append(vert)
                
            # Agregamos toda la informacion de los tres vertices de
            # esta cara de corrido al buffer de vertices. Si hay
            # cuatro vertices, creamos un segundo triangulo
            for value in faceVerts[0]: vertexBuffer.append(value)
            for value in faceVerts[1]: vertexBuffer.append(value)
            for value in faceVerts[2]: vertexBuffer.append(value)
            if len(faceVerts) == 4:
                for value in faceVerts[0]: vertexBuffer.append(value)
                for value in faceVerts[2]: vertexBuffer.append(value)
                for value in faceVerts[3]: vertexBuffer.append(value)

                 
            self.glDrawPrimitives(vertexBuffer, 3)
       
    def glTriangle(self,A, B, C):
        # Hay que asegurar que los vertices entran
		# en orden: Ay > By > Cy
        if A[1] < B[1]:
            A, B = B, A
        if A[1] < C[1]:
            A, C = C, A
        if B[1] < C[1]:
            B, C = C, B
            

        def flatBottom(vA, vB, vC):


            try: #por si es partido 0
                mBA = (vB[0] - vA[0]) / (vB[1] - vA[1])
                mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
            except: 
                pass
            
            else: 
                if vB[0] > vC[0]:
                    vB, vC = vC, vB

                #dibujar una linea de un punto a otro, pero primero que salgan los puntos xd
                x0 = vB[0]
                x1 = vC[0]
                
                for y in range( round(vB[1]), round(vA[1]+1)): #  que vaya de 2 en 2
                    #informacion del pixle en el momento
                    for x in range(round(x0 -1 ),round(x1 +1)): #+1 para incluir al ultimo
                        vP= [x, y]
                        self.glDrawTrianglePoint(vA, vB, vC, vP)
                    x0 += mBA
                    x1 += mCA
                    
                    
                    
        def flatTop(vA, vB, vC):
            
            try: #por si es partido 0

                mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
                mCB = (vC[0] - vB[0]) / (vC[1] - vB[1])
                
            except: 
                pass
            else: 
                if vA[0] > vB[0]:
                    vA, vB = vB,vA
                #dibujar una linea de un punto a otro, pero primero que salgan los puntos xd
                x0 = vA[0]
                x1 = vB[0]
                
                for y in range( round(vA[1]), round(vC[1] - 1), -1):
                    for x in range(round(x0 - 1), round(x1 + 1)):
                        vP =[x, y]
                        self.glDrawTrianglePoint(vA, vB, vC, vP)

                    x0 -= mCA
                    x1 -= mCB  
      

        #3 casos luego de dibujar las lineas
        #b en y es igual a c en y
        if B[1] == C[1]: #La punta esta arriba
            #la parte plana esta abajo y la punta esta arriba
            flatBottom(A,B,C)
                   
        elif A[1] == B[1]: 
            #la parte plana esta arriba y la punta esta abajo
            flatTop(A,B,C)
        
        else:
            #divido el triangulo en dos partes y 
            #dibuja ambos tipos de triangulos
            
            #teorema del intercepto
            #para el valor de x=A[0] + ( (B[1] - A[1])/ (C[1]) - A[1] ) * (C[0] - A[0])
            #para el valor de y el valor de b
            #D = [A[0] + ( (B[1] - A[1])/ (C[1]) - A[1] ) * (C[0] - A[0]) , B[1] ]
            D = [A[0] + ((B[1] - A[1]) / (C[1] - A[1])) * (C[0] - A[0]), B[1]]
            flatBottom(A,B,D)
            flatTop(B,D,C)
         
    def glDrawTrianglePoint(self, A, B, C, P):
        x = P[0]
        y = P[1]
        
        #Si el punto no esta dentro de la ventana, lo descartamos
        if not (0 <= x < self.width) or not (0<=y<self.height):
            return
        #Obtenemos las coordenadas baricentricas del punto P
        #en este triangulo. Si no son validas, no dibujamos
        bCoords= barycentricCoords(A, B, C, P)
        

        if bCoords == None: 
            return
        
        u, v, w = bCoords
        
        #Si contamos un Fragment Shader, obtener el color de ahi
        color = self.currColor
        if self.fragmentShader!=None:
            #Mandar los parAmetros necesarios al shader
            verts = (A, B, C)
            color = self.fragmentShader(verts = verts, 
                                        bCoords = bCoords)
        self.glPoint(x, y, color)


   
    def glDrawPrimitives(self, buffer, vertexOffset):
        # El buffer es un listado de valores que representan
		# toda la informacion de un vertice (posicion, coordenadas
		# de textura, normales, color, etc.). El VertexOffset se
		# refiere a cada cuantos valores empieza la informacion
		# de un vertice individual
		# Se asume que los primeros tres valores de un vertice
		# corresponden a Posicion.


        if self.primitiveType == POINTS:
            # Si son puntos, revisamos el buffer en saltos igual
			# al Vertex Offset. El valor X y Y de cada vertice
			# corresponden a los dos primeros valores.
            
            for i in range(0, len(buffer), vertexOffset):
                x = buffer[i]
                y = buffer[i + 1]
                self.glPoint(x, y)
                        
        elif self.primitiveType == LINES: 
            # Si son lineas, revisamos el buffer en saltos igual
			# a 3 veces el Vertex Offset, porque cada trio corresponde
			# a un triangulo. 
            
            for i in range(0, len(buffer), vertexOffset* 3):
                for j in range(3):
                    # Hay que dibujar la linea de un vertice al siguiente
                    x0 = buffer[i + vertexOffset * j +0]
                    y0 = buffer[i + vertexOffset * j +1]
         
                    #en caso de que sea el ultimo vertice, el siguiente seria el primro
                    x1 = buffer[i+ vertexOffset * ((j+1)%3) + 0]
                    y1 = buffer[i+ vertexOffset * ((j+1)%3) + 1]
                    
                    self.glLine((x0, y0), (x1, y1))
                       
        elif self.primitiveType == TRIANGLES: 
            # Si son triangulos revisamos el buffer en saltos igual
			# a 3 veces el Vertex Offset, porque cada trio corresponde
			# a un triangulo.
            for i in range(0, len(buffer), vertexOffset* 3):
                # Necesitamos tres vertices para mandar a dibujar el triangulo.
				# Cada vertice necesita todos sus datos, la cantidad de estos
				# datos es igual a VertexOffset
                A= [buffer[i + j + vertexOffset * 0] for j in range(vertexOffset)]
                B= [buffer[i + j + vertexOffset * 1] for j in range(vertexOffset)]
                C= [buffer[i + j + vertexOffset * 2] for j in range(vertexOffset)]
                self.glTriangle(A, B, C)
                
