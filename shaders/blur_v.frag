#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2D u_texture;

in vec2 texcoord;

const float weights[5] = float[] (0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);

void main() {
    vec2 tex_offset = 1.0 / textureSize(u_texture, 0);
    vec3 result = texture(u_texture, texcoord).rgb * weights[0];
    
    for(int i = 1; i < 5; ++i) {
        result += texture(u_texture, texcoord + vec2(0.0, tex_offset.y * i)).rgb * weights[i];
        result += texture(u_texture, texcoord - vec2(0.0, tex_offset.y * i)).rgb * weights[i];
    }
    
    fragColor = vec4(result, 1.0);
} 