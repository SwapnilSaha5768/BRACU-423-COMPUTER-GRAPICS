from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math


background_color = [1.0, 1.0, 1.0]
raindrops_color = [0.0, 0.0, 0.0]
angle = 90


def draw_triangle():
    glBegin(GL_TRIANGLES)
    if background_color == [1.0, 1.0, 1.0]:
        glColor3f(0.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)

    glVertex2f(240, 350)
    glVertex2f(660, 350)
    glVertex2f(450, 450)
    glEnd()

 
    glBegin(GL_TRIANGLES)
    if background_color == [1.0, 1.0, 1.0]:
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(0.0, 0.0, 0.0)

    glVertex2f(310, 365)
    glVertex2f(590, 365)
    glVertex2f(450, 430)
    glEnd()


def draw_lines():
    glLineWidth(3)
    glBegin(GL_LINES)
    if background_color == [1.0, 1.0, 1.0]:
        glColor3f(0.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)

    # House
    glVertex2f(260, 350)
    glVertex2f(260, 100)
    glVertex2f(640, 350)
    glVertex2f(640, 100)
    glVertex2f(260, 100)
    glVertex2f(640, 100)

    # Window
    glVertex2f(500, 250)
    glVertex2f(600, 250)
    glVertex2f(500, 330)
    glVertex2f(600, 330)
    glVertex2f(500, 290)
    glVertex2f(600, 290)
    glVertex2f(500, 250)
    glVertex2f(500, 330)
    glVertex2f(600, 250)
    glVertex2f(600, 330)
    glVertex2f(550, 250)
    glVertex2f(550, 330)

    # Door
    glVertex2f(330, 100)
    glVertex2f(330, 250)
    glVertex2f(430, 100)
    glVertex2f(430, 250)
    glVertex2f(330, 250)
    glVertex2f(430, 250)

    glEnd()

def draw_points():
    glPointSize(7)
    glBegin(GL_POINTS)
    if (background_color[0]==1.0 and background_color[1]==1.0 and background_color[2]==1.0) :
        glColor3f(0.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)

    glVertex2f(420, 180)
    glEnd()


def rain_droplets():
    glLineWidth(2)
    glBegin(GL_LINES)
    number_of_droplets = 100
    for i in range(number_of_droplets):
        x = random.randint(1, 1000)
        y = random.randint(300, 1000)
        length = 20
        x1 = x - length * math.cos(math.radians(angle))
        y1 = y - length

        if background_color == [1.0, 1.0, 1.0]:
            glColor3f(0.0, 0.0, 0.0)
        else:
            glColor3f(1.0, 1.0, 1.0)

        glVertex2f(x, y)
        glVertex2f(x1, y1)
    glEnd()


def background():
    glClearColor(*background_color, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)


def specialKeyListener(key, x, y):
    global angle
    if key == GLUT_KEY_LEFT:
        angle -= 5
    elif key == GLUT_KEY_RIGHT:
        angle += 5
    glutPostRedisplay()


def keyboardListener(key, x, y):
    global background_color, raindrops_color

    if key == b'a':
        if (background_color[0] >= 1.0 and background_color[1] >= 1.0 and background_color[2] >= 1.0) and (
                raindrops_color[0] <= 0.0 and raindrops_color[1] <= 0.0 and raindrops_color[2] <= 0.0):
            background_color = [1.0, 1.0, 1.0]
            raindrops_color = [0.0, 0.0, 0.0]
        else:
            background_color[0] += 1
            background_color[1] += 1
            background_color[2] += 1
            raindrops_color[0] -= 1
            raindrops_color[1] -= 1
            raindrops_color[2] -= 1

    if key == b's':
        if (background_color[0] <= 0.0 and background_color[1] <= 0.0 and background_color[2] <= 0.0) and (
                raindrops_color[0] >= 1.0 and raindrops_color[1] >= 1.0 and raindrops_color[2] >= 1.0):
            background_color = [0.0, 0.0, 0.0]
            raindrops_color = [1.0, 1.0, 1.0]
        else:
            background_color[0] -= 1
            background_color[1] -= 1
            background_color[2] -= 1
            raindrops_color[0] += 1
            raindrops_color[1] += 1
            raindrops_color[2] += 1


def iterate():
    glViewport(0, 0, 1000, 1000)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1000, 0.0, 1000, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    background()
    rain_droplets()
    draw_lines()
    draw_triangle()
    draw_points()
    glutSwapBuffers()


def rain_timer(value):
    glutTimerFunc(100, rain_timer, 0)
    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"House with Rain")
glutDisplayFunc(showScreen)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)
glutTimerFunc(100, rain_timer, 0)
glutMainLoop()
