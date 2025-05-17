#version 330 core

layout(location = 0) out vec4 fragColor;

in vec3 color;

uniform vec3 u_fog_color;
uniform float u_fog_density;

void main() {
    vec3 col = color;

    float dist = gl_FragCoord.z / gl_FragCoord.w;
    col = mix(col, u_fog_color, 1.0 - exp(-u_fog_density * dist * dist));

    fragColor = vec4(col, 1.0);
}