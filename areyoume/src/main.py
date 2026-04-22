#todo: add main menu

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from logic import reset_game, update_camera_view
import os
import simplepbr
import time
import music 
import world
import ground
from sprint import handle_sprint
import json
import optimizer

#definitions
startspeed = 10
flying_gravity = -2
startgravity = 3.67676767
cam_dist = 0
black = color.black
#me = sigma


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
SAVE_FILE = os.path.join(parent_dir, 'worldobjects', 'level_map.json')


optimizer.load_optimized_level() 


app = Ursina(title='AreYouMe')              #start game
window.fullscreen = True
window.show_ursina_splash = False     
pipeline = simplepbr.init()
window.icon = '../assets/textures/icon.ico'
window.exit_button.enabled = False
window.cog_button.enabled = False


#setups
world.setup_world() 
ground.setup_ground() 


player = FirstPersonController(position=(0, 2, 0))
player.cursor.visible = False

# alvin
player.character = Entity(
    model='../assets/alvin/alvin.glb', 
    parent=player, 
    scale=1, 
    y=1, 
    rotation_y=0,
    color = black, 
    enabled=False
    
)

camera.parent = player.camera_pivot
camera.position = (0, 0, 0)
camera.rotation_x = 0

mouse.locked = True

def update():
    global cam_dist
    
    #if held_keys['up arrow']:
        #player.position += player.forward * startspeed * time.dt
    #if held_keys['down arrow']:
        #player.position += player.back * startspeed * time.dt
    #if held_keys['left arrow']:
        #player.position += player.left * startspeed * time.dt
    #if held_keys['right arrow']:
        #player.position += player.right * startspeed * time.dt
    

    if player.position.y < -30:
        reset_game(player)
        
    handle_sprint(player, startspeed)
    
    # Update camera based on current cam_dist
    cam_dist = update_camera_view(player, camera, cam_dist)

    if held_keys['space']:
        player.gravity = flying_gravity
    else:
        player.gravity = startgravity
    
    
    
def input(key):
    global cam_dist
    
    if key == 'escape':
        quit()
        
    if key == 'r':
        reset_game(player, [])

    # Scroll detection
    if key == 'scroll up':
        cam_dist -= 1
    if key == 'scroll down':
        cam_dist += 1

#music.start() #you can add a hashtag if you want the music to stfu. it'll look like that: #music.start()
app.run()