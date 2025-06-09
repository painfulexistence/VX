#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2D u_screen_texture;
uniform sampler2D u_depth_texture;
uniform sampler2D u_normal_texture;
uniform float u_exposure;
uniform float u_time;
uniform float u_near_z;
uniform float u_far_z;
uniform mat4 m_inv_proj;
uniform mat4 m_inv_view;

in vec2 texcoord;


const float gamma = 2.2;
const float inv_gamma = 1.0 / gamma;
const vec3 edge_color = vec3(0.1, 0.1, 0.1); // vec3(0.2, 0.5, 0.4);

vec3 exponential_tonemap(vec3 col) {
    return vec3(1.0) - exp(-col);
}

vec3 aces_tonemap(vec3 col) {
    float a = 2.51f;
    float b = 0.03f;
    float c = 2.43f;
    float d = 0.59f;
    float e = 0.14f;
    return clamp((col * (a * col + b)) / (col * (c * col + d) + e), 0.0, 1.0);
}

vec3 uncharted2_tonemap(vec3 col) {
    float A = 0.15;
    float B = 0.50;
    float C = 0.10;
    float D = 0.20;
    float E = 0.02;
    float F = 0.30;
    return ((col*(A*col+C*B)+D*E)/(col*(A*col+B)+D*F))-E/F;
}

float linearize_depth(float depth) {
    float z = depth * 2.0 - 1.0;
    return (2.0 * u_near_z * u_far_z) / (u_far_z + u_near_z - z * (u_far_z - u_near_z));
}

vec3 reconstruct_world_pos(vec2 screen_uv) {
    float depth = texture(u_depth_texture, screen_uv).r;
    vec4 depth_clip_pos = vec4(screen_uv * 2.0 - 1.0, depth * 2.0 - 1.0, 1.0);
    vec4 depth_h_view_pos = m_inv_proj * depth_clip_pos;
    vec4 depth_view_pos = vec4(depth_h_view_pos.xyz / depth_h_view_pos.w, 1.0);
    vec4 depth_world_pos = m_inv_view * depth_view_pos;
    return depth_world_pos.xyz;
}

float sobel_color(vec2 uv) {
    vec2 texel_size = 1.0 / textureSize(u_screen_texture, 0);
    float tl = length(texture(u_screen_texture, texcoord + vec2(-texel_size.x, texel_size.y)).rgb);
    float t = length(texture(u_screen_texture, texcoord + vec2(0.0, texel_size.y)).rgb);
    float tr = length(texture(u_screen_texture, texcoord + vec2(texel_size.x, texel_size.y)).rgb);
    float l = length(texture(u_screen_texture, texcoord + vec2(-texel_size.x, 0.0)).rgb);
    float c = length(texture(u_screen_texture, texcoord).rgb);
    float r = length(texture(u_screen_texture, texcoord + vec2(texel_size.x, 0.0)).rgb);
    float bl = length(texture(u_screen_texture, texcoord + vec2(-texel_size.x, -texel_size.y)).rgb);
    float b = length(texture(u_screen_texture, texcoord + vec2(0.0, -texel_size.y)).rgb);
    float br = length(texture(u_screen_texture, texcoord + vec2(texel_size.x, -texel_size.y)).rgb);
    float gx = -tl + tr - 2.0 * l + 2.0 * r - bl + br;
    float gy = -tl - 2.0 * t - tr + bl + 2.0 * b + br;
    return sqrt(gx * gx + gy* gy);
}

