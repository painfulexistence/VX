#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2D u_screen_texture;
uniform float u_time;

in vec2 texcoord;

void main() {
    float _ = u_time;

    vec2 texelSize = 1.0 / textureSize(u_screen_texture, 0);
    
    vec4 h = texture(u_screen_texture, texcoord + vec2(texelSize.x, 0.0)) -
             texture(u_screen_texture, texcoord - vec2(texelSize.x, 0.0));
             
    vec4 v = texture(u_screen_texture, texcoord + vec2(0.0, texelSize.y)) -
             texture(u_screen_texture, texcoord - vec2(0.0, texelSize.y));
             
    fragColor = vec4(sqrt((h * h + v * v).rgb), 1.0);
}