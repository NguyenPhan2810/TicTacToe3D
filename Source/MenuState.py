from GameState import *
from PlayGround import *
import pygame
from OpenGL.GL import *
import configuration as cfg
import enum

class MenuState(BaseState):
    def __init__(self):
        self.font = None

    def constructor(self):
        self.font = pygame.font.SysFont('Corbel',35)