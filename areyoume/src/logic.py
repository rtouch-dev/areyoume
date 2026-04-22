# logic.py
from ursina import clamp, Vec3


current_checkpoint = Vec3(0, 2, 0)

def reset_game(player, enemies=None):
    # שימוש בנקודה שנשמרה במקום בערך קבוע
    player.position = current_checkpoint
    player.rotation = (0, 0, 0)
    
    if hasattr(player, 'health'):
        player.health = 100

    if enemies:
        for e in enemies:
            e.position = e.start_position
            e.health = 100

def update_camera_view(player, camera, camera_distance):
    dist = clamp(camera_distance, 0, 20)
    if dist <= 0:
        camera.position = (0, 0, 0)
        player.character.enabled = False
    else:
        player.character.enabled = True
        camera.position = (0, (dist / 4) + 1, -dist)
    return dist