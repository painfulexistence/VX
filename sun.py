from mesh import QuadMesh
from settings import *
import glm
import moderngl as gl

class Sun:
    def __init__(self, ctx, shader):
        self.ctx = ctx
        self.shader = shader
        self.mesh = QuadMesh(ctx, shader)
        self.height = 64
        self.radius = 20.0
        self.color = COLOR_VIVID_GOLD * 10.0
        self.light_color = COLOR_WHITE * 3.0
        self.light_direction = glm.normalize(glm.vec3(0.0, -1.0, 0.5))
        self.m_model = self.get_model_matrix()

    def get_model_matrix(self):            
        position = glm.vec3(CENTER_X, self.height, CENTER_Z)
        rot = glm.mat4()

        if self.light_direction.z > 0:
            atan = self.light_direction.x / self.light_direction.z
            position.z = CENTER_Z - CHUNK_SIZE * WORLD_DEPTH
            position.x = CENTER_X - CHUNK_SIZE * WORLD_DEPTH * atan
        elif self.light_direction.z < 0:
            atan = self.light_direction.x / self.light_direction.z
            position.z = CENTER_Z + CHUNK_SIZE * WORLD_DEPTH
            position.x = CENTER_X + CHUNK_SIZE * WORLD_DEPTH * atan
        else:
            if self.light_direction.x > 0:
                position.x = CENTER_X - CHUNK_SIZE * WORLD_WIDTH
                position.z = CENTER_Z
                rot = glm.rotate(rot, glm.radians(90), glm.vec3(0, 1, 0))
            elif self.light_direction.x < 0:
                position.x = CENTER_X + CHUNK_SIZE * WORLD_WIDTH
                position.z = CENTER_Z
                rot = glm.rotate(rot, glm.radians(90), glm.vec3(0, 1, 0))
            else:
                position.y = 2 * self.height
                rot = glm.rotate(rot, glm.radians(90), glm.vec3(1, 0, 0))

        return glm.translate(glm.mat4(), position) * rot * glm.scale(glm.mat4(), glm.vec3(self.radius))

    def render(self):
        self.shader["m_model"].write(self.m_model)
        self.shader["u_color"].write(self.color)

        self.ctx.disable(gl.CULL_FACE)
        self.mesh.render()
        self.ctx.enable(gl.CULL_FACE)