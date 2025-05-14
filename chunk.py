from mesh import ChunkMesh
from settings import *
import numpy as np
import glm


class Chunk:
    def __init__(self, ctx, shader, position):
        self.ctx = ctx
        self.voxels = self.build_voxels()
        self.mesh = ChunkMesh(ctx, shader, self.voxels)
        self.m_model = glm.translate(glm.mat4(), position)

    def build_voxels(self):
        voxels = np.zeros(CHUNK_VOLUME, dtype="uint8")
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    voxels[x + z * CHUNK_SIZE + y * CHUNK_AREA] = (
                        x + y + z
                        if int(glm.simplex(glm.vec3(x, y, z) * 0.1) + 1)
                        else 0
                    )
        return voxels

    def update(self):
        pass

    def render(self):
        self.mesh.render()
