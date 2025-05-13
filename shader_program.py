from settings import *


class ShaderProgram:
    def __init__(self, ctx, shader_name):
        self.ctx = ctx
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_src = file.read()
        with open(f"shaders/{shader_name}.frag") as file:
            fragment_src = file.read()
        self.program = ctx.program(
            vertex_shader=vertex_src, fragment_shader=fragment_src
        )
        self.uniforms = {}

    def use(self):
        self.program.use()

    def set_texture(self, name, unit):
        pass
        # texture.use(unit=unit)

    def release(self):
        self.program.release()
