import json
import os
from ursina import *
import logic # ייבוא הלוגיקה כדי שנוכל להגדיר את הצ'קפוינטים

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
SAVE_FILE = os.path.join(parent_dir, 'worldobjects', 'level_map.json')

directions = {
    'top':    (0, 1, 0),
    'bottom': (0,-1, 0),
    'left':   (-1,0, 0),
    'right':  (1, 0, 0),
    'front':  (0, 0, 1),
    'back':   (0, 0,-1),
}

face_vertices = {
    'top':    [(0,1,0),(1,1,0),(1,1,1),(0,1,1)],
    'bottom': [(0,0,0),(1,0,0),(1,0,1),(0,0,1)],
    'left':   [(0,0,0),(0,1,0),(0,1,1),(0,0,1)],
    'right':  [(1,0,0),(1,1,0),(1,1,1),(1,0,1)],
    'front':  [(0,0,1),(1,0,1),(1,1,1),(0,1,1)],
    'back':   [(0,0,0),(1,0,0),(1,1,0),(0,1,0)],
}

def create_checkpoint_trigger(pos):
    """יוצר ישות שקופה שמתפקדת כטריגר לצ'קפוינט"""
    trigger = Entity(
        model='cube',
        color=color.green,
        alpha=0.3, # חצי שקוף כדי שתראה איפה זה בבדיקות
        position=pos + Vec3(0, 1, 0), # מעל הקובייה
        scale=1,
        collider='box',
        is_checkpoint=True # סימון ללוגיקה
    )
    return trigger

def optimize_bq():
    print("Loading Better Quality (BQ) optimization...")
    level_parent = Entity(model=None, collider=None) 
    checkpoints = []

    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)
        for item in data:
            # יצירת הקובייה הגרפית
            Entity(
                parent=level_parent,
                model='cube',
                texture='white_cube',
                position=(item['x'], item['y'], item['z']),
                scale=1
            )
            # אם זו קוביית צ'קפוינט, ניצור לה טריגר נפרד
            if item.get('checkpoint', False):
                create_checkpoint_trigger(Vec3(item['x'], item['y'], item['z']))

    level_parent.combine()
    level_parent.collider = 'mesh' 
    level_parent.texture = 'white_cube'
    
    for child in level_parent.children:
        destroy(child)
        
    return level_parent

def optimize_pmode():
    print("Loading Performance Mode (PMODE) optimization...")
    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)

    blocks = set((int(b['x']), int(b['y']), int(b['z'])) for b in data)
    
    # חילוץ צ'קפוינטים
    for item in data:
        if item.get('checkpoint', False):
            create_checkpoint_trigger(Vec3(item['x'], item['y'], item['z']))

    vertices = []
    triangles = []
    uvs = []
    vertex_index = 0

    for (x, y, z) in blocks:
        for face, direction in directions.items():
            neighbor = (x + direction[0], y + direction[1], z + direction[2])
            if neighbor in blocks:
                continue

            verts = face_vertices[face]
            for vx, vy, vz in verts:
                vertices.append(Vec3(vx + x, vy + y, vz + z))

            triangles += [
                vertex_index, vertex_index+1, vertex_index+2,
                vertex_index, vertex_index+2, vertex_index+3
            ]

            uvs += [(0,0),(1,0),(1,1),(0,1)]
            vertex_index += 4

    mesh = Mesh(vertices=vertices, triangles=triangles, uvs=uvs, mode='triangle')
    entity = Entity(model=mesh, texture='white_cube', collider='mesh')
    return entity

def load_optimized_level():
    if not os.path.exists(SAVE_FILE):
        return None

    print("--- Level Optimizer ---")
    while True:
        choice = input("Enter mode (BQ / PMODE): ").strip().upper()
        if choice == 'BQ':
            return optimize_bq()
        elif choice == 'PMODE':
            return optimize_pmode()
        else:
            print("Invalid input.")