from settings import *
from frustum import Frustum
import glm

class Camera:
    def __init__(self, position, yaw, pitch) -> None:
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.proj_matrix = glm.perspective(FOV, ASPECT_RATIO, NEAR_Z, FAR_Z)
        self.view_matrix = self.get_view_matrix()

        self.frustum = Frustum(self.proj_matrix * self.view_matrix)

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def update(self):
        self.forward.x = glm.cos(self.pitch) * glm.cos(self.yaw)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.cos(self.pitch) * glm.sin(self.yaw)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

        self.view_matrix = self.get_view_matrix()
        self.frustum.update_planes(self.proj_matrix * self.view_matrix)

    def move(self, delta):
        self.position += delta.x * self.right + delta.y * self.up + delta.z * self.forward

    def rotate_yaw(self, delta):
        self.yaw += delta

    def rotate_pitch(self, delta):
        self.pitch += delta

    def is_visible(self, bsphere):
        return self.frustum.is_inside(bsphere)