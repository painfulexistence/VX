#version 330 core

layout(location = 0) in ivec3 in_position;
layout(location = 1) in int voxel_id;
layout(location = 2) in int face_id;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 color;

vec3 palette(float t) {
    // Palette 1
    // vec3 a = vec3(0.80, 0.15, 0.56);
    // vec3 b = vec3(0.61, 0.30, 0.12);
    // vec3 c = vec3(0.64, 0.10, 0.59);
    // vec3 d = vec3(0.38, 0.86, 0.47);
    // Palette 2
    // vec3 a = vec3(0.288, 0.303, 0.466);
    // vec3 b = vec3(0.806, 0.664, 0.998);
    // vec3 c = vec3(1.253, 0.992, 1.569);
    // vec3 d = vec3(3.379, 3.574, 3.026);
    // Palette 3
    // vec3 a = vec3(0.420, 0.696, 0.625);
    // vec3 b = vec3(0.791, 0.182, 0.271);
    // vec3 c = vec3(0.368, 0.650, 0.103);
    // vec3 d = vec3(0.913, 3.624, 0.320);
    // Palette 4
    // vec3 a = vec3(0.427, 0.346, 0.372);
    // vec3 b = vec3(0.288, 0.918, 0.336);
    // vec3 c = vec3(0.635, 1.136, 0.404);
    // vec3 d = vec3(1.893, 0.663, 1.910);
    // Palette 5
    vec3 a = vec3(0.746, 0.815, 0.846);
    vec3 b = vec3(0.195, 0.283, 0.187);
    vec3 c = vec3(1.093, 1.417, 1.405);
    vec3 d = vec3(5.435, 2.400, 5.741);
    return a + b * cos(6.28318 * (c * t + d));
}

void main() {
    color = palette(float(voxel_id) / 50.0);
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}
