#version 330 core

layout(location = 0) out vec4 fragColor;

in vec3 color;
in vec3 frag_pos;
in vec3 normal;

uniform float u_water_line;
uniform vec3 u_under_water_color;
uniform vec3 u_fog_color;
uniform float u_fog_density;
uniform vec3 u_light_direction;
uniform vec3 u_light_color;

void main() {
    vec3 col = color;

    vec3 norm = normalize(normal);
    vec3 diff = max(dot(norm, -u_light_direction), 0.0) * col * u_light_color;
    col = mix(col, diff, 0.2);

    float dist = gl_FragCoord.z / gl_FragCoord.w;
    float height_factor = smoothstep(0.0, 24.0, frag_pos.y);
    vec3 fog_color = mix(u_fog_color * 0.5, u_fog_color, height_factor);
    col = mix(col, fog_color, 1.0 - exp(-u_fog_density * dist * dist));

    if (frag_pos.y < u_water_line) {
        col *= 0.8;
        col = mix(col, u_under_water_color, 0.5);
    }

    fragColor = vec4(col, 1.0);
}
