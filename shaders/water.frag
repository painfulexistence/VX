#version 330 core

layout(location = 0) out vec4 fragColor;
layout(location = 1) out vec4 fragNormal;

in vec2 uv;
in vec3 normal;
in vec3 frag_pos;
in float depth;

uniform vec3 u_deep_color;
uniform vec3 u_shallow_color;
uniform vec3 u_fog_color;
uniform float u_fog_density;
uniform vec3 u_light_direction;
uniform vec3 u_light_color;

void main() {
    vec3 col = mix(u_shallow_color, u_deep_color, smoothstep(16.0, 32.0, -depth));

    vec3 norm = normalize(normal);
    vec3 diff = max(dot(norm, -u_light_direction), 0.0) * col * u_light_color;
    col = mix(col, diff, 0.2);

    vec3 view_dir = normalize(-frag_pos);
    float fresnel = pow(1.0 - max(dot(norm, view_dir), 0.0), 3.0);
    col = mix(col, vec3(1.0), fresnel * 0.5);

    float dist = gl_FragCoord.z / gl_FragCoord.w;
    col = mix(col, u_fog_color, 1.0 - exp(-u_fog_density * dist * dist));
    
    fragColor = vec4(col, 0.5);
    fragNormal = vec4(norm, 1.0);
}