from settings import *
from frustum import Frustum
import glm
from typing import Dict, Optional, Tuple


class BaseCamera3D:
    def __init__(self, position, yaw, pitch) -> None:
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.proj_matrix = glm.perspective(glm.radians(FOV), ASPECT_RATIO, NEAR_Z, FAR_Z)
        self.view_matrix = self.get_view_matrix()

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def update(self, dt=0):
        self.forward.x = glm.cos(self.pitch) * glm.cos(self.yaw)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.cos(self.pitch) * glm.sin(self.yaw)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

        self.view_matrix = self.get_view_matrix()

    def move(self, delta):
        self.position += delta.x * self.right + delta.y * self.up + delta.z * self.forward

    def rotate_yaw(self, delta):
        self.yaw += delta

    def rotate_pitch(self, delta):
        self.pitch += delta

    def is_visible(self, bsphere):
        return True

    def screen_to_world(self, screen_x: float, screen_y: float, 
                            screen_width: int, screen_height: int) -> glm.vec3:
        ndc_x = (2.0 * screen_x / screen_width) - 1.0
        ndc_y = 1.0 - (2.0 * screen_y / screen_height)
        clip_pos = glm.vec4(ndc_x, ndc_y, -1.0, 1.0)
        inv_proj = glm.inverse(self.proj_matrix)
        view_pos = inv_proj * clip_pos
        
        view_pos.w = 0.0
        view_dir = glm.vec3(view_pos)
        view_dir = glm.normalize(view_dir)
        
        inv_view = glm.inverse(self.view_matrix)
        world_dir = glm.vec3(inv_view * glm.vec4(view_dir, 0.0))
        world_dir = glm.normalize(world_dir)
        
        return world_dir

    def world_to_screen(self, world_pos: glm.vec3, 
                       screen_width: int, screen_height: int) -> Tuple[float, float, bool]:
        world_pos_homogeneous = glm.vec4(world_pos, 1.0)
        clip_pos = self.proj_matrix * self.view_matrix * world_pos_homogeneous
        
        if clip_pos.w <= 0.0:
            return 0.0, 0.0, False
        
        ndc_x = clip_pos.x / clip_pos.w
        ndc_y = clip_pos.y / clip_pos.w
        ndc_z = clip_pos.z / clip_pos.w
        
        is_visible = (-1.0 <= ndc_x <= 1.0 and 
                      -1.0 <= ndc_y <= 1.0 and 
                      -1.0 <= ndc_z <= 1.0)
        
        screen_x = (ndc_x + 1.0) * 0.5 * screen_width
        screen_y = (1.0 - ndc_y) * 0.5 * screen_height
        
        return screen_x, screen_y, is_visible

class Camera(BaseCamera3D):
    def __init__(self, position, yaw, pitch) -> None:
        super().__init__(position, yaw, pitch)
        self.frustum = Frustum(self.proj_matrix * self.view_matrix)

    def update(self, dt=0):
        super().update(dt)
        self.frustum.update_planes(self.proj_matrix * self.view_matrix)

    def is_visible(self, bsphere):
        return self.frustum.is_inside(bsphere)

class DebugCamera3D(BaseCamera3D) :
    def __init__(self, position, yaw, pitch, move_speed: float = 50.0):
        super().__init__(position, yaw, pitch)
        self.move_speed = move_speed


class CameraManager3D:
    def __init__(self):
        self.cameras: Dict[str, BaseCamera3D] = {}
        self.current_camera_name: Optional[str] = None

    def add(self, name: str, camera: BaseCamera3D) -> None:
        if name in self.cameras:
            raise ValueError(f"Camera '{name}' already exists")
        self.cameras[name] = camera

        # Auto-set as current if it's the first camera
        if self.current_camera_name is None:
            self.current_camera_name = name

    def get_by_name(self, name: str) -> Optional[BaseCamera3D]:
        return self.cameras.get(name)

    def current(self) -> BaseCamera3D:
        if self.current_camera_name is None:
            raise RuntimeError("No cameras added to CameraManager3D")

        if self.current_camera_name not in self.cameras:
            raise KeyError(f"Current camera '{self.current_camera_name}' not found")

        return self.cameras[self.current_camera_name]

    def switch(self, name: str) -> None:
        if name not in self.cameras:
            raise KeyError(f"Camera '{name}' not found")

        old_name = self.current_camera_name
        self.current_camera_name = name

        # Optional: Copy position from old camera to new camera for smooth transition
        # (Uncomment if you want cameras to start from previous camera's position)
        # if old_name and old_name in self.cameras:
        #     old_cam = self.cameras[old_name]
        #     new_cam = self.cameras[name]
        #     if hasattr(new_cam, 'set_position'):
        #         new_cam.set_position(old_cam.position)

    def update(self, dt: float) -> None:
        camera = self.current()
        camera.update(dt)

    def list_cameras(self) -> list:
        return list(self.cameras.keys())

    def remove_camera(self, name: str) -> None:
        if name == self.current_camera_name:
            raise ValueError(f"Cannot remove current camera '{name}'. Switch to another camera first.")

        if name in self.cameras:
            del self.cameras[name]
