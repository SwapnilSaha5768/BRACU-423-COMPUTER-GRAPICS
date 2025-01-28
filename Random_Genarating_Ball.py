from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

point = []
left_position = 0
width = 500
bottom_position = 0
height = 500
size = 25
point_speed = 0.5
left_mouse = False
right_mouse = None
initial_time = 0
spacebar = False
colors = []


def draw_point():
    global left_mouse, initial_time, spacebar

    glEnable(GL_POINT_SMOOTH)
    glPointSize(size)
    glBegin(GL_POINTS)

    for i in range(len(point)):
        x, y, color, x_direction, y_direction = point[i]

        if spacebar:
            x_direction = 0
            y_direction = 0
            left_mouse = False

        if left_mouse and not spacebar:
            current_time = glutGet(GLUT_ELAPSED_TIME)
            time_diff = (current_time - initial_time) % 900

            if time_diff < 100:
                color = (0.0, 0.0, 0.0)
            else:
                original_color = colors[i]
                color = original_color

        glColor3f(*color)
        glVertex2f(x, y)

        x += point_speed * x_direction
        y += point_speed * y_direction

        if x < left_position + size:
            x = left_position + size
            x_direction = -x_direction
        if x > width - size:
            x = width - size
            x_direction = -x_direction
        if y < bottom_position + size:
            y = bottom_position + size
            y_direction = -y_direction
        if y > height - size:
            y = height - size
            y_direction = -y_direction

        point[i] = (x, y, color, x_direction, y_direction)

    glEnd()


def create_random_point(x, y):
    if left_position < x < width and bottom_position < y < height:
        r, g, b = (random.random(), random.random(), random.random())
        color = (r, g, b)
        x_direction = random.choice([-1, 1])
        y_direction = random.choice([-1, 1])
        point.append((x, y, color, x_direction, y_direction))
        colors.append(color)


def mouseListener(button, state, x, y):
    global left_mouse, initial_time, spacebar

    if spacebar:
        return
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        create_random_point(x, 500 - y)

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        if left_mouse == False:
            left_mouse = not left_mouse

        else:
            left_mouse = not left_mouse


def specialKeysListener(key, x, y):
    global point_speed, left_mouse, spacebar
    if key == GLUT_KEY_UP:
        point_speed += 0.1

    elif key == GLUT_KEY_DOWN:
        point_speed -= 0.1
    print(point_speed)


def keyboardListener(key, x, y):
    global spacebar, point_speed, left_mouse, right_mouse

    if key == b" ":
        spacebar = not spacebar
        if spacebar:
            right_mouse = left_mouse
            left_mouse = False
            for i in range(len(point)):
                x, y, color, x_direction, y_direction = point[i]
                x_direction = 0
                y_direction = 0
                point[i] = (x, y, color, x_direction, y_direction)
        else:
            left_mouse = right_mouse
            right_mouse = None
            for i in range(len(point)):
                x_direction = random.choice([-1, 1])
                y_direction = random.choice([-1, 1])
                point[i] = (point[i][0], point[i][1], point[i][2], x_direction, y_direction)

def draw_box():
    glLineWidth(10)
    glBegin(GL_LINES)
    glVertex2f(width, height)
    glVertex2f(left_position, height)

    glVertex2f(left_position, height)
    glVertex2f(left_position, bottom_position)

    glVertex2f(width, bottom_position)
    glVertex2f(left_position, bottom_position)

    glVertex2f(width, bottom_position)
    glVertex2f(width, height)
    glEnd()

def iterate():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 500, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    glColor3f(1.0, 1.0, 1.0)

    draw_box()
    draw_point()

    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutCreateWindow(b"Display")
glutDisplayFunc(display)
glutMouseFunc(mouseListener)
glutSpecialFunc(specialKeysListener)
glutKeyboardFunc(keyboardListener)
glutIdleFunc(display)
glutMainLoop()