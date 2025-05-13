import pygame
from camera import Camera
from settings import *
import glm


class Player(Camera):
    def __init__(self, position) -> None:
        super().__init__(position, -90, 0)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        dx = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        dy = int(keys[pygame.K_r]) - int(keys[pygame.K_f])
        dz = int(keys[pygame.K_w]) - int(keys[pygame.K_s])
        if dx != 0 or dy != 0 or dz != 0:
            direction = glm.normalize(glm.vec3(dx, dy, dz))
            self.move(direction * PLAYER_SPEED * dt)

        rx = int(keys[pygame.K_l]) - int(keys[pygame.K_j])
        ry = int(keys[pygame.K_i]) - int(keys[pygame.K_k])
        self.rotate_yaw(rx * PLAYER_ROTATE_SPEED * dt)
        self.rotate_pitch(ry * PLAYER_ROTATE_SPEED * dt)

        super().update()
