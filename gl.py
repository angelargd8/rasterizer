#from ctypes.wintypes import POINT
import struct #para generar tipo de variables con el tamaño especifico
from math import tan, pi
from tkinter import SEL  #para generar tipo de variables con el tamaño especifico
from camara import Camara
import random

#funciones para asegurar el tamaño: 
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

                        

    def glPoint(self, x, y, color = None):
        # Pygame empieza a renderizar desde la esquina 
        # superior izquierda. Hay que volter el valor 
        if (0<=x<self.width) and (0 <= y <self.height):
            # Pygame recibe los colores en un rango de 0 a 255
            color = [int(i * 255) for i in (color or self.currColor)]
            self.screen.set_at((x, self.height - 1 - y), color)
            self.frameBuffer[x][y] = color           


    def glLine(self, vo,  v1, color = None):
        # y = mx + b
        xo = int(vo[0])
        x1 = int(v1[0])
        yo = int(vo[1])
        y1 = int(v1[1])

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
            
            vertexBuffer  = []
            
            #en el modelo hay que agarrar las caras y los vertices
            #por cada cara del modelo
            for face in model.faces: 
                # revisamos cuntos vertices tiene la cara
                #cuatro vertices, hay que crear un segundo triangulo
                vertCount = len(face)
                #obtenemos los vertices de la cara actual 
                v0 = model.vertices[face[0][0] - 1] #-1 porque en el obj los indices empiezan en 1
                v1 = model.vertices[face[1][0] - 1]
                v2 = model.vertices[face[2][0] - 1]
                
                if vertCount == 4:
                    if len(face[3])>0:
                        v3 = model.vertices[face[3][0]-1]
                    else: 
                        continue
                    
                #SI contmos un vertex shader, se manda 
                #cada vertice para transformalor. recordr
                #pasar las matrices necesrias para usarlas
                #dentro del shader    
                if self.vertexShader:
                    v0 = self.vertexShader(v0, modelMatrix = mMat, viewMatrix = self.camara.GetViewMatrix(), projectionMatrix = self.projectionMatrix, viewportMatrix = self.viewportMatrix)
                    v1 = self.vertexShader(v1, modelMatrix = mMat, viewMatrix = self.camara.GetViewMatrix(), projectionMatrix = self.projectionMatrix, viewportMatrix = self.viewportMatrix)
                    v2 = self.vertexShader(v2, modelMatrix = mMat, viewMatrix = self.camara.GetViewMatrix(), projectionMatrix = self.projectionMatrix, viewportMatrix = self.viewportMatrix)
                    if vertCount==4:
                        v3 = self.vertexShader(v3, modelMatrix = mMat, viewMatrix = self.camara.GetViewMatrix(), projectionMatrix = self.projectionMatrix, viewportMatrix = self.viewportMatrix)
                
                vertexBuffer.append(v0)
                vertexBuffer.append(v1)
                vertexBuffer.append(v2)
                
                if vertCount == 4:
                    vertexBuffer.append(v0)
                    vertexBuffer.append(v2)
                    vertexBuffer.append(v3)
             
                            
                #dibujar la cara
                #self.glPoint(int(v0[0]),int(v0[1])) #x,y
                #self.glPoint(int(v1[0]),int(v1[1]))
                #self.glPoint(int(v2[0]),int(v2[1]))
                #if vertCount == 4:
                #    self.glPoint(int(v3[0]),int(v3[1]))
                    
                #dibujar la cara conlineas
                #self.glLine((v0[0],v0[1]), (v1[0],v1[1]))
                #self.glLine((v1[0],v1[1]), (v2[0],v2[1]))
                #self.glLine((v2[0],v2[1]), (v0[0],v0[1]))
                #if vertCount == 4: 
                 #   self.glLine((v0[0],v0[1]), (v2[0],v2[1]))
                 #   self.glLine((v2[0],v2[1]), (v3[0],v3[1]))
                 #   self.glLine((v3[0], v3[1]), (v0[0],v0[1]))
                 
            self.glDrawPrimitives(vertexBuffer)
       
    def glTriangle(self,A, B, C, color=None):
        if A[1] < B[1]:
            A, B = B, A
        if A[1] < C[1]:
            A, C = C, A
        if B[1] < C[1]:
            B, C = C, B
            
        # self.glLine( (A[0], A[1]) , (B[0],B[1]) )
        # self.glLine( (B[0], B[1]) , (C[0],C[1]) )
        # self.glLine( (C[0], C[1]) , (A[0],A[1]) )

        def flatBottom(vA, vB, vC):
            try: #por si es partido 0
                mBA = (vB[0] - vA[0]) / (vB[1] - vA[1])
                mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
            except: 
                pass
            
            else: 
                #dibujar una linea de un punto a otro, pero primero que salgan los puntos xd
                x0 = vB[0]
                x1 = vC[0]
                for y in range( int(vB[1]), int(vA[1])  ): #  que vaya de 2 en 2
                    self.glLine([x0, y], [x1, y], color)
                    #x0 += 1/mBA
                    #x1 += 1/mCA
                    x0 += mBA   
                    x1 += mCA 
                    
        def flatTop(vA, vB, vC):
            try: #por si es partido 0

                mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
                mCB = (vC[0] - vB[0]) / (vC[1] - vB[1])
                
            except: 
                pass
            else: 
                #dibujar una linea de un punto a otro, pero primero que salgan los puntos xd
                x0 = vA[0]
                x1 = vB[0]
                
                for y in range( int(vA[1]), int(vC[1]),-1): # -1 para que vaya hacia abajo
                    self.glLine([x0, y,], [x1, y], color)
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

    def glDrawPrimitives(self, buffer):
        if self.primitiveType == POINTS:
                for point in buffer: 
                    self.glPoint(int(point[0]),int(point[1]))
                        
        elif self.primitiveType == LINES: 
            for i in range(0, len(buffer), 3):
                p0 = buffer[i]
                p1 = buffer[i+1]
                p2 = buffer[i+2]
                #p0 en x, p0 en y, p1 en x, p1 en y
                self.glLine((p0[0], p0[1]), (p1[0], p1[1]))
                self.glLine((p1[0], p1[1]), (p2[0], p2[1]))                
                self.glLine((p2[0], p2[1]), (p0[0], p0[1]))  
         
        elif self.primitiveType == TRIANGLES: 
            for i in range(0, len(buffer), 3):
                p0 = buffer[i]
                p1 = buffer[i+1]
                p2 = buffer[i+2]
                
                color= [random.random(), random.random(), random.random()]

                self.glTriangle(p0, p1, p2, color)
                
