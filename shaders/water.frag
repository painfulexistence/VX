#version 330 core

layout(location = 0) out vec4 fragColor;
layout(location = 1) out vec4 fragNormal;

in vec2 texcoord;
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
uniform float u_water_line;
uniform mat4 m_inv_proj;
uniform mat4 m_inv_view;


const float beer_absorption_coef = 0.095; // if higher, water will become dark quicker

float linearize_depth(float depth) {
    float z = depth * 2.0 - 1.0;
    return (2.0 * u_near_z * u_far_z) / (u_far_z + u_near_z - z * (u_far_z - u_near_z));
}

vec3 reconstruct_world_pos_from_depth(vec2 screen_uv, float depth) {
    vec4 depth_clip_pos = vec4(screen_uv * 2.0 - 1.0, depth * 2.0 - 1.0, 1.0);
    vec4 depth_h_view_pos = m_inv_proj * depth_clip_pos;
    vec4 depth_view_pos = vec4(depth_h_view_pos.xyz / depth_h_view_pos.w, 1.0);
    vec4 depth_world_pos = m_inv_view * depth_view_pos;
    return depth_world_pos.xyz;
}

void main() {
    vec3 norm = normalize(normal);
    vec3 view_dir = normalize(u_camera_pos - frag_pos);
    vec3 light_dir = normalize(-u_light_direction);
    vec3 half_dir = normalize(light_dir + view_dir);

    if (u_camera_pos.y < u_water_line) {
        vec3 col = mix(u_shallow_color, u_deep_color, smoothstep(2.0, 32.0, u_water_line - u_camera_pos.y));
        fragColor = vec4(col, 0.9);
        fragNormal = vec4(norm, 1.0);
        return;
    }

    vec2 screen_uv = gl_FragCoord.xy / textureSize(u_depth_texture, 0);
    float depth = texture(u_depth_texture, screen_uv).r;
    vec3 depth_world_pos = reconstruct_world_pos_from_depth(screen_uv, depth);

    float water_thickness = max(frag_pos.y - depth_world_pos.y, 0.0);
    float beer_factor = max(1.0 - exp(-water_thickness * beer_absorption_coef), 0.0);
    vec3 col = mix(u_shallow_color, u_deep_color, beer_factor);

    float diff = max(dot(norm, light_dir), 0.0);
    float spec = pow(max(dot(norm, half_dir), 0.0), 128.0);
    float fresnel = pow(1.0 - max(dot(norm, view_dir), 0.0), 5.0);

    vec3 diffuse = diff * col * u_light_color;
    vec3 specular = spec * vec3(1.0) * u_light_color;
    col = mix(col, diffuse + specular, 0.2);
    col = mix(col, vec3(1.0), fresnel * 0.5);

    float dist = length(u_camera_pos - frag_pos); // old version: linearize_depth(depth);
    col = mix(col, u_fog_color, 1.0 - exp(-u_fog_density * dist * dist));
    fragColor = vec4(col, smoothstep(0.1, 0.9, beer_factor));
    fragNormal = vec4(norm, 1.0);
}