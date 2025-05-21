#version 330 core

layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;
layout(location = 2) in vec2 in_texcoord;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;
uniform float u_time;
uniform float u_wave_strength;
uniform float u_wave_speed;

out vec2 uv;
out vec3 normal;
out vec3 frag_pos;
out float view_depth;

void main() {
    vec3 pos = in_position;
    float wave = sin(u_time * u_wave_speed + in_position.x * 0.5) * 
                 cos(u_time * u_wave_speed + in_position.z * 0.5) * u_wave_strength;             
    // pos.y += wave;

    vec4 world_pos = m_model * vec4(pos, 1.0);
        
    uv = in_texcoord;
    normal = mat3(transpose(inverse(m_model))) * in_normal;
    frag_pos = world_pos.xyz;
    view_depth = -(m_view * world_pos).z;

    gl_Position = m_proj * m_view * world_pos;
}