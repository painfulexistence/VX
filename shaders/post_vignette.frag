#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2D u_screen_texture;
uniform float u_time;

in vec2 texcoord;

void main() {
    float _ = u_time;

    vec2 uv = texcoord * 2.0 - 1.0;
    float vignetteStrength = 0.7;
    float vignette = 1.0 - dot(uv, uv) * vignetteStrength;
    
    vec4 color = texture(u_screen_texture, texcoord);
    color.rgb *= vignette;
    
    fragColor = color;
}