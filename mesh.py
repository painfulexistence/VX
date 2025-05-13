import numpy as np
from settings import *


class BaseMesh:
    def __init__(self, ctx, program):
        self.ctx = ctx
        self.program = program
        self.vao = None
        self.setup()

    def setup(self):
        raise NotImplementedError("Mesh classes must implement the setup method")

    def render(self):
        self.vao.render()


class QuadMesh(BaseMesh):
    def __init__(self, ctx, program):
        super().__init__(ctx, program)

    def setup(self):
        vertices = [
            (0.5, 0.5, 0.0),
            (-0.5, 0.5, 0.0),
            (0.5, -0.5, 0.0),
            (0.5, -0.5, 0.0),
            (-0.5, 0.5, 0.0),
            (-0.5, -0.5, 0.0),
        ]
        colors = [(0, 1, 0), (1, 0, 0), (0, 0, 1), (0, 0, 1), (1, 0, 0), (0, 1, 0)]
        vertex_data = np.hstack([vertices, colors], dtype="float32")
        vbo = self.ctx.buffer(vertex_data)
        self.vao = self.ctx.vertex_array(
            self.program, [(vbo, "3f 3f", "in_position", "in_color")], skip_errors=True
        )


class ChunkMesh(BaseMesh):
    def __init__(self, ctx, program, voxels):
        self.voxels = voxels
        super().__init__(ctx, program)

    def setup(self):
        vertex_data = build_chunk_mesh(self.voxels)
        vbo = self.ctx.buffer(vertex_data)
        self.vao = self.ctx.vertex_array(
            self.program,
            [(vbo, "3u1 1u1 1u1", "in_position", "voxel_id", "face_id")],
            skip_errors=True,
        )


def is_void(voxel_pos, chunk_voxels):
    x, y, z = voxel_pos
    if 0 <= x < CHUNK_SIZE and 0 <= y < CHUNK_SIZE and 0 <= z < CHUNK_SIZE:
        if chunk_voxels[x + z * CHUNK_SIZE + y * CHUNK_AREA] > 0:
            return False
    return True


def build_chunk_mesh(chunk_voxels):
    vertex_data = np.empty(CHUNK_VOLUME * 18 * 5, dtype="uint8")
    index = 0

    for x in range(CHUNK_SIZE):
        for z in range(CHUNK_SIZE):
            for y in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + z * CHUNK_SIZE + y * CHUNK_AREA]
                if not (voxel_id > 0):
                    continue

                # top
                if is_void((x, y + 1, z), chunk_voxels):
                    v0 = (x, y + 1, z, voxel_id, 0)
                    v1 = (x, y + 1, z + 1, voxel_id, 0)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 0)
                    v3 = (x + 1, y + 1, z, voxel_id, 0)
                    for v in (v0, v1, v2, v2, v3, v0):
                        for attr in v:
                            vertex_data[index] = attr
                            index += 1

                # bottom
                if is_void((x, y - 1, z), chunk_voxels):
                    v0 = (x + 1, y, z, voxel_id, 1)
                    v1 = (x + 1, y, z + 1, voxel_id, 1)
                    v2 = (x, y, z + 1, voxel_id, 1)
                    v3 = (x, y, z, voxel_id, 1)
                    for v in (v0, v1, v2, v2, v3, v0):
                        for attr in v:
                            vertex_data[index] = attr
                            index += 1

                # right
                if is_void((x + 1, y, z), chunk_voxels):
                    v0 = (x + 1, y + 1, z + 1, voxel_id, 2)
                    v1 = (x + 1, y, z + 1, voxel_id, 2)
                    v2 = (x + 1, y, z, voxel_id, 2)
                    v3 = (x + 1, y + 1, z, voxel_id, 2)
                    for v in (v0, v1, v2, v2, v3, v0):
                        for attr in v:
                            vertex_data[index] = attr
                            index += 1

                # left
                if is_void((x - 1, y, z), chunk_voxels):
                    v0 = (x, y + 1, z, voxel_id, 3)
                    v1 = (x, y, z, voxel_id, 3)
                    v2 = (x, y, z + 1, voxel_id, 3)
                    v3 = (x, y + 1, z + 1, voxel_id, 3)
                    for v in (v0, v1, v2, v2, v3, v0):
                        for attr in v:
                            vertex_data[index] = attr
                            index += 1

                # front
                if is_void((x, y, z + 1), chunk_voxels):
                    v0 = (x, y + 1, z + 1, voxel_id, 4)
                    v1 = (x, y, z + 1, voxel_id, 4)
                    v2 = (x + 1, y, z + 1, voxel_id, 4)
                    v3 = (x + 1, y + 1, z + 1, voxel_id, 4)
                    for v in (v0, v1, v2, v2, v3, v0):
                        for attr in v:
                            vertex_data[index] = attr
                            index += 1

                # back
                if is_void((x, y, z - 1), chunk_voxels):
                    v0 = (x + 1, y + 1, z, voxel_id, 5)
                    v1 = (x + 1, y, z, voxel_id, 5)
                    v2 = (x, y, z, voxel_id, 5)
                    v3 = (x, y + 1, z, voxel_id, 5)
                    for v in (v0, v1, v2, v2, v3, v0):
                        for attr in v:
                            vertex_data[index] = attr
                            index += 1

    return vertex_data[: index + 1]
