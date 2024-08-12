
import pygame
from pygame.locals import *
from gl import *
from model import Model
from shaders import  vertexShader, unlitShader, gouradShader, flatShader, toonShader, blueToonShader,glowShader, WaterShader, holographicShader, iridescentShader

#traslacion: mover un objeto de un punto a otro, x, y,z
#escala: tamanio del objeto, x, y, z
#rotacion: rotar un objeto en x, y, z

# width = 800 
# height = 540
width = 514 #
height = 514
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.vertexShader = vertexShader
rend.fragmentShader = unlitShader

# puntoA = [50, 50, 0]
# puntoB = [250, 500, 0]
# puntoC = [500, 50, 0]

def Modelo(translate0, translate1, translate2, scale0, scale1, scale2, fragmentShader):
    modelo = Model("models/model.obj") #cargar el modelo
    modelo.LoadTexture("textures/model.bmp") #cargar la textura)
    modelo.vertexShader = vertexShader
    modelo.fragmentShader = fragmentShader
    modelo.translate[0] = translate0
    modelo.translate[1] = translate1
    modelo.translate[2] = translate2
    modelo.scale[0] = scale0
    modelo.scale[2] = scale1
    modelo.scale[1] = scale2
    return modelo

modelo1  = Modelo(0, 0, -10, 1.5, 1.5, 1.5, unlitShader)
modelo2  = Modelo(3, 0, -10, 1.5, 1.5, 1.5, gouradShader)
modelo3  = Modelo(0, 0, -8, 1.5, 1.5, 1.5, toonShader)
modelo4  = Modelo(-3, 0, -10, 1.5, 1.5, 1.5, flatShader)
modelo5  = Modelo(0, 0, -10, 1.5, 1.5, 1.5, blueToonShader)
modelo6  = Modelo(0, 0, -10, 1.5, 1.5, 1.5, glowShader)
modelo7  = Modelo(3, 0, -10, 1.5, 1.5, 1.5, WaterShader)
modelo8  = Modelo(-3, 0, -10, 1.5, 1.5, 1.5, holographicShader)
modelo9  = Modelo(0, 0, -8, 1.5, 1.5, 1.5, iridescentShader)

#rend.models.append(modelo9) #agregar el modelo a la lista de modelos
#rend.models.append(modelo2)
#rend.models.append(modelo3)
#rend.models.append(modelo4)

rend.models.append(modelo7)
rend.models.append(modelo8)
rend.models.append(modelo9)

#rend.glColor(1, 0, 0.5) #lineas
#rend.glClearColor(0.5, 1, 1) #fondo
     
isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_SPACE or event.key == pygame.K_s:
                rend.glGenerateFrameBuffer("output.bmp")
                
            elif event.key == pygame.K_RIGHT:
                rend.camara.translate[0] += 10
                
            elif event.key == pygame.K_LEFT:
                rend.camara.translate[0] -= 10
                
            elif event.key == pygame.K_UP:
                rend.camara.translate[1] += 10
                
            elif event.key == pygame.K_DOWN:
                rend.camara.translate[1] -= 10
                
            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS
                
            elif event.key == pygame.K_2:
                rend.primitiveType = LINES
            
            elif event.key == pygame.K_3:
                rend.primitiveType = TRIANGLES
                

    rend.glClear()
    
    rend.glRender()

    #rend.glTriangle(puntoA, puntoB, puntoC)
   
    pygame.display.flip()
    clock.tick(60)

rend.glGenerateFrameBuffer("output.bmp")
pygame.quit()