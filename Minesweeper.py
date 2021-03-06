import pygame
import numpy
import math
import random
from math import floor as sinDecimal

pygame.init()

#prueba cambio git

#unidades
unit = 40
inicial = 60
ladoTablero = 12
cantBombas = sinDecimal(ladoTablero * ladoTablero / 5)

#colores
white = (255, 255, 255)
red = (255, 0, 0)
pink = (200, 0, 0)
black = (0,0,0)
grey = (96, 96,  96)
green = (0, 255, 0)

#foto granada
granada = pygame.image.load("granada.png")
sizeFoto = (sinDecimal(unit/2), sinDecimal(unit*0.8))
granada = pygame.transform.scale(granada, sizeFoto)

#foto bandera
banderita = pygame.image.load("banderita.png")
sizeFoto = (sinDecimal(unit/2), sinDecimal(unit*0.8))
banderita = pygame.transform.scale(banderita, sizeFoto)

#dibujar ventana
gameDisplay = pygame.display.set_mode((600,600))
gameDisplay.fill(white)
pygame.display.set_caption('Minesweeper')

clock = pygame.time.Clock()

#clase
class Square():
    def __init__(self, x, y, esBomba):
        self.x = x
        self.y = y
        self.width = unit
        self.height = unit
        self.esBomba = esBomba
        self.num = -1
        self.wasPressed = False
        self.bandera = False

    def draw(self, color):
        pygame.draw.rect(gameDisplay, color, (self.x, self.y, unit, unit))

    def cambiarNumero(self, n):
        self.num = n

    def mostrarNum(self):
        fuente = pygame.font.SysFont("arial",sinDecimal(unit/2))
        numero = fuente.render(str(self.num), True, black)
        rect = numero.get_rect()
        rect.center = (self.x + sinDecimal(unit/2), self.y + sinDecimal(unit/2))
        gameDisplay.blit(numero, rect)

#funciones
def generarNumBombas():
    posBombas = []

    for i in range(cantBombas):
        num = random.randint(0, (ladoTablero * ladoTablero) - 1)
        while num in posBombas:
            num = random.randint(0, (ladoTablero * ladoTablero) - 1)
        posBombas.append(num)

    return posBombas

def turnNumToPos(num):
    i = sinDecimal(num / ladoTablero)
    j = num % ladoTablero
    pos = [i, j]
    return pos

def makeTablero(posBombas):
    tablero = numpy.empty( (ladoTablero,ladoTablero), dtype=object)

    for i in range(ladoTablero):
        for j in range(ladoTablero):
            if [i, j] in posBombas:
                esBomba = True
            else:
                esBomba = False
            tablero[i][j] = Square(inicial + unit * j, inicial + unit * i, esBomba)

    return tablero

def generarNumeros(tablero):
    for i in range(ladoTablero):
        for j in range(ladoTablero):
            if not tablero[i][j].esBomba:
                bombasAlrededor = 0
                
                if j - 1 >= 0 and i - 1 >= 0: #arriba izq
                    if tablero[i-1][j-1].esBomba:
                        bombasAlrededor += 1
                if i - 1 >= 0: #arriba
                    if tablero[i-1][j].esBomba:
                        bombasAlrededor += 1
                if j + 1 <= ladoTablero-1 and i - 1 >= 0: #arriba der
                    if tablero[i-1][j+1].esBomba:
                        bombasAlrededor += 1
                if j - 1 >= 0: #izq
                    if tablero[i][j-1].esBomba:
                        bombasAlrededor += 1
                if j + 1 <= ladoTablero-1: #der
                    if tablero[i][j+1].esBomba:
                        bombasAlrededor += 1
                if j - 1 >= 0 and i + 1 <= ladoTablero-1: #abajo izq
                    if tablero[i+1][j-1].esBomba:
                        bombasAlrededor += 1
                if i + 1 <= ladoTablero-1: #abajo
                    if tablero[i+1][j].esBomba:
                        bombasAlrededor += 1
                if j + 1 <= ladoTablero-1 and i + 1 <= ladoTablero-1: #abajo der
                    if tablero[i+1][j+1].esBomba:
                        bombasAlrededor += 1

                tablero[i][j].cambiarNumero(bombasAlrededor)

