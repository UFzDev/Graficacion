import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

TAM = 0.25 
RADIO = TAM * 0.35
CENTRO = TAM * 0.5
OFFSET = -1.0

def main():
    pygame.init()
    pygame.display.set_mode((600, 600), DOUBLEBUF | OPENGL)
    
    fichas = []
    for j in range(8):
        for i in range(8):
            if j < 2:
                fichas.append(Ficha(i, j, "circulo", (0.0, 1.0, 1.0)))
            elif j >= 6:
                fichas.append(Ficha(i, j, "triangulo", (1.0, 0.0, 1.0)))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT)

        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    glColor3f(1, 1, 1)
                else:
                    glColor3f(0, 0, 0)
                
                x = -1 + i * 0.25
                y = -1 + j * 0.25
                glBegin(GL_QUADS)
                glVertex2f(x, y)
                glVertex2f(x + 0.25, y)
                glVertex2f(x + 0.25, y + 0.25)
                glVertex2f(x, y + 0.25)
                glEnd()

        for f in fichas:
            f.dibujar()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

class Ficha:
    def __init__(self, i, j, tipo, color):
        self.i = i
        self.j = j
        self.tipo = tipo
        self.color = color

    def dibujar(self):
        glColor3f(*self.color)
        x = -1 + self.i * 0.25 + 0.125
        y = -1 + self.j * 0.25 + 0.125
        
        if self.tipo == "circulo":
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(x, y)
            for n in range(33):
                a = 2 * math.pi * n / 32
                glVertex2f(x + math.cos(a) * 0.08, y + math.sin(a) * 0.08)
            glEnd()
        else:
            glBegin(GL_TRIANGLES)
            glVertex2f(x, y + 0.1)
            glVertex2f(x - 0.08, y - 0.08)
            glVertex2f(x + 0.08, y - 0.08)
            glEnd()

if __name__ == "__main__":
    main()
