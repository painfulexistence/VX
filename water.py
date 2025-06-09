import moderngl as gl
from mesh import WaterMesh
import glm
from settings import *

class Water:
    def __init__(self, ctx, shader):
        self.ctx = ctx
        self.mesh = WaterMesh(ctx, shader, (CHUNK_SIZE * WORLD_WIDTH, CHUNK_SIZE * WORLD_DEPTH))
        self.shader = shader
        self.shallow_color = COLOR_MINT_GREEN
        self.deep_color = COLOR_INDIGO
        self.wave_speed = 1.0
        self.wave_strength = 0.1
        z_offset = 0.05 # to avoid z-fighting
        self.m_model = glm.translate(glm.mat4(), glm.vec3(0.0, WATER_LINE + z_offset, 0.0))

    def update(self, dt):
        pass

    def render(self):
        self.shader["m_model"].write(self.m_model)
        self.shader["u_deep_color"].write(self.deep_color)
        self.shader["u_shallow_color"].write(self.shallow_color)
        self.shader["u_wave_speed"].value = self.wave_speed
        self.shader["u_wave_strength"].value = self.wave_strength
        self.shader["u_water_line"].value = WATER_LINE
    
        self.ctx.enable(gl.BLEND)
        self.ctx.disable(gl.CULL_FACE)
        # self.ctx.depth_mask = False
        self.ctx.blend_func = gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA
        self.mesh.render()
        # self.ctx.depth_mask = True
        self.ctx.disable(gl.BLEND)
        self.ctx.enable(gl.CULL_FACE)