def drawTablero(tablero):

    perdio = False
    
    for i in range(ladoTablero):
        for j in range(ladoTablero):
            if (i % 2 == 0):
                if (j % 2 == 0):
                    color = red
                else:
                    color = pink
            else:
                if (j % 2 == 0):
                    color = pink
                else:
                    color = red
            tablero[i][j].draw(color)
            if tablero[i][j].bandera:
                rectFoto = banderita.get_rect()
                rectFoto.center = (tablero[i][j].x + sinDecimal(unit/2), tablero[i][j].y + sinDecimal(unit/2))
                gameDisplay.blit(banderita, rectFoto)
            else:
                if tablero[i][j].wasPressed:
                    if tablero[i][j].num != -1:
                        if tablero[i][j].num != 0:
                            tablero[i][j].draw(grey)
                            tablero[i][j].mostrarNum()
                        else:
                            tablero[i][j].draw(grey)
                    else:
                        rectFoto = granada.get_rect()
                        rectFoto.center = (tablero[i][j].x + sinDecimal(unit/2), tablero[i][j].y + sinDecimal(unit/2))
                        gameDisplay.blit(granada, rectFoto)
                        perdio = True
    return perdio

def presionarAlrededor(tablero, i, j):
    if j - 1 >= 0 and i - 1 >= 0 and not tablero[i-1][j-1].wasPressed: #arriba izq
        tablero[i-1][j-1].wasPressed = True
        if tablero[i-1][j-1].num == 0:
            presionarAlrededor(tablero, i-1, j-1)
    if i - 1 >= 0 and not tablero[i-1][j].wasPressed: #arriba
        tablero[i-1][j].wasPressed = True
        if tablero[i-1][j].num == 0:
            presionarAlrededor(tablero, i-1, j)
    if j + 1 <= ladoTablero-1 and i - 1 >= 0 and not tablero[i-1][j+1].wasPressed: #arriba der
        tablero[i-1][j+1].wasPressed = True
        if tablero[i-1][j+1].num == 0:
            presionarAlrededor(tablero, i-1, j+1)
    if j - 1 >= 0 and not tablero[i][j-1].wasPressed: #izq
        tablero[i][j-1].wasPressed = True
        if tablero[i][j-1].num == 0:
            presionarAlrededor(tablero, i, j-1)
    if j + 1 <= ladoTablero-1 and not tablero[i][j+1].wasPressed: #der
        tablero[i][j+1].wasPressed = True
        if tablero[i][j+1].num == 0:
            presionarAlrededor(tablero, i, j+1)
    if j - 1 >= 0 and i + 1 <= ladoTablero-1 and not tablero[i+1][j-1].wasPressed: #abajo izq
        tablero[i+1][j-1].wasPressed = True
        if tablero[i+1][j-1].num == 0:
            presionarAlrededor(tablero, i+1, j-1)
    if i + 1 <= ladoTablero-1 and not tablero[i+1][j].wasPressed: #abajo
        tablero[i+1][j].wasPressed = True
        if tablero[i+1][j].num == 0:
            presionarAlrededor(tablero, i+1, j)
    if j + 1 <= ladoTablero-1 and i + 1 <= ladoTablero-1 and not tablero[i+1][j+1].wasPressed: #abajo der
        tablero[i+1][j+1].wasPressed = True
        if tablero[i+1][j+1].num == 0:
            presionarAlrededor(tablero, i+1, j+1)

def gameOver():
    
    pygame.draw.rect(gameDisplay, black, (140, 210, 320, 170))#borde
    pygame.draw.rect(gameDisplay, red, (150, 220, 300, 150))
    
    fuente = pygame.font.SysFont("arial",50)
    msg = fuente.render("GAME OVER", True, black)
    rect = msg.get_rect()
    rect.center = (300, 295)
    gameDisplay.blit(msg, rect)

