#version 330 core

layout(location = 0) in ivec3 in_position;
layout(location = 1) in int voxel_id;
layout(location = 2) in int face_id;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 color;
out vec3 frag_pos;
out vec3 normal;
out vec3 atlas_texcoord;

const float light_levels[6] = float[](1.0, 0.5, 0.9, 0.9, 0.9, 0.9);
const vec3 normals[6] = vec3[](
    vec3(0.0, 1.0, 0.0), // top
    vec3(0.0, -1.0, 0.0), // bottom
    vec3(1.0, 0.0, 0.0), // right
    vec3(-1.0, 0.0, 0.0), // left
    vec3(0.0, 0.0, 1.0), // front
    vec3(0.0, 0.0, -1.0) // back
);
const int tile_ids[6] = int[](
    2, 0, 1, 1, 1, 1
);
const vec2 uvs[36] = vec2[](
    vec2(0, 1), vec2(0, 0), vec2(1, 0), vec2(1, 0), vec2(1, 1), vec2(0, 1), // top
    vec2(0, 1), vec2(0, 0), vec2(1, 0), vec2(1, 0), vec2(1, 1), vec2(0, 1), // bottom
    vec2(0, 1), vec2(0, 0), vec2(1, 0), vec2(1, 0), vec2(1, 1), vec2(0, 1), // right
    vec2(0, 1), vec2(0, 0), vec2(1, 0), vec2(1, 0), vec2(1, 1), vec2(0, 1), // left
    vec2(0, 1), vec2(0, 0), vec2(1, 0), vec2(1, 0), vec2(1, 1), vec2(0, 1), // front
    vec2(0, 1), vec2(0, 0), vec2(1, 0), vec2(1, 0), vec2(1, 1), vec2(0, 1) // back
);

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
    vec3 a = vec3(0.427, 0.346, 0.372);
    vec3 b = vec3(0.288, 0.918, 0.336);
    vec3 c = vec3(0.635, 1.136, 0.404);
    vec3 d = vec3(1.893, 0.663, 1.910);
    // Palette 5
    // vec3 a = vec3(0.746, 0.815, 0.846);
    // vec3 b = vec3(0.195, 0.283, 0.187);
    // vec3 c = vec3(1.093, 1.417, 1.405);
    // vec3 d = vec3(5.435, 2.400, 5.741);
    // Palette 6
    // vec3 a = vec3(0.686, 0.933, 0.933);
    // vec3 b = vec3(0.957, 0.643, 0.957);
    // vec3 c = vec3(0.867, 0.627, 0.867);
    // vec3 d = vec3(1.961, 2.871, 1.702);
    return a + b * cos(6.28318 * (c * t + d));
}

void main() {
    vec2 uv = uvs[face_id * 6 + gl_VertexID % 6];

    // atlas_texcoord = vec2(
    //     (tile_ids[face_id] + uv.x) / 3,
    //     1.0 - ((voxel_id % 8) + uv.y) / 8
    // );
    atlas_texcoord = vec3(
        (tile_ids[face_id] + uv.x) / 3.0,
        uv.y,
        voxel_id % 8
    );
    color = palette(float(voxel_id) / 50.0);

    vec4 world_pos = m_model * vec4(in_position, 1.0);
    frag_pos = world_pos.xyz;
    normal = mat3(transpose(inverse(m_model))) * normals[face_id];

    gl_Position = m_proj * m_view * world_pos;
}
