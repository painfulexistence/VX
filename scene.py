from world import World
from player import Player
import glm


class Scene:
    def __init__(self, ctx, shaders):
        self.ctx = ctx
        self.shaders = shaders
        self.chunk_shader = self.shaders["chunk"].program
        self.world = World(self.ctx, self.shaders)
        self.player = Player(glm.vec3(0, 0, 5))

    def update(self, dt):
        self.world.update(dt)
        self.player.update(dt)

    def render(self):
        self.chunk_shader["m_proj"].write(self.player.proj_matrix)
        self.chunk_shader["m_view"].write(self.player.view_matrix)

        self.world.render()
