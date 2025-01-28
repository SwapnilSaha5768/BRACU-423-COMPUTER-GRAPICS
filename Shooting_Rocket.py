from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Window size
width = 400
height = 600

# Shooter
x_center = width // 2
y_center = 20
rocket_width = 20
rocket_height = 30
speed_shooter = 15

# Fireball
firing_speed = 15
fire_details = []

# Falling
falling_balls = []
balls_speed = 2.0

# Score
score = 0
lives = 3
miss_fire = 0
Gameover = False
Pause = False


def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    # Buttons
    draw_left_arrow()
    draw_cross()
    drawplaypause()

    # Shooter
    draw_shooting_rocket()

    # Falling Circles and Fireballs
    if not Gameover:
        draw_fireballs()
        draw_falling_balls()

    if Gameover:
        draw_gameover_screen()

    glutSwapBuffers()


def draw_pixel(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def midpoint_circle(x_center, y_center, radius):
    x = 0
    y = radius
    p = 1 - radius
    draw_circle_points(x_center, y_center, x, y)
    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * x - 2 * y + 1
        draw_circle_points(x_center, y_center, x, y)


def draw_circle_points(xc, yc, x, y):
    draw_pixel(xc + x, yc + y)
    draw_pixel(xc - x, yc + y)
    draw_pixel(xc + x, yc - y)
    draw_pixel(xc - x, yc - y)
    draw_pixel(xc + y, yc + x)
    draw_pixel(xc - y, yc + x)
    draw_pixel(xc + y, yc - x)
    draw_pixel(xc - y, yc - x)


def draw_shooting_rocket():
    global x_center, y_center, rocket_width, rocket_height
    glColor3f(1.0, 1.0, 0.0)

    draw_rectangle(x_center - rocket_width // 2, y_center,
                   x_center + rocket_width // 2, y_center + rocket_height)

    draw_triangle(x_center, y_center + rocket_height + 20,
                  x_center - rocket_width // 2, y_center + rocket_height,
                  x_center + rocket_width // 2, y_center + rocket_height)

    draw_triangle(x_center - rocket_width // 2, y_center + 10,
                  x_center - rocket_width // 2 - 15, y_center,
                  x_center - rocket_width // 2, y_center)
    draw_triangle(x_center + rocket_width // 2, y_center + 10,
                  x_center + rocket_width // 2 + 15, y_center,
                  x_center + rocket_width // 2, y_center)

    draw_rectangle(x_center - 10, y_center - 15, x_center + 10, y_center)


def draw_rectangle(x1, y1, x2, y2):
    for x in range(int(x1), int(x2) + 1):
        for y in range(int(y1), int(y2) + 1):
            draw_pixel(x, y)


def draw_triangle(x1, y1, x2, y2, x3, y3):
    draw_line(x1, y1, x2, y2)
    draw_line(x2, y2, x3, y3)
    draw_line(x3, y3, x1, y1)


def draw_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        draw_pixel(x1, y1)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def draw_fireballs():
    global fire_details
    for fireball in fire_details:
        glColor3f(1.0, 1.0, 1.0)
        midpoint_circle(fireball['x'], fireball['y'], 5)


def draw_falling_balls():
    global falling_balls, Pause
    for circle in falling_balls:
        if circle['is_unique']:
            if not Pause:
                circle['radius_phase'] += 0.1
            circle['radius'] = circle['radius_base'] + circle['radius_delta'] * math.sin(circle['radius_phase'])
        glColor3fv(circle['color'])
        midpoint_circle(circle['x'], circle['y'], int(circle['radius']))




def draw_gameover_screen():
    glColor3f(1.0, 0.0, 0.0)
    glRasterPos2f(width // 2 - 100, height // 2)
    for char in f"GAME OVER! SCORE: {score}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def draw_left_arrow():
    glColor3f(0.0, 1.0, 1.0)
    draw_line(30, 550, 100, 550)
    draw_line(50, 570, 30, 550)
    draw_line(50, 530, 30, 550)


def draw_cross():
    glColor3f(1.0, 0.0, 0.0)
    draw_line(320, 530, 370, 570)
    draw_line(320, 570, 370, 530)


def drawplaypause():
    glColor3f(1.0, 1.0, 0.0)
    if Pause:
        # Draw Play Triangle
        draw_triangle(200, 530, 200, 570, 230, 550)
    else:
        # Draw Pause Lines
        draw_line(190, 570, 190, 520)
        draw_line(210, 570, 210, 520)


def mouse_listener(button, state, x, y):
    global Pause, Gameover, score
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = height - y
        if 30 <= x <= 100 and 530 <= y <= 570:
            restart_game()
        elif 190 <= x <= 230 and 520 <= y <= 570:
            toggle_pause()
        elif 320 <= x <= 370 and 530 <= y <= 570:
            print(f"Goodbye! Final Score: {score}")
            glutLeaveMainLoop()


def restart_game():
    global falling_balls, fire_details, score, lives, miss_fire, Gameover, Pause
    falling_balls.clear()
    fire_details.clear()
    score = 0
    lives = 3
    miss_fire = 0
    Gameover = False
    Pause = False


def move_fireballs():
    global fire_details, miss_fire, Gameover
    if Pause:
        return
    for fireball in fire_details[:]:
        fireball['y'] += firing_speed
        if fireball['y'] > height:
            fire_details.remove(fireball)
            miss_fire += 1
            if miss_fire >= 3:
                Gameover = True


def move_falling_balls():
    global falling_balls, lives, Gameover
    if Pause:
        return
    for circle in falling_balls[:]:
        circle['y'] -= balls_speed
        if circle['y'] < 0:
            falling_balls.remove(circle)
            lives -= 1
            if lives <= 0:
                Gameover = True


def check_collisions():
    global fire_details, falling_balls, score, Gameover
    for fireball in fire_details[:]:
        for circle in falling_balls[:]:
            distance = ((fireball['x'] - circle['x']) ** 2 + (fireball['y'] - circle['y']) ** 2) ** 0.5
            if distance <= circle['radius']:
                fire_details.remove(fireball)
                falling_balls.remove(circle)
                score += circle.get('score', 1)
                print('Score:', score)
    
    for circle in falling_balls:
        if (abs(circle['x'] - x_center) <= (rocket_width // 2 + circle['radius']) and
                abs(circle['y'] - y_center - rocket_height) <= (rocket_height + circle['radius'])):
            Gameover = True
            print("Game Over! The shooter collided with a falling circle.")
            break


def create_circle():
    if Pause:
        return
    x = random.randint(30, width - 30)
    y = random.randint(height, height + 100)

    if random.random() < 0.2:
        falling_balls.append({
            'x': x,
            'y': y,
            'radius_base': 15,
            'radius_delta': 5,
            'radius_phase': random.uniform(0, math.pi * 2),
            'is_unique': True,
            'color': (1.0, 0.0, 1.0),
            'score': 3
        })
    else:
        falling_balls.append({
            'x': x,
            'y': y,
            'radius': 15,
            'is_unique': False,
            'color': (0.5, 1.0, 0.5),
            'score': 1
        })


def update(value):
    if not Gameover and not Pause:
        move_fireballs()
        move_falling_balls()
        check_collisions()
        if len(falling_balls) < 5:
            create_circle()
    glutPostRedisplay()
    glutTimerFunc(33, update, 0)


def key_listener(key, x, y):
    global x_center, fire_details
    if Pause or Gameover:
        return
    if key == b'a':
        x_center = max(x_center - speed_shooter, rocket_width // 2)
    elif key == b'd':
        x_center = min(x_center + speed_shooter, width - rocket_width // 2)
    elif key == b' ':
        fire_details.append({'x': x_center, 'y': y_center + rocket_height})


def toggle_pause():
    global Pause
    Pause = not Pause


def iterate():
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Shooting the Falling Circles")
    glutDisplayFunc(show_screen)
    glutIdleFunc(show_screen)
    glutMouseFunc(mouse_listener)
    glutKeyboardFunc(key_listener)
    glutTimerFunc(33, update, 0)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glutMainLoop()


if __name__ == "__main__":
    main()