float sobel_depth(vec2 uv) {
    vec2 texel_size = 1.0 / textureSize(u_depth_texture, 0);
    float tl = linearize_depth(texture(u_depth_texture, uv + vec2(-texel_size.x, texel_size.y)).r);
    float t = linearize_depth(texture(u_depth_texture, uv + vec2(0.0, texel_size.y)).r);
    float tr = linearize_depth(texture(u_depth_texture, uv + vec2(texel_size.x, texel_size.y)).r);
    float l = linearize_depth(texture(u_depth_texture, uv + vec2(-texel_size.x, 0.0)).r);
    float c = linearize_depth(texture(u_depth_texture, uv).r);
    float r = linearize_depth(texture(u_depth_texture, uv + vec2(texel_size.x, 0.0)).r);
    float bl = linearize_depth(texture(u_depth_texture, uv + vec2(-texel_size.x, -texel_size.y)).r);
    float b = linearize_depth(texture(u_depth_texture, uv + vec2(0.0, -texel_size.y)).r);
    float br = linearize_depth(texture(u_depth_texture, uv + vec2(texel_size.x, -texel_size.y)).r);
    float gx = -tl + tr - 2.0 * l + 2.0 * r - bl + br;
    float gy = -tl - 2.0 * t - tr + bl + 2.0 * b + br;
    return sqrt(gx * gx + gy * gy);
}

float sobel_position(vec2 uv) {
    vec2 texel_size = 1.0 / textureSize(u_depth_texture, 0);
    vec3 tl = reconstruct_world_pos(uv + vec2(-texel_size.x, texel_size.y));
    vec3 t = reconstruct_world_pos(uv + vec2(0.0, texel_size.y));
    vec3 tr = reconstruct_world_pos(uv + vec2(texel_size.x, texel_size.y));
    vec3 l = reconstruct_world_pos(uv + vec2(-texel_size.x, 0.0));
    vec3 c = reconstruct_world_pos(uv);
    vec3 r = reconstruct_world_pos(uv + vec2(texel_size.x, 0.0));
    vec3 bl = reconstruct_world_pos(uv + vec2(-texel_size.x, -texel_size.y));
    vec3 b = reconstruct_world_pos(uv + vec2(0.0, -texel_size.y));
    vec3 br = reconstruct_world_pos(uv + vec2(texel_size.x, -texel_size.y));
    vec3 gx = -tl + tr - 2.0 * l + 2.0 * r - bl + br;
    vec3 gy = -tl - 2.0 * t - tr + bl + 2.0 * b + br;
    return sqrt(dot(gx, gx) + dot(gy, gy));
}

float sobel_normal(vec2 uv) {
    vec2 texel_size = 1.0 / textureSize(u_normal_texture, 0);
    vec3 tl = texture(u_normal_texture, uv + vec2(-texel_size.x, texel_size.y)).rgb;
    vec3 t = texture(u_normal_texture, uv + vec2(0.0, texel_size.y)).rgb;
    vec3 tr = texture(u_normal_texture, uv + vec2(texel_size.x, texel_size.y)).rgb;
    vec3 l = texture(u_normal_texture, uv + vec2(-texel_size.x, 0.0)).rgb;
    vec3 c = texture(u_normal_texture, uv).rgb;
    vec3 r = texture(u_normal_texture, uv + vec2(texel_size.x, 0.0)).rgb;
    vec3 bl = texture(u_normal_texture, uv + vec2(-texel_size.x, -texel_size.y)).rgb;
    vec3 b = texture(u_normal_texture, uv + vec2(0.0, -texel_size.y)).rgb;
    vec3 br = texture(u_normal_texture, uv + vec2(texel_size.x, -texel_size.y)).rgb;
    vec3 gx = -tl + tr - 2.0 * l + 2.0 * r - bl + br;
    vec3 gy = -tl - 2.0 * t - tr + bl + 2.0 * b + br;
    return sqrt(dot(gx, gx) + dot(gy, gy));
}

void main() {
    float _ = u_time;

    vec3 col = texture(u_screen_texture, texcoord).rgb;

    // sRGB to linear
    col = pow(col, vec3(gamma));

    // Exposure
    col *= u_exposure;

    // Tone mapping
    // col = exponential_tonemap(col);

    // Outline
    float brightness = length(col);
    float edge_strength = 1.0 - smoothstep(2.0, 4.0, brightness);

    float edge = max(
        smoothstep(0.1, 0.4, sobel_position(texcoord)) * 0.5,
        smoothstep(0.1, 0.5, sobel_normal(texcoord)) * 1.0
    );
    edge = smoothstep(0.0, 1.0, edge);
    col = mix(col, edge_color, edge * edge_strength);

    // Linear to sRGB
    col = pow(col, vec3(inv_gamma));

    fragColor = vec4(col, 1.0);
}