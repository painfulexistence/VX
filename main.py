from settings import *
import moderngl as gl
import glm
import pygame
from scene import Scene
from shader_program import ShaderProgram


class VoxelEngine:
    def __init__(self):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
        )
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)

        pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.OPENGL | pygame.DOUBLEBUF
        )
        pygame.display.set_caption(f"{WINDOW_TITLE}")

        self.ctx = gl.create_context()
        self.ctx.gc_mode = "auto"

        self.ctx.enable(flags=gl.DEPTH_TEST | gl.CULL_FACE)

        self.clock = pygame.time.Clock()
        self.running = True

        self.shaders = {
            "quad": ShaderProgram(self.ctx, "quad"),
            "chunk": ShaderProgram(self.ctx, "chunk"),
        }
        self.scene = Scene(self.ctx, self.shaders)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            pygame.display.set_caption(
                f"{WINDOW_TITLE} ({int(self.clock.get_fps())} FPS)"
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.scene.update(dt)

            self.ctx.clear(color=glm.vec3(0.58, 0.83, 0.99))
            self.scene.render()
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = VoxelEngine()
    game.run()
