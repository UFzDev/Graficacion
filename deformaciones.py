import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

def draw_shape():
    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(-0.5, 0.5, 0)
    glVertex3f(0.5, 0.5, 0)
    glVertex3f(0.5, -0.5, 0)
    glVertex3f(-0.5, -0.5, 0)
    glEnd()

def apply_deformation(factor):
    matrix = [
        1, factor, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1
    ]
    glMultMatrixf(matrix)

def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        
        t = pygame.time.get_ticks() / 1000.0
        shear_factor = math.sin(t) * 0.8
        
        apply_deformation(shear_factor)
        draw_shape()
        
        glPopMatrix()
        
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()