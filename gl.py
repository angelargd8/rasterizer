from ctypes.wintypes import POINT
import struct #para generar tipo de variables con el tamaño especifico

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
        
        self.glColor(1,1,1)
        self.glClearColor(0,0,0)
        self.glClear()

        self.vertexShader=None
        
        self.primitiveType = POINTS
        
        self.models =[]

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
                    v3 = model.vertices[face[3][0]-1]
                    
                #SI contmos un vertex shader, se manda 
                #cada vertice para transformalor. recordr
                #pasar las matrices necesrias para usarlas
                #dentro del shader    
                if self.vertexShader:
                    v0 = self.vertexShader(v0, modelMatrix = mMat)
                    v1 = self.vertexShader(v1, modelMatrix = mMat)
                    v2 = self.vertexShader(v2, modelMatrix = mMat)
                    if vertCount==4:
                        v3 = self.vertexShader(v3, modelMatrix = mMat)
                
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
                
