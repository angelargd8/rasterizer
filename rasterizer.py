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
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()
rend = Render(screen)
rend.vertexShader = vertexShader
modelo1 = Model("pollo.obj") #cargar el modelo
#modelo1.translate[0] = width/2         #x
modelo1.translate[1] = -1 #height/2#1.7  #y
modelo1.translate[2] = -5               #z
modelo1.scale[0]=0.5
modelo1.scale[1]=0.5
modelo1.scale[2]=0.5
modelo1.rotate[0] = 0
modelo1.rotate[1] = 250#180#250
modelo1.rotate[2] = 0
rend.models.append(modelo1) #agregar el modelo a la lista de modelos
#rend.glColor(1, 0, 0.5) #lineas
#rend.glClearColor(0.5, 1, 1) #fondo

def resetCamara():
    rend.camara.translate = [0,0,0]
    rend.camara.rotate = [0,0,0]

isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_SPACE:
                rend.glGenerateFrameBuffer("DutchAngleShot.bmp")
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
                pass
            
            #medium shot
            elif event.key == pygame.K_a:
                resetCamara()
                rend.camara.translate[2] -= 2.5
                rend.camara.translate[1] += 1
                if event.key == pygame.K_s:
                    rend.glGenerateFrameBuffer("MediumShot.bmp")

            #low angle shot
            elif event.key == pygame.K_b:
                resetCamara()
                rend.camara.rotate[0] -= 35
                rend.camara.translate[1] += 3
                rend.camara.translate[2] -= 1
                if event.key == pygame.K_s:
                    rend.glGenerateFrameBuffer("LowAngleShot.bmp")              

            #high angle shot
            elif event.key == pygame.K_c:
                resetCamara()
                rend.camara.translate[2] -= 2
                rend.camara.translate[1] -= 3
                rend.camara.translate[0] -=0.1
                rend.camara.rotate[1] -=4
                rend.camara.rotate[0] = 35
                if event.key == pygame.K_s:
                    rend.glGenerateFrameBuffer("HighAngleShot.bmp")

            #Dutch angle shot
            elif event.key == pygame.K_d:
                resetCamara()
                rend.camara.rotate[2] = 20
                if event.key == pygame.K_s:
                    rend.glGenerateFrameBuffer("DutchAngleShot.bmp")
            #reset camara
            elif event.key == pygame.K_r:
                resetCamara()


    rend.glClear()
    rend.glRender()
    pygame.display.flip()
    clock.tick(60)


rend.glGenerateFrameBuffer("output.bmp")
pygame.quit()