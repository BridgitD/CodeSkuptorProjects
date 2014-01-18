# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600.0
HEIGHT = 400.0       
BALL_RADIUS = 20.0
PAD_WIDTH = 8.0
PAD_HEIGHT = 80.0
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0.0, 0.0]
paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
paddle1_vel = [0.0, 0.0]
paddle2_vel = [0.0, 0.0]
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new ball in middle of table
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel[0] = random.randrange(120.0, 240.0) / 60.0
    ball_vel[1] = - random.randrange(60.0, 180.0) / 60.0
    if direction == LEFT:
        ball_vel[0] = - ball_vel[0]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    spawn_ball(LEFT)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
         
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # vertical collisions
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # horizontal collisions
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if paddle1_pos[1] + HALF_PAD_HEIGHT >= ball_pos[1] >= paddle1_pos[1] - HALF_PAD_HEIGHT:
            ball_vel[0] = -1.1 * ball_vel[0]
        else:
            spawn_ball(RIGHT)
            score2 += 1
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        if paddle2_pos[1] + HALF_PAD_HEIGHT >= ball_pos[1] >= paddle2_pos[1] - HALF_PAD_HEIGHT:
            ball_vel[0] = -1.1 * ball_vel[0]
        else:
            spawn_ball(LEFT)
            score1 += 1
        
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel[1]
    paddle2_pos[1] += paddle2_vel[1]
    
    if paddle1_pos[1] < HALF_PAD_HEIGHT:
        paddle1_pos[1] = HALF_PAD_HEIGHT
    elif paddle1_pos[1] > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    elif paddle2_pos[1] < HALF_PAD_HEIGHT:
        paddle2_pos[1] = HALF_PAD_HEIGHT
    elif paddle2_pos[1] > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    
    # draw paddles
    c.draw_polygon([(0, paddle1_pos[1] - HALF_PAD_HEIGHT),
                   (PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT),
                   (PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT),
                   (0, paddle1_pos[1] + HALF_PAD_HEIGHT)], 1, "Yellow", "Yellow")
    c.draw_polygon([(WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT),
                     (WIDTH - PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT),
                     (WIDTH - PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT),
                     (WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT)], 1, "Red", "Red")
    
    # draw scores
    c.draw_text(str(score1), (WIDTH / 3, HEIGHT / 3), 36, "Yellow")
    c.draw_text(str(score2), ((2 * WIDTH / 3), HEIGHT / 3), 36, "Red")

# Event Handlers

def keydown(key):
    global paddle1_vel, paddle2_vel
    vel = 8
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel[1] += vel
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel[1] += -vel
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel[1] += vel
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] += - vel
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s'] or key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] = 0
    elif key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['up']:
        paddle2_vel[1] = 0

def restart():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
restart_button = frame.add_button("Restart!", restart)

# start frame
new_game()
frame.start()
