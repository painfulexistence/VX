from mesh import ChunkMesh
from bounding_volume import BoundingSphere
from settings import *
import numpy as np
import glm


class Chunk:
    def __init__(self, ctx, shader, position, world):
        self.ctx = ctx
        self.shader = shader
        self.position = position
        self.world = world
        self.is_empty = True
        self.voxels = np.zeros(CHUNK_VOLUME, dtype="uint8")
        self.mesh = None
        self.m_model = glm.translate(glm.mat4(), glm.vec3(position) * CHUNK_SIZE)
        self.bsphere = BoundingSphere(glm.vec3(position) * CHUNK_SIZE + glm.vec3(HALF_CHUNK_SIZE), CHUNK_BSPHERE_RADIUS)

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
        if np.any(voxels):
            self.is_empty = False
        return voxels

    def build_mesh(self):
        self.mesh = ChunkMesh(self.ctx, self.shader, self.position, self.world)

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
