
import pygame
from pygame.locals import *
from gl import *
from model import Model
from shaders import vertexShader

#traslacion: mover un objeto de un punto a otro, x, y,z
#escala: tamanio del objeto, x, y, z
#rotacion: rotar un objeto en x, y, z

width = 512#960
height =512# 540
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()
rend = Render(screen)
rend.vertexShader = vertexShader

modelo1 = Model("face.obj") #cargar el modelo
#modelo1.translate[0] = width/4
modelo1.translate[1] =-1
modelo1.translate[2] =-5

modelo1.scale[0]=0.1#10
modelo1.scale[1]=0.1#10
modelo1.scale[2]=0.1#10

#modelo2 = Model("model.obj")
#modelo2.translate[0] = width/4 *3
#modelo2.translate[1] =height/2
#modelo2.translate[2] =200

#modelo2.scale[0]=200
#modelo2.scale[1]=200
#modelo2.scale[2]=200
rend.models.append(modelo1) #agregar el modelo a la lista de modelos
#rend.models.append(modelo2)
#rend.glColor(1, 0, 0.5) #lineas
#rend.glClearColor(0.5, 1, 1) #fondo


#triangle1 = [[10,80],[50,160],[70,80]]
#triangle2 = [[180,50],[150,1],[70,180]]
#triangle3 = [[180,120],[120,160],[130,150]]

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
            
            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS
                
            elif event.key == pygame.K_2:
                rend.primitiveType = LINES

            elif event.key == pygame.K_3:
                rend.primitiveType= TRIANGLES
                
            elif event.key == pygame.K_RIGHT:
                rend.camara.translate[0] += 10
                
            elif event.key == pygame.K_LEFT:
                rend.camara.translate[0] -= 10
                
            elif event.key == pygame.K_UP:
                rend.camara.translate[1] += 10
                
            elif event.key == pygame.K_DOWN:
                rend.camara.translate[1] -= 10

    #for i in range(100):
    #    rend.glPoint(480 + i,270 + i)

 #   for x in range(0, width, 10):
  #      rend.glLine((0,0), (x, height))
  #      rend.glLine((0, height - 1), (x, 0))
  #      rend.glLine((width - 1, 0), (x, height))
  #      rend.glLine((width - 1, height - 1), (x, 0))

    rend.glClear()
    
    rend.glRender()
    #rend.glTriangle(triangle1[0], triangle1[1],triangle1[2],)
    #rend.glTriangle(triangle2[0], triangle2[1],triangle2[2],)
    #rend.glTriangle(triangle3[0], triangle3[1],triangle3[2],)
   
    pygame.display.flip()
    clock.tick(60)

rend.glGenerateFrameBuffer("output.bmp")
pygame.quit()