
import pygame
from pygame.locals import *
from gl import *
from model import Model
from shaders import vertexShader

#traslacion: mover un objeto de un punto a otro, x, y,z
#escala: tamanio del objeto, x, y, z
#rotacion: rotar un objeto en x, y, z

width = 400
height = 400
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()
rend = Render(screen)
rend.vertexShader = vertexShader

modelo1 = Model("face.obj") #cargar el modelo
#modelo1.translate[0] = width/2
modelo1.translate[1] = -1 #height/2#1.7
modelo1.translate[2] = -5

modelo1.scale[0]=0.1
modelo1.scale[1]=0.1
modelo1.scale[2]=0.1

rend.models.append(modelo1) #agregar el modelo a la lista de modelos

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
                rend.primitiveType = LINES
                

    rend.glClear()
    
    rend.glRender()
   
    pygame.display.flip()
    clock.tick(60)

rend.glGenerateFrameBuffer("output.bmp")
pygame.quit()