from pgzero.actor import Actor 
import pgzrun
from random import randint
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))

WIDTH = 1400
HEIGHT = 800
mango = Actor("mango")
apple = Actor("apple")
score = 0
message = ""
time_left = 60  # Game duration in seconds
game_over = False
frame_count = 0
password_mode = False
password_input = ""
secret_active = False

def draw():
    screen.fill((200, 180, 255))
    mango.draw()
    apple.draw()
    
    # Draw score and time
    screen.draw.text(f"Score: {score}", (20, 20), color="white", fontsize=50, sysfontname="courier", bold=True, shadow=(2, 2))
    screen.draw.text(f"Time: {time_left}", (1100, 20), color="white", fontsize=50, sysfontname="courier", bold=True, shadow=(2, 2))
    
    # Show secret mode indicator
    if secret_active:
        screen.draw.text("★ SECRET MODE ★", center=(700, 100), color="gold", fontsize=40, sysfontname="courier", bold=True, shadow=(2, 2))
    
    if message == "Good shot!":
        screen.draw.text(message, center=(700, 750), color="green", fontsize=80, sysfontname="courier", bold=True, shadow=(2, 2))
    elif message == "You missed!":
        screen.draw.text(message, center=(700, 400), color="red", fontsize=80, sysfontname="courier", bold=True, shadow=(2, 2))
    elif message == "Oh no! Wrong fruit!":
        screen.draw.text(message, center=(700, 400), color="red", fontsize=80, sysfontname="courier", bold=True, shadow=(2, 2))
    
    # Show password input mode
    if password_mode:
        screen.draw.text(f"Password: {password_input}", center=(700, 400), color="yellow", fontsize=40, sysfontname="courier", bold=True, shadow=(2, 2))
    
    if game_over:
        screen.draw.text("GAME OVER!", center=(700, 300), color="white", fontsize=100, sysfontname="courier", bold=True, shadow=(2, 2))
        screen.draw.text(f"Final Score: {score}", center=(700, 450), color="white", fontsize=60, sysfontname="courier", bold=True, shadow=(2, 2))

def fruits_overlap():
    return mango.colliderect(apple)
                         
def place_mango():
    mango.x = randint(50, 1350)
    mango.y = randint(50, 750)
    # Keep trying new positions until they don't overlap
    while fruits_overlap():
        mango.x = randint(50, 1350)
        mango.y = randint(50, 750)
    
def place_apple():
    apple.x = randint(50, 1350)
    apple.y = randint(50, 750)
    # Keep trying new positions until they don't overlap
    while fruits_overlap():
        apple.x = randint(50, 1350)
        apple.y = randint(50, 750)
    
def on_mouse_down(pos):
    global score, message
    
    if game_over or password_mode:
        return
    
    if mango.collidepoint(pos):
        score += 1
        message = "Good shot!"
        sounds.pop.play()
        place_mango()
        place_apple()
    elif apple.collidepoint(pos):
        score = score - 5
        message = "Oh no! Wrong fruit!"
        sounds.pop.play()
        place_apple()
        place_mango()
    else:
        message = "You missed!"

def on_key_down(key):
    global password_mode, password_input, secret_active
    
    if password_mode:
        if key == keys.RETURN:
            # Check if password matches current score
            if password_input == str(score):
                secret_active = True
                password_input = ""
                password_mode = False
            else:
                password_input = ""
                password_mode = False
        elif key == keys.BACKSPACE:
            password_input = password_input[:-1]
        else:
            # Add number to password
            password_input += chr(key)
    else:
        # Press 'P' to activate password mode
        if key == keys.P:
            password_mode = True
            password_input = ""

def update():
    global time_left, game_over, frame_count, score
    
    if not game_over:
        frame_count += 1
        # Assuming 60 FPS, decrease time every 60 frames (1 second)
        if frame_count >= 60:
            time_left -= 1
            frame_count = 0
            if time_left <= 0:
                time_left = 0
                game_over = True
        
        # Secret mode: double points!
        if secret_active and frame_count % 10 == 0:
            score += 1

# Initialize game
place_mango()
place_apple()

# Change to script directory and play music
os.chdir(script_dir)
music.play("chiptune_background.wav")

pgzrun.go()
