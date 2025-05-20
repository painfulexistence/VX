#version 330 core

layout(location = 0) out vec4 fragColor;

in vec3 view_dir;

uniform vec3 u_sky_color;
uniform vec3 u_horizon_color;
// uniform samplerCube skybox;


vec3 skybox_color(vec3 direction) {
    vec3 dir = normalize(direction);
    float t = (dir.y + 1.0) * 0.5;
    return mix(u_horizon_color, u_sky_color, t);
}

void main() {
    // vec3 col = texture(skybox, view_dir);
    vec3 col = skybox_color(view_dir);
    fragColor = vec4(col, 1.0);
}