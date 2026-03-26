import pygame as pg;
from OpenGL.GL import *
from OpenGL.GLU import *
import random

class App:

    jugador_obj = None
    posjugadorx = 0
    posjugadory = 0
    tamañojugadorx = 0.05
    tamañojugadory = 0.1
    direccion = 0
    proyectiles = []
    cantidad_enemigos = 5
    lista_enemigos = []
    cantidad_personas = 3
    lista_personas = []
    running = True


    def __init__(self):
        pg.init()
        pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption("Seaquest")
        self.clock = pg.time.Clock()
        glClearColor(0.53, 0.81, 0.92, 1.0)
        self.enemigos()
        self.personas()
        self.mainLoop()

    def mainLoop(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:
                        self.posjugadory += 0.05
                    if event.key == pg.K_s:
                        self.posjugadory -= 0.05
                    if event.key == pg.K_a:
                        self.posjugadorx -= 0.05
                        self.direccion = 0
                    if event.key == pg.K_d:
                        self.posjugadorx += 0.05
                        self.direccion = 1
                    if event.key == pg.K_SPACE:
                        self.disparo()
            glClear(GL_COLOR_BUFFER_BIT)
            
            self.jugador()
            self.colisiones()

            for p in self.proyectiles:
                p.mover()
                p.dibujar()

            for e in self.lista_enemigos:
                e.dibujar()
            
            for p in self.lista_personas:
                p.dibujar()

            pg.display.flip()
            self.clock.tick(60)
        self.quit()

    def quit(self):
        pg.quit()
    
    def jugador(self):
        self.jugador_obj = Rectangulo(self.posjugadorx, self.posjugadory, self.tamañojugadory, self.tamañojugadorx, 1.0, 1.0, 0.0)
        self.jugador_obj.dibujar()

    def disparo(self):
        v = -0.05 if self.direccion == 0 else 0.05
        self.proyectiles.append(Rectangulo(self.posjugadorx, self.posjugadory, 0.05, 0.02, 1.0, 0.5, 0.0, v))

    def enemigos(self):
        self.lista_enemigos = []
        for i in range(self.cantidad_enemigos):
            ex = random.uniform(-0.9, 0.9)
            ey = random.uniform(-0.9, 0.9)
            self.lista_enemigos.append(Rectangulo(ex, ey, self.tamañojugadory, self.tamañojugadorx, 1.0, 0.0, 0.0))
    
    def personas(self):
        self.lista_personas = []
        for i in range(self.cantidad_personas):
            px = random.uniform(-0.9, 0.9)
            py = random.uniform(-0.9, 0.9)
            self.lista_personas.append(Triangulo(px, py, self.tamañojugadory, self.tamañojugadorx, 0.0, 1.0, 0.0))
    
    def colisiones(self):
        for p in self.proyectiles:
            for e in self.lista_enemigos:
                if p.check_collision(e):
                    self.proyectiles.remove(p)
                    self.lista_enemigos.remove(e)
                    return
        
        for p in self.proyectiles:
            for i in self.lista_personas:
                if p.check_collision(i):
                    self.proyectiles.remove(p)
                    self.lista_personas.remove(i)
                    self.running = False
                    return

        for p in self.lista_personas:
            if self.jugador_obj.check_collision(p):
                self.lista_personas.remove(p)
                return

        if not self.lista_enemigos and not self.lista_personas:
            print("Juego superado.")
            self.running = False

class Rectangulo:
    def __init__(self, x, y, w, h, r, g, b, vx=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.g = g
        self.b = b
        self.vx = vx
    
    def mover(self):
        self.x += self.vx
    
    def dibujar(self):
        glColor3f(self.r, self.g, self.b)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.w, self.y)
        glVertex2f(self.x + self.w, self.y + self.h)
        glVertex2f(self.x, self.y + self.h)
        glEnd()

    def check_collision(self, other):
        return (self.x < other.x + other.w and
                self.x + self.w > other.x and
                self.y < other.y + other.h and
                self.y + self.h > other.y)
    
class Triangulo:
    def __init__(self, x, y, w, h, r, g, b):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.g = g
        self.b = b
    
    def dibujar(self):
        glColor3f(self.r, self.g, self.b)
        glBegin(GL_TRIANGLES)
        glVertex2f(self.x + self.w / 2, self.y + self.h)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.w, self.y)
        glEnd()
        
    def check_collision(self, other):
        return (self.x < other.x + other.w and
                self.x + self.w > other.x and
                self.y < other.y + other.h and
                self.y + self.h > other.y)
        
if __name__ == "__main__":
    app = App()