#version 330 core

layout(location = 0) out vec4 fragColor;
layout(location = 1) out vec4 fragNormal;

in vec3 color;
in vec3 frag_pos;
in vec3 normal;

in vec3 atlas_texcoord;
uniform float u_water_line;
uniform vec3 u_under_water_color;
uniform vec3 u_fog_color;
uniform float u_fog_density;
uniform vec3 u_light_direction;
uniform vec3 u_light_color;
uniform sampler2DArray u_atlas;
uniform vec3 u_camera_pos;

void main() {
    vec3 col = texture(u_atlas, atlas_texcoord).rgb;
    col = color;

    vec3 norm = normalize(normal);
    vec3 ambient = vec3(0.1);
    vec3 diffuse = max(dot(norm, -u_light_direction), 0.0) * col * u_light_color;
    vec3 view_dir = normalize(u_camera_pos - frag_pos);
    vec3 refl_dir = reflect(u_light_direction, norm);
    float spec = pow(max(dot(view_dir, refl_dir), 0.0), 32.0);
    vec3 specular = 0.2 * spec * vec3(1.0);

    col = mix(col, ambient + diffuse + specular, 0.2);

    // FIXME: depth calculation is wrong
    float dist = gl_FragCoord.z / gl_FragCoord.w;
    float height_factor = smoothstep(0.0, 24.0, frag_pos.y);
    vec3 fog_color = mix(u_fog_color * 0.5, u_fog_color, height_factor);
    col = mix(col, fog_color, 1.0 - exp(-u_fog_density * dist * dist));

    if (frag_pos.y < u_water_line) {
        col *= 0.8;
        col = mix(col, u_under_water_color, 0.5);
    }

    fragColor = vec4(col, 1.0);
    fragNormal = vec4(norm, 1.0);
}
