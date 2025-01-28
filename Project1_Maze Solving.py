from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
import math
import random
import time
import ctypes


# Define the maze lines
maze_lines = [
    (10, 490, 490, 490), (10, 10, 490, 10), (10, 10, 10, 490), (490, 10, 490, 490),
    (90, 490, 90, 420), (295,490,295,420), (420, 490, 420, 440), (10, 350, 125, 350),
    (125, 350, 125, 450), (250, 320, 250, 370), (190, 320, 350, 320), (350, 220, 350, 320),
    (350, 270, 390, 270), (390, 270, 390, 330), (190, 280, 190, 320), (70, 280, 190, 280),
    (70, 280, 70, 310), (70, 310, 150, 310), (150, 310, 150, 410), (150, 410, 270, 410),
    (270, 370, 270, 410), (270, 370, 320, 370), (320, 370, 320, 440), (360, 370, 490, 370),
    (360, 370, 360, 460), (360, 460, 387, 460), (387, 400, 387, 460), (387, 400, 460, 400),
    (460, 400, 460, 450), (60, 10, 60, 100), (60, 100, 150, 100), (150, 100, 150, 200),
    (150, 200, 280, 200), (280, 200, 280, 280), (280, 280, 320, 280), (400, 100, 490, 100),
    (400, 100, 400, 200), (400, 200, 440, 200), (440, 150, 440, 200), (200, 10, 200, 100),
    (180, 100, 200, 100), (180, 100, 180, 150), (180, 150, 350, 150), (350, 180, 350, 150),
    (10, 150, 60, 150), (60, 150, 60, 235), (60, 235, 220, 235), (220, 235, 220, 280),
    (440, 250, 490, 250), (300, 10, 300, 70), (250, 110, 330, 110), (330, 60, 330, 110),
    (330, 60, 440, 60)
]


BUFFER_ZONE = 10
count = 0

def distance_to_line(px, py, x1, y1, x2, y2):
    if x1 == x2:  # Vertical line
        return abs(px - x1)
    if y1 == y2:  # Horizontal line
        return abs(py - y1)
    
    numerator = abs((y2 - y1) * px - (x2 - x1) * py + x2 * y1 - y2 * x1)
    denominator = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
    return numerator / denominator

def is_point_too_close_to_lines(px, py, maze_lines, buffer_zone):
    for (x1, y1, x2, y2) in maze_lines:
        if distance_to_line(px, py, x1, y1, x2, y2) < buffer_zone:
            return True
    return False

def generate_keys_without_touching_lines(maze_lines, num_keys=6, max_range=450):
    keys = []
    while len(keys) < num_keys:
        key_x = random.randint(5, max_range)
        key_y = random.randint(5, max_range)
        if not is_point_too_close_to_lines(key_x, key_y, maze_lines, BUFFER_ZONE):
            keys.append((key_x, key_y))
    
    return keys

def generate_ball_position(maze_lines, buffer_zone, max_range=450):
    while True:
        ball_x = 374
        ball_y = 440
        if not is_point_too_close_to_lines(ball_x, ball_y, maze_lines, buffer_zone):
            return ball_x, ball_y

keys = generate_keys_without_touching_lines(maze_lines)
#print("Generated keys:", keys)

ball_x, ball_y = generate_ball_position(maze_lines, BUFFER_ZONE)
#print("Ball position:", ball_x, ball_y)

ball_radius = 6
ball_step = 10 
score = 0
gamePaused = False
gameOver = False
time_limit = 60 
time_remaining = time_limit
paused_time = 0  # Initialize paused_time
pause_start_time = 0  # Initialize pause_start_time
if count == 0:
    start_time = time.time()
    count == 1
else:
    start_time = 0


def draw_pixel(x, y, color):
    glPointSize(2) # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glColor3f(color[0], color[1], color[2])
    glVertex2f(x, y) # jekhane show korbe pixel
    glEnd()

def findzone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if (abs(dx) > abs(dy)):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx <= 0 and dy >= 0:
            zone = 3
        elif dx <= 0 and dy <= 0:
            zone = 4
        elif dx >= 0 and dy <= 0:
            zone = 7

    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx <= 0 and dy >= 0:
            zone = 2
        elif dx <= 0 and dy <= 0:
            zone = 5
        elif dx >= 0 and dy <= 0:
            zone = 6
    return zone

def convert_zone(zone, x, y):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, x)
    elif zone == 7:
        return (x, -y)

def original_zone(zone, x, y):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

