#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2D u_screen_texture;
uniform sampler2D u_bloom_texture;

in vec2 texcoord;

const float bloom_strength = 2.0;

void main() {
    vec3 col = texture(u_screen_texture, texcoord).rgb;

    // Bloom
    vec3 bloom = texture(u_bloom_texture, texcoord).rgb * bloom_strength;    
    col += bloom;
    
    fragColor = vec4(col, 1.0);
}