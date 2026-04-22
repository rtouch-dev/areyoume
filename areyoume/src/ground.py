from ursina import Entity, color
def setup_ground():
    ground = Entity(
        model='plane', 
        scale=(100, 1, 100), 
        texture='../assets/textures/floor.jpg', 
        texture_scale=(10, 10), 
        collider='box',
        color=color.white,
        position=(0,0,0)
)
    
    return ground