danger_zones = [
    (100, 150, 5), #circle_, circle_y, radius
    (250, 250, 5),
    (20, 20, 5),
    (50, 50, 5),    
    (250, 400, 5),  
    (100, 450, 5),   
    (450, 300, 5),  
    (300, 250, 5),  
    (350, 100, 5)                    
]

def draw_danger_zones():
    for zone in danger_zones:
        center_x, center_y, radius = zone
        mid_circle(center_x, center_y, radius, [1.0, 0.0, 0.0])  # Red color for danger zones

def check_danger_collision(ball_x, ball_y, danger_zones):
    for zone in danger_zones:
        center_x, center_y, radius = zone
        if math.sqrt((ball_x - center_x)**2 + (ball_y - center_y)**2) <= (ball_radius + radius):
            return True
    return False

def draw_line(x1, y1, x2, y2, color):
    zone = findzone(x1, y1, x2, y2)
    x1, y1 = convert_zone(zone, x1, y1)
    x2, y2 = convert_zone(zone, x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)
    y = y1
    for x in range(x1, x2):
        x0 = original_zone(zone, x, y)[0]
        y0 = original_zone(zone, x, y)[1]
        draw_pixel(x0, y0, color)
        # x +=1
        if d >= 0:
            d += incrNE
            y += 1
        else:
            d += incrE

oscillating_circles = []

# Function to add oscillating circles with unique properties
def add_oscillating_circle(base_radius, color, frequency, amplitude, maze_lines=maze_lines):

    circle_x, circle_y = generate_ball_position(maze_lines, BUFFER_ZONE)

    def generate_circle_position(maze_lines, buffer_zone=25, max_range=450):
        while True:
            circle_x = random.randint(10, max_range)
            circle_y = random.randint(10, max_range)
            # Check kortese circle position not too close to any maze line
            if not is_point_too_close_to_lines(circle_x, circle_y, maze_lines, buffer_zone):
                return circle_x, circle_y

    for i in range(1):
        circle_x, circle_y = generate_circle_position(maze_lines, BUFFER_ZONE)

    # Ensure the maximum radius does not make the circle touch the maze lines
    max_radius = base_radius + amplitude
    while is_point_too_close_to_lines(circle_x, circle_y, maze_lines, max_radius):
        circle_x, circle_y = generate_circle_position(maze_lines, max_radius)

    circle = {
        "x": circle_x,
        "y": circle_y,
        "base_radius": base_radius,
        "color": color,
        "frequency": frequency,
        "amplitude": amplitude,
        "start_time": time.time()
    }
    oscillating_circles.append(circle)

def circ_points(xc, yc, x, y, color):
    draw_pixel(xc + x, yc + y, color)
    draw_pixel(xc + y, yc + x, color)
    draw_pixel(xc + y, yc - x, color)
    draw_pixel(xc + x, yc - y, color)
    draw_pixel(xc - x, yc - y, color)
    draw_pixel(xc - y, yc - x, color)
    draw_pixel(xc - y, yc + x, color)
    draw_pixel(xc - x, yc + y, color)

def mid_circle(center_x, center_y, radius, color):
    d = 1 - radius
    x = 0
    y = radius
    circ_points(center_x, center_y, x, y, color)
    while x < y:
        if d < 0:
            d += 2 * x + 3
            x += 1
        else:
            d += 2 * x - 2 * y + 5
            x += 1
            y -= 1
        circ_points(center_x, center_y, x, y, color)

def draw_oscillating_circles():
    global score, ball_radius, ball_x, ball_y, time_limit, start_time, ball_step, maze_lines, gamePaused
    current_time = time.time()
    for circle in oscillating_circles:
        if gamePaused or gameOver:
            dynamic_radius = circle.get("last_radius", circle["base_radius"])
        else:
            elapsed_time = current_time - circle["start_time"]
            dynamic_radius = circle["base_radius"] + circle["amplitude"] * math.sin(2 * math.pi * circle["frequency"] * elapsed_time)
            circle["last_radius"] = max(dynamic_radius, 6)  # Store the last calculated radius
        
        smooth_radius = max(dynamic_radius, 6)
        mid_circle(circle["x"], circle["y"], smooth_radius, circle["color"])
        
        # Only check for collisions if the game is not paused
        if not gamePaused and math.sqrt((ball_x - circle["x"])**2 + (ball_y - circle["y"])**2) <= (ball_radius + smooth_radius):
            score += 5
            print("Score:", score)
            oscillating_circles.remove(circle)
            
            # Generate a new circle position
            circle_x1, circle_y1 = generate_ball_position(maze_lines, BUFFER_ZONE)
            def generate_circle_position(maze_lines, buffer_zone=25, max_range=450):
                while True:
                    circle_x1 = random.randint(10, max_range)
                    circle_y1 = random.randint(10, max_range)
                    if not is_point_too_close_to_lines(circle_x1, circle_y1, maze_lines, buffer_zone):
                        return circle_x1, circle_y1
            
            base_radius=random.randint(2, 3)
            amplitude=random.randint(10, 15)

            for i in range(1):
                circle_x, circle_y = generate_circle_position(maze_lines, BUFFER_ZONE)

            max_radius = base_radius + amplitude
            while is_point_too_close_to_lines(circle_x, circle_y, maze_lines, max_radius):
                circle_x, circle_y = generate_circle_position(maze_lines, max_radius)
            oscillating_circles.append({
                "x": circle_x,
                "y": circle_y,
                "base_radius": base_radius,
                "color": [0, random.random(), 1],
                "frequency": random.uniform(0.2, 0.5),
                "amplitude": amplitude,
                "start_time": current_time
            })

    score_text = f"Score: {score}"
    glColor3f(1.0, 0.5, 0.5)
    glRasterPos2f(400, 500)
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(char))) 

