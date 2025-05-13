from chunk import Chunk
from player import Player
import glm


class Scene:
    def __init__(self, ctx, shaders):
        self.ctx = ctx
        self.shaders = shaders
        self.quad_shader = self.shaders["quad"].program
        self.chunk_shader = self.shaders["chunk"].program
        self.chunk = Chunk(self.ctx, self.chunk_shader)
        self.player = Player(glm.vec3(0, 0, 5))

    def update(self, dt):
        self.player.update(dt)

        self.chunk_shader["m_proj"].write(self.player.proj_matrix)
        self.chunk_shader["m_view"].write(self.player.view_matrix)
        self.chunk_shader["m_model"].write(glm.mat4())

    def render(self):
        self.chunk.render()
