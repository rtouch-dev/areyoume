import logging
from ursina import *
def setup_world():
    logging.basicConfig(level=logging.DEBUG)
    Sky(texture='../assets/textures/sky.jpg')
    logging.debug("World Environment Loaded.") #why not
