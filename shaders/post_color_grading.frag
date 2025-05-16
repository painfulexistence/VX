#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2D u_screen_texture;
uniform float u_time;

in vec2 texcoord;


vec3 warm(vec3 color) {
    return vec3(
        dot(color, vec3(1.0, 0.1, 0.1)),
        dot(color, vec3(0.1, 0.8, 0.1)),
        dot(color, vec3(0.1, 0.1, 0.8))
    );
}

vec3 cool(vec3 color) {
    return vec3(
        dot(color, vec3(0.8, 0.1, 0.1)),
        dot(color, vec3(0.1, 0.9, 0.1)),
        dot(color, vec3(0.1, 0.1, 1.0))
    );
}

vec3 sepia(vec3 color) {
    return vec3(
        dot(color, vec3(0.393, 0.769, 0.189)),
        dot(color, vec3(0.349, 0.686, 0.168)),
        dot(color, vec3(0.272, 0.534, 0.131))
    );
}

void main() {
    float _ = u_time;

    vec4 color = texture(u_screen_texture, texcoord);
    color.rgb = sepia(color.rgb);
    
    fragColor = color;
}