from chunk import Chunk
from settings import *
import numpy as np
import glm


class World:
    def __init__(self, ctx, shaders):
        self.ctx = ctx
        self.shaders = shaders
        self.quad_shader = self.shaders["quad"].program
        self.chunk_shader = self.shaders["chunk"].program
        self.chunks = [None for _ in range(WORLD_VOLUME)]
        self.voxels = np.empty([WORLD_VOLUME, CHUNK_VOLUME], dtype="uint8")
        self.build_chunks()

    def build_chunks(self):
        for x in range(WORLD_WIDTH):
            for z in range(WORLD_DEPTH):
                for y in range(WORLD_HEIGHT):
                    chunk = Chunk(
                        self.ctx, self.chunk_shader, glm.vec3(x, y, z) * CHUNK_SIZE
                    )
                    chunk_index = x + z * WORLD_WIDTH + y * WORLD_AREA
                    self.chunks[chunk_index] = chunk
                    # self.voxels[chunk_index] = chunk.build_voxels()
                    # chunk.voxels = self.voxles[chunk_index]
                    # chunk.build_mesh(self)

    def update(self, dt):
        for chunk in self.chunks:
            chunk.update()

    def render(self):
        for chunk in self.chunks:
            self.chunk_shader["m_model"].write(chunk.m_model)
            chunk.render()
