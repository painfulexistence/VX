from skybox import Skybox
from sun import Sun
from world import World
from player import Player
from water import Water
from camera import CameraManager3D, DebugCamera3D
import glm
import pygame
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

        # Initialize camera manager with multiple cameras
        self.camera_manager = CameraManager3D()
        self.camera_manager.add("player", self.player.camera)
        self.camera_manager.add("debug", DebugCamera3D(self.player.camera.position, -90, 0, 50.0))
        self.camera_manager.switch("player")

        # For backward compatibility
        self.camera = self.camera_manager.current()

        # Camera switch cooldown
        self.camera_switch_cooldown = 0.0

    def update(self, dt):
        self.world.update(dt)
        self.water.update(dt)

        # Update camera reference (in case of switch)
        self.camera = self.camera_manager.current()
        current_camera_name = self.camera_manager.current_camera_name

        # Handle camera switching (press C to toggle)
        self.camera_switch_cooldown = max(0, self.camera_switch_cooldown - dt)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c] and self.camera_switch_cooldown <= 0:
            next_cam = "debug" if current_camera_name == "player" else "player"
            self.camera_manager.switch(next_cam)
            self.camera_switch_cooldown = 0.3  # 300ms cooldown
            print(f"Switched to {next_cam} camera")
            # Update camera reference after switch
            self.camera = self.camera_manager.current()
            current_camera_name = next_cam

        # Handle input for current camera
        if current_camera_name == "player":
            # Player controls: WASD for movement, IJKL for rotation
            player_cam = self.player.camera
            dx = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
            dz = int(keys[pygame.K_w]) - int(keys[pygame.K_s])
            
            if dx != 0 or dz != 0:
                direction = glm.normalize(glm.vec3(dx, 0, dz))
                player_cam.move(direction * PLAYER_SPEED * dt)

            # Rotation with IJKL
            rx = int(keys[pygame.K_l]) - int(keys[pygame.K_j])
            ry = int(keys[pygame.K_i]) - int(keys[pygame.K_k])
            if rx != 0:
                player_cam.rotate_yaw(rx * PLAYER_ROTATE_SPEED * dt)
            if ry != 0:
                player_cam.rotate_pitch(ry * PLAYER_ROTATE_SPEED * dt)

        elif current_camera_name == "debug":
            # DebugCamera3D controls: WASD for movement, RF for up/down, Arrow keys for rotation
            debug_cam = self.camera_manager.get_by_name("debug")
            
            # Rotation (arrow keys)
            rx = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
            ry = int(keys[pygame.K_UP]) - int(keys[pygame.K_DOWN])
            
            if rx != 0 or ry != 0:
                rotate_speed = 2.0
                debug_cam.yaw += rx * rotate_speed * dt
                debug_cam.pitch += ry * rotate_speed * dt
                
                # Clamp pitch to avoid gimbal lock
                debug_cam.pitch = glm.clamp(debug_cam.pitch, glm.radians(-89.0), glm.radians(89.0))
            
            # Movement (WASD + RF for up/down)
            dx = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
            dz = int(keys[pygame.K_w]) - int(keys[pygame.K_s])
            
            # Up/Down movement (RF - only for debug camera)
            dy = int(keys[pygame.K_r]) - int(keys[pygame.K_f])
            
            if dx != 0 or dy != 0 or dz != 0:
                # Vectors will be updated in camera.update(dt) below
                # But we need them now for movement, so update manually
                debug_cam.update(0)  # Update vectors without time delta
                
                move_vec = glm.vec3(0)
                move_vec += dx * debug_cam.right
                move_vec += dy * glm.vec3(0, 1, 0)  # World up
                move_vec += dz * debug_cam.forward
                
                if glm.length(move_vec) > 0:
                    move_vec = glm.normalize(move_vec)
                    debug_cam.position += move_vec * debug_cam.move_speed * dt

        # Update camera state (vectors and matrices)
        self.camera_manager.update(dt)

    def render_opaque(self):
        view_matrix = glm.mat4(glm.mat3(self.camera.view_matrix)) # getting rid of translation
        self.skybox_shader["m_proj"].write(self.camera.proj_matrix)
        self.skybox_shader["m_view"].write(view_matrix)
        self.skybox.render()

        self.sun_shader["m_proj"].write(self.camera.proj_matrix)
        self.sun_shader["m_view"].write(self.camera.view_matrix)
        self.sun_shader["u_fog_color"].write(COLOR_WHITE)
        self.sun_shader["u_fog_density"].value = 0.000003
        self.sun.render()

        self.chunk_shader["m_proj"].write(self.camera.proj_matrix)
        self.chunk_shader["m_view"].write(self.camera.view_matrix)
        self.chunk_shader["u_camera_pos"].write(self.camera.position)
        self.chunk_shader["u_water_line"].value = WATER_LINE
        self.chunk_shader["u_under_water_color"].write(self.water.deep_color)
        self.chunk_shader["u_fog_color"].write(self.skybox.sky_color)
        self.chunk_shader["u_fog_density"].value = 0.00001
        self.chunk_shader["u_light_direction"].write(self.sun.light_direction)
        self.chunk_shader["u_light_color"].write(self.sun.light_color)
        self.world.render(self.camera)

    def render_water(self):
        self.water_shader["m_proj"].write(self.camera.proj_matrix)
        self.water_shader["m_view"].write(self.camera.view_matrix)
        self.water_shader["m_inv_proj"].write(glm.inverse(self.camera.proj_matrix))
        self.water_shader["m_inv_view"].write(glm.inverse(self.camera.view_matrix))
        self.water_shader["u_camera_pos"].write(self.camera.position)
        self.water_shader["u_fog_color"].write(self.skybox.sky_color)
        self.water_shader["u_fog_density"].value = 0.00001
        self.water_shader["u_light_direction"].write(self.sun.light_direction)
        self.water_shader["u_light_color"].write(self.sun.light_color)
        self.water.render()
