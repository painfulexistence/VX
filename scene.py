from skybox import Skybox
from sun import Sun
from world import World
from player import Player
from water import Water
import glm
from settings import *


class Scene:
    def __init__(self, ctx, shaders):
        self.ctx = ctx
        self.shaders = shaders
        self.chunk_shader = self.shaders["chunk"].program
        self.skybox_shader = self.shaders["skybox"].program
        self.water_shader = self.shaders["water"].program
        self.sun_shader = self.shaders["sun"].program

        self.skybox = Skybox(self.ctx, self.skybox_shader)
        self.sun = Sun(self.ctx, self.sun_shader)
        self.world = World(self.ctx, self.shaders)
        self.player = Player(
            glm.vec3(
                WORLD_WIDTH * HALF_CHUNK_SIZE,
                WORLD_HEIGHT * CHUNK_SIZE,
                WORLD_DEPTH * HALF_CHUNK_SIZE,
            )
        )
        self.water = Water(self.ctx, self.water_shader)

    def update(self, dt):
        self.world.update(dt)
        self.player.update(dt)
        self.water.update(dt)

    def render(self):
        view_matrix = glm.mat4(glm.mat3(self.player.view_matrix)) # getting rid of translation
        self.skybox_shader["m_proj"].write(self.player.proj_matrix)
        self.skybox_shader["m_view"].write(view_matrix)
        self.skybox.render()

        self.sun_shader["m_proj"].write(self.player.proj_matrix)
        self.sun_shader["m_view"].write(self.player.view_matrix)
        self.sun_shader["u_fog_color"].write(COLOR_WHITE)
        self.sun_shader["u_fog_density"].value = 0.000003
        self.sun.render()

        self.chunk_shader["m_proj"].write(self.player.proj_matrix)
        self.chunk_shader["m_view"].write(self.player.view_matrix)
        self.chunk_shader["u_water_line"].value = WATER_LINE
        self.chunk_shader["u_under_water_color"].write(self.water.deep_color)
        self.chunk_shader["u_fog_color"].write(self.skybox.sky_color)
        self.chunk_shader["u_fog_density"].value = 0.00001
        self.chunk_shader["u_light_direction"].write(self.sun.light_direction)
        self.chunk_shader["u_light_color"].write(self.sun.light_color)
        self.world.render()

        self.water_shader["m_proj"].write(self.player.proj_matrix)
        self.water_shader["m_view"].write(self.player.view_matrix)
        self.water_shader["u_fog_color"].write(self.skybox.sky_color)
        self.water_shader["u_fog_density"].value = 0.00001
        self.water_shader["u_light_direction"].write(self.sun.light_direction)
        self.water_shader["u_light_color"].write(self.sun.light_color)
        self.water.render()
