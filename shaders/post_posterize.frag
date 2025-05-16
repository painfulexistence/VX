#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2D u_screen_texture;
uniform float u_time;

in vec2 texcoord;

void main() {
    float _ = u_time;

    vec4 color = texture(u_screen_texture, texcoord);
    float levels = 5.0;
    color.rgb = floor(color.rgb * levels) / levels;
    
    fragColor = color;
}