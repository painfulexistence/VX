#version 330 core

layout(location = 0) out vec4 fragColor;

in vec3 color;

void main() {
    vec3 col = color;

    // float dist = gl_FragCoord.z / gl_FragCoord.w;
    // col = mix(col, vec3(0.5, 0.5, 0.6), 1.0 - exp(-0.00001 * dist * dist));

    fragColor = vec4(col, 1.0);
}