def iterate():
    glViewport(0, 0, 500, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 600, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def check_collision(x, y, dx, dy):
    # Define the maze lines for collision detection
    maze_lines = [
        (10, 490, 490, 490), (10, 10, 490, 10), (10, 10, 10, 490), (490, 10, 490, 490),
        (90, 490, 90, 420), (295,490,295,420), (420, 490, 420, 440), (10, 350, 125, 350),
        (125, 350, 125, 450), (240, 320, 240, 370), (190, 320, 350, 320), (350, 220, 350, 320),
        (350, 270, 390, 270), (390, 270, 390, 330), (190, 280, 190, 320), (70, 280, 190, 280),
        (70, 280, 70, 310), (70, 310, 150, 310), (150, 310, 150, 410), (150, 410, 270, 410),
        (270, 370, 270, 410), (270, 370, 320, 370), (320, 370, 320, 440), (360, 370, 490, 370),
        (360, 370, 360, 460), (360, 460, 387, 460), (387, 400, 387, 460), (387, 400, 460, 400),
        (460, 400, 460, 450), (60, 10, 60, 100), (60, 100, 150, 100), (150, 100, 150, 200),
        (150, 200, 280, 200), (280, 200, 280, 280), (280, 280, 320, 280), (400, 100, 490, 100),
        (400, 100, 400, 200), (400, 200, 440, 200), (440, 150, 440, 200), (200, 10, 200, 100),
        (180, 100, 200, 100), (180, 100, 180, 150), (180, 150, 350, 150), (350, 180, 350, 150),
        (10, 150, 60, 150), (60, 150, 60, 235), (60, 235, 220, 235), (220, 235, 220, 280),
        (440, 250, 490, 250), (300, 10, 300, 70), (250, 110, 330, 110), (330, 60, 330, 110),
        (330, 60, 440, 60)
    ]

    for line in maze_lines:
        x1, y1, x2, y2 = line
        dist = point_line_distance(x, y, x1, y1, x2, y2)
        if dist <= ball_radius:
            return True

    return False

def point_line_distance(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.sqrt((px - x1)**2 + (py - y1)**2)
    else:
        t = ((px - x1) * dx + (py - y1) * dy) / (dx**2 + dy**2)
        t = max(0, min(1, t))
        nearest_x, nearest_y = x1 + t * dx, y1 + t * dy
        return math.sqrt((px - nearest_x)**2 + (py - nearest_y)**2)

def key(x, y):
    mid_circle(x, y, 7, [0, 1, 0])

def draw_arrow():
    glColor3f(0.0, 1.0, 1.0)
    draw_line(10, 570, 60, 570, [0, 0, 1])
    draw_line(10, 570, 35, 595, [0, 0, 1])
    draw_line(35, 545, 10, 570, [0, 0, 1])

def draw_cross():
    glColor3f(1.0, 0.0, 0.0)
    draw_line(450, 550, 490, 590, [1, 0, 0])
    draw_line(490, 550, 450, 590, [1, 0, 0])

def draw_pause_button():
    glColor3f(1.0, 1.0, 0.0)
    draw_line(245, 590, 245, 550, [1, 1, 0])
    draw_line(255, 550, 255, 590, [1, 1, 0])

def draw_play_button():
    glColor3f(1.0, 1.0, 0.0)
    draw_line(235, 590, 275, 570, [1, 1, 0])
    draw_line(235, 550, 235, 590, [1, 1, 0])
    draw_line(235, 550, 275, 570, [1, 1, 0])

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    global score, gamePaused, time_remaining, paused_time, pause_start_time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_oscillating_circles()
    draw_danger_zones()
    glLoadIdentity()
    iterate()

    maze_lines = [
        (10, 490, 490, 490), (10, 10, 490, 10), (10, 10, 10, 490), (490, 10, 490, 490),
        (90, 490, 90, 420), (295,490,295,420), (420, 490, 420, 440), (10, 350, 125, 350),
        (125, 350, 125, 450), (240, 320, 240, 370), (190, 320, 350, 320), (350, 220, 350, 320),
        (350, 270, 390, 270), (390, 270, 390, 330), (190, 280, 190, 320), (70, 280, 190, 280),
        (70, 280, 70, 310), (70, 310, 150, 310), (150, 310, 150, 410), (150, 410, 270, 410),
        (270, 370, 270, 410), (270, 370, 320, 370), (320, 370, 320, 440), (360, 370, 490, 370),
        (360, 370, 360, 460), (360, 460, 387, 460), (387, 400, 387, 460), (387, 400, 460, 400),
        (460, 400, 460, 450), (60, 10, 60, 100), (60, 100, 150, 100), (150, 100, 150, 200),
        (150, 200, 280, 200), (280, 200, 280, 280), (280, 280, 320, 280), (400, 100, 490, 100),
        (400, 100, 400, 200), (400, 200, 440, 200), (440, 150, 440, 200), (200, 10, 200, 100),
        (180, 100, 200, 100), (180, 100, 180, 150), (180, 150, 350, 150), (350, 180, 350, 150),
        (10, 150, 60, 150), (60, 150, 60, 235), (60, 235, 220, 235), (220, 235, 220, 280),
        (440, 250, 490, 250), (300, 10, 300, 70), (250, 110, 330, 110), (330, 60, 330, 110),
        (330, 60, 440, 60)
    ]

    for line in maze_lines:
        x1, y1, x2, y2 = line
        draw_line(x1, y1, x2, y2, [1.0, 1.0, 1.0])

    mid_circle(ball_x, ball_y, ball_radius, [1.0, 1.0, 1.0])  # ball er er color set kora
    draw_arrow()
    draw_cross()
    if gamePaused:
        draw_play_button()
    else:
        draw_pause_button()

    # Draw keys
    for i in keys:
        key_x, key_y = i
        key(key_x, key_y)

    # keys er point calculate kora
    for i in keys:
        key_x, key_y = i
        if abs(ball_x - key_x) <= ball_step and abs(ball_y - key_y) <= ball_step:
            score += 1
            print("Score:", score)
            keys.remove(i)  # key remove kore dibe

    score_text = f"Score: {score}"
    glColor3f(1.0, 0.5, 0.5)
    glRasterPos2f(400, 500)
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(char)))

    if not gamePaused:
        current_time = time.time()
        elapsed_time = current_time - start_time - paused_time
        time_remaining = max(0, time_limit - int(elapsed_time))
        text = f"Time Remaining: {time_remaining} seconds"
        glColor3f(1.0, 1.0, 0.0)  
        glRasterPos2f(20, 500)  
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(char)))
    else:
        text = f"Time Remaining: {time_remaining} seconds"
        glColor3f(1.0, 0.0, 0.0)  
        glRasterPos2f(20, 500)  
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(char)))

    if len(keys) == 0:
        # Game win condition
        game_win_text = "Game win!"
        gamePaused = True
        glColor3f(1.0, 1.0, 0.0)  # Yellow color for game win text
        glRasterPos2f(200, 520)  # Position to display game win text
        for char in game_win_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(char)))

        # Stop the timer
        glutTimerFunc(0, timer, 0)

    elif time_remaining == 0:
        # Game over condition
        game_over_text = "Game over!"
        glColor3f(1.0, 0.0, 0.0)  # Red color
        glRasterPos2f(200, 520)  # position set korse
        for char in game_over_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(char)))
        # Stop the timer
        glutTimerFunc(0, timer, 0)

    elif check_danger_collision(ball_x, ball_y, danger_zones):
        # Game over condition
        game_over_text = "Game over!"
        glColor3f(1.0, 0.0, 0.0)
        glRasterPos2f(200, 520)  # position set korse
        for char in game_over_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(char)))
        # Stop the timer
        glutTimerFunc(0, timer, 0)

    glutSwapBuffers()

