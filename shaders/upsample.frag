#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2D u_texture;
uniform sampler2D u_blend_texture;

in vec2 texcoord;


const float filter_radius = 0.005;

const float weights[9] = float[9](
    1.0, 2.0, 1.0,
    2.0, 4.0, 2.0,
    1.0, 2.0, 1.0
);

void main() {
    vec3 color = vec3(0.0);
    vec2 texel_size = 1.0 / textureSize(u_texture, 0);
    int idx = 0;
    for (int y = -1; y <= 1; ++y) {
        for (int x = -1; x <= 1; ++x) {
            vec2 offset = vec2(x, y) * filter_radius;
            color += texture(u_texture, texcoord + offset).rgb * weights[idx++];
        }
    }
    color /= 16.0;
    vec3 blend_color = texture(u_blend_texture, texcoord).rgb;

    fragColor = vec4(color + blend_color, 1.0);
}