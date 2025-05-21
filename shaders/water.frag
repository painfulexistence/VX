#version 330 core

layout(location = 0) out vec4 fragColor;
layout(location = 1) out vec4 fragNormal;

in vec2 uv;
in vec3 normal;
in vec3 frag_pos;
in float view_depth;

uniform sampler2D u_depth_texture;
uniform vec3 u_deep_color;
uniform vec3 u_shallow_color;
uniform vec3 u_fog_color;
uniform float u_fog_density;
uniform vec3 u_light_direction;
uniform vec3 u_light_color;
uniform float u_near_z = 0.1;
uniform float u_far_z = 2000.0;
uniform vec3 u_camera_pos;

float linearize_depth(float depth) {
    float z = depth * 2.0 - 1.0;
    return (2.0 * u_near_z * u_far_z) / (u_far_z + u_near_z - z * (u_far_z - u_near_z));
}

void main() {
    float depth = texture(u_depth_texture, uv).r;
    float d = linearize_depth(depth);
    float water_thickness = max(d - view_depth, 0.0);
    float beer_factor = smoothstep(0.0, 32.0, water_thickness); // exp(-water_thickness * 10.0);
    vec3 col = mix(u_shallow_color, u_deep_color, beer_factor);

    vec3 norm = normalize(normal);
    vec3 diff = max(dot(norm, -u_light_direction), 0.0) * col * u_light_color;
    col = mix(col, diff, 0.2);

    vec3 view_dir = normalize(u_camera_pos - frag_pos);
    float fresnel = pow(1.0 - max(dot(norm, view_dir), 0.0), 3.0);
    col = mix(col, vec3(1.0), fresnel * 0.5);

    float dist = d;
    col = mix(col, u_fog_color, 1.0 - exp(-u_fog_density * dist * dist));
    
    fragColor = vec4(col, 0.8);
    fragNormal = vec4(norm, 1.0);
}