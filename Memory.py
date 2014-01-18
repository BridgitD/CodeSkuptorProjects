# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global deck 
    global exposed
    global state
    global card_location
    global turns
    global label
    deck = range(1, 9) * 2
    exposed = [False] * 16
    state = 0
    card_location = []
    random.shuffle(deck)
    turns = 0
    label.set_text("Turns = " + str(turns))

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed
    global state
    global card_location
    global deck
    global turns
    x = pos[0] // 50
    card_location.append(x)
    if exposed[x] == False:
        if state == 0:
            exposed[x] = True
            state = 1
        elif state == 1:
            exposed[x] = True
            state = 2
            turns += 1
            label.set_text("Turns = " + str(turns))
        elif state == 2:
            if deck[card_location[-2]] == deck[card_location[-3]]:
                state = 1
            else:
                exposed[card_location[-2]] = False
                exposed[card_location[-3]] = False
                state = 1
            exposed[x] = True
    else:
        pass

            
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global deck
    global exposed
    card_position = range(16)
    for place in card_position:
        if exposed[place] == False:
            canvas.draw_polygon([(place * 50, 0), ((place + 1) * 50, 0), ((place + 1) * 50, 100), (place * 50, 100)], 2, "Red", "Green")
        if exposed[place] == True:
            canvas.draw_text(str(deck[place]), ((place * 50) + 15, 60), 40, "White")

    

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = ")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
