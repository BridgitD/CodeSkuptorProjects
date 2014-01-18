import simplegui
import math
import random

#### GLOBALS ####

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

#### IMAGES ####
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

#### TRANSFORMATIONS ####
# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

#### CLASSES ####
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    # Draw Handler
    def draw(self,canvas):
        if self.thrust == True:
            canvas.draw_image(self.image, (self.image_center[0] + 90, self.image_center[1]), 
                                           self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                              self.pos, self.image_size, self.angle)

    # Update Method
    def update(self):
        global forward
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel

        # Acceleration
        if self.thrust == True:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0]
            self.vel[1] += acc[1]

        # Velocity
        friction = 0.5
        self.vel[0] *= (1 - friction)
        self.vel[1] *= (1 - friction)
                
    # Turning the Ship
    def turn_left(self, down0_or_up1):
        angle_vel_change = 0.1
        if down0_or_up1 == 0:
            self.angle_vel += -angle_vel_change
        elif down0_or_up1 == 1:
            self.angle_vel = 0
            
    def turn_right(self, down0_or_up1):
        angle_vel_change = 0.1
        if down0_or_up1 == 0:
            self.angle_vel += angle_vel_change
        elif down0_or_up1 == 1:
            self.angle_vel = 0
    
    # Turn on the Thrusters
    def thrusters(self, down0_or_up1):
        if down0_or_up1 == 0:
            self.thrust = True
            ship_thrust_sound.play()
        elif down0_or_up1 == 1:
            self.thrust = False
            ship_thrust_sound.rewind()

    # Shoot Missles
    def attack(self, down0_or_up1):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_speed = 1.2
        missile_pos = (self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1])
        missile_vel = ((self.vel[0] + forward[0] * 2) * missile_speed, (self.vel[1] + forward[1] * 2) * missile_speed)
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
        if down0_or_up1 == 0:
            missile_group.add(a_missile)
            
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += .5
        if self.age >= self.lifespan:
            return True
        elif self.age < self.lifespan:
            return False
        
    # Collisions!
    def collide(self, other_object):
        pos1 = self.pos
        pos2 = other_object.pos
        radius1 = self.radius
        radius2 = other_object.radius
        if dist(pos1, pos2) < radius1 + radius2:
            return True
        else:
            return False

#### ADDITIONAL HELPER FUNCTIONS ####
# Rock-Ship collision
def group_collide(sprite_set, other_object):
    global lives
    for sprite in list(sprite_set):
        if sprite.collide(other_object) == True:
            sprite_set.discard(sprite)
            return True

# Missile-Rock collision
def group_group_collide(sprite_set1, sprite_set2):
    global missile_hits
    missile_hits = 0
    for sprite in list(sprite_set1):
        if group_collide(sprite_set2, sprite) == True:
            sprite_set1.discard(sprite)
            missile_hits += 1
    return missile_hits

#### DRAW METHODS ####
# Iterate draw methods for sprite sets
def process_sprite_group(sprite_set, canvas):
    for sprite in sprite_set:
        sprite.draw(canvas)
    for sprite in list(sprite_set):
        if sprite.update() == True:
            sprite_set.pop()
        
# Spawn a rock into rock set
def rock_spawner():
    global rock_group, my_ship
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
    rock_spin = random.random() * .2 - .1
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_spin, asteroid_image, asteroid_info)
    if dist(a_rock.pos, my_ship.pos) > a_rock.radius + my_ship.radius:
        if len(rock_group) == 12:
            rock_group.pop()
            rock_group.add(a_rock)
        elif len(rock_group) < 12:
            rock_group.add(a_rock)

# Draw method        
def draw(canvas):
    global time, lives, score, rock_group, missile_group, started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # draw & update ship and sprites
    if started == True:
        my_ship.draw(canvas)
        my_ship.update()
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
    
    # collision time!
    if group_collide(rock_group, my_ship) == True:
        lives -= 1
    if group_group_collide(rock_group, missile_group) > 0:
        global score, missile_hits
        score += missile_hits
        
    # Score and Time
    canvas.draw_text("Score: " + str(score), (WIDTH - 100, 40), 24, "White")
    canvas.draw_text("Lives: " + str(lives), (20, 40), 24, "White")

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    
    # resetting the game
    if lives == 0:
        started = False
        rock_group = set([])
        missile_group = set([])
        canvas.draw_text("GAME OVER", (WIDTH / 3 + 15, 50), 36, "Red")
        soundtrack.pause()

        
#### INITIALIZING ####
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
timer = simplegui.create_timer(1000.0, rock_spawner)

# initialize ship and two sprite sets
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 300, ship_image, ship_info)
rock_group = set([])
missile_group = set([])        

#### HANDLERS ####
# mouseclick handler that resets UI and conditions whether splash image is drawn
def click(pos):
    global started, timer, score, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        timer.start()
        score = 0
        lives = 3
        soundtrack.rewind()
        soundtrack.play()

# dictionary for keystrokes
keystroke = {"left": my_ship.turn_left,
             "right": my_ship.turn_right,
             "up": my_ship.thrusters,
             "space": my_ship.attack
            }

# keyup and keydown
def keydown(key):
    for i in keystroke:
        if key == simplegui.KEY_MAP[i]:
            keystroke[i](0)

def keyup(key):
    for i in keystroke:
        if key == simplegui.KEY_MAP[i]:
            keystroke[i](1)
    
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

    
#### LET'S GO! ####
# get things rolling
frame.start()

