
import pygame
from pygame.locals import *
from gl import *
from model import Model
from shaders import vertexShader

#traslacion: mover un objeto de un punto a otro, x, y,z
#escala: tamanio del objeto, x, y, z
#rotacion: rotar un objeto en x, y, z

width = 960
height = 540
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
rend = Render(screen)
rend.vertexShader = vertexShader

modelo1 = Model("face.obj") #cargar el modelo
modelo1.translate[0] = width/2
modelo1.translate[1] =height/2
modelo1.scale[0]=10
modelo1.scale[1]=10
modelo1.scale[2]=10

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
                modelo1.rotate[1] += 10
            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS
            elif event.key == pygame.K_2:
                rend.primitiveType = LINES
  

    #for i in range(100):
    #    rend.glPoint(480 + i,270 + i)

 #   for x in range(0, width, 10):
  #      rend.glLine((0,0), (x, height))
  #      rend.glLine((0, height - 1), (x, 0))
  #      rend.glLine((width - 1, 0), (x, height))
  #      rend.glLine((width - 1, height - 1), (x, 0))

    rend.glClear
    
    rend.glRender()
   
    pygame.display.flip()
    clock.tick(60)

rend.glGenerateFrameBuffer("output.bmp")
pygame.quit()