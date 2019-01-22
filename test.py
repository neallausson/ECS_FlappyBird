from maths import Vector2D
from ecs import System

class TransformComponent(object):
    def __init__(self,x,y,rot=None):
        self.pos = Vector2D(x,y)
        self.rot = rot

class RigiBodyComponent(object):
    def __init__(self, vel_x=0,vel_y=0,acc_x=0 , acc_y=0):
        self.vel = Vector2D(vel_x,vel_y)
        self.acc = Vector2D(acc_x,acc_y)

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

from ecs import World
from time import time

world = World()

gravity = world.add_system(GravitySystem(force=-9.8), priority=1)
movement = world.add_system(MovementSystem(), priority = 0)

player = world.create_entity(
TransformComponent(100,100),
RigiBodyComponent()
)

last_time = time()

while True:
    current_time = time()
    dt = current_time - last_time
    last_time = current_time

    world.update(dt)
