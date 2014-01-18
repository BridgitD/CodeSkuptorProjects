# Creates a Stopwatch

import simplegui

# define global variables
time = 0
win = 0
game = 0

# helper function that converts time in tenths of seconds into formatted string A:BC.D
def format(t):
    minutes = t // 600
    tens_secs = ((t // 10) % 60) // 10
    secs = ((t // 10) % 60) % 10
    mili_secs = (((t % 10) % 60) % 10) % 10
    return str(minutes) + ":" + str(tens_secs) + str(secs) + "." + str(mili_secs)
    
# event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()

def stop():
    global win
    global game
    if timer.is_running():
        timer.stop()
        game += 1
        if time % 10 == 0:
            win += 1

def reset():
    global time
    global win
    global game
    time = 0
    win = 0
    game = 0

# event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time += 1
    
# draw handler
def draw_handler(canvas):
    global time
    global win
    global game
    canvas.draw_text("How good are your reflexes?", (15, 15), 20, "Green")
    canvas.draw_text(format(time), (100,75), 32, "Red")
    canvas.draw_text(str(win) + "/" + str(game), (200, 50), 24, "White")
    canvas.draw_text("Click exactly on the second mark to win", (15, 115), 20, "Green")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 350, 125)
frame.set_draw_handler(draw_handler)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)
start_button = frame.add_button('Start', start)
stop_button = frame.add_button('Stop', stop)
reset_button = frame.add_button('Reset', reset)

# start frame
frame.start()
