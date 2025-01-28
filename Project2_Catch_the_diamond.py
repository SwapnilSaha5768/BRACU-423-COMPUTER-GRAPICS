from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random, math, time

W_Width, W_Height = 500, 700

# Game state variables
bowl_x = 250
diamond_x, diamond_y = 250, 700
game_over = False
paused = False
score = 0
diamond_speed = 5  # Diamond fall speed (initial)

# ------------- Midpoint Line Drawing Algorithm start -------------------------------
def draw_points(x, y, width=3):
    glPointSize(width) #pixel size for every point in the line, default holo 3
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()

def zoneOf(x1,y1, x2,y2):
    dx = x2-x1
    dy = y2-y1
    #print(f"original dx={dx} and dy={dy} and abs(dx)={abs(dx)} and abs(dy)={abs(dy)}")
    if dx == 0 and dy == 0:
        return 0  # ei case ta adou hobe kina jani na kintu eta chara khali error dey
    elif dx == 0:
        return 1 if dy > 0 else 5  # vertical line akar shomoy
    elif dy == 0:
        return 0 if dx > 0 else 4  # horizontal line akar shomoy
    elif dx > 0 and dy > 0:
        return 0 if abs(dx) > abs(dy) else 1
    elif dx < 0 and dy > 0:
        return 3 if abs(dx) > abs(dy) else 2
    elif dx < 0 and dy < 0:
        return 4 if abs(dx) > abs(dy) else 5
    elif dx > 0 and dy < 0:
        return 7 if abs(dx) > abs(dy) else 6
    else:
        raise Exception("Unexpected case in zoneOf() function")
    
def converted_point_in_zone0(x, y, zone):
    if zone == 1:
        return y, x
    if zone == 2:
        return y, -x
    if zone == 3:
        return -x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return -y, x
    if zone == 7:
        return x, -y

def converted_back_to_OGzone(x, y, zone):
    if zone == 1:
        return y, x
    if zone == 2:
        return -y, x
    if zone == 3:
        return x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return y, -x
    if zone == 7:
        return x, -y

def drawLineWithMPL(x1, y1, x2, y2, width=3):
    zone = zoneOf(x1,y1,x2,y2)
    #print(f"Zone is {zone}")
    if zone!=0:
        x1, y1 = converted_point_in_zone0(x1,y1,zone)
        x2, y2 = converted_point_in_zone0(x2,y2,zone)
    dx = x2-x1
    dy = y2-y1
    d = 2*(dy)-dx
    y = y1
    draw_points(x1,y1, width) # prothom point eke felo
    for x in range(x1+1, x2+1): # second point theke loop shuru hoye x2 porjonto jabe
        if d>0: # North-East e jao
            if zone!=0:
                draw_points(*converted_back_to_OGzone(x, y+1, zone),width) #original zone e ako point ta ke
            else:
                draw_points(x, y+1, width)
            d += 2*(dy-dx)
            y += 1 # increment koro y ke since N-E gecho
        else:   # East e jao
            if zone!=0:
                draw_points(*converted_back_to_OGzone(x, y, zone), width) #original zone e ako point ta ke
            else: 
                draw_points(x, y, width)
            d += 2*dy
#-----------------Midpoint Line Drawing Algorithm end --------------------------------

#---------------- Game objects drawing functions start --------------------------------------
def draw_bowl(x):
    global game_over
    if game_over:
        glColor3f(1.0, 0.0, 0.0)  # Red color when game over
    else:
        glColor3f(1.0, 1.0, 1.0)  # White color normally
    h = 20
    drawLineWithMPL(x-35,0, x+35,0)
    drawLineWithMPL(x-50,h, x+50,h)
    drawLineWithMPL(x-50,h, x-35,0)
    drawLineWithMPL(x+35,0, x+50,h)


def draw_resetButton():
    glColor3f(0, 0.7, 0.7)
    drawLineWithMPL(20,650, 70,650, 4)
    drawLineWithMPL(20,650, 50,670, 4)
    drawLineWithMPL(20,650, 50,630, 4)

def draw_exitButton():
    glColor3f(1.0, 0.0, 0.0)
    drawLineWithMPL(500-20-50,670, 500-20,630, 4)
    drawLineWithMPL(500-20-50,630, 500-20,670, 4)

def draw_pauseButton():
    glColor3f(1.0, 0.55, 0.0)
    drawLineWithMPL(250-5,670, 250-5,630, 4)
    drawLineWithMPL(250+5,670, 250+5,630, 4)

def draw_resumeButton():
    glColor3f(1.0, 0.55, 0.0)
    drawLineWithMPL(250-25,670, 250-25,630, 4)
    drawLineWithMPL(250-25,670, 250+25,(630+670)/2, 4)
    drawLineWithMPL(250-25,630, 250+25,(630+670)/2, 4)

def draw_diamond(x,y):
    glColor3f(1.0, 1.0, 0.0)
    drawLineWithMPL(x,y, x-15,y-15, 4)
    drawLineWithMPL(x,y, x+15,y-15, 4)
    drawLineWithMPL(x-15,y-15, x,y-30, 4)
    drawLineWithMPL(x+15,y-15, x,y-30, 4)




#----------------- Game objects drawing functions end ---------------------------------

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glLoadIdentity()

    draw_resetButton()
    draw_exitButton()
    if paused:
        draw_resumeButton()
    else:
        draw_pauseButton()
    draw_bowl(bowl_x)
    draw_diamond(diamond_x, diamond_y)


    glutSwapBuffers()

def animate(value):
    global diamond_y, diamond_x, game_over, score, diamond_speed

    if not paused and not game_over:
        diamond_y -= diamond_speed  # Adjust falling speed here

        # Check for collision with bowl
        if diamond_y <= 20 and abs(diamond_x - bowl_x) <= 50:
            score += 1
            print(f"Score: {score}")
            diamond_speed += 1
            reset_diamond()
        elif diamond_y <= 0:
            game_over = True
            print("Game Over!")
            print(f"Last Score: {score}")

    glutPostRedisplay()
    glutTimerFunc(30, animate, 0)  # Call animate every 30 milliseconds

def reset_diamond():
    global diamond_x, diamond_y
    diamond_x = random.randint(0, W_Width)
    diamond_y = W_Height - 50  # Start just below the buttons

def reset_game():
    global bowl_x, game_over, score
    bowl_x = 250
    game_over = False
    score = 0
    reset_diamond()

def keyboard(key, x, y):
    global bowl_x
    if not paused and not game_over:
        if key == GLUT_KEY_LEFT and bowl_x > 50:
            bowl_x -= 10
        elif key == GLUT_KEY_RIGHT and bowl_x < W_Width - 50:
            bowl_x += 10
    glutPostRedisplay()

def mouse(button, state, x, y):
    global paused, game_over
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Convert mouse coordinates
        y = W_Height - y
        
        # Reset button
        if 20 <= x <= 70 and 630 <= y <= 670:
            reset_game()
        # Exit button
        elif W_Width - 70 <= x <= W_Width - 20 and 630 <= y <= 670:
            glutLeaveMainLoop()
        # Pause/Resume button
        elif 225 <= x <= 275 and 630 <= y <= 670:
            paused = not paused

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, W_Width, 0, W_Height)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Catch the Diamond!")

init()
glutDisplayFunc(display)
glutTimerFunc(0, animate, 0)
glutSpecialFunc(keyboard)
glutMouseFunc(mouse)

reset_game()  # Initialize the game state
glutMainLoop()