import numpy as np


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
    def __init__(self, ctx, program):
        super().__init__(ctx, program)

    def setup(self):
        pass
