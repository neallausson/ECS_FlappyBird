from components import SpriteSheetSequenceComponent
from components import RectangleColliderComponent
from components import ResetPositionSystem
from components import ObstacleTagComponent
from components import ScrollableSystem
from components import RenderableSystem
from components import TransformComponent
from components import RigiBodyComponent
from components import PlayerTagComponent
from components import PipeStateComponent
from components import PipeTagComponent
from components import ScoreComponent
from components import FlapComponent

from maths import Vector2D
from ecs import System

import pygame as pg
import numpy as np
import physics

class SpriteSheetSequenceSystem(System):
    def __init__(self):
        super().__init__()

    def update(self, dt, *args, **kwargs):
        components = self.world.get_components(SpriteSheetSequenceComponent,RenderableSystem)
        if components is None: return

        for ent,(sss, rend) in components:
            sss.clock += dt

            sss.index += int(sss.clock / sss.duration)
            sss.index %= len(sss.sprites)
            rend.sprite = sss.sprites[sss.index]

            if sss.clock > sss.duration: sss.clock = 0

class RenderableSystem(System):
    def __init__(self,window):
        super().__init__()
        self.window = window
        self.w = window.get_width()
        self.h = window.get_height()

    def update(self, *args, **kwargs):
        components = self.world.get_components(TransformComponent, RenderableComponent)
        if components is None : return

        components.sort(key=lambda x: x[1][1].depth)
        for ent, (trans,rend) in components:
            sprite = rend.sprite
            if trans.rot != None:
                sprite = pg.transform.rotate(sprite.copy(),trans.rot)
                rend.pos = Vector2D(-0.5 * sprite.get_width(),0.5)

class GravitySystem(System):
    def __init__(self, force=-9.8):
        super().__init__()
        self.force = force

    def update(self, *args, **kwargs):
        components = self.world.get_component(RigiBodyComponent)
        if components is None: return

        for ent,rigid in components:
            rigid.acc += Vector2D(0,self.force)

class MovementSystem(System):
    def __init__(self):
        super().__init__()

    def update(self,dt,*args, **kwargs):
        components = self.World.get_components(TransformComponent,RigiBodyComponent)
        if components is None: return

        for ent,(trans,rigid) in components:
            last_vel = Vector2D(rigid.vel.x,rigid.vel.y)
            rigid.vel += rigid.acc * dt
            trans.pos += 0.5 * (last_vel + rigid.vel)*dt

            rigid.acc = Vector2D()
