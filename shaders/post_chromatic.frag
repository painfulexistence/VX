#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2D u_screen_texture;
uniform float u_time;

in vec2 texcoord;

void main() {
    float _ = u_time;

    float u = texcoord.x;
    float v = texcoord.y;
    float du = (u - 0.5) * (u - 0.5) * 0.01;
    float dv = (v - 0.5) * (v - 0.5) * 0.01;

    float r = texture(u_screen_texture, vec2(u - 2 * du, v + 4 * dv)).r;
    float g = texture(u_screen_texture, vec2(u + 1 * du, v - 1 * dv)).g;
    float b = texture(u_screen_texture, vec2(u + 5 * du, v - 3 * dv)).b;
	
	fragColor = vec4(r, g, b, 1.0);
}