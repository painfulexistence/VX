from mesh import SkyboxMesh
from settings import *

class Skybox:
    def __init__(self, ctx, shader):
        self.ctx = ctx
        self.shader = shader
        self.mesh = SkyboxMesh(ctx, shader)
        # self.texture = self.ctx.texture_cube(
        #     size=(1024, 1024),
        #     components=3,
        #     data=None
        # )
        # self.sky_color = COLOR_MINT_GREEN
        # self.horizon_color = COLOR_LEMON_CREAM
        self.sky_color = COLOR_ORANGE_DUST
        self.horizon_color = COLOR_DARK_ORANGE

    def render(self):
        self.shader["u_sky_color"].write(self.sky_color)
        self.shader["u_horizon_color"].write(self.horizon_color)

        self.ctx.depth_func = "<="
        self.ctx.depth_mask = False
        # self.texture.use(0)
        # self.shader["skybox"] = 0
        self.mesh.render()
        self.ctx.depth_func = "<"
        self.ctx.depth_mask = True 