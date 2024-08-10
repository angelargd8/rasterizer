
import pygame
from pygame.locals import *
from gl import *
from model import Model
from shaders import  vertexShader, unlitShader, gouradShader, flatShader, toonShader, blueToonShader

#traslacion: mover un objeto de un punto a otro, x, y,z
#escala: tamanio del objeto, x, y, z
#rotacion: rotar un objeto en x, y, z

width = 960 #
height = 540
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.vertexShader = vertexShader
rend.fragmentShader = unlitShader

puntoA = [50, 50, 0]
puntoB = [250, 500, 0]
puntoC = [500, 50, 0]

modelo1 = Model("models/model.obj") #cargar el modelo
modelo1.LoadTexture("textures/model.bmp") #cargar la textura)
modelo1.vertexShader = vertexShader
modelo1.fragmentShader = blueToonShader
modelo1.translate[0] = 3
modelo1.translate[2] = -10
modelo1.scale[0] =1.5
modelo1.scale[2] =1.5
modelo1.scale[1] =1.5

# modelo1 = Model("models/model.obj") #cargar el modelo
# modelo1.LoadTexture("textures/model.bmp") #cargar la textura)
# modelo1.vertexShader = vertexShader
# modelo1.fragmentShader = unlitShader
# modelo1.translate[0] = 3
# modelo1.translate[2] = -10
# modelo1.scale[0] =1.5
# modelo1.scale[2] =1.5
# modelo1.scale[1] =1.5

# modelo2 = Model("models/model.obj") #cargar el modelo
# modelo2.LoadTexture("textures/model.bmp") #cargar la textura)
# modelo2.vertexShader = vertexShader
# modelo2.fragmentShader = gouradShader
# modelo2.translate[0] = -1
# modelo2.translate[2] = -8
# modelo2.scale[0] =1.5
# modelo2.scale[2] =1.5
# modelo2.scale[1] =1.5



# modelo3 = Model("models/model.obj") #cargar el modelo
# modelo3.LoadTexture("textures/model.bmp") #cargar la textura)
# modelo3.vertexShader = vertexShader
# modelo3.fragmentShader = flatShader
# modelo3.translate[0] = 1
# modelo3.translate[2] = -8
# modelo3.scale[0] =1.5
# modelo3.scale[2] =1.5
# modelo3.scale[1] =1.5


# modelo4 = Model("models/model.obj") #cargar el modelo
# modelo4.LoadTexture("textures/model.bmp") #cargar la textura)
# modelo4.vertexShader = vertexShader
# modelo4.fragmentShader = toonShader
# modelo4.translate[0] = 3
# modelo4.translate[2] = -8
# modelo4.scale[0] =1.5
# modelo4.scale[2] =1.5
# modelo4.scale[1] =1.5


rend.models.append(modelo1) #agregar el modelo a la lista de modelos
# rend.models.append(modelo2)
# rend.models.append(modelo3)
# rend.models.append(modelo4)
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