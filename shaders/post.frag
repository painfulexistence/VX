#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2D u_screen_texture;

in vec2 uv;

void main() {
    vec4 color = texture(u_screen_texture, uv);
    fragColor = color;
}