def update(value):
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def move(key, x, y):
    global ball_x, ball_y, gamePaused
    if key == GLUT_KEY_UP and not gamePaused and not gameOver:
        new_y = ball_y + ball_step
        if not check_collision(ball_x, new_y, 0, ball_step):
            ball_y = new_y
    elif key == GLUT_KEY_DOWN and not gamePaused and not gameOver:
        new_y = ball_y - ball_step
        if not check_collision(ball_x, new_y, 0, -ball_step):
            ball_y = new_y
    if key == GLUT_KEY_LEFT and not gamePaused and not gameOver:
        new_x = ball_x - ball_step
        if not check_collision(new_x, ball_y, -ball_step, 0):
            ball_x = new_x
    elif key == GLUT_KEY_RIGHT and not gamePaused and not gameOver:
        new_x = ball_x + ball_step
        if not check_collision(new_x, ball_y, ball_step, 0):
            ball_x = new_x

def keyboard(key, x, y):
    global ball_x, ball_y, gamePaused, pause_start_time, paused_time

    if key == b'w':
        if not gamePaused:
            new_y = ball_y + ball_step
            if not check_collision(ball_x, new_y, 0, ball_step):
                ball_y = new_y  # Move up
    elif key == b's':
        if not gamePaused:
            new_y = ball_y - ball_step
            if not check_collision(ball_x, new_y, 0, -ball_step):
                ball_y = new_y  # Move down
    elif key == b'a':
        if not gamePaused:
            new_x = ball_x - ball_step
            if not check_collision(new_x, ball_y, -ball_step, 0):
                ball_x = new_x  # Move left
    elif key == b'd':
        if not gamePaused:
            new_x = ball_x + ball_step
            if not check_collision(new_x, ball_y, ball_step, 0):
                ball_x = new_x  # Move right

    elif key == b'p':
        gamePaused = not gamePaused
        if gamePaused:
            pause_start_time = time.time()
            print("Game Paused")
        else:
            paused_time += time.time() - pause_start_time
            print("Game Resumed")

    elif key == b'r':
        gamePaused = not gamePaused
        restartGame()
        # gamePaused = False

    elif key == b'x':
        print("Goodbye")
        print("Score:", score)
        glutLeaveMainLoop()

    glutPostRedisplay()

