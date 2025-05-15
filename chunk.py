from mesh import ChunkMesh
from settings import *
import numpy as np
import glm


class Chunk:
    def __init__(self, ctx, shader, position):
        self.ctx = ctx
        self.position = position
        self.voxels = self.build_voxels()
        self.mesh = ChunkMesh(ctx, shader, self.voxels)
        self.m_model = glm.translate(glm.mat4(), glm.vec3(position) * CHUNK_SIZE)

    def build_voxels(self):
        voxels = np.zeros(CHUNK_VOLUME, dtype="uint8")

        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                wx = cx + x
                wz = cz + z
                world_height = int(terrain((wx, wz)) * 32 + 32)
                local_height = min(world_height - cy, CHUNK_SIZE)
                for y in range(local_height):
                    wy = cy + y
                    voxels[x + z * CHUNK_SIZE + y * CHUNK_AREA] = wy + 1
        return voxels

    def update(self):
        pass

    def render(self):
        self.mesh.render()


def terrain(p):
    sum = 0
    freq = 0.005
    amp = 1.0
    for _ in range(8):
        sum += amp * glm.simplex(glm.vec2(p) * freq)
        freq *= 2.0
        amp /= 2.0
    sum /= 2  # normalization
    return sum
