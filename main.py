from settings import *
import moderngl as gl
import glm
import pygame
from scene import Scene
from shader_program import ShaderProgram
from mesh import ScreenQuadMesh


class VoxelEngine:
    def __init__(self):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
        )
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
        # pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        # pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)

        pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            flags=pygame.OPENGL | pygame.DOUBLEBUF,
            vsync=VSYNC,
        )
        pygame.display.set_caption(f"{WINDOW_TITLE}")

        self.ctx = gl.create_context()
        self.ctx.gc_mode = "auto"

        self.ctx.enable(flags=gl.DEPTH_TEST | gl.CULL_FACE | gl.BLEND)

        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.running = True

        self.shaders = {
            "quad": ShaderProgram(self.ctx, "quad"),
            "chunk": ShaderProgram(self.ctx, "chunk"),
            "post": ShaderProgram(self.ctx, "post"),
            "skybox": ShaderProgram(self.ctx, "skybox"),
            "sun": ShaderProgram(self.ctx, "sun"),
            "water": ShaderProgram(self.ctx, "water"),
            "brightness": ShaderProgram(self.ctx, "brightness"),
            "blur_h": ShaderProgram(self.ctx, "blur_h"),
            "blur_v": ShaderProgram(self.ctx, "blur_v"),
            "bloom": ShaderProgram(self.ctx, "bloom"),
        }

        self.scene_fbo = self.ctx.framebuffer(
            color_attachments=[
                self.ctx.texture((WINDOW_WIDTH, WINDOW_HEIGHT), 4, samples=4, dtype="f4")
            ],
            depth_attachment=self.ctx.depth_renderbuffer((WINDOW_WIDTH, WINDOW_HEIGHT), samples=4),
        )
        self.resolve_fbo = self.ctx.framebuffer(
            color_attachments=[
                self.ctx.texture((WINDOW_WIDTH, WINDOW_HEIGHT), 4, dtype="f4")
            ],
            depth_attachment=self.ctx.depth_renderbuffer((WINDOW_WIDTH, WINDOW_HEIGHT))
        )
        self.brightness_fbo = self.ctx.framebuffer(
            color_attachments=[
                self.ctx.texture((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), 4, dtype="f4")
            ]
        )
        self.blur_fbos = [
            self.ctx.framebuffer(
                color_attachments=[
                    self.ctx.texture((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), 4, dtype="f4")
                ]
            ),
            self.ctx.framebuffer(
                color_attachments=[
                    self.ctx.texture((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), 4, dtype="f4")
                ]
            )
        ]
        self.bloom_fbo = self.ctx.framebuffer(
            color_attachments=[
                self.ctx.texture((WINDOW_WIDTH, WINDOW_HEIGHT), 4, dtype="f4")
            ]
        )

        self.scene = Scene(self.ctx, self.shaders)
        self.brightness_quad = ScreenQuadMesh(self.ctx, self.shaders["brightness"].program)
        self.blur_quads = [
            ScreenQuadMesh(self.ctx, self.shaders["blur_h"].program),
            ScreenQuadMesh(self.ctx, self.shaders["blur_v"].program),
        ]
        self.bloom_quad = ScreenQuadMesh(self.ctx, self.shaders["bloom"].program)
        self.post_quad = ScreenQuadMesh(self.ctx, self.shaders["post"].program)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            dt = self.clock.tick() / 1000
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            pygame.display.set_caption(
                f"{WINDOW_TITLE} ({int(self.clock.get_fps())} FPS)"
            )

            self.scene.update(dt)

            self.scene_fbo.use()
            self.ctx.clear(color=SCENE_BG_COLOR)
            self.shaders["water"].program["u_time"] = elapsed_time;
            self.scene.render()

            self.resolve_fbo.use()
            self.ctx.copy_framebuffer(self.resolve_fbo, self.scene_fbo)

            self.brightness_fbo.use()
            self.resolve_fbo.color_attachments[0].use(0)
            self.shaders["brightness"].program["u_texture"] = 0
            self.brightness_quad.render()

            self.blur_fbos[0].use()
            self.brightness_fbo.color_attachments[0].use(0)
            self.shaders["blur_h"].program["u_texture"] = 0
            self.blur_quads[0].render()

            self.blur_fbos[1].use()
            self.blur_fbos[0].color_attachments[0].use(0)
            self.shaders["blur_v"].program["u_texture"] = 0
            self.blur_quads[1].render()
                
            for i in range(4):
                self.blur_fbos[0].use()
                self.blur_fbos[1].color_attachments[0].use(0)
                self.shaders["blur_h"].program["u_texture"] = 0
                self.blur_quads[0].render()

                self.blur_fbos[1].use()
                self.blur_fbos[0].color_attachments[0].use(0)
                self.shaders["blur_v"].program["u_texture"] = 0
                self.blur_quads[1].render()
            
            self.bloom_fbo.use()
            self.resolve_fbo.color_attachments[0].use(0)
            self.blur_fbos[0].color_attachments[0].use(1)
            self.shaders["bloom"].program["u_screen_texture"] = 0
            self.shaders["bloom"].program["u_bloom_texture"] = 1
            self.bloom_quad.render()

            self.ctx.screen.use()
            # self.ctx.clear()
            self.ctx.disable(gl.DEPTH_TEST)
            self.bloom_fbo.color_attachments[0].use(0)
            self.shaders["post"].program["u_screen_texture"] = 0
            self.shaders["post"].program["u_time"] = elapsed_time
            self.post_quad.render()
            self.ctx.enable(gl.DEPTH_TEST)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = VoxelEngine()
    game.run()