def restartGame():
    global ball_x, ball_y, ball_radius, ball_step, score, keys, gamePaused, gameOver, time_limit, time_remaining, start_time, paused_time, pause_start_time, oscillating_circles

    keys = generate_keys_without_touching_lines(maze_lines)

    oscillating_circles = []

    for i in range(3):
        add_oscillating_circle(
            base_radius=random.randint(2, 3),
            color=[0, random.random(), 1],
            frequency=random.uniform(0.2, 0.3),
            amplitude=random.randint(10, 15)
        )
    ball_x, ball_y = generate_ball_position(maze_lines, BUFFER_ZONE)
    ball_radius = 6
    ball_step = 10 
    score = 0
    gamePaused = False
    time_limit = 60 
    time_remaining = 60 
    start_time = time.time()
    paused_time = 0  # Reset paused_time on restart
    pause_start_time = 0  # Reset pause_start_time on restart
    gameOver = False
    print("Starting over!")
    glutPostRedisplay()

timer_remain = None

def mouse(button, state, x, y):
    global gamePaused, gameOver, printed, score, pause_start_time, paused_time

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if x >= 10 and x <= 80 and y >= 10 and y <= 70:
            gamePaused = not gamePaused
            if gamePaused:
                pause_start_time = time.time()
                print(f"Game Over! Score: {score}")
            else:
                paused_time += time.time() - pause_start_time
            restartGame()

        if x >= 235 and x <= 275 and y >= 8  and y <= 65:
            gamePaused = not gamePaused
            if gamePaused:
                pause_start_time = time.time()
                print("Game Paused")
            else:
                paused_time += time.time() - pause_start_time
                print("Game Resumed")
            glutPostRedisplay()
            
        if x >= 420 and x <= 490 and y >= 20 and y <= 80:
            printed = True
            print("Goodbye")
            print("Score:", score)
            gameOver = True
            glutLeaveMainLoop()

        print(f"Mouse clicked at ({x}, {y})")
        glutPostRedisplay()

for i in range(3):  # Add 3 random circles
    add_oscillating_circle(
        base_radius=random.randint(2, 3),
        color=[0, random.random(), 1],
        frequency=random.uniform(0.2, 0.3),
        amplitude=random.randint(10, 15)
    )

def timer(value):
    global time_remaining, gamePaused, last_time

    if not gamePaused:
        if time_remaining < 0:
            time_remaining -= 1
        else:
            gamePaused = True

    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 600)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Maze quest")  # window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutSpecialFunc(move)
glutTimerFunc(16, update, 0)

glutMainLoop()