def mostrarTodasLasBombas(posBombas):

    for i in range(ladoTablero):
        for j in range(ladoTablero):
            if [i, j] in posBombas:
                rectFoto = granada.get_rect()
                rectFoto.center = (tablero[i][j].x + sinDecimal(unit/2), tablero[i][j].y + sinDecimal(unit/2))
                gameDisplay.blit(granada, rectFoto)

def retry():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    isHovering = mouse[0] > 140 and mouse[0] < 460 and mouse[1] > 380 and mouse[1] < 550

    pygame.draw.rect(gameDisplay, black, (140, 380, 320, 100))#borde
    pygame.draw.rect(gameDisplay, green, (150, 390, 300, 80))
    fuente = pygame.font.SysFont("arial",30)
    msg = fuente.render("RETRY", True, black)
    rect = msg.get_rect()
    rect.center = (300, 420)
    gameDisplay.blit(msg, rect)

    pressed = click[0] == 1 and isHovering

    return pressed

def victoria():
    
    pygame.draw.rect(gameDisplay, black, (140, 210, 320, 170))#borde
    pygame.draw.rect(gameDisplay, green, (150, 220, 300, 150))
    
    fuente = pygame.font.SysFont("arial",35)
    msg = fuente.render("CONGRATULATIONS", True, black)
    rect = msg.get_rect()
    rect.center = (300, 295)
    gameDisplay.blit(msg, rect)


def cuadradoMouse():
    mouse = pygame.mouse.get_pos()

    i = sinDecimal((mouse[1] - inicial) / 40)
    j = sinDecimal((mouse[0] - inicial) / 40)

    if i > ladoTablero - 1:
        i = ladoTablero - 1
    if j > ladoTablero - 1:
        j = ladoTablero - 1

    return i, j

def accionesMouse(tablero):
    click = pygame.mouse.get_pressed()
    i, j = cuadradoMouse() #i es posY, j es posX
    bombasEncontradas = 0

    if not tablero[i][j].wasPressed:
        tablero[i][j].draw((255, 100, 100))

    if click[0] == 1:
        tablero[i][j].wasPressed = True
        tablero[i][j].bandera = False
        if tablero[i][j].num == 0:
            presionarAlrededor(tablero, i, j)
    if click[2] == 1 and not tablero[i][j].wasPressed:
        if tablero[i][j].bandera:
            tablero[i][j].bandera = False
            if tablero[i][j].esBomba:
                bombasEncontradas -= 1
        else:
            tablero[i][j].bandera = True
            if tablero[i][j].esBomba:
                bombasEncontradas += 1
    
    return bombasEncontradas
            

while True:
    #inicializacion
    print(cantBombas)
    cantBombasEncontradas = 0
    numBombas = generarNumBombas()
    posBombas = []
    for i in range(cantBombas):
        posBombas.append(turnNumToPos(numBombas[i]))

    tablero = makeTablero(posBombas)
    generarNumeros(tablero)
    perdio = False
    tiempoEspera = 0
    pasoTiempoEspera = False

    #Main Loop
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if not perdio:
            perdio = drawTablero(tablero)
            cantBombasEncontradas += accionesMouse(tablero)
            if cantBombasEncontradas == cantBombas:
                victoria()
                if tiempoEspera < 20 and not pasoTiempoEspera:
                    tiempoEspera += 1
                else:
                    pasoTiempoEspera = True
                    if retry():
                        pygame.time.wait(300)
                        break
        else:
            mostrarTodasLasBombas(posBombas)
            if tiempoEspera < 60 and not pasoTiempoEspera:
                tiempoEspera += 1
            else:
                pasoTiempoEspera = True
                gameOver()
                if retry():
                    pygame.time.wait(300)
                    break

        pygame.display.update()
        clock.tick(30)
