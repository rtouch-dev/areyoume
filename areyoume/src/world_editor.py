from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json
import os
import simplepbr
import world
import ground

app = Ursina(title='AreYouMe - World Editor')

window.fullscreen = True
window.show_ursina_splash = False     
pipeline = simplepbr.init()
window.icon = '../assets/textures/icon.ico'
window.cog_button.enabled = True
world.setup_world() 
ground.setup_ground() 

editor_cam = EditorCamera()

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
SAVE_DIR = os.path.join(parent_dir, 'worldobjects')
BACKUP_DIR = os.path.join(SAVE_DIR, 'backups')
SAVE_FILE = os.path.join(SAVE_DIR, 'level_map.json')
OPTIMIZER_BACKUP = os.path.join(SAVE_DIR, 'level_map_no_mesh.json')

if not os.path.exists(SAVE_DIR): os.makedirs(SAVE_DIR)
if not os.path.exists(BACKUP_DIR): os.makedirs(BACKUP_DIR)

blocks = []

class EditorBlock(Entity):
    def __init__(self, position=(0,0,0), is_checkpoint=False):
        super().__init__(
            model='cube',
            texture='white_cube',
            color=color.green if is_checkpoint else color.white,
            collider='box',
            position=position,
            scale=1
        )
        self.is_checkpoint = is_checkpoint
        blocks.append(self)

def get_next_backup_name():
    i = 1
    while True:
        backup_path = os.path.join(BACKUP_DIR, f'backup_{i}.json')
        if not os.path.exists(backup_path):
            return backup_path
        i += 1

def save_world():
    if os.path.exists(SAVE_FILE):
        new_backup = get_next_backup_name()
        os.rename(SAVE_FILE, new_backup)

    if os.path.exists(OPTIMIZER_BACKUP):
        os.remove(OPTIMIZER_BACKUP)
        
    # שמירת נתונים כולל האם הקובייה היא צ'קפוינט
    data = [{
        'x': b.x, 
        'y': b.y, 
        'z': b.z, 
        'checkpoint': getattr(b, 'is_checkpoint', False)
    } for b in blocks]
    
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"World Saved with Checkpoints to: {SAVE_FILE}")

def load_world():
    target = OPTIMIZER_BACKUP if os.path.exists(OPTIMIZER_BACKUP) else SAVE_FILE
    
    if os.path.exists(target):
        for b in blocks: destroy(b)
        blocks.clear()
        with open(target, 'r') as f:
            loaded_data = json.load(f)
            for item in loaded_data:
                if isinstance(item, dict):
                    EditorBlock(
                        position=(item['x'], item['y'], item['z']), 
                        is_checkpoint=item.get('checkpoint', False)
                    )
                else:
                    EditorBlock(position=(item[0], item[1], item[2]))
        print("World Loaded.")

def input(key):
    # הפיכה לצ'קפוינט: לחיצה על C + עכבר שמאלי על קובייה קיימת
    if key == 'left mouse down' and held_keys['c']:
        if mouse.hovered_entity and isinstance(mouse.hovered_entity, EditorBlock):
            mouse.hovered_entity.is_checkpoint = True
            mouse.hovered_entity.color = color.green
            print("Block set as Checkpoint!")
            return

    if key == 'left mouse down':
        if mouse.hovered_entity:
            new_pos = mouse.hovered_entity.position + mouse.normal
            EditorBlock(position=new_pos)
        else:
            target_pos = camera.position + camera.forward * 5
            EditorBlock(position=(round(target_pos.x), round(target_pos.y), round(target_pos.z)))

    if key == 'right mouse down':
        if mouse.hovered_entity and isinstance(mouse.hovered_entity, EditorBlock):
            blocks.remove(mouse.hovered_entity)
            destroy(mouse.hovered_entity)

    if key == 's': save_world()
    if key == 'l': load_world()
    if key == 'escape': quit()

load_world()
app.run()