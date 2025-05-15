from chunk import Chunk
from settings import *
import numpy as np


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
                    chunk = Chunk(self.ctx, self.chunk_shader, (x, y, z), self)
                    chunk_index = x + z * WORLD_WIDTH + y * WORLD_AREA
                    self.chunks[chunk_index] = chunk
                    self.voxels[chunk_index] = chunk.voxels = chunk.build_voxels()
        for chunk in self.chunks:
            chunk.build_mesh() # depends on self.voxels

    def update(self, dt):
        for chunk in self.chunks:
            chunk.update()

    def render(self):
        for chunk in self.chunks:
            if not chunk.is_empty:
                self.chunk_shader["m_model"].write(chunk.m_model)
                chunk.render()
