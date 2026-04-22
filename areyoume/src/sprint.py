from ursina import *
import time

#  creating object onec for all
tired_text = Entity(
    parent=camera.ui,
    model='quad',
    texture='../assets/textures/no_stamina.png',
    scale=(0.25, 0.028),
    # X=0 למרכז, Y=0.45 כדי שיהיה למעלה (במערכת ה-UI של Ursina)
    # הערה: אם אתה רוצה להשתמש בערכים מוחלטים כמו 5-, וודא שזה מתאים לקנה המידה של ה-UI שלך
    position=(0, 0.45), 
    origin=(0, 0.5), 
    enabled=False # waiting in memory like a good boi
)
tired_text.texture.filtering = None

# logics
sprinttimer = 0
cansprint = True
cooldowntime = 0

def handle_sprint(player, startspeed):
    global sprinttimer, cansprint, cooldowntime
    
    # cooldown check
    if not cansprint and time.time() >= cooldowntime:
        cansprint = True
        # simply:yes or no
        tired_text.enabled = False 

    # sprint logic
    if held_keys['left shift'] and cansprint:
        player.speed = 30 
        sprinttimer += time.dt
        
        if sprinttimer >= 5:
            cansprint = False
                        
            tired_text.enabled = True # modechanger
            sprinttimer = 0
            player.speed = startspeed
            cooldowntime = time.time() + 5 
    else:
        player.speed = startspeed
        if not held_keys['left shift']:
            sprinttimer = 0