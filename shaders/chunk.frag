#version 330 core

layout(location = 0) out vec4 fragColor;

in vec3 color;
in vec3 frag_pos;

uniform float u_water_line;
uniform vec3 u_under_water_color;
uniform vec3 u_fog_color;

void main() {
    vec3 col = color;

    float dist = gl_FragCoord.z / gl_FragCoord.w;
    col = mix(col, u_fog_color, 1.0 - exp(-0.00002 * dist * dist));

    if (frag_pos.y < u_water_line) {
        col *= 0.8;
        col = mix(col, u_under_water_color, 0.5);
    }

    fragColor = vec4(col, 1.0);
}
