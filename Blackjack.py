# Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
game_deck = []
player_hand = []
dealer_hand = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        hand_str = ""
        for card in self.hand:
            hand_str += (str(card) + " ")
        return "Hand contains " + hand_str

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        hand_value = 0
        for card in self.hand:
            hand_value += VALUES[card.get_rank()]
        if 'A' not in [self.hand[i].get_rank() for i in range(len(self.hand))]:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value

    def draw(self, canvas, pos):
        card_pos = pos
        for card in self.hand:
            card.draw(canvas, pos)
            pos[0] += 90
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        dealt_card = self.deck[0]
        self.deck.pop(0)
        return dealt_card
    
    def __str__(self):
        deck_str = ""
        for card in self.deck:
            deck_str += (str(card) + " ")
        return "Deck contains " + deck_str


#define event handlers for buttons
def deal():
    global outcome, in_play, game_deck, player_hand, dealer_hand, outcome, score
    
    if in_play == True:
        # You lose
        in_play = False
        outcome = "Dealer wins."
        score -= 1
    
    else:
        # New shuffled deck
        game_deck = Deck()
        game_deck.shuffle()
    
        # New hands
        player_hand = Hand()
        dealer_hand = Hand()
        
        # Deal two cards
        player_hand.add_card(game_deck.deal_card())
        dealer_hand.add_card(game_deck.deal_card())
        player_hand.add_card(game_deck.deal_card())
        dealer_hand.add_card(game_deck.deal_card())
    
        in_play = True
        outcome = "Hit or Stand?"

def hit():
    global in_play, game_deck, player_hand, dealer_hand, score, outcome
 
    # if the hand is in play, hit the player
    if player_hand.get_value() < 21:
        player_hand.add_card(game_deck.deal_card())
        
        # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            outcome = "You have busted."
            in_play = False
            score -= 1
    else:
        outcome = "You have busted."
       
def stand():
    global in_play, game_deck, player_hand, dealer_hand, score, outcome
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == False:
        outcome = "You have busted."
    else:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(game_deck.deal_card())

        # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21:
            outcome = "Dealer busted."
            score += 1
        else:
            if player_hand.get_value() <= dealer_hand.get_value():
                outcome = "Dealer wins."
                score -= 1
            else:
                outcome = "Player wins."
                score += 1
        in_play = False
    
    

# draw handler    
def draw(canvas):
    # Draw Title
    canvas.draw_text("Blackjack", [200, 550], 50, 'Aqua')

    # Draw explanations
    canvas.draw_text("Player", [75, 325], 36, 'Black')
    canvas.draw_text("Dealer", [75, 125], 36, 'Black')
    canvas.draw_text(outcome, [75, 50], 40, 'Lime')
    canvas.draw_text("Score: " + str(score), [400, 300], 36, 'Yellow')

    # Draw player hand
    player_hand.draw(canvas, [100, 350])

    # Draw dealer hand
    dealer_hand.draw(canvas, [100, 150])
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (100 + CARD_BACK_CENTER[0], 150 + CARD_BACK_CENTER[1]), CARD_BACK_SIZE)



# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
