import moderngl as gl
from mesh import SkyboxMesh


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
        
    def render(self):        
        self.ctx.depth_func = "<="
        self.ctx.depth_mask = False
        # self.texture.use(0)
        # self.shader["skybox"] = 0
        self.mesh.render()
        self.ctx.depth_func = "<"
        self.ctx.depth_mask